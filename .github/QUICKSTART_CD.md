# Quick Start: Continuous Deployment

This is a quick reference guide for enabling continuous deployment. For complete details, see [CONTINUOUS_DEPLOYMENT.md](../CONTINUOUS_DEPLOYMENT.md).

## ⚡ Quick Setup (5 minutes)

### 1. Get API Token
1. Go to https://www.pythonanywhere.com/account/#api_token
2. Click "Create a new API token"
3. Copy the token

### 2. Add GitHub Secrets
1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Add these secrets:
   - `PYTHONANYWHERE_USERNAME` = your username
   - `PYTHONANYWHERE_API_TOKEN` = your API token

### 3. Configure Auto-Pull (Recommended)
On PythonAnywhere → **Tasks** tab:
- Command: `cd /home/yourusername/HobbyBudgetTracker && git pull origin main`
- Frequency: Hourly
- Replace `yourusername` with your actual username

### 4. Test It
1. Push a change to main branch
2. Check **Actions** tab for deployment status
3. Wait for scheduled task to run (or manually pull code)
4. Verify changes at your PythonAnywhere URL

## 📋 Three Options for Code Pulling

Choose **one** of these options:

### Option A: Manual (Simplest)
After each deployment, manually run:
```bash
cd ~/HobbyBudgetTracker && git pull origin main
```

### Option B: Scheduled Task (Recommended ⭐)
Set up on PythonAnywhere → Tasks tab:
```bash
cd /home/yourusername/HobbyBudgetTracker && git pull origin main
```
Frequency: Hourly (or your preference)

### Option C: WSGI-based (Advanced)
Add to your WSGI file before importing the app:
```python
import subprocess
subprocess.run(['git', 'pull', 'origin', 'main'], cwd=project_home, check=True)
```

## 🔧 Manual Deployment

Run the script when needed:
```bash
export PYTHONANYWHERE_USERNAME=your_username
export PYTHONANYWHERE_API_TOKEN=your_token
./deploy_pythonanywhere.sh
```

## ❗ Troubleshooting

**Deployment skipped?**
- Check that GitHub secrets are set correctly
- Verify secret names match exactly (case-sensitive)

**Changes not visible?**
- Ensure code pulling is configured (Step 3 above)
- Check that scheduled task is running
- Manually run `git pull` to verify

**Reload failed?**
- Verify API token is valid
- Check domain name in secrets
- Look at GitHub Actions logs for details

## 📚 Documentation

- **Full guide**: [CONTINUOUS_DEPLOYMENT.md](../CONTINUOUS_DEPLOYMENT.md)
- **Secrets setup**: [SECRETS_SETUP.md](SECRETS_SETUP.md)
- **Initial deployment**: [DEPLOYMENT.md](../DEPLOYMENT.md)

## ✅ Checklist

- [ ] PythonAnywhere app deployed and working
- [ ] API token obtained
- [ ] GitHub secrets configured
- [ ] Code pulling method configured
- [ ] Test deployment successful
- [ ] Changes visible on PythonAnywhere

---

**Need help?** See [CONTINUOUS_DEPLOYMENT.md](../CONTINUOUS_DEPLOYMENT.md) for detailed instructions and troubleshooting.
