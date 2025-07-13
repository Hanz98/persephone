# Persephone

A cross-platform GUI application built with Python and Toga, capable of running on Windows, Linux, Android, and iOS.

## Quick Start

For impatient developers who want to get started immediately:

```bash
# Clone and setup
git clone https://github.com/Hanz98/persephone.git
cd persephone
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -e .[dev]

# Verify setup
pytest
python -m persephone

# Start developing
git checkout -b feature/my-feature
# Make your changes...
black src/ tests/ && flake8 src/ tests/ && pytest
git commit -m "Add my feature"
```

For detailed setup instructions, see the [Development Environment Setup](#development-environment-setup) section below.

## Features

- Cross-platform compatibility (Windows, Linux, macOS, Android, iOS)
- Modern GUI built with Toga (BeeWare framework)
- Comprehensive test suite with pytest
- Automated CI/CD pipeline with GitHub Actions
- Code quality tools (Black, Flake8, MyPy)

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher (3.9+ recommended for best compatibility)
- Git 2.20 or higher
- A terminal/command prompt
- Text editor or IDE (see [Development Tools and Scripts](#development-tools-and-scripts) section below)

### System Dependencies

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y \
  pkg-config \
  python3-dev \
  libgtk-3-dev \
  libgdk-pixbuf2.0-dev \
  libcairo-gobject2 \
  libgirepository1.0-dev \
  gir1.2-webkit2-4.0
```

#### macOS
```bash
brew install gobject-introspection gtk+3
```

#### Windows
No additional system dependencies required.

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Hanz98/persephone.git
cd persephone
```

2. **Create and activate a virtual environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate it (Linux/macOS)
source venv/bin/activate

# Activate it (Windows Command Prompt)
venv\Scripts\activate.bat

# Activate it (Windows PowerShell)
venv\Scripts\Activate.ps1
```

3. **Upgrade pip and install the package in development mode:**
```bash
# Upgrade pip to latest version
pip install --upgrade pip

# Install the package with development dependencies
pip install -e .[dev]
```

4. **Set up pre-commit hooks for code style enforcement:**
```bash
pre-commit install
```

5. **Verify the installation:**
```bash
# Run the development environment verification script
python scripts/verify_dev_env.py

# Or manually run tests to ensure everything is working
pytest

# Check code style
black src/ tests/ --check
flake8 src/ tests/
mypy src/
```

## Development Tools and Scripts

The repository includes several helpful tools and scripts to streamline development:

### Environment Verification Script

```bash
# Verify your development environment is set up correctly
python scripts/verify_dev_env.py
```

This script checks:
- Python version compatibility
- Virtual environment setup
- Required development tools (Black, Flake8, MyPy, pytest)
- Project file structure
- Basic import and test functionality

### VS Code Configuration

The repository includes VS Code configuration files in `.vscode/`:
- `settings.json`: Python interpreter, formatting, linting, and testing settings
- `extensions.json`: Recommended extensions for Python development

These files will automatically configure VS Code for optimal Persephone development when you open the project.

### Pre-commit Hooks

Automated code quality checks run before each commit:
```bash
# Install hooks (one-time setup)
pre-commit install

# Run all hooks manually
pre-commit run --all-files

# Update hook versions
pre-commit autoupdate
```

The hooks automatically:
- Format code with Black
- Sort imports with isort
- Check code style with Flake8
- Verify type annotations with MyPy
- Run the test suite


### Visual Studio Code (Recommended)

1. **Install recommended extensions:**
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.flake8",
    "ms-python.mypy-type-checker",
    "ms-python.isort",
    "tamasfe.even-better-toml",
    "ms-python.debugpy"
  ]
}
```

2. **Configure VS Code settings (.vscode/settings.json):**
```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "python.sortImports.args": ["--profile", "black"],
  "editor.formatOnSave": true,
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": ["tests/"]
}
```

### PyCharm

1. **Configure Python interpreter:**
   - Go to File → Settings → Project → Python Interpreter
   - Add interpreter → Existing environment → Select `venv/bin/python`

2. **Enable code formatting:**
   - Go to File → Settings → Tools → External Tools
   - Add Black, Flake8, and MyPy as external tools

3. **Configure pytest:**
   - Go to Run → Edit Configurations
   - Add new pytest configuration pointing to the `tests/` directory

### Other Editors

For other editors like Vim, Emacs, or Sublime Text, ensure you have:
- Python language server (Pylsp, Pyright, or similar)
- Syntax highlighting for Python and TOML
- Integration with Black, Flake8, and MyPy
- pytest integration for running tests

## Docker Development Environment

For developers who prefer containerized development:

### Using Docker

1. **Create a Dockerfile for development:**
```dockerfile
# This file would be created as .devcontainer/Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    pkg-config \
    python3-dev \
    libgtk-3-dev \
    libgdk-pixbuf2.0-dev \
    libcairo-gobject2 \
    libgirepository1.0-dev \
    gir1.2-webkit2-4.0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy requirements and install dependencies
COPY pyproject.toml requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -e .[dev]

# Copy source code
COPY . .

# Install pre-commit hooks
RUN pre-commit install

EXPOSE 8000
CMD ["bash"]
```

2. **Docker Compose for development:**
```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  persephone-dev:
    build: 
      context: .
      dockerfile: .devcontainer/Dockerfile
    volumes:
      - .:/workspace
      - venv:/workspace/venv
    environment:
      - PYTHONPATH=/workspace/src
    ports:
      - "8000:8000"
    stdin_open: true
    tty: true

volumes:
  venv:
```

3. **Using the Docker environment:**
```bash
# Build and run the development container
docker-compose -f docker-compose.dev.yml up -d

# Enter the container
docker-compose -f docker-compose.dev.yml exec persephone-dev bash

# Run tests inside container
docker-compose -f docker-compose.dev.yml exec persephone-dev pytest

# Stop the container
docker-compose -f docker-compose.dev.yml down
```

## Development Workflow

### Daily Development Cycle

1. **Start development session:**
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Pull latest changes
git pull origin main

# Install any new dependencies
pip install -e .[dev]
```

2. **Make changes:**
```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your code changes
# Edit files in src/persephone/ or tests/

# Run tests frequently during development
pytest tests/ -v

# Run specific test file
pytest tests/test_persephone.py -v
```

3. **Before committing:**
```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Check linting
flake8 src/ tests/

# Type checking
mypy src/

# Run full test suite
pytest

# Run pre-commit hooks manually (optional, they run automatically on commit)
pre-commit run --all-files
```

4. **Commit and push:**
```bash
# Stage changes
git add .

# Commit (pre-commit hooks will run automatically)
git commit -m "Add: descriptive commit message"

# Push to your feature branch
git push origin feature/your-feature-name
```

### Testing Strategy

#### Unit Tests
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src/persephone --cov-report=html

# Run specific test class
pytest tests/test_persephone.py::TestPersephone -v

# Run specific test method
pytest tests/test_persephone.py::TestPersephone::test_app_creation -v

# Run tests with detailed output
pytest -v -s
```

#### Integration Tests
```bash
# Run tests that require GUI components (if Toga is available)
pytest tests/ -k "not mock" -v

# Run only mock tests (for CI environments without GUI)
pytest tests/ -k "mock" -v
```

#### Performance Testing
```bash
# Run tests with timing information
pytest --durations=10

# Run with memory profiling (requires pytest-memray)
pytest --memray
```

## Debugging

### Using Python Debugger

1. **Add breakpoints in code:**
```python
import pdb; pdb.set_trace()  # Traditional pdb
# or
breakpoint()  # Python 3.7+ builtin
```

2. **Debug with pytest:**
```bash
# Drop into debugger on test failure
pytest --pdb

# Drop into debugger on first failure, then continue
pytest --pdb -x

# Debug specific test
pytest tests/test_persephone.py::test_name --pdb
```

3. **IDE Debugging:**
   - Set breakpoints in your IDE
   - Run tests or application in debug mode
   - Use step-through debugging features

### Logging

Enable debug logging during development:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues and Solutions

#### Virtual Environment Issues
```bash
# Recreate virtual environment if corrupted
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]
```

#### Import Issues
```bash
# Ensure PYTHONPATH includes src directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

#### GUI Issues on Linux
```bash
# If GUI tests fail, ensure X11 forwarding (for remote development)
export DISPLAY=:0

# For WSL users
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}'):0.0
```


### Development Mode
```bash
python -m persephone
```

### Using Briefcase (for production builds)
```bash
# Create the application scaffolding
briefcase create

# Run in development mode
briefcase dev

# Build the application
briefcase build

# Package for distribution
briefcase package
```

## Testing & Code Quality

### Running Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src/persephone --cov-report=html

# Run tests verbosely
pytest -v
```

### Code Style & Quality
The project enforces code quality through pre-commit hooks and CI/CD:

- **Black**: Code formatting (line length: 88 characters)
- **isort**: Import sorting (Black profile)
- **Flake8**: Linting and syntax checking
- **MyPy**: Type checking
- **Pytest**: Unit testing with coverage

#### Manual Quality Checks
```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Check formatting without applying changes
black src/ tests/ --check

# Linting
flake8 src/ tests/

# Type checking
mypy src/

# Run all quality checks in sequence
black src/ tests/ && isort src/ tests/ && flake8 src/ tests/ && mypy src/ && pytest
```

#### Pre-commit Hooks
The project uses pre-commit hooks to ensure code quality:
```bash
# Install hooks (run once)
pre-commit install

# Run hooks manually on all files
pre-commit run --all-files

# Update hook versions
pre-commit autoupdate
```

## Environment Variables and Configuration

### Development Environment Variables

Create a `.env` file in the project root for local development:
```bash
# .env file (do not commit this file)
PYTHONPATH=src
DEBUG=true
LOG_LEVEL=DEBUG

# For GUI development
DISPLAY=:0  # Linux/WSL only

# For testing
PYTEST_CURRENT_TEST=1
```

Load environment variables in your shell:
```bash
# Option 1: Source the .env file
set -a && source .env && set +a

# Option 2: Use python-dotenv (if installed)
pip install python-dotenv
```

### Configuration Files

The project uses several configuration files:

- **pyproject.toml**: Project metadata, dependencies, and tool configurations
- **.pre-commit-config.yaml**: Pre-commit hook configurations
- **.gitignore**: Git ignore patterns
- **requirements.txt**: Pinned dependencies for reproducible builds

## Common Development Tasks

### Adding New Dependencies

1. **Add to pyproject.toml:**
```toml
[project.dependencies]
new-package = ">=1.0.0"

# Or for development dependencies
[project.optional-dependencies]
dev = [
    # ... existing deps
    "new-dev-package>=1.0.0",
]
```

2. **Update installation:**
```bash
pip install -e .[dev]
```

3. **Update requirements.txt:**
```bash
pip freeze > requirements.txt
```

### Creating New Tests

1. **Add test file in tests/ directory:**
```python
# tests/test_new_feature.py
import pytest
from persephone import NewFeature

class TestNewFeature:
    def test_new_functionality(self):
        # Arrange
        feature = NewFeature()
        
        # Act
        result = feature.do_something()
        
        # Assert
        assert result == expected_value
```

2. **Run the new tests:**
```bash
pytest tests/test_new_feature.py -v
```

### Adding New Application Features

1. **Create feature module:**
```python
# src/persephone/new_feature.py
from typing import Optional

class NewFeature:
    def __init__(self) -> None:
        pass
    
    def do_something(self) -> str:
        return "Hello from new feature"
```

2. **Update main application:**
```python
# src/persephone/__init__.py
from .new_feature import NewFeature
```

3. **Add tests and documentation**

### Building and Distribution

```bash
# Create distribution packages
python -m build

# Install locally from wheel
pip install dist/persephone-*.whl

# Upload to test PyPI (requires credentials)
twine upload --repository testpypi dist/*

# Upload to production PyPI (requires credentials)
twine upload dist/*
```

### Performance Profiling

```bash
# Profile application startup
python -m cProfile -o profile_output.prof -m persephone

# Analyze profile results
python -c "import pstats; pstats.Stats('profile_output.prof').sort_stats('cumulative').print_stats(20)"

# Memory profiling (requires memory_profiler)
pip install memory_profiler
python -m memory_profiler src/persephone/__main__.py
```

### Documentation

```bash
# Generate API documentation (if sphinx is installed)
pip install sphinx sphinx-autodoc-typehints
sphinx-quickstart docs
sphinx-build -b html docs docs/_build/html

# Serve documentation locally
python -m http.server 8000 --directory docs/_build/html
```

### Linting
```bash
flake8 src/ tests/
```

### Type Checking
```bash
mypy src/
```

## Building for Different Platforms

### Desktop Platforms

#### Linux AppImage
```bash
briefcase package linux AppImage
```

#### Windows MSI
```bash
briefcase package windows
```

#### macOS DMG
```bash
briefcase package macOS
```

### Mobile Platforms

#### Android APK
```bash
briefcase create android
briefcase build android
briefcase package android
```

#### iOS App
```bash
briefcase create iOS
briefcase build iOS
briefcase package iOS
```

## Project Structure

```
persephone/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD pipeline
├── src/
│   └── persephone/
│       ├── __init__.py         # Main application module
│       └── __main__.py         # Application entry point
├── tests/
│   ├── conftest.py             # Test configuration
│   └── test_persephone.py      # Unit tests
├── resources/                  # Application resources (icons, etc.)
├── pyproject.toml              # Project configuration and dependencies
├── README.md                   # This file
├── LICENSE                     # Apache 2.0 license
└── .gitignore                  # Git ignore rules
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure code quality (`pytest && black . && flake8`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Common Issues and Solutions

#### Installation Issues

**Problem: `pip install -e .[dev]` fails**
```bash
# Solution 1: Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Solution 2: Use pip's new resolver
pip install --use-feature=fast-deps -e .[dev]

# Solution 3: Install dependencies individually
pip install -r requirements.txt
pip install -e .
```

**Problem: Virtual environment activation fails**
```bash
# Windows: Execution policy error
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Linux/macOS: Permission issues
chmod +x venv/bin/activate
```

#### System Dependencies

**Linux: Missing system dependencies**
```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y \
  pkg-config python3-dev libgtk-3-dev libgdk-pixbuf2.0-dev \
  libcairo-gobject2 libgirepository1.0-dev gir1.2-webkit2-4.0

# CentOS/RHEL/Fedora  
sudo yum install -y pkg-config python3-devel gtk3-devel \
  gdk-pixbuf2-devel cairo-gobject-devel gobject-introspection-devel \
  webkit2gtk3-devel

# Arch Linux
sudo pacman -S pkg-config python gtk3 gdk-pixbuf2 cairo \
  gobject-introspection webkit2gtk
```

**macOS: Homebrew dependency issues**
```bash
# Reinstall dependencies
brew uninstall --ignore-dependencies gtk+3 gobject-introspection
brew install gtk+3 gobject-introspection

# If using Apple Silicon Mac
arch -arm64 brew install gtk+3 gobject-introspection

# Clear Homebrew cache if issues persist
brew cleanup
```

**Windows: Long path issues**
```powershell
# Enable long paths in Windows (requires admin privileges)
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
  -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

#### Development Environment Issues

**Problem: Tests fail with import errors**
```bash
# Solution 1: Ensure PYTHONPATH is set
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Solution 2: Reinstall in development mode
pip uninstall persephone
pip install -e .

# Solution 3: Check Python path in test
python -c "import sys; print('\n'.join(sys.path))"
```

**Problem: Pre-commit hooks fail**
```bash
# Update hooks
pre-commit autoupdate

# Clear pre-commit cache
pre-commit clean

# Reinstall hooks
pre-commit uninstall
pre-commit install

# Skip hooks temporarily (not recommended)
git commit --no-verify -m "message"
```

**Problem: Black and Flake8 conflicts**
```bash
# Check configuration in pyproject.toml
[tool.black]
line-length = 88

[tool.flake8]
max-line-length = 88
extend-ignore = E203, W503
```

#### GUI and Platform-Specific Issues

**Linux: GUI doesn't start**
```bash
# Check if X11 forwarding is enabled (remote development)
echo $DISPLAY
xauth list

# For WSL users
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0

# Install X11 apps (if missing)
sudo apt-get install x11-apps
xeyes  # Test X11 forwarding
```

**macOS: Permission issues**
```bash
# Grant terminal access to accessibility features
# System Preferences → Security & Privacy → Privacy → Accessibility

# For notarization issues during distribution
codesign --force --deep --sign "Developer ID" app.dmg
```

**Windows: DLL issues**
```bash
# Ensure Visual C++ Redistributable is installed
# Download from Microsoft website

# Check for conflicting Python installations
where python
python --version
```

#### Testing Issues

**Problem: Tests pass locally but fail in CI**
```bash
# Ensure consistent Python version
python --version

# Check for environment-specific dependencies
pip list --outdated

# Run tests in clean environment
pip install tox
tox

# Debug CI-specific issues
pytest --tb=long -v
```

**Problem: Coverage reports are incomplete**
```bash
# Ensure coverage configuration is correct
[tool.pytest.ini_options]
addopts = "--cov=src/persephone --cov-report=html --cov-report=term-missing"

# Run coverage manually
coverage run -m pytest
coverage report
coverage html
```

#### Performance Issues

**Problem: Application is slow**
```bash
# Profile the application
python -m cProfile -o profile.prof -m persephone
python -c "import pstats; pstats.Stats('profile.prof').print_stats(20)"

# Check memory usage
pip install memory_profiler
python -m memory_profiler src/persephone/__main__.py

# Monitor system resources
htop  # Linux/macOS
taskmgr  # Windows
```

#### Development Tool Issues

**Problem: IDE doesn't recognize modules**
```bash
# VS Code: Check Python interpreter path
# Command Palette → Python: Select Interpreter

# PyCharm: Invalidate caches
# File → Invalidate Caches and Restart

# Check PYTHONPATH
echo $PYTHONPATH
```

**Problem: Type checking fails unexpectedly**
```bash
# Clear MyPy cache
mypy --cache-dir=/tmp/mypy_cache src/

# Update type stubs
pip install --upgrade types-all

# Check MyPy configuration
mypy --show-config
```

### Getting Help

If you encounter issues not covered here:

1. **Check existing issues:** [GitHub Issues](https://github.com/Hanz98/persephone/issues)
2. **Search discussions:** [GitHub Discussions](https://github.com/Hanz98/persephone/discussions)
3. **Create a new issue** with:
   - Operating system and version
   - Python version (`python --version`)
   - Complete error message and stack trace
   - Steps to reproduce the issue
   - Output of `pip list` in your virtual environment

### Useful Commands for Debugging

```bash
# System information
python -m sysconfig
python -c "import platform; print(platform.platform())"

# Package information
pip show persephone
pip list --outdated

# Git information
git status
git log --oneline -10

# Environment information
env | grep -E "(PYTHON|PATH|DISPLAY)"
which python
which pip
```

For more help, please open an issue on GitHub with detailed information about your problem.