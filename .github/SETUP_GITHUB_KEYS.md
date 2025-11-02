# GitHub Authentication Setup Guide

This guide explains how to set up GitHub keys and secrets for CI/CD automation.

## Setting Up GitHub Personal Access Token (PAT)

### Step 1: Generate a Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name (e.g., "CI/CD Pipeline Token")
4. Select the following scopes:
   - `repo` - Full control of private repositories
   - `workflow` - Update GitHub Action workflows
   - `write:packages` - Upload packages to GitHub Package Registry (if needed)
   - `read:packages` - Download packages from GitHub Package Registry (if needed)
5. Click "Generate token"
6. **Copy the token immediately** - you won't be able to see it again!

### Step 2: Add Token to GitHub Secrets

1. Go to your repository on GitHub
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `GITHUB_TOKEN`
5. Value: Paste your personal access token
6. Click "Add secret"

## Setting Up SSH Deploy Key (Alternative Method)

### Step 1: Generate SSH Key Pair

```bash
ssh-keygen -t ed25519 -C "ci-cd-deploy-key" -f ~/.ssh/github_deploy_key
```

**Important**: Do NOT set a passphrase for the deploy key, as it needs to work automatically in CI/CD.

### Step 2: Add Public Key to GitHub

1. Copy the public key:
   ```bash
   cat ~/.ssh/github_deploy_key.pub
   ```

2. Go to your repository → Settings → Deploy keys
3. Click "Add deploy key"
4. Title: "CI/CD Deploy Key"
5. Key: Paste the public key
6. Check "Allow write access" if you need to push to the repository
7. Click "Add key"

### Step 3: Add Private Key to GitHub Secrets

1. Copy the private key:
   ```bash
   cat ~/.ssh/github_deploy_key
   ```

2. Go to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `DEPLOY_KEY`
5. Value: Paste the entire private key (including `-----BEGIN OPENSSH PRIVATE KEY-----` and `-----END OPENSSH PRIVATE KEY-----`)
6. Click "Add secret"

## Setting Up Deployment Secrets

### For Remote Server Deployment

If you're deploying to a remote server, add these secrets:

1. `DEPLOY_HOST` - The hostname or IP address of your deployment server
2. `DEPLOY_USER` - The SSH username for deployment
3. `DEPLOY_KEY` or `DEPLOY_SSH_KEY` - The SSH private key for server access

### Example: Adding Deployment Secrets

```bash
# In GitHub repository settings:
DEPLOY_HOST=example.com
DEPLOY_USER=deploy
DEPLOY_SSH_KEY=<your-ssh-private-key>
```

## Using Secrets in GitHub Actions

Secrets are automatically available in GitHub Actions workflows via `${{ secrets.SECRET_NAME }}`.

Example in workflow file:
```yaml
- name: Deploy to production
  env:
    DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
    DEPLOY_HOST: ${{ secrets.DEPLOY_HOST }}
```

## Security Best Practices

1. **Never commit secrets to the repository**
2. Use different tokens for different purposes
3. Rotate tokens regularly
4. Use fine-grained permissions when possible
5. Review token usage regularly
6. Use deploy keys with minimal required permissions

## Troubleshooting

### Token Not Working
- Check that the token has the correct scopes
- Verify the token hasn't expired
- Ensure the secret name matches exactly in the workflow

### SSH Key Not Working
- Verify the public key is added as a deploy key
- Check that "Allow write access" is enabled if pushing
- Ensure the private key includes headers and footers

### Permission Denied
- Verify repository permissions for the token
- Check branch protection rules
- Ensure workflow has necessary permissions

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Managing Deploy Keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys)
- [Creating Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

