
# FlowForge Quick Start Guide

Get **FlowForge** up and running in minutes! This guide will help you set up your CI/CD pipeline orchestration platform.

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git

## Step 1: Initial Setup

### Clone and Navigate

```bash
cd /home/devops/Documents/CI_CD
```

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
make install-dev
# Or manually:
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
```

## Step 2: Configure GitHub Authentication

### Option A: Using the Setup Script (Recommended)

```bash
make setup-github-key
# Or:
bash scripts/setup_github_key.sh
```

Follow the on-screen instructions to:
1. Add the public key to GitHub Deploy Keys
2. Add the private key to GitHub Secrets

### Option B: Manual Setup

1. Generate SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "ci-cd-deploy-key" -f ~/.ssh/github_deploy_key -N ""
   ```

2. Add public key to GitHub:
   - Go to Repository → Settings → Deploy keys
   - Add new deploy key with the contents of `~/.ssh/github_deploy_key.pub`

3. Add private key to GitHub Secrets:
   - Go to Repository → Settings → Secrets → Actions
   - Add new secret named `DEPLOY_KEY` with the contents of `~/.ssh/github_deploy_key`

### Personal Access Token (Alternative)

1. Generate token: GitHub Settings → Developer settings → Personal access tokens
2. Add to secrets: Repository → Settings → Secrets → Actions
3. Name: `GITHUB_TOKEN`
4. Value: Your token

## Step 3: Configure Application

### Create Environment File

```bash
cp env.example .env
```

### Edit Configuration

Edit `.env` file with your settings:

```env
APP_NAME=FlowForge
DEBUG=True
PORT=8000
GITHUB_TOKEN=your_token_here
```

## Step 4: Run the Application

### Development Mode

```bash
make run
# Or:
python -m src.main
```

The application will start on `http://localhost:8000`

### Test Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Application info
curl http://localhost:8000/api/v1/info
```

## Step 5: Verify CI/CD Pipeline

### Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Setup FlowForge CI/CD platform"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Check GitHub Actions

1. Go to your GitHub repository
2. Click on "Actions" tab
3. You should see the CI/CD pipeline running
4. Wait for all jobs to complete

## Common Commands

### Development

```bash
make help              # Show all available commands
make install           # Install production dependencies
make install-dev       # Install development dependencies
make test              # Run tests
make test-cov          # Run tests with coverage
make lint              # Run linter
make format            # Format code
make run               # Run application
```

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test
pytest tests/test_main.py -v
```

### Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Check formatting
black --check src/ tests/

# Run linter
flake8 src/ tests/
```

## Troubleshooting

### Import Errors

If you get import errors:
```bash
pip install -e .
```

### Port Already in Use

Change the port in `.env`:
```env
PORT=8001
```

### GitHub Actions Failing

1. Check that secrets are properly configured
2. Verify repository permissions
3. Check workflow logs in GitHub Actions tab

### Tests Not Running

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests explicitly
python -m pytest tests/
```

## Next Steps

1. **Customize FlowForge**:
   - Update `src/config.py` for your needs
   - Modify `src/api/routes.py` to add endpoints
   - Extend configuration for your pipeline requirements

2. **Add Features**:
   - See `ARCHITECTURE.md` for extension points
   - Add new modules in `src/` directory
   - Create corresponding tests

3. **Configure Deployment**:
   - Update deployment section in `.github/workflows/ci-cd.yml`
   - Add deployment secrets
   - Configure production environment

4. **Set Up Pre-commit Hooks**:
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Getting Help

- Check `README.md` for detailed documentation
- Review `ARCHITECTURE.md` for architecture details
- See `.github/SETUP_GITHUB_KEYS.md` for authentication setup

## Important Notes

- ⚠️ **Never commit secrets** - use `.env` file (which is gitignored)
- ⚠️ **Keep private keys secure** - never share or commit them
- ✅ **All code in English** - for consistency and collaboration
- ✅ **Test before pushing** - run `make all` before commits

---

Happy coding! 🚀

