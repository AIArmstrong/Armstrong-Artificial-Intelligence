#!/usr/bin/env python3
"""
Example Feedback Scoring System
Links examples to feedback-learning.md and score-tracker.md for effectiveness tracking
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

class ExampleFeedbackScorer:
    def __init__(self):
        self.aai_root = Path("/mnt/c/Users/Brandon/AAI")
        self.examples_dir = self.aai_root / "examples"
        self.metadata_file = self.examples_dir / "metadata.json"
        self.feedback_file = self.aai_root / "brain/workflows/feedback-learning.md"
        self.score_tracker_file = self.aai_root / "brain/modules/score-tracker.md"
        self.queue_file = self.aai_root / "brain/logs/queue.json"
        
    def load_examples_metadata(self):
        """Load examples metadata"""
        if not self.metadata_file.exists():
            return {"examples": {}, "statistics": {}}
        
        with open(self.metadata_file, 'r') as f:
            return json.load(f)
    
    def save_examples_metadata(self, metadata):
        """Save examples metadata"""
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def parse_feedback_learning(self):
        """Parse feedback-learning.md for example-related feedback"""
        if not self.feedback_file.exists():
            return []
        
        with open(self.feedback_file, 'r') as f:
            content = f.read()
        
        # Extract feedback entries
        feedback_entries = []
        
        # Look for feedback entries with example references
        pattern = r'### ([^\\n]+)\\n\\*\\*.*?\\*\\*: ([^\\n]+)\\n\\n\\*\\*Learning\\*\\*:\\s*\\n(.*?)(?=\\n###|\\n---|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            timestamp_info = match[0]
            feedback_type = match[1]
            learning_content = match[2]
            
            # Extract timestamp
            timestamp_match = re.search(r'(\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2})', timestamp_info)
            timestamp = timestamp_match.group(1) if timestamp_match else datetime.now().isoformat()
            
            # Check if this feedback relates to examples
            if any(keyword in learning_content.lower() for keyword in ['example', 'pattern', 'template', 'code']):
                feedback_entries.append({
                    'timestamp': timestamp,
                    'type': feedback_type,
                    'content': learning_content.strip(),
                    'example_related': True
                })
        
        return feedback_entries
    
    def extract_example_usage_from_queue(self):
        """Extract example usage patterns from queue completions"""
        if not self.queue_file.exists():
            return []
        
        with open(self.queue_file, 'r') as f:
            queue_data = json.load(f)
        
        usage_patterns = []
        
        # Check completed tasks for example usage
        for task in queue_data.get('completed', []):
            task_description = task.get('description', '')
            
            # Look for example-related keywords
            if any(keyword in task_description.lower() for keyword in ['example', 'pattern', 'template']):
                usage_patterns.append({
                    'task_id': task['id'],
                    'task_title': task['title'],
                    'description': task_description,
                    'completed': task.get('completed', datetime.now().isoformat()),
                    'success_indicators': self.extract_success_indicators(task)
                })
        
        return usage_patterns
    
    def extract_success_indicators(self, task):
        """Extract success indicators from task data"""
        indicators = {
            'completed_successfully': task.get('status') == 'completed',
            'had_errors': False,
            'duration_reasonable': True,
            'user_satisfaction': 'unknown'
        }
        
        # Check for error indicators in description
        error_keywords = ['error', 'failed', 'bug', 'issue', 'problem']
        if any(keyword in task.get('description', '').lower() for keyword in error_keywords):
            indicators['had_errors'] = True
        
        # Estimate duration reasonableness
        estimated = task.get('estimated_duration', '')
        if 'hour' in estimated:
            try:
                hours = int(re.search(r'(\\d+)', estimated).group(1))
                # Simple heuristic: tasks > 5 hours might indicate complexity issues
                indicators['duration_reasonable'] = hours <= 5
            except:
                pass
        
        return indicators
    
    def calculate_example_score(self, example_id, usage_data, feedback_data):
        """Calculate comprehensive score for an example"""
        score_components = {
            'usage_frequency': 0.0,
            'success_rate': 0.0,
            'recency': 0.0,
            'feedback_quality': 0.0,
            'complexity_appropriateness': 0.0
        }
        
        # Usage frequency score (0-1)
        usage_count = len([u for u in usage_data if example_id in u.get('description', '')])
        score_components['usage_frequency'] = min(usage_count / 10.0, 1.0)  # Cap at 10 uses
        
        # Success rate score (0-1)
        if usage_count > 0:
            successful_uses = sum(1 for u in usage_data 
                                if example_id in u.get('description', '') and 
                                   u.get('success_indicators', {}).get('completed_successfully', False))
            score_components['success_rate'] = successful_uses / usage_count
        
        # Recency score (0-1) - higher for recently used examples
        recent_uses = [u for u in usage_data if example_id in u.get('description', '')]
        if recent_uses:
            most_recent = max(recent_uses, key=lambda x: x.get('completed', ''))
            days_since_use = (datetime.now() - datetime.fromisoformat(most_recent['completed'][:19])).days
            score_components['recency'] = max(0, 1 - (days_since_use / 30.0))  # Decay over 30 days
        
        # Feedback quality score (0-1)
        relevant_feedback = [f for f in feedback_data if example_id in f.get('content', '')]
        if relevant_feedback:
            # Simple heuristic: positive feedback keywords
            positive_keywords = ['success', 'work', 'good', 'effective', 'helpful']
            negative_keywords = ['error', 'failed', 'problem', 'issue', 'bug']
            
            positive_count = sum(1 for f in relevant_feedback 
                               for keyword in positive_keywords 
                               if keyword in f['content'].lower())
            negative_count = sum(1 for f in relevant_feedback 
                               for keyword in negative_keywords 
                               if keyword in f['content'].lower())
            
            total_feedback = positive_count + negative_count
            if total_feedback > 0:
                score_components['feedback_quality'] = positive_count / total_feedback
        
        # Complexity appropriateness (placeholder - would be enhanced with actual complexity analysis)
        score_components['complexity_appropriateness'] = 0.7  # Default reasonable score
        
        # Calculate weighted average
        weights = {
            'usage_frequency': 0.2,
            'success_rate': 0.3,
            'recency': 0.2,
            'feedback_quality': 0.2,
            'complexity_appropriateness': 0.1
        }
        
        final_score = sum(score_components[component] * weights[component] 
                         for component in score_components)
        
        return {
            'final_score': final_score,
            'components': score_components,
            'calculated_at': datetime.now().isoformat()
        }
    
    def update_example_scores(self):
        """Update scores for all examples based on usage and feedback"""
        metadata = self.load_examples_metadata()
        
        # Get feedback and usage data
        feedback_data = self.parse_feedback_learning()
        usage_data = self.extract_example_usage_from_queue()
        
        # Update scores for each example
        examples = metadata.get('examples', {})
        updated_count = 0
        
        for example_id, example_data in examples.items():
            # Calculate new score
            score_data = self.calculate_example_score(example_id, usage_data, feedback_data)
            
            # Update example metadata
            example_data['feedback_score'] = score_data['final_score']
            example_data['score_components'] = score_data['components']
            example_data['last_scored'] = score_data['calculated_at']
            
            # Update usage statistics
            example_usage = [u for u in usage_data if example_id in u.get('description', '')]
            if example_usage:
                example_data['usage_count'] = len(example_usage)
                example_data['last_used'] = max(u['completed'] for u in example_usage)
                
                # Calculate success rate
                successful_uses = sum(1 for u in example_usage 
                                    if u.get('success_indicators', {}).get('completed_successfully', False))
                example_data['success_rate'] = successful_uses / len(example_usage)
            
            updated_count += 1
        
        # Update overall statistics
        if 'statistics' not in metadata:
            metadata['statistics'] = {}
        
        metadata['statistics'].update({
            'last_scoring_update': datetime.now().isoformat(),
            'total_examples_scored': updated_count,
            'feedback_entries_processed': len(feedback_data),
            'usage_patterns_analyzed': len(usage_data)
        })
        
        # Save updated metadata
        self.save_examples_metadata(metadata)
        
        return {
            'updated_examples': updated_count,
            'feedback_entries': len(feedback_data),
            'usage_patterns': len(usage_data),
            'metadata_file': str(self.metadata_file)
        }
    
    def generate_scoring_report(self):
        """Generate human-readable scoring report"""
        metadata = self.load_examples_metadata()
        examples = metadata.get('examples', {})
        
        if not examples:
            return "No examples found to score."
        
        # Sort examples by score
        sorted_examples = sorted(examples.items(), 
                               key=lambda x: x[1].get('feedback_score', 0), 
                               reverse=True)
        
        report = f"""# Example Scoring Report

## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CDT')}

## Scoring Summary
- **Total Examples**: {len(examples)}
- **Average Score**: {sum(e.get('feedback_score', 0) for _, e in examples.items()) / len(examples):.2f}
- **Last Update**: {metadata.get('statistics', {}).get('last_scoring_update', 'Never')}

## Top Performing Examples

"""
        
        for example_id, example_data in sorted_examples[:10]:  # Top 10
            score = example_data.get('feedback_score', 0)
            usage_count = example_data.get('usage_count', 0)
            success_rate = example_data.get('success_rate', 0)
            
            report += f"### {example_data.get('title', example_id)}\\n"
            report += f"**Score**: {score:.2f}/1.0\\n"
            report += f"**Usage**: {usage_count} times\\n"
            report += f"**Success Rate**: {success_rate:.1%}\\n"
            report += f"**Category**: {example_data.get('category', 'Unknown')}\\n\\n"
        
        # Examples needing attention
        low_scoring = [e for e in sorted_examples if e[1].get('feedback_score', 0) < 0.3]
        
        if low_scoring:
            report += "## Examples Needing Attention\\n"
            for example_id, example_data in low_scoring:
                score = example_data.get('feedback_score', 0)
                report += f"- **{example_data.get('title', example_id)}** (Score: {score:.2f})\\n"
        
        report += """
## Scoring Components
- **Usage Frequency**: How often the example is used
- **Success Rate**: Percentage of successful implementations
- **Recency**: How recently the example was used
- **Feedback Quality**: Positive vs negative feedback
- **Complexity Appropriateness**: How well complexity matches use cases

## Recommendations
- Examples with scores < 0.3 should be reviewed or retired
- Examples with scores > 0.7 should be promoted and featured
- Examples with high usage but low success rates need improvement

---
*Generated by Example Feedback Scoring System*
"""
        
        return report
    
    def save_scoring_report(self, report):
        """Save scoring report to file"""
        report_path = self.examples_dir / "scoring-report.md"
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        return report_path

def main():
    scorer = ExampleFeedbackScorer()
    
    # Update example scores
    results = scorer.update_example_scores()
    
    print(f"Updated {results['updated_examples']} examples")
    print(f"Processed {results['feedback_entries']} feedback entries")
    print(f"Analyzed {results['usage_patterns']} usage patterns")
    
    # Generate and save report
    report = scorer.generate_scoring_report()
    report_path = scorer.save_scoring_report(report)
    
    print(f"Scoring report saved to: {report_path}")
    
    return results

if __name__ == '__main__':
    main()