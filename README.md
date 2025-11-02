# FlowForge

**FlowForge** - A modern, powerful CI/CD pipeline orchestration platform designed for flexible deployment and automation workflows. Forge your deployment pipelines with ease.

## ✨ Features

- **🔧 Automated CI/CD Pipeline**: GitHub Actions workflow for continuous integration and deployment
- **🏗️ Modular Architecture**: Clean, extensible codebase structure designed for scalability
- **🧪 Testing Framework**: Comprehensive test suite with pytest and coverage reporting
- **⚙️ Configuration Management**: Environment-based configuration system with sensible defaults
- **🌐 RESTful API**: Modern API endpoints for pipeline orchestration and monitoring
- **🔗 GitHub Integration**: Seamless integration with GitHub for version control and automation
- **🚀 Production Ready**: Built with best practices, ready for deployment

## Architecture

```
CI_CD/
├── .github/
│   ├── workflows/
│   │   └── ci-cd.yml          # GitHub Actions CI/CD pipeline
│   └── SETUP_GITHUB_KEYS.md   # GitHub authentication guide
├── src/
│   ├── __init__.py            # Package initialization
│   ├── main.py                # Application entry point
│   ├── config.py              # Configuration management
│   └── api/
│       ├── __init__.py
│       └── routes.py          # API route definitions
├── tests/
│   ├── __init__.py
│   ├── test_main.py           # Main module tests
│   └── test_config.py         # Configuration tests
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── setup.py                   # Package setup script
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git
- GitHub account with repository access

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd CI_CD
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
APP_NAME=FlowForge
APP_VERSION=1.0.0
DEBUG=False
HOST=0.0.0.0
PORT=8000
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=your_username/your_repo
```

### GitHub Setup

Follow the instructions in `.github/SETUP_GITHUB_KEYS.md` to configure GitHub authentication for CI/CD.

## Usage

### Running the Application

```bash
python -m src.main
```

Or install as a package:

```bash
pip install -e .
flowforge
```

### Running Tests

```bash
pytest tests/ -v
```

With coverage:

```bash
pytest tests/ -v --cov=src --cov-report=html
```

### Running Linter

```bash
flake8 src/ tests/
```

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci-cd.yml`) automatically:

1. **Tests**: Runs tests on every push and pull request
2. **Linting**: Checks code quality with flake8
3. **Build**: Creates distribution packages
4. **Deploy**: Deploys to production (on main branch)

### Pipeline Stages

- **Test Job**: Runs unit tests and linting
- **Build Job**: Creates application packages
- **Deploy Job**: Deploys to production environment

## Customization

### FlowForge Customization

1. Update `APP_NAME` in `src/config.py` for custom branding
2. Modify API endpoints in `src/api/routes.py` to add your features
3. Extend configuration in `src/config.py` for additional settings

### Adding New Features

1. Create new modules in `src/` directory
2. Add corresponding tests in `tests/` directory
3. Update requirements if needed
4. Update CI/CD pipeline if deployment process changes

### Modifying Design

- Update API endpoints in `src/api/routes.py`
- Modify configuration in `src/config.py`
- Add new routes and functionality as needed

## Development

### Code Style

This project follows PEP 8 style guidelines. Use:

- `black` for code formatting
- `flake8` for linting
- `isort` for import sorting

```bash
black src/ tests/
isort src/ tests/
flake8 src/ tests/
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Write or update tests
4. Ensure all tests pass
5. Commit with clear messages (in English)
6. Push to your branch
7. Create a pull request

## Security

- Never commit secrets or API keys
- Use GitHub Secrets for sensitive information
- Regularly rotate authentication tokens
- Review dependencies for security vulnerabilities

## License

FlowForge is customizable for your specific needs. Modify and extend it according to your requirements.

## Support

For issues and questions, please create an issue in the GitHub repository.

---

**Note**: All code, comments, and Git commits should be in English for consistency and international collaboration.

