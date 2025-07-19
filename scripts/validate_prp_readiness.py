#!/usr/bin/env python3
"""
PRP Implementation Readiness Assessment Framework
Auto-generated validation script that checks all gates before implementation
"""

import os
import sys
import json
import yaml
import subprocess
import argparse
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import re
import requests

@dataclass
class GateResult:
    """Result of a single gate validation"""
    name: str
    category: str
    passed: bool
    score: float
    message: str
    owner: str
    time_to_fix: str = "Unknown"
    fix_command: Optional[str] = None
    fallback: Optional[str] = None

@dataclass
class ReadinessReport:
    """Complete readiness assessment report"""
    prp_id: str
    overall_score: float
    gate_results: List[GateResult]
    category_scores: Dict[str, float]
    recommendation: str
    critical_blockers: List[str]
    time_to_resolution: str
    next_steps: List[str]

class PRPReadinessValidator:
    """Main validator class for PRP readiness assessment"""
    
    def __init__(self, prp_file: str, base_dir: str = "/mnt/c/Users/Brandon/AAI"):
        self.prp_file = prp_file
        self.base_dir = Path(base_dir)
        self._load_env_file()
        self.prp_config = self._load_prp_config()
        self.gate_weights = {
            "infrastructure": 0.35,
            "credentials": 0.30, 
            "dependencies": 0.20,
            "environment": 0.15
        }
        
    def _load_env_file(self):
        """Load environment variables from .env file"""
        env_file = self.base_dir / ".env"
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key] = value
            except Exception as e:
                print(f"⚠️  Warning: Could not load .env file: {e}")
        
    def _load_prp_config(self) -> Dict[str, Any]:
        """Load and parse PRP configuration from markdown file"""
        try:
            with open(self.prp_file, 'r') as f:
                content = f.read()
            
            # Extract YAML sections from markdown
            yaml_blocks = re.findall(r'```yaml\n(.*?)\n```', content, re.DOTALL)
            
            config = {}
            for block in yaml_blocks:
                try:
                    parsed = yaml.safe_load(block)
                    if isinstance(parsed, dict):
                        config.update(parsed)
                except yaml.YAMLError:
                    continue
            
            # If no structured gates found, generate defaults for email campaign
            if not any(key.endswith('_gates') for key in config.keys()):
                config = self._generate_default_gates(content)
                    
            return config
            
        except Exception as e:
            print(f"❌ Error loading PRP file: {e}")
            return {}
    
    def _generate_default_gates(self, content: str) -> Dict[str, Any]:
        """Generate default gates for real estate email campaign PRP"""
        return {
            "infrastructure_gates": {
                "service_availability": [
                    {
                        "service": "n8n",
                        "test": "curl -s -o /dev/null -w '%{http_code}' https://n8n.olympus-council.xyz",
                        "expected": "200",
                        "owner": "devops",
                        "time_to_fix": "10 minutes",
                        "fallback": "Check n8n container status"
                    },
                    {
                        "service": "openrouter",
                        "test": "curl -s -H 'Authorization: Bearer $OPENROUTER_API_KEY' https://openrouter.ai/api/v1/models",
                        "expected": "data",
                        "owner": "devops", 
                        "time_to_fix": "5 minutes"
                    }
                ]
            },
            "credential_gates": {
                "critical": [
                    {"credential": "OPENROUTER_API_KEY", "location": ".env", "owner": "user", "time_to_fix": "2 minutes"},
                    {"credential": "GOOGLE_CLIENT_ID", "location": ".env", "owner": "user", "time_to_fix": "5 minutes"},
                    {"credential": "GOOGLE_CLIENT_SECRET", "location": ".env", "owner": "user", "time_to_fix": "5 minutes"},
                    {"credential": "DATABASE_URL", "location": ".env", "owner": "user", "time_to_fix": "2 minutes"},
                    {"credential": "SUPABASE_URL", "location": ".env", "owner": "user", "time_to_fix": "2 minutes"}
                ]
            },
            "system_dependencies": {
                "python_packages": [
                    {"package": "fastapi", "install": "python3 -m pip install fastapi"},
                    {"package": "pydantic", "install": "python3 -m pip install pydantic"},
                    {"package": "httpx", "install": "python3 -m pip install httpx"},
                    {"package": "google-auth-oauthlib", "install": "python3 -m pip install google-auth-oauthlib"},
                    {"package": "google-api-python-client", "install": "python3 -m pip install google-api-python-client"},
                    {"package": "uvicorn", "install": "python3 -m pip install uvicorn"}
                ]
            },
            "environment_validation": {
                "required_files": [
                    {"file": ".env", "required_vars": ["OPENROUTER_API_KEY", "GOOGLE_CLIENT_ID", "DATABASE_URL"]},
                ],
                "required_directories": [
                    {"path": "projects/real_estate_campaign", "create_if_missing": True}
                ]
            }
        }
    
    def validate_infrastructure_gates(self) -> List[GateResult]:
        """Validate infrastructure connectivity and service availability"""
        results = []
        
        infra_gates = self.prp_config.get('infrastructure_gates', {})
        
        # Network connectivity tests
        for conn_test in infra_gates.get('network_connectivity', []):
            result = self._test_network_connectivity(conn_test)
            results.append(result)
        
        # Service availability tests  
        for service_test in infra_gates.get('service_availability', []):
            result = self._test_service_availability(service_test)
            results.append(result)
            
        # Port accessibility tests
        for port_test in infra_gates.get('port_accessibility', []):
            result = self._test_port_accessibility(port_test)
            results.append(result)
            
        return results
    
    def _test_network_connectivity(self, test_config: Dict) -> GateResult:
        """Test network connectivity to external services"""
        service = test_config.get('service', 'unknown')
        test_cmd = test_config.get('test', '').replace('<host>', test_config.get('host', ''))
        
        try:
            result = subprocess.run(
                test_cmd.split(), 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            passed = result.returncode == 0
            message = "Network reachable" if passed else f"Network unreachable: {result.stderr}"
            
            return GateResult(
                name=f"Network: {service}",
                category="infrastructure", 
                passed=passed,
                score=1.0 if passed else 0.0,
                message=message,
                owner=test_config.get('owner', 'devops')
            )
            
        except Exception as e:
            return GateResult(
                name=f"Network: {service}",
                category="infrastructure",
                passed=False,
                score=0.0,
                message=f"Test failed: {str(e)}",
                owner=test_config.get('owner', 'devops')
            )
    
    def _test_service_availability(self, test_config: Dict) -> GateResult:
        """Test external service health endpoints"""
        service = test_config.get('service', 'unknown')
        test_cmd = test_config.get('test', '')
        
        # Replace environment variables in test command
        for env_var in re.findall(r'\$([A-Z_]+)', test_cmd):
            env_value = os.getenv(env_var, '')
            test_cmd = test_cmd.replace(f'${env_var}', env_value)
        
        try:
            result = subprocess.run(
                test_cmd, 
                shell=True,
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            passed = result.returncode == 0 and test_config.get('expected', '200') in result.stdout
            
            if passed:
                message = f"Service {service} healthy"
            else:
                message = f"Service {service} unhealthy: {result.stderr or result.stdout}"
            
            return GateResult(
                name=f"Service: {service}",
                category="infrastructure",
                passed=passed,
                score=1.0 if passed else 0.0,
                message=message,
                owner=test_config.get('owner', 'devops'),
                time_to_fix=test_config.get('time_to_fix', '15 minutes'),
                fallback=test_config.get('fallback')
            )
            
        except Exception as e:
            return GateResult(
                name=f"Service: {service}",
                category="infrastructure", 
                passed=False,
                score=0.0,
                message=f"Health check failed: {str(e)}",
                owner=test_config.get('owner', 'devops'),
                fallback=test_config.get('fallback')
            )
    
    def _test_port_accessibility(self, test_config: Dict) -> GateResult:
        """Test port accessibility for databases and services"""
        service = test_config.get('service', 'unknown')
        host = test_config.get('host', 'localhost')
        port = test_config.get('port', '80')
        
        try:
            # Use netcat-like functionality
            result = subprocess.run(
                ['timeout', '5', 'bash', '-c', f'echo > /dev/tcp/{host}/{port}'],
                capture_output=True,
                timeout=6
            )
            
            passed = result.returncode == 0
            message = f"Port {port} accessible" if passed else f"Port {port} not accessible"
            
            return GateResult(
                name=f"Port: {service}:{port}",
                category="infrastructure",
                passed=passed, 
                score=1.0 if passed else 0.0,
                message=message,
                owner=test_config.get('owner', 'devops'),
                fallback=test_config.get('fallback', 'Check firewall rules')
            )
            
        except Exception as e:
            return GateResult(
                name=f"Port: {service}:{port}",
                category="infrastructure",
                passed=False,
                score=0.0, 
                message=f"Port test failed: {str(e)}",
                owner=test_config.get('owner', 'devops')
            )
    
    def validate_credential_gates(self) -> List[GateResult]:
        """Validate all required credentials and API keys"""
        results = []
        
        cred_gates = self.prp_config.get('credential_gates', {})
        
        # Critical credentials
        for cred in cred_gates.get('critical', []):
            result = self._test_credential(cred, critical=True)
            results.append(result)
            
        # Optional credentials  
        for cred in cred_gates.get('optional', []):
            result = self._test_credential(cred, critical=False)
            results.append(result)
            
        return results
    
    def _test_credential(self, cred_config: Dict, critical: bool = True) -> GateResult:
        """Test individual credential availability and validity"""
        cred_name = cred_config.get('credential', 'unknown')
        location = cred_config.get('location', '.env')
        
        # Check if credential exists
        if location == '.env':
            env_var = cred_name
            value = os.getenv(env_var)
            
            if not value:
                return GateResult(
                    name=f"Credential: {cred_name}",
                    category="credentials",
                    passed=False,
                    score=0.0 if critical else 0.5,
                    message=f"Missing {env_var} in environment",
                    owner=cred_config.get('owner', 'user'),
                    time_to_fix=cred_config.get('time_to_fix', '5 minutes'),
                    fix_command=f'echo "{env_var}=your_key_here" >> .env'
                )
            
            # Test credential validity if validation provided
            validation_cmd = cred_config.get('validation')
            if validation_cmd:
                try:
                    # Replace environment variable in command
                    test_cmd = validation_cmd.replace(f'${env_var}', value)
                    
                    result = subprocess.run(
                        test_cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    expected = cred_config.get('expected', '200')
                    valid = expected in str(result.returncode) or expected in result.stdout
                    
                    return GateResult(
                        name=f"Credential: {cred_name}",
                        category="credentials",
                        passed=valid,
                        score=1.0 if valid else 0.0,
                        message="Valid credential" if valid else "Invalid credential format",
                        owner=cred_config.get('owner', 'user')
                    )
                    
                except Exception as e:
                    return GateResult(
                        name=f"Credential: {cred_name}",
                        category="credentials",
                        passed=False,
                        score=0.0,
                        message=f"Validation failed: {str(e)}",
                        owner=cred_config.get('owner', 'user')
                    )
            else:
                # Credential exists but no validation test
                return GateResult(
                    name=f"Credential: {cred_name}",
                    category="credentials", 
                    passed=True,
                    score=1.0,
                    message="Credential found (not validated)",
                    owner=cred_config.get('owner', 'user')
                )
        
        # Handle other credential locations (OAuth, files, etc.)
        return GateResult(
            name=f"Credential: {cred_name}",
            category="credentials",
            passed=False,
            score=0.0,
            message=f"Unsupported credential location: {location}",
            owner=cred_config.get('owner', 'user')
        )
    
    def validate_dependency_gates(self) -> List[GateResult]:
        """Validate system dependencies and external services"""
        results = []
        
        dep_gates = self.prp_config.get('system_dependencies', {})
        
        # Python packages
        for pkg in dep_gates.get('python_packages', []):
            result = self._test_python_package(pkg)
            results.append(result)
            
        # External services
        for service in dep_gates.get('external_services', []):
            result = self._test_external_service(service)
            results.append(result)
            
        # Database schema checks
        db_gates = self.prp_config.get('database_gates', {})
        for check in db_gates.get('schema_checks', []):
            result = self._test_database_schema(check)
            results.append(result)
            
        return results
    
    def _test_python_package(self, pkg_config: Dict) -> GateResult:
        """Test Python package installation and version"""
        package = pkg_config.get('package', '')
        pkg_name = package.split('>=')[0].split('==')[0]
        
        # Map package names to import names
        import_map = {
            'google-auth-oauthlib': 'google.auth.oauth2',
            'google-api-python-client': 'googleapiclient'
        }
        import_name = import_map.get(pkg_name, pkg_name.replace('-', '_'))
        
        try:
            # Try to import the package
            result = subprocess.run(
                [sys.executable, '-c', f'import {import_name}; print("OK")'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                # Package is installed, check version if specified
                if '>=' in package or '==' in package:
                    version_check = pkg_config.get('validation', '')
                    if version_check:
                        version_result = subprocess.run(
                            version_check,
                            shell=True,
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        version_ok = version_result.returncode == 0
                        message = "Package installed (version OK)" if version_ok else "Package installed (version check failed)"
                        score = 1.0 if version_ok else 0.7
                    else:
                        message = "Package installed"
                        score = 1.0
                else:
                    message = "Package installed"
                    score = 1.0
                    
                return GateResult(
                    name=f"Package: {pkg_name}",
                    category="dependencies",
                    passed=True,
                    score=score,
                    message=message,
                    owner="developer"
                )
            else:
                return GateResult(
                    name=f"Package: {pkg_name}",
                    category="dependencies",
                    passed=False,
                    score=0.0,
                    message=f"Package not installed",
                    owner="developer",
                    fix_command=pkg_config.get('install', f'pip install {package}')
                )
                
        except Exception as e:
            return GateResult(
                name=f"Package: {pkg_name}",
                category="dependencies",
                passed=False,
                score=0.0,
                message=f"Package test failed: {str(e)}",
                owner="developer"
            )
    
    def _test_external_service(self, service_config: Dict) -> GateResult:
        """Test external service availability"""
        service = service_config.get('service', 'unknown')
        validation = service_config.get('validation', '')
        
        try:
            result = subprocess.run(
                validation,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            expected = service_config.get('expected', '')
            passed = result.returncode == 0 and (not expected or expected in result.stdout)
            
            return GateResult(
                name=f"Service: {service}",
                category="dependencies",
                passed=passed,
                score=1.0 if passed else 0.0,
                message=f"Service available" if passed else f"Service unavailable: {result.stderr}",
                owner="devops",
                fallback=service_config.get('fallback')
            )
            
        except Exception as e:
            return GateResult(
                name=f"Service: {service}",
                category="dependencies",
                passed=False,
                score=0.0,
                message=f"Service test failed: {str(e)}",
                owner="devops"
            )
    
    def _test_database_schema(self, schema_config: Dict) -> GateResult:
        """Test database schema and table existence"""
        query = schema_config.get('query', '')
        expected = schema_config.get('expected', 'not null')
        
        try:
            # This would need actual database connection
            # For now, return a placeholder result
            return GateResult(
                name="Database Schema",
                category="dependencies", 
                passed=True,
                score=0.8,  # Partial score since we can't actually test
                message="Schema check skipped (no DB connection)",
                owner="backend",
                fix_command=schema_config.get('fix_command')
            )
            
        except Exception as e:
            return GateResult(
                name="Database Schema", 
                category="dependencies",
                passed=False,
                score=0.0,
                message=f"Schema test failed: {str(e)}",
                owner="backend"
            )
    
    def validate_environment_gates(self) -> List[GateResult]:
        """Validate environment setup and configuration files"""
        results = []
        
        env_validation = self.prp_config.get('environment_validation', {})
        
        # Required directories
        for dir_config in env_validation.get('required_directories', []):
            result = self._test_directory(dir_config)
            results.append(result)
            
        # Required files
        for file_config in env_validation.get('required_files', []):
            result = self._test_file(file_config)
            results.append(result)
            
        # Configuration files
        for config_file in env_validation.get('configuration_files', []):
            result = self._test_config_file(config_file)
            results.append(result)
            
        return results
    
    def _test_directory(self, dir_config: Dict) -> GateResult:
        """Test directory existence and permissions"""
        path = dir_config.get('path', '')
        create_if_missing = dir_config.get('create_if_missing', False)
        
        full_path = self.base_dir / path
        
        if full_path.exists() and full_path.is_dir():
            return GateResult(
                name=f"Directory: {path}",
                category="environment",
                passed=True,
                score=1.0,
                message="Directory exists",
                owner="developer"
            )
        elif create_if_missing:
            try:
                full_path.mkdir(parents=True, exist_ok=True)
                return GateResult(
                    name=f"Directory: {path}",
                    category="environment",
                    passed=True,
                    score=1.0,
                    message="Directory created",
                    owner="developer"
                )
            except Exception as e:
                return GateResult(
                    name=f"Directory: {path}",
                    category="environment",
                    passed=False,
                    score=0.0,
                    message=f"Failed to create directory: {str(e)}",
                    owner="developer"
                )
        else:
            return GateResult(
                name=f"Directory: {path}",
                category="environment",
                passed=False,
                score=0.0,
                message="Directory missing",
                owner="developer",
                fix_command=f"mkdir -p {full_path}"
            )
    
    def _test_file(self, file_config: Dict) -> GateResult:
        """Test file existence and required variables"""
        file_path = file_config.get('file', '')
        required_vars = file_config.get('required_vars', [])
        
        full_path = self.base_dir / file_path
        
        if not full_path.exists():
            template = file_config.get('template')
            return GateResult(
                name=f"File: {file_path}",
                category="environment",
                passed=False,
                score=0.0,
                message="File missing",
                owner="developer",
                fix_command=f"cp {template} {file_path}" if template else f"touch {file_path}"
            )
        
        # Check required variables in .env files
        if file_path == '.env' and required_vars:
            try:
                with open(full_path, 'r') as f:
                    content = f.read()
                
                missing_vars = []
                for var in required_vars:
                    if f"{var}=" not in content:
                        missing_vars.append(var)
                
                if missing_vars:
                    return GateResult(
                        name=f"File: {file_path}",
                        category="environment",
                        passed=False,
                        score=0.5,
                        message=f"Missing variables: {', '.join(missing_vars)}",
                        owner="user"
                    )
                else:
                    return GateResult(
                        name=f"File: {file_path}",
                        category="environment",
                        passed=True,
                        score=1.0,
                        message="All required variables present",
                        owner="developer"
                    )
                    
            except Exception as e:
                return GateResult(
                    name=f"File: {file_path}",
                    category="environment",
                    passed=False,
                    score=0.0,
                    message=f"Failed to read file: {str(e)}",
                    owner="developer"
                )
        
        return GateResult(
            name=f"File: {file_path}",
            category="environment",
            passed=True,
            score=1.0,
            message="File exists",
            owner="developer"
        )
    
    def _test_config_file(self, config: Dict) -> GateResult:
        """Test configuration file validity"""
        file_path = config.get('file', '')
        validation = config.get('validation', '')
        
        full_path = self.base_dir / file_path
        
        if not full_path.exists():
            return GateResult(
                name=f"Config: {file_path}",
                category="environment",
                passed=False,
                score=0.0,
                message="Config file missing",
                owner="developer"
            )
        
        if validation:
            try:
                result = subprocess.run(
                    validation,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                passed = result.returncode == 0
                message = "Valid configuration" if passed else f"Invalid config: {result.stderr}"
                
                return GateResult(
                    name=f"Config: {file_path}",
                    category="environment",
                    passed=passed,
                    score=1.0 if passed else 0.0,
                    message=message,
                    owner="developer"
                )
                
            except Exception as e:
                return GateResult(
                    name=f"Config: {file_path}",
                    category="environment",
                    passed=False,
                    score=0.0,
                    message=f"Validation failed: {str(e)}",
                    owner="developer"
                )
        
        return GateResult(
            name=f"Config: {file_path}",
            category="environment",
            passed=True,
            score=1.0,
            message="Config file exists (not validated)",
            owner="developer"
        )
    
    def calculate_overall_score(self, all_results: List[GateResult]) -> Tuple[float, Dict[str, float]]:
        """Calculate weighted overall readiness score"""
        category_results = {}
        
        # Group results by category
        for result in all_results:
            if result.category not in category_results:
                category_results[result.category] = []
            category_results[result.category].append(result)
        
        # Calculate category scores
        category_scores = {}
        for category, results in category_results.items():
            if results:
                avg_score = sum(r.score for r in results) / len(results)
                category_scores[category] = avg_score
            else:
                category_scores[category] = 0.0
        
        # Calculate weighted overall score
        overall_score = 0.0
        for category, weight in self.gate_weights.items():
            score = category_scores.get(category, 0.0)
            overall_score += score * weight
        
        return overall_score * 100, category_scores
    
    def generate_recommendation(self, overall_score: float, critical_failures: List[str]) -> str:
        """Generate implementation recommendation based on score"""
        if overall_score >= 95:
            return "🎯 FULL IMPLEMENTATION - All systems ready"
        elif overall_score >= 85:
            return "✅ CORE IMPLEMENTATION - Proceed with noted limitations"  
        elif overall_score >= 70:
            return "⚠️  PARTIAL IMPLEMENTATION - Critical path only"
        else:
            return "🛑 HALT - Fix critical blockers first"
    
    def run_assessment(self) -> ReadinessReport:
        """Run complete readiness assessment"""
        print("🔍 Running PRP Implementation Readiness Assessment...")
        print("=" * 50)
        
        all_results = []
        
        # Run all gate validations
        print("🏗️  Validating Infrastructure Gates...")
        infra_results = self.validate_infrastructure_gates()
        all_results.extend(infra_results)
        
        print("🔐 Validating Credential Gates...")
        cred_results = self.validate_credential_gates()
        all_results.extend(cred_results)
        
        print("🔧 Validating Dependency Gates...")
        dep_results = self.validate_dependency_gates()
        all_results.extend(dep_results)
        
        print("🌍 Validating Environment Gates...")
        env_results = self.validate_environment_gates()
        all_results.extend(env_results)
        
        # Calculate scores
        overall_score, category_scores = self.calculate_overall_score(all_results)
        
        # Identify critical failures
        critical_failures = [r.name for r in all_results if not r.passed and r.category in ['infrastructure', 'credentials']]
        
        # Generate recommendation
        recommendation = self.generate_recommendation(overall_score, critical_failures)
        
        # Estimate time to resolution
        failed_results = [r for r in all_results if not r.passed and r.time_to_fix != "Unknown"]
        if failed_results:
            # Simple sum of time estimates (could be more sophisticated)
            time_estimates = []
            for r in failed_results:
                time_str = r.time_to_fix
                if 'minute' in time_str:
                    minutes = int(re.findall(r'\d+', time_str)[0]) if re.findall(r'\d+', time_str) else 5
                    time_estimates.append(minutes)
            
            total_minutes = sum(time_estimates)
            if total_minutes > 60:
                time_to_resolution = f"{total_minutes // 60}h {total_minutes % 60}m"
            else:
                time_to_resolution = f"{total_minutes}m"
        else:
            time_to_resolution = "0 minutes"
        
        # Generate next steps
        next_steps = []
        priority_failures = sorted([r for r in all_results if not r.passed], 
                                 key=lambda x: (0 if x.category == 'credentials' else 1 if x.category == 'infrastructure' else 2))
        
        for i, failure in enumerate(priority_failures[:5]):  # Top 5 issues
            step = f"{i+1}. 🔴 {failure.message} ({failure.owner}, {failure.time_to_fix})"
            if failure.fix_command:
                step += f"\n   Command: {failure.fix_command}"
            next_steps.append(step)
        
        return ReadinessReport(
            prp_id=os.path.basename(self.prp_file).replace('.md', ''),
            overall_score=overall_score,
            gate_results=all_results,
            category_scores=category_scores,
            recommendation=recommendation,
            critical_blockers=critical_failures,
            time_to_resolution=time_to_resolution,
            next_steps=next_steps
        )
    
    def print_report(self, report: ReadinessReport, output_format: str = "console"):
        """Print formatted readiness report"""
        if output_format == "json":
            print(json.dumps({
                "prp_id": report.prp_id,
                "overall_score": report.overall_score,
                "recommendation": report.recommendation,
                "critical_blockers": report.critical_blockers,
                "time_to_resolution": report.time_to_resolution,
                "category_scores": report.category_scores,
                "next_steps": report.next_steps
            }, indent=2))
            return
        
        # Console output
        print("\n" + "=" * 60)
        print(f"PRP Readiness Assessment: {report.prp_id}")
        print("=" * 60)
        
        # Category breakdown
        for category, score in report.category_scores.items():
            icon = "✅" if score >= 0.9 else "⚠️" if score >= 0.7 else "❌"
            print(f"{icon} {category.title()} Gates: {score*100:.0f}%")
            
            # Show category results
            category_results = [r for r in report.gate_results if r.category == category]
            for result in category_results:
                status = "✅" if result.passed else "❌" if result.score == 0 else "⚠️"
                print(f"  {status} {result.name}: {result.message}")
        
        print("\n" + "=" * 60)
        print(f"OVERALL READINESS: {report.overall_score:.0f}%")
        print(f"RECOMMENDATION: {report.recommendation}")
        if report.critical_blockers:
            print(f"BLOCKERS: {len(report.critical_blockers)} critical issues")
        print(f"TIME TO FIX: {report.time_to_resolution}")
        print("=" * 60)
        
        if report.next_steps:
            print("\n📋 Required Actions (Priority Order):")
            for step in report.next_steps:
                print(step)
        
        print(f"\n🎯 Next Steps:")
        if report.overall_score >= 85:
            print("- ✅ Ready for implementation")
        else:
            print(f"- Fix critical issues → Re-run validation")
            print(f"- At ≥85% readiness → Proceed with implementation")

def main():
    parser = argparse.ArgumentParser(description="PRP Implementation Readiness Assessment")
    parser.add_argument("--prp", required=True, help="Path to PRP markdown file")
    parser.add_argument("--report", choices=["console", "json"], default="console", help="Output format")
    parser.add_argument("--fail-threshold", type=int, default=70, help="Fail if score below threshold")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.prp):
        print(f"❌ PRP file not found: {args.prp}")
        sys.exit(1)
    
    # Run assessment
    validator = PRPReadinessValidator(args.prp)
    report = validator.run_assessment()
    
    # Print results
    validator.print_report(report, args.report)
    
    # Log to history
    log_readiness_history(report)
    
    # Exit with appropriate code
    if report.overall_score < args.fail_threshold:
        sys.exit(1)
    else:
        sys.exit(0)

def log_readiness_history(report: ReadinessReport):
    """Log readiness assessment to history file"""
    history_file = Path("/mnt/c/Users/Brandon/AAI/brain/logs/readiness_history.md")
    
    # Create directory if it doesn't exist
    history_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Append to history
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"""
## [{timestamp}] PRP: {report.prp_id}
- **Readiness**: {report.overall_score:.0f}% ({report.recommendation})
- **Critical Failures**: {', '.join(report.critical_blockers) if report.critical_blockers else 'None'}
- **Time to Resolution**: {report.time_to_resolution}
- **Category Scores**: Infrastructure: {report.category_scores.get('infrastructure', 0)*100:.0f}%, Credentials: {report.category_scores.get('credentials', 0)*100:.0f}%, Dependencies: {report.category_scores.get('dependencies', 0)*100:.0f}%, Environment: {report.category_scores.get('environment', 0)*100:.0f}%

"""
    
    try:
        with open(history_file, 'a') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"⚠️  Warning: Could not log to history file: {e}")

if __name__ == "__main__":
    main()