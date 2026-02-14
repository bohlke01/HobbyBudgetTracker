# GitHub Secrets Setup Template

This file helps you set up the required secrets for continuous deployment to PythonAnywhere.

## Required Secrets

Add these secrets in your GitHub repository:

**Settings** → **Secrets and variables** → **Actions** → **New repository secret**

### 1. PYTHONANYWHERE_USERNAME
- **Value:** `your_pythonanywhere_username`
- **Description:** Your PythonAnywhere username (e.g., john_doe)

### 2. PYTHONANYWHERE_API_TOKEN
- **Value:** `your_api_token_from_pythonanywhere`
- **Description:** Get this from https://www.pythonanywhere.com/account/#api_token
- **How to get:**
  1. Log in to PythonAnywhere
  2. Go to Account → API Token
  3. Click "Create a new API token" if you don't have one
  4. Copy the token

### 3. PYTHONANYWHERE_DOMAIN (Optional)
- **Value:** `username.pythonanywhere.com`
- **Description:** Your PythonAnywhere domain
- **Note:** If not set, defaults to `{username}.pythonanywhere.com`
- **When to set:** Only if you have a custom domain different from the default

## Verification

After adding the secrets:

1. Go to your repository's **Actions** tab
2. Look for "Deploy to PythonAnywhere" workflow
3. The next push to main should trigger a deployment
4. Or manually trigger it using "Run workflow" button

## Troubleshooting

If secrets are not working:
- Verify secret names match exactly (case-sensitive)
- Check API token hasn't expired
- Ensure you have admin access to the repository
- Re-create the secret if needed

## Security Notes

- Never commit secrets to the repository
- GitHub secrets are encrypted and only visible during workflow runs
- Regularly rotate your API tokens
- Only repository admins can view/modify secrets

## Next Steps

After setting up secrets:
1. Push a change to the main branch
2. Monitor the deployment in Actions tab
3. Verify your app updated at https://yourusername.pythonanywhere.com

For more details, see [CONTINUOUS_DEPLOYMENT.md](CONTINUOUS_DEPLOYMENT.md)
