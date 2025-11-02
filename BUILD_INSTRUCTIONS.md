# FlowForge Build Instructions for GitHub

## Current Status

✅ **Code is committed and ready for push**
- Initial commit: `939db0a` - Setup FlowForge CI/CD platform
- Documentation commit: `3d8dce4` - Git setup documentation
- Total files: 28 files ready for GitHub

## 🔐 Authentication Required

To push code to GitHub and trigger the CI/CD build, you need to authenticate.

### Option 1: SSH Authentication (Recommended)

If you have SSH key configured:

```bash
cd /home/devops/Documents/CI_CD

# Already configured for SSH
git remote -v  # Should show git@github.com:Franklin-security/FlowForge.git

# Push to GitHub
git push -u origin main
```

If SSH key is not configured, generate one:

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/github_flowforge

# Add to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github_flowforge

# Display public key (add to GitHub)
cat ~/.ssh/github_flowforge.pub
```

Then add the public key to GitHub:
1. Go to GitHub → Settings → SSH and GPG keys
2. Click "New SSH key"
3. Paste the public key content
4. Save

### Option 2: Personal Access Token (HTTPS)

```bash
cd /home/devops/Documents/CI_CD

# Switch to HTTPS
git remote set-url origin https://github.com/Franklin-security/FlowForge.git

# Push (will prompt for credentials)
git push -u origin main
# Username: Franklin-security (or your GitHub username)
# Password: <your-personal-access-token>
```

To create Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` scope
3. Use token as password when pushing

### Option 3: GitHub CLI

```bash
# Install gh CLI if not installed
# Ubuntu/Debian: sudo apt install gh
# Or: https://cli.github.com/

# Authenticate
gh auth login

# Push code
cd /home/devops/Documents/CI_CD
git push -u origin main
```

## 🚀 After Successful Push

Once code is pushed, GitHub Actions will automatically:

1. **Run Tests** (`test` job):
   - Install dependencies
   - Run linting (flake8)
   - Execute pytest tests
   - Generate coverage reports

2. **Build Application** (`build` job):
   - Build Python package (sdist, wheel)
   - Upload build artifacts

3. **Deploy** (`deploy` job):
   - Only runs on `main` branch
   - Ready for deployment configuration

## 📊 Monitoring Build Status

After push, check build status:

1. **GitHub Web Interface**:
   - Go to: https://github.com/Franklin-security/FlowForge
   - Click "Actions" tab
   - View workflow runs

2. **Command Line** (if using GitHub CLI):
   ```bash
   gh workflow list
   gh run list
   gh run watch
   ```

## 🔧 CI/CD Pipeline Configuration

The workflow is configured in `.github/workflows/ci-cd.yml`:

- **Trigger**: Push to `main` or `develop` branches
- **Python Version**: 3.11
- **Jobs**: Test → Build → Deploy (if main branch)

## ⚙️ Build Artifacts

After successful build:
- Distribution packages available in GitHub Actions artifacts
- Download from: Repository → Actions → Workflow run → Artifacts

## 🐛 Troubleshooting

### Authentication Issues

```bash
# Check SSH connection
ssh -T git@github.com

# Check git credentials
git config --list | grep -E "user|credential"

# Clear cached credentials (if using HTTPS)
git credential-cache exit
```

### Push Fails

```bash
# Check remote URL
git remote -v

# Verify branch
git branch

# Check commit status
git log --oneline -5

# Force push (if needed, be careful!)
# git push -u origin main --force
```

### Build Fails in GitHub Actions

1. Check workflow logs in GitHub Actions tab
2. Verify dependencies in `requirements.txt`
3. Ensure Python version matches (3.11)
4. Check test coverage requirements

## 📝 Current Commits Ready to Push

```bash
# View commits
git log --oneline

# Should show:
# 3d8dce4 docs: Add Git setup completion documentation
# 939db0a Initial commit: Setup FlowForge CI/CD platform
```

## ✅ Quick Push Command

Once authentication is set up:

```bash
cd /home/devops/Documents/CI_CD
git push -u origin main
```

---

**Next Step**: Set up authentication (SSH key or PAT) and run `git push -u origin main`

