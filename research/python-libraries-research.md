# Python Libraries Research: AST Parsing, Docker SDK, GitPython, and Security Scanning

## Table of Contents
1. [AST Parsing for Multiple Languages](#ast-parsing-for-multiple-languages)
2. [Docker SDK for Python](#docker-sdk-for-python)
3. [GitPython for Repository Management](#gitpython-for-repository-management)
4. [Security Scanning Tools](#security-scanning-tools)
5. [Performance and Compatibility Considerations](#performance-and-compatibility-considerations)
6. [Recommendations](#recommendations)

---

## AST Parsing for Multiple Languages

### Tree-sitter: The Gold Standard for Multi-Language Parsing

Tree-sitter is an incremental parsing library and parser generator that provides excellent support for parsing multiple programming languages including Python, JavaScript, TypeScript, and Go.

#### Key Features:
- **Incremental Parsing**: Updates syntax trees efficiently as source code changes
- **Error Recovery**: Handles incomplete or invalid code gracefully
- **Performance**: 36x speedup compared to traditional parsers in benchmarks
- **Multi-language Support**: Single interface for 160+ programming languages
- **Concrete Syntax Trees (CST)**: Provides exact representation of source code

#### Installation Options (2024):

**Recommended: tree-sitter-language-pack**
```bash
pip install tree-sitter-language-pack
```
- Actively maintained with 165+ languages
- Type-safe with full typing support
- Zero GPL dependencies (MIT, Apache 2.0 licenses)
- Pre-built wheels for easy installation

**Alternative: tree-sitter-languages** (Unmaintained)
```bash
pip install tree-sitter-languages
```

**Core Library:**
```bash
pip install tree-sitter
```

#### Usage Examples:

**Using tree-sitter-language-pack:**
```python
from tree_sitter_language_pack import get_binding, get_language, get_parser

# Get language-specific components
python_binding = get_binding('python')
python_lang = get_language('python')
python_parser = get_parser('python')

# Parse code
code = """
def hello_world():
    print("Hello, World!")
"""
tree = python_parser.parse(code.encode())
root_node = tree.root_node

# Query for function definitions
query = python_lang.query("""
(function_definition
  name: (identifier) @function_name
  body: (block) @function_body)
""")

captures = query.captures(root_node)
for node, capture_name in captures:
    print(f"{capture_name}: {node.text.decode()}")
```

**Multi-language parsing:**
```python
from tree_sitter_language_pack import get_parser

# Support for multiple languages
parsers = {
    'python': get_parser('python'),
    'javascript': get_parser('javascript'),
    'typescript': get_parser('typescript'),
    'go': get_parser('go')
}

def parse_file(filepath, language):
    with open(filepath, 'r') as f:
        content = f.read()
    
    parser = parsers[language]
    tree = parser.parse(content.encode())
    return tree
```

#### Advantages over Python's Built-in AST:
- Handles multiple languages with unified interface
- Better error recovery for incomplete code
- Incremental parsing for real-time editing
- Maintains exact source code representation
- Significantly faster for large codebases

---

## Docker SDK for Python

### Official Docker SDK for Python (docker-py)

The official Docker SDK for Python provides a Pythonic interface to the Docker Engine API, allowing you to perform any Docker operation from within Python applications.

#### Latest Version (2024):
- **Version**: 7.1.0 (documented stable version)
- **Last Updated**: May 23, 2024
- **Repository**: https://github.com/docker/docker-py
- **Documentation**: https://docker-py.readthedocs.io/

#### Installation:
```bash
pip install docker
```

#### Key Features:
- Complete Docker Engine API coverage
- Container lifecycle management
- Image building and management
- Volume and network operations
- Docker Swarm support
- Authentication and registry operations

#### Usage Examples:

**Basic Container Operations:**
```python
import docker

# Initialize client
client = docker.from_env()

# List containers
containers = client.containers.list()
print(f"Running containers: {len(containers)}")

# Run a container
container = client.containers.run(
    "python:3.11-slim",
    "python -c 'print(\"Hello from Docker!\")'",
    remove=True,
    detach=False
)
print(container.decode())

# Build an image
image = client.images.build(
    path="./my-app",
    tag="my-app:latest",
    dockerfile="Dockerfile"
)
```

**Advanced Container Management:**
```python
import docker
from docker.errors import ContainerError, ImageNotFound

class DockerManager:
    def __init__(self):
        self.client = docker.from_env()
    
    def run_container_with_monitoring(self, image, command, **kwargs):
        """Run container with comprehensive monitoring"""
        try:
            container = self.client.containers.run(
                image,
                command,
                detach=True,
                **kwargs
            )
            
            # Monitor container logs
            for log in container.logs(stream=True):
                print(log.decode().strip())
            
            # Wait for completion and get exit code
            result = container.wait()
            return result['StatusCode']
            
        except ImageNotFound:
            print(f"Image {image} not found")
            return -1
        except ContainerError as e:
            print(f"Container error: {e}")
            return e.exit_status
        finally:
            # Cleanup
            if 'container' in locals():
                container.remove()
    
    def build_and_push(self, dockerfile_path, tag, registry_url):
        """Build image and push to registry"""
        # Build image
        image = self.client.images.build(
            path=dockerfile_path,
            tag=tag,
            pull=True
        )
        
        # Tag for registry
        registry_tag = f"{registry_url}/{tag}"
        image.tag(registry_tag)
        
        # Push to registry
        push_log = self.client.images.push(registry_tag, stream=True)
        for line in push_log:
            print(line)
```

#### Compatibility:
- Python 3.7+
- Compatible with Python 3.11 and 3.12
- Cross-platform support (Windows, macOS, Linux)
- Docker Engine API version compatibility

---

## GitPython for Repository Management

### GitPython: Python Git Repository Interface

GitPython provides object model access to Git repositories with both high-level (porcelain) and low-level (plumbing) interfaces.

#### Latest Version (2024):
- **Version**: 3.1.44 (latest documented)
- **Maintenance Status**: Maintenance mode (stable, community-driven)
- **Repository**: https://github.com/gitpython-developers/GitPython
- **Documentation**: https://gitpython.readthedocs.io/

#### Installation:
```bash
pip install GitPython
```

#### Key Features:
- Repository cloning and initialization
- Branch, tag, and remote management
- Commit history and diff operations
- Submodule management
- Configuration access
- Git object manipulation

#### Usage Examples:

**Repository Cloning:**
```python
import git
import os

def clone_repository(repo_url, local_dir, branch=None):
    """Clone repository with error handling"""
    try:
        if branch:
            repo = git.Repo.clone_from(
                repo_url, 
                local_dir, 
                branch=branch
            )
        else:
            repo = git.Repo.clone_from(repo_url, local_dir)
        
        print(f"Repository cloned to {local_dir}")
        return repo
    
    except git.exc.GitCommandError as e:
        print(f"Git command error: {e}")
        return None
    except Exception as e:
        print(f"Error cloning repository: {e}")
        return None

# Example usage
repo = clone_repository(
    'https://github.com/user/repository.git',
    '/tmp/my-repo',
    branch='main'
)
```

**Repository Management:**
```python
import git
from datetime import datetime

class GitRepositoryManager:
    def __init__(self, repo_path):
        self.repo = git.Repo(repo_path)
    
    def get_status(self):
        """Get repository status"""
        return {
            'active_branch': self.repo.active_branch.name,
            'is_dirty': self.repo.is_dirty(),
            'untracked_files': self.repo.untracked_files,
            'modified_files': [item.a_path for item in self.repo.index.diff(None)],
            'staged_files': [item.a_path for item in self.repo.index.diff("HEAD")]
        }
    
    def create_and_switch_branch(self, branch_name):
        """Create and switch to new branch"""
        try:
            new_branch = self.repo.create_head(branch_name)
            new_branch.checkout()
            return True
        except Exception as e:
            print(f"Error creating branch: {e}")
            return False
    
    def commit_changes(self, message, files=None):
        """Commit changes to repository"""
        try:
            if files:
                self.repo.index.add(files)
            else:
                self.repo.git.add('--all')
            
            commit = self.repo.index.commit(message)
            return commit.hexsha
        except Exception as e:
            print(f"Error committing changes: {e}")
            return None
    
    def get_commit_history(self, max_count=10):
        """Get recent commit history"""
        commits = []
        for commit in self.repo.iter_commits(max_count=max_count):
            commits.append({
                'sha': commit.hexsha[:8],
                'message': commit.message.strip(),
                'author': str(commit.author),
                'date': datetime.fromtimestamp(commit.committed_date)
            })
        return commits
    
    def pull_latest(self, remote='origin', branch=None):
        """Pull latest changes from remote"""
        try:
            if not branch:
                branch = self.repo.active_branch.name
            
            origin = self.repo.remotes[remote]
            origin.pull(branch)
            return True
        except Exception as e:
            print(f"Error pulling changes: {e}")
            return False
```

**Submodule Management:**
```python
def manage_submodules(repo_path):
    """Advanced submodule management"""
    repo = git.Repo(repo_path)
    
    # List submodules
    submodules = repo.submodules
    print(f"Found {len(submodules)} submodules")
    
    # Update all submodules
    for submodule in submodules:
        print(f"Updating submodule: {submodule.name}")
        submodule.update(init=True, recursive=True)
    
    # Add new submodule
    new_submodule = repo.create_submodule(
        'new-module',
        'path/to/submodule',
        'https://github.com/user/submodule.git'
    )
    
    return repo.submodules
```

#### Compatibility:
- Requires Git executable in PATH
- Python 3.7+
- Compatible with Python 3.11 and 3.12
- Cross-platform support

---

## Security Scanning Tools

### 1. Bandit - Python-Specific SAST Tool

Bandit is the most popular Python security scanner, designed to find common security issues in Python code.

#### Installation:
```bash
pip install bandit
```

#### Features:
- Common vulnerability detection (injection, hardcoded secrets, etc.)
- IDE integration support
- CI/CD pipeline integration
- Configurable security profiles
- JSON/XML/CSV output formats

#### Usage Examples:

**Basic Scanning:**
```python
import subprocess
import json

def run_bandit_scan(target_path, output_format='json'):
    """Run Bandit security scan"""
    cmd = [
        'bandit',
        '-r',  # recursive
        target_path,
        '-f', output_format,
        '-o', f'bandit_report.{output_format}'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if output_format == 'json':
            with open(f'bandit_report.json', 'r') as f:
                report = json.load(f)
            return report
        
        return result.stdout
    
    except Exception as e:
        print(f"Error running Bandit: {e}")
        return None

# Example usage
report = run_bandit_scan('./src')
if report:
    print(f"Found {len(report.get('results', []))} security issues")
```

### 2. Semgrep - Multi-Language SAST Tool

Semgrep is a powerful open-source static analysis tool supporting multiple languages.

#### Installation:
```bash
pip install semgrep
```

#### Features:
- Multi-language support (Python, JavaScript, Go, Java, etc.)
- Custom rule creation
- Large public ruleset
- Fast scanning performance
- CI/CD integration

#### Usage Examples:

**Python Integration:**
```python
import subprocess
import json

class SemgrepScanner:
    def __init__(self):
        self.config_options = [
            'auto',  # Auto-detect rules
            'p/python',  # Python-specific rules
            'p/security-audit',  # Security-focused rules
            'p/owasp-top-10'  # OWASP Top 10 rules
        ]
    
    def scan_directory(self, path, config='auto'):
        """Run Semgrep scan on directory"""
        cmd = [
            'semgrep',
            '--config', config,
            '--json',
            '--output', 'semgrep_report.json',
            path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            with open('semgrep_report.json', 'r') as f:
                report = json.load(f)
            
            return self._process_results(report)
        
        except Exception as e:
            print(f"Error running Semgrep: {e}")
            return None
    
    def _process_results(self, report):
        """Process Semgrep results"""
        findings = []
        for result in report.get('results', []):
            finding = {
                'rule_id': result.get('check_id'),
                'severity': result.get('extra', {}).get('severity'),
                'message': result.get('extra', {}).get('message'),
                'file': result.get('path'),
                'line': result.get('start', {}).get('line'),
                'code': result.get('extra', {}).get('lines')
            }
            findings.append(finding)
        
        return findings

# Example usage
scanner = SemgrepScanner()
findings = scanner.scan_directory('./src', 'p/python')
```

### 3. Safety - Python Dependency Vulnerability Scanner

Safety checks Python dependencies against known security vulnerabilities.

#### Installation:
```bash
pip install safety
```

#### Usage Examples:

```python
import subprocess
import json

def check_dependencies_safety():
    """Check Python dependencies for vulnerabilities"""
    cmd = ['safety', 'check', '--json']
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout:
            vulnerabilities = json.loads(result.stdout)
            return vulnerabilities
        
        return []
    
    except Exception as e:
        print(f"Error running Safety: {e}")
        return None

# Example usage
vulns = check_dependencies_safety()
if vulns:
    print(f"Found {len(vulns)} vulnerable dependencies")
    for vuln in vulns:
        print(f"- {vuln['package']} {vuln['installed_version']}: {vuln['vulnerability']}")
```

### 4. Alternative Tools for Different Use Cases

**For JavaScript/TypeScript (npm audit alternatives):**
- **audit-ci**: `npm install -g audit-ci`
- **yarn audit**: Built into Yarn package manager
- **npm-check-updates**: `npm install -g npm-check-updates`

**Enterprise SAST Solutions:**
- **Checkmarx**: Enterprise-level multi-language SAST
- **Veracode**: Cloud-based security scanning platform
- **SonarQube**: Code quality and security analysis
- **Snyk**: Cloud-based vulnerability scanning

---

## Performance and Compatibility Considerations

### Python 3.11+ Compatibility

#### Key Changes:
- **AST Validation**: Python 3.11 validates AST node positions, raising ValueError for invalid positions
- **New Syntax Support**: TryStar nodes for `except*` syntax (3.11), TypeAlias nodes (3.12)
- **Performance Improvements**: Significant speed improvements in Python 3.11/3.12

#### Tree-sitter Performance Advantages:
- **Incremental Parsing**: Only re-parses changed portions of code
- **Memory Efficiency**: Shares unchanged tree portions between parses
- **Response Time**: Millisecond response times vs. seconds for traditional parsers
- **Error Recovery**: Graceful handling of syntax errors

### Large Codebase Considerations

#### Tree-sitter Benefits:
```python
import time
from tree_sitter_language_pack import get_parser

def benchmark_parsing(code_files):
    """Benchmark parsing performance"""
    parser = get_parser('python')
    
    start_time = time.time()
    
    for file_path in code_files:
        with open(file_path, 'rb') as f:
            content = f.read()
        
        tree = parser.parse(content)
        # Process tree as needed
    
    end_time = time.time()
    return end_time - start_time

# For incremental parsing
def incremental_parse_example():
    """Example of incremental parsing benefits"""
    parser = get_parser('python')
    
    # Initial parse
    code = b"def hello(): pass"
    tree = parser.parse(code)
    
    # Edit: add a new function
    new_code = b"def hello(): pass\ndef world(): pass"
    
    # Tree-sitter efficiently updates only the changed portion
    new_tree = parser.parse(new_code, tree)
    
    return new_tree
```

#### Docker SDK Performance:
- Use connection pooling for multiple operations
- Leverage streaming for large builds/pulls
- Implement proper cleanup to avoid resource leaks

#### GitPython Optimization:
```python
def optimize_git_operations(repo_path):
    """Optimized Git operations for large repositories"""
    repo = git.Repo(repo_path)
    
    # Use bare repositories for read-only operations
    if not repo.bare:
        bare_repo = repo.clone('/tmp/bare_repo', bare=True)
    
    # Optimize commit iteration
    commits = list(repo.iter_commits('main', max_count=100, skip=0))
    
    # Use git command directly for complex operations
    repo.git.log('--oneline', '-n', '10')
    
    return repo
```

---

## Recommendations

### 1. AST Parsing for Multiple Languages

**Primary Recommendation: Tree-sitter with tree-sitter-language-pack**

```bash
pip install tree-sitter tree-sitter-language-pack
```

**Reasons:**
- Best performance for large codebases
- Supports 165+ languages with unified interface
- Excellent error recovery
- Incremental parsing capabilities
- Active maintenance and type safety

**Use Cases:**
- Code analysis tools
- IDE/editor development
- Static analysis across multiple languages
- Real-time syntax highlighting

### 2. Docker SDK for Python

**Recommendation: Official Docker SDK (docker-py)**

```bash
pip install docker
```

**Reasons:**
- Official Docker support
- Comprehensive API coverage
- Well-documented and maintained
- Python 3.11+ compatibility
- Production-ready

**Best Practices:**
- Use context managers for resource cleanup
- Implement proper error handling
- Leverage streaming for large operations
- Use connection pooling for high-frequency operations

### 3. GitPython for Repository Management

**Recommendation: GitPython with careful configuration**

```bash
pip install GitPython
```

**Considerations:**
- Stable but in maintenance mode
- Excellent for programmatic Git operations
- Requires Git executable in PATH
- Good Python 3.11+ compatibility

**Alternatives to Consider:**
- `dulwich`: Pure Python Git implementation
- `pygit2`: libgit2 bindings for Python

### 4. Security Scanning Tools

**Multi-Tool Approach Recommended:**

**For Python Code:**
```bash
pip install bandit semgrep safety
```

**For JavaScript/TypeScript:**
- Use `npm audit` or `yarn audit`
- Consider `audit-ci` for CI/CD pipelines

**Enterprise Solutions:**
- Evaluate SonarQube for comprehensive analysis
- Consider Snyk for dependency vulnerabilities
- Checkmarx or Veracode for enterprise needs

### 5. Implementation Strategy

**Recommended Technology Stack:**
```python
# requirements.txt
tree-sitter>=0.24.0
tree-sitter-language-pack>=0.9.0
docker>=7.1.0
GitPython>=3.1.44
bandit>=1.7.5
semgrep>=1.45.0
safety>=3.0.0
```

**Integration Example:**
```python
from tree_sitter_language_pack import get_parser
import docker
import git
import subprocess

class CodeAnalysisPlatform:
    def __init__(self):
        self.parsers = {
            'python': get_parser('python'),
            'javascript': get_parser('javascript'),
            'typescript': get_parser('typescript'),
            'go': get_parser('go')
        }
        self.docker_client = docker.from_env()
    
    def analyze_repository(self, repo_url, analysis_type='full'):
        """Complete repository analysis pipeline"""
        # 1. Clone repository
        repo = git.Repo.clone_from(repo_url, '/tmp/analysis')
        
        # 2. Parse code files
        results = {}
        for root, dirs, files in os.walk('/tmp/analysis'):
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.go')):
                    file_path = os.path.join(root, file)
                    results[file_path] = self.parse_file(file_path)
        
        # 3. Run security scans
        security_results = self.run_security_scans('/tmp/analysis')
        
        # 4. Generate Docker analysis environment
        if analysis_type == 'full':
            container_results = self.run_containerized_analysis()
        
        return {
            'parsing_results': results,
            'security_results': security_results,
            'container_results': container_results if analysis_type == 'full' else None
        }
    
    def parse_file(self, file_path):
        """Parse file based on extension"""
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.go': 'go'
        }
        
        ext = os.path.splitext(file_path)[1]
        language = extension_map.get(ext)
        
        if language and language in self.parsers:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            tree = self.parsers[language].parse(content)
            return tree.root_node.sexp()
        
        return None
    
    def run_security_scans(self, path):
        """Run comprehensive security scanning"""
        results = {}
        
        # Bandit for Python
        bandit_cmd = ['bandit', '-r', path, '-f', 'json']
        results['bandit'] = subprocess.run(bandit_cmd, capture_output=True, text=True)
        
        # Semgrep for multi-language
        semgrep_cmd = ['semgrep', '--config', 'auto', '--json', path]
        results['semgrep'] = subprocess.run(semgrep_cmd, capture_output=True, text=True)
        
        return results
```

This comprehensive research document provides the foundation for building robust code analysis and security scanning tools using the best Python libraries available in 2024, with excellent compatibility for Python 3.11+ and optimal performance for large codebases.