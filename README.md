# Persephone

A cross-platform GUI application built with Python and Toga, capable of running on Windows, Linux, Android, and iOS.

## Features

- Cross-platform compatibility (Windows, Linux, macOS, Android, iOS)
- Modern GUI built with Toga (BeeWare framework)
- Comprehensive test suite with pytest
- Automated CI/CD pipeline with GitHub Actions
- Code quality tools (Black, Flake8, MyPy)

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- Git

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

1. Clone the repository:
```bash
git clone https://github.com/Hanz98/persephone.git
cd persephone
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e .[dev]
```

## Running the Application

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

## Testing

Run the test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src/persephone --cov-report=html
```

## Code Quality

### Formatting
```bash
black src/ tests/
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

### Common Issues

#### Linux: Missing system dependencies
Make sure all GTK+ and GObject Introspection dependencies are installed as shown in the setup instructions.

#### macOS: Homebrew dependencies
If you encounter issues with GTK+, try reinstalling with:
```bash
brew uninstall --ignore-dependencies gtk+3
brew install gtk+3
```

#### Windows: Long path issues
Enable long path support in Windows if you encounter path-related errors during builds.

For more help, please open an issue on GitHub.