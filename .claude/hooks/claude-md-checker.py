#!/usr/bin/env python3
"""
Advanced Claude.md Compliance Checker Hook
Implements context-aware rule triggering, relevance scoring, and intelligent compliance monitoring
"""

import json
import re
import sys
import os
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum
import argparse

class AlertLevel(Enum):
    CRITICAL = "❗"
    ADVISORY = "⚠️"
    INFO = "ℹ️"

class ComplianceStatus(Enum):
    FOLLOWED = "✅"
    VIOLATED = "❌"
    OVERRIDDEN = "🔄"
    SKIPPED = "⏭️"

@dataclass
class RuleMetadata:
    rule_id: str
    content: str
    section: str
    alert_level: AlertLevel
    last_used: Optional[datetime]
    usage_count: int
    compliance_score: float
    version_hash: str
    created_date: datetime
    last_updated: datetime
    tags: Set[str]
    phase_relevance: Set[str]

@dataclass
class SessionContext:
    current_tool: str
    intent_tags: Set[str]
    phase: str
    task_type: str
    file_paths: List[str]
    session_id: str

class ClaudeMdChecker:
    def __init__(self):
        self.aai_root = Path("/mnt/c/Users/Brandon/AAI")
        self.claude_md_path = self.aai_root / "brain" / "Claude.md"
        self.compliance_log = self.aai_root / "brain" / "logs" / "rule-compliance.log"
        self.rule_metadata_file = self.aai_root / ".claude" / "hooks" / "rule-metadata.json"
        self.session_context_file = self.aai_root / "brain" / "cache" / "session-context.json"
        
        # Load existing metadata
        self.rule_metadata = self.load_rule_metadata()
        self.session_context = self.extract_session_context()
        
    def load_rule_metadata(self) -> Dict[str, RuleMetadata]:
        """Load rule metadata from JSON file"""
        if not self.rule_metadata_file.exists():
            return {}
        
        try:
            with open(self.rule_metadata_file, 'r') as f:
                data = json.load(f)
                
            metadata = {}
            for rule_id, rule_data in data.items():
                # Convert datetime strings back to datetime objects
                rule_data['last_used'] = datetime.fromisoformat(rule_data['last_used']) if rule_data.get('last_used') else None
                rule_data['created_date'] = datetime.fromisoformat(rule_data['created_date'])
                rule_data['last_updated'] = datetime.fromisoformat(rule_data['last_updated'])
                rule_data['alert_level'] = AlertLevel(rule_data['alert_level'])
                rule_data['tags'] = set(rule_data['tags'])
                rule_data['phase_relevance'] = set(rule_data['phase_relevance'])
                
                metadata[rule_id] = RuleMetadata(**rule_data)
                
            return metadata
        except Exception as e:
            print(f"Warning: Could not load rule metadata: {e}")
            return {}
    
    def save_rule_metadata(self):
        """Save rule metadata to JSON file"""
        self.rule_metadata_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to serializable format
        serializable_data = {}
        for rule_id, rule_meta in self.rule_metadata.items():
            data = asdict(rule_meta)
            data['last_used'] = data['last_used'].isoformat() if data['last_used'] else None
            data['created_date'] = data['created_date'].isoformat()
            data['last_updated'] = data['last_updated'].isoformat()
            data['alert_level'] = data['alert_level'].value
            data['tags'] = list(data['tags'])
            data['phase_relevance'] = list(data['phase_relevance'])
            serializable_data[rule_id] = data
        
        with open(self.rule_metadata_file, 'w') as f:
            json.dump(serializable_data, f, indent=2)
    
    def extract_session_context(self) -> SessionContext:
        """Extract context from current session and environment"""
        # Get current tool from command line args
        current_tool = sys.argv[0] if len(sys.argv) > 0 else "unknown"
        
        # Extract intent tags from recent commands/files
        intent_tags = set()
        phase = "unknown"
        task_type = "general"
        file_paths = []
        
        # Try to read session context if it exists
        if self.session_context_file.exists():
            try:
                with open(self.session_context_file, 'r') as f:
                    context_data = json.load(f)
                    intent_tags = set(context_data.get('intent_tags', []))
                    phase = context_data.get('phase', 'unknown')
                    task_type = context_data.get('task_type', 'general')
                    file_paths = context_data.get('file_paths', [])
            except:
                pass
        
        # Extract context from environment variables if available
        env_phase = os.environ.get('AAI_PHASE', '')
        if env_phase:
            phase = env_phase
            
        # Extract intent from current working directory or recent git commits
        try:
            if (self.aai_root / ".git").exists():
                import subprocess
                result = subprocess.run(['git', 'log', '--oneline', '-n', '5'], 
                                      cwd=self.aai_root, capture_output=True, text=True)
                if result.returncode == 0:
                    log_text = result.stdout.lower()
                    if 'test' in log_text or 'pytest' in log_text:
                        intent_tags.add('#testing')
                    if 'refactor' in log_text:
                        intent_tags.add('#refactor')
                    if 'research' in log_text:
                        intent_tags.add('#research')
                    if 'implement' in log_text:
                        intent_tags.add('#implement')
        except:
            pass
        
        return SessionContext(
            current_tool=current_tool,
            intent_tags=intent_tags,
            phase=phase,
            task_type=task_type,
            file_paths=file_paths,
            session_id=datetime.now().strftime("%Y%m%d_%H%M%S")
        )
    
    def parse_claude_md(self) -> List[RuleMetadata]:
        """Parse Claude.md and extract rules with metadata"""
        if not self.claude_md_path.exists():
            print(f"ERROR: Claude.md not found at {self.claude_md_path}")
            return []
        
        with open(self.claude_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        rules = []
        current_section = "Unknown"
        rule_counter = 0
        
        # Split content into sections
        sections = re.split(r'^## (.+)$', content, flags=re.MULTILINE)
        
        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                section_title = sections[i].strip()
                section_content = sections[i + 1].strip()
                current_section = section_title
                
                # Extract individual rules from bullets and numbered lists
                rule_patterns = [
                    r'^\s*[-*]\s*\*\*(.+?)\*\*\s*[-–—]\s*(.+?)(?=^\s*[-*]|\n\n|\Z)',
                    r'^\s*\d+\.\s*\*\*(.+?)\*\*\s*[-–—]\s*(.+?)(?=^\s*\d+\.|\n\n|\Z)',
                    r'^\s*[-*]\s*(.+?)(?=^\s*[-*]|\n\n|\Z)',
                ]
                
                for pattern in rule_patterns:
                    matches = re.finditer(pattern, section_content, re.MULTILINE | re.DOTALL)
                    for match in matches:
                        rule_counter += 1
                        rule_id = f"RULE-{rule_counter:03d}"
                        
                        if len(match.groups()) >= 2:
                            rule_title = match.group(1).strip()
                            rule_desc = match.group(2).strip()
                            rule_content = f"{rule_title} - {rule_desc}"
                        else:
                            rule_content = match.group(1).strip()
                        
                        # Determine alert level based on keywords
                        alert_level = self.determine_alert_level(rule_content, section_title)
                        
                        # Extract tags and phase relevance
                        tags = self.extract_tags(rule_content)
                        phase_relevance = self.extract_phase_relevance(rule_content, section_title)
                        
                        # Create version hash
                        version_hash = hashlib.md5(rule_content.encode()).hexdigest()[:8]
                        
                        # Check if rule exists in metadata
                        existing_rule = self.rule_metadata.get(rule_id)
                        if existing_rule and existing_rule.version_hash == version_hash:
                            # Rule unchanged, keep existing metadata
                            rules.append(existing_rule)
                        else:
                            # New or changed rule
                            rule_meta = RuleMetadata(
                                rule_id=rule_id,
                                content=rule_content,
                                section=section_title,
                                alert_level=alert_level,
                                last_used=existing_rule.last_used if existing_rule else None,
                                usage_count=existing_rule.usage_count if existing_rule else 0,
                                compliance_score=existing_rule.compliance_score if existing_rule else 1.0,
                                version_hash=version_hash,
                                created_date=existing_rule.created_date if existing_rule else datetime.now(),
                                last_updated=datetime.now(),
                                tags=tags,
                                phase_relevance=phase_relevance
                            )
                            rules.append(rule_meta)
                            self.rule_metadata[rule_id] = rule_meta
        
        return rules
    
    def determine_alert_level(self, rule_content: str, section: str) -> AlertLevel:
        """Determine alert level based on rule content and section"""
        critical_keywords = [
            'must', 'never', 'always', 'critical', 'essential', 'required',
            'mandatory', 'security', 'safety', 'backup', 'protected'
        ]
        
        advisory_keywords = [
            'should', 'recommend', 'prefer', 'consider', 'suggest',
            'best practice', 'optimize', 'enhance'
        ]
        
        critical_sections = [
            'Essential Principles', 'Core Rules', 'Critical Decision Protocols',
            'Protection & Safety', 'Security'
        ]
        
        rule_lower = rule_content.lower()
        section_lower = section.lower()
        
        if any(keyword in rule_lower for keyword in critical_keywords) or \
           any(sect.lower() in section_lower for sect in critical_sections):
            return AlertLevel.CRITICAL
        elif any(keyword in rule_lower for keyword in advisory_keywords):
            return AlertLevel.ADVISORY
        else:
            return AlertLevel.INFO
    
    def extract_tags(self, rule_content: str) -> Set[str]:
        """Extract hashtags and semantic tags from rule content"""
        tags = set()
        
        # Extract explicit hashtags
        hashtag_pattern = r'#(\w+)'
        hashtags = re.findall(hashtag_pattern, rule_content)
        tags.update(f"#{tag}" for tag in hashtags)
        
        # Extract semantic tags based on keywords
        tag_mapping = {
            'docker': '#docker',
            'test': '#testing',
            'research': '#research',
            'jina': '#jina',
            'documentation': '#docs',
            'api': '#api',
            'security': '#security',
            'backup': '#backup',
            'module': '#module',
            'example': '#examples',
            'scoring': '#scoring',
            'neural': '#neural',
            'decision': '#decision',
            'pipeline': '#pipeline'
        }
        
        rule_lower = rule_content.lower()
        for keyword, tag in tag_mapping.items():
            if keyword in rule_lower:
                tags.add(tag)
        
        return tags
    
    def extract_phase_relevance(self, rule_content: str, section: str) -> Set[str]:
        """Extract which phases this rule is relevant to"""
        phases = set()
        
        phase_keywords = {
            'phase 1': 'foundation',
            'phase 2': 'intelligence', 
            'phase 3': 'optimization',
            'foundation': 'foundation',
            'intelligence': 'intelligence',
            'optimization': 'optimization',
            'testing': 'testing',
            'deployment': 'deployment',
            'research': 'research'
        }
        
        content_lower = f"{rule_content} {section}".lower()
        
        for keyword, phase in phase_keywords.items():
            if keyword in content_lower:
                phases.add(phase)
        
        # Default to all phases if none specified
        if not phases:
            phases = {'foundation', 'intelligence', 'optimization'}
        
        return phases
    
    def calculate_rule_relevance(self, rule: RuleMetadata) -> float:
        """Calculate relevance score for current session context"""
        score = 0.0
        
        # Base relevance
        score += 0.3
        
        # Phase relevance
        if self.session_context.phase in rule.phase_relevance:
            score += 0.3
        
        # Intent tag matching
        common_tags = rule.tags.intersection(self.session_context.intent_tags)
        if common_tags:
            score += 0.2 * len(common_tags)
        
        # Usage frequency (more used = more relevant)
        if rule.usage_count > 0:
            score += min(0.1, rule.usage_count * 0.01)
        
        # Recency (recently used = more relevant)
        if rule.last_used:
            days_since_use = (datetime.now() - rule.last_used).days
            if days_since_use < 7:
                score += 0.1 * (7 - days_since_use) / 7
        
        # Compliance score (well-followed rules = more relevant)
        score += 0.1 * rule.compliance_score
        
        return min(score, 1.0)
    
    def check_stale_rules(self, rules: List[RuleMetadata]) -> List[RuleMetadata]:
        """Identify stale rules that need review"""
        stale_rules = []
        cutoff_date = datetime.now() - timedelta(days=30)
        
        for rule in rules:
            is_stale = (
                rule.last_updated < cutoff_date or
                (rule.last_used and rule.last_used < cutoff_date) or
                rule.compliance_score < 0.3
            )
            
            if is_stale:
                stale_rules.append(rule)
        
        return stale_rules
    
    def perform_preflight_check(self, relevant_rules: List[RuleMetadata]) -> Dict:
        """Perform pre-flight compliance check"""
        results = {
            'critical_violations': [],
            'advisory_warnings': [],
            'compliance_summary': {},
            'recommended_actions': []
        }
        
        for rule in relevant_rules:
            if rule.alert_level == AlertLevel.CRITICAL:
                # Check for common critical violations
                violations = self.check_critical_rule_compliance(rule)
                if violations:
                    results['critical_violations'].extend(violations)
            elif rule.alert_level == AlertLevel.ADVISORY:
                warnings = self.check_advisory_rule_compliance(rule)
                if warnings:
                    results['advisory_warnings'].extend(warnings)
        
        # Generate recommended actions
        if results['critical_violations']:
            results['recommended_actions'].append(
                "🚨 Critical violations detected. Address before proceeding."
            )
        
        if results['advisory_warnings']:
            results['recommended_actions'].append(
                "⚠️  Advisory warnings found. Consider addressing for optimal compliance."
            )
        
        return results
    
    def check_critical_rule_compliance(self, rule: RuleMetadata) -> List[str]:
        """Check compliance for critical rules"""
        violations = []
        
        rule_lower = rule.content.lower()
        
        # Docker compliance
        if 'docker' in rule_lower and 'must use docker' in rule_lower:
            if not self.check_docker_available():
                violations.append(f"Docker not available but required by {rule.rule_id}")
        
        # Testing compliance
        if 'test' in rule_lower and ('must' in rule_lower or 'always' in rule_lower):
            if self.session_context.current_tool in ['Write', 'Edit'] and \
               any('.py' in path for path in self.session_context.file_paths):
                if not self.check_tests_exist():
                    violations.append(f"Tests required but missing - {rule.rule_id}")
        
        # Backup compliance
        if 'backup' in rule_lower and 'before' in rule_lower:
            if self.session_context.current_tool in ['Edit', 'MultiEdit']:
                violations.append(f"Backup recommended before edits - {rule.rule_id}")
        
        return violations
    
    def check_advisory_rule_compliance(self, rule: RuleMetadata) -> List[str]:
        """Check compliance for advisory rules"""
        warnings = []
        
        rule_lower = rule.content.lower()
        
        # Code quality warnings
        if 'pep8' in rule_lower or 'format' in rule_lower:
            warnings.append(f"Consider code formatting - {rule.rule_id}")
        
        # Documentation warnings
        if 'document' in rule_lower and self.session_context.current_tool == 'Write':
            warnings.append(f"Documentation recommended - {rule.rule_id}")
        
        return warnings
    
    def check_docker_available(self) -> bool:
        """Check if Docker is available"""
        try:
            import subprocess
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def check_tests_exist(self) -> bool:
        """Check if tests exist for current project"""
        test_dirs = ['tests', 'test']
        for test_dir in test_dirs:
            test_path = self.aai_root / test_dir
            if test_path.exists() and any(test_path.glob('*.py')):
                return True
        return False
    
    def log_compliance_event(self, rule_id: str, status: ComplianceStatus, details: str = ""):
        """Log compliance event to audit trail"""
        self.compliance_log.parent.mkdir(parents=True, exist_ok=True)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_context.session_id,
            'rule_id': rule_id,
            'status': status.value,
            'details': details,
            'tool': self.session_context.current_tool,
            'phase': self.session_context.phase
        }
        
        with open(self.compliance_log, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        # Update rule metadata
        if rule_id in self.rule_metadata:
            rule = self.rule_metadata[rule_id]
            rule.last_used = datetime.now()
            rule.usage_count += 1
            
            # Update compliance score
            if status == ComplianceStatus.FOLLOWED:
                rule.compliance_score = min(1.0, rule.compliance_score + 0.1)
            elif status == ComplianceStatus.VIOLATED:
                rule.compliance_score = max(0.0, rule.compliance_score - 0.2)
    
    def generate_compliance_report(self, rules: List[RuleMetadata]) -> str:
        """Generate human-readable compliance report"""
        relevant_rules = sorted(rules, key=self.calculate_rule_relevance, reverse=True)[:10]
        stale_rules = self.check_stale_rules(rules)
        
        report = f"""
🧠 Claude.md Compliance Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Session: {self.session_context.session_id}
Phase: {self.session_context.phase}
Tool: {self.session_context.current_tool}

📊 TOP RELEVANT RULES ({len(relevant_rules)}):
"""
        
        for i, rule in enumerate(relevant_rules[:5], 1):
            relevance = self.calculate_rule_relevance(rule)
            report += f"""
{i}. {rule.alert_level.value} {rule.rule_id} (Relevance: {relevance:.2f})
   Section: {rule.section}
   Content: {rule.content[:100]}...
   Last Used: {rule.last_used.strftime('%Y-%m-%d') if rule.last_used else 'Never'}
   Compliance: {rule.compliance_score:.2f}
"""
        
        if stale_rules:
            report += f"""
⚠️  STALE RULES REQUIRING REVIEW ({len(stale_rules)}):
"""
            for rule in stale_rules[:3]:
                report += f"   • {rule.rule_id}: {rule.content[:80]}...\n"
        
        # Preflight check
        preflight = self.perform_preflight_check(relevant_rules)
        
        if preflight['critical_violations']:
            report += f"""
🚨 CRITICAL VIOLATIONS:
"""
            for violation in preflight['critical_violations']:
                report += f"   • {violation}\n"
        
        if preflight['advisory_warnings']:
            report += f"""
⚠️  ADVISORY WARNINGS:
"""
            for warning in preflight['advisory_warnings']:
                report += f"   • {warning}\n"
        
        if preflight['recommended_actions']:
            report += f"""
🎯 RECOMMENDED ACTIONS:
"""
            for action in preflight['recommended_actions']:
                report += f"   • {action}\n"
        
        return report
    
    def run_dashboard_command(self, args: argparse.Namespace):
        """Run dashboard command for rule inspection"""
        rules = self.parse_claude_md()
        
        if args.phase:
            rules = [r for r in rules if args.phase in r.phase_relevance]
        
        if args.stale:
            rules = self.check_stale_rules(rules)
        
        if args.unused:
            rules = [r for r in rules if r.usage_count == 0]
        
        print(self.generate_compliance_report(rules))
        
        if args.suggest_updates:
            print("\n🔧 SUGGESTED UPDATES:")
            for rule in rules:
                if rule.compliance_score < 0.3:
                    print(f"   • Consider making {rule.rule_id} advisory instead of critical")
                elif rule.usage_count == 0:
                    print(f"   • Consider retiring unused rule {rule.rule_id}")
    
    def main(self):
        """Main execution function"""
        # Parse command line arguments
        parser = argparse.ArgumentParser(description='Claude.md Compliance Checker')
        parser.add_argument('--dashboard', action='store_true', help='Show compliance dashboard')
        parser.add_argument('--phase', help='Filter by phase')
        parser.add_argument('--stale', action='store_true', help='Show stale rules only')
        parser.add_argument('--unused', action='store_true', help='Show unused rules only')
        parser.add_argument('--suggest-updates', action='store_true', help='Suggest rule updates')
        
        args = parser.parse_args()
        
        if args.dashboard:
            self.run_dashboard_command(args)
            return
        
        # Normal hook execution
        rules = self.parse_claude_md()
        
        if not rules:
            print("⚠️  No rules found in Claude.md")
            return
        
        # Calculate relevance and get top rules
        relevant_rules = sorted(rules, key=self.calculate_rule_relevance, reverse=True)[:10]
        
        # Perform preflight check
        preflight = self.perform_preflight_check(relevant_rules)
        
        # Show critical violations (blocking)
        if preflight['critical_violations']:
            print("🚨 CRITICAL COMPLIANCE VIOLATIONS DETECTED:")
            for violation in preflight['critical_violations']:
                print(f"   ❌ {violation}")
            print("\n🛑 Please address critical violations before proceeding.")
            
            # Log violations
            for violation in preflight['critical_violations']:
                rule_id = violation.split(' ')[-1] if 'RULE-' in violation else 'UNKNOWN'
                self.log_compliance_event(rule_id, ComplianceStatus.VIOLATED, violation)
            
            # Save metadata and exit
            self.save_rule_metadata()
            sys.exit(1)
        
        # Show advisory warnings (non-blocking)
        if preflight['advisory_warnings']:
            print("⚠️  Advisory compliance warnings:")
            for warning in preflight['advisory_warnings']:
                print(f"   • {warning}")
        
        # ALWAYS show that hook is running
        print("🧠 Claude.md Hook: Checking compliance before tool execution")
        
        # Show relevant rules summary
        print(f"📋 Active Rules (Top {len(relevant_rules)}):")
        for rule in relevant_rules[:3]:
            relevance = self.calculate_rule_relevance(rule)
            print(f"   {rule.alert_level.value} {rule.rule_id} (rel: {relevance:.2f})")
        
        # Check for stale rules
        stale_rules = self.check_stale_rules(rules)
        if stale_rules:
            print(f"📅 {len(stale_rules)} stale rules need review (run --dashboard --stale)")
        
        # Log successful check
        for rule in relevant_rules[:5]:
            self.log_compliance_event(rule.rule_id, ComplianceStatus.FOLLOWED, "Pre-task check")
        
        # Save updated metadata
        self.save_rule_metadata()
        
        print("✅ Claude.md compliance check complete")

if __name__ == "__main__":
    checker = ClaudeMdChecker()
    checker.main()