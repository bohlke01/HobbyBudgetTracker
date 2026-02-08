# GitHub Actions Workflow - Tests and Coverage

This document explains the GitHub Actions workflow that automatically runs tests and calculates test coverage for the HobbyBudgetTracker project.

## Workflow File

Location: `.github/workflows/test-coverage.yml`

## What Does This Workflow Do?

The workflow automatically:
1. **Runs all unit tests** using Python's unittest framework
2. **Calculates test coverage** using coverage.py
3. **Tests on multiple Python versions** (3.8, 3.9, 3.10, 3.11, 3.12)
4. **Displays coverage reports** in the GitHub Actions interface
5. **Uploads coverage data** to Codecov (optional)
6. **Archives coverage reports** as downloadable artifacts

## When Does It Run?

The workflow is triggered by:
- **Push events** to branches: `main`, `develop`, or any `copilot/**` branch
- **Pull requests** targeting `main` or `develop` branches

## Workflow Steps

### 1. Checkout Code
Uses `actions/checkout@v4` to clone the repository.

### 2. Set Up Python
Uses `actions/setup-python@v5` to set up the specified Python version.

### 3. Install Dependencies
```bash
python -m pip install --upgrade pip
pip install coverage
pip install -r requirements.txt  # if exists
pip install -e .  # install package in editable mode
```

### 4. Run Tests with Coverage
```bash
coverage run -m unittest discover tests
coverage report
coverage xml
```

This runs all tests in the `tests/` directory with coverage tracking.

### 5. Display Coverage Summary
Creates a formatted coverage report in the GitHub Actions summary page.

### 6. Upload to Codecov (Optional)
Only runs for Python 3.12:
- Uploads coverage.xml to Codecov
- Requires `CODECOV_TOKEN` secret to be configured
- Does not fail the build if upload fails

### 7. Archive Coverage Reports
Only runs for Python 3.12:
- Saves `coverage.xml` and `.coverage` as artifacts
- Can be downloaded from the workflow run page

## Configuration

### Adding Codecov Token (Optional)

To enable Codecov integration:
1. Sign up at [codecov.io](https://codecov.io)
2. Add your repository
3. Get your upload token
4. Add it to GitHub Secrets:
   - Go to: Settings → Secrets and variables → Actions
   - Create new secret: `CODECOV_TOKEN`
   - Paste your token

### Customizing Python Versions

To change which Python versions are tested, edit the matrix in the workflow file:

```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
```

### Customizing Branches

To change which branches trigger the workflow:

```yaml
on:
  push:
    branches: [main, develop, your-branch-pattern/**]
  pull_request:
    branches: [main, develop]
```

## Viewing Results

### GitHub Actions Tab
1. Go to the repository on GitHub
2. Click the "Actions" tab
3. Select a workflow run to see:
   - Test results for each Python version
   - Coverage report in the summary
   - Downloadable coverage artifacts

### README Badge
The workflow status is displayed as a badge in the README:

```markdown
![Tests and Coverage](https://github.com/bohlke01/HobbyBudgetTracker/actions/workflows/test-coverage.yml/badge.svg)
```

## Local Testing

To run the same tests locally that the workflow runs:

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run -m unittest discover tests

# View coverage report
coverage report

# Generate HTML report
coverage html
# Open htmlcov/index.html in browser
```

## Current Coverage Statistics

As of the latest run:
- **Total Tests**: 41
- **Overall Coverage**: 55.5%
- **Module Breakdown**:
  - `models.py`: 100%
  - `__init__.py`: 100%
  - `database.py`: 94%
  - `cli.py`: 62%
  - `web.py`: 1% (needs integration tests)

## Troubleshooting

### Workflow Not Running
- Check that you pushed to a branch that matches the trigger conditions
- Verify GitHub Actions is enabled for the repository

### Tests Failing
- Check the workflow logs for error messages
- Run tests locally to reproduce the issue
- Ensure all dependencies are listed in `requirements.txt`

### Coverage Not Uploading to Codecov
- Verify `CODECOV_TOKEN` secret is set correctly
- Check Codecov dashboard for error messages
- The workflow will continue even if upload fails

## Further Improvements

Potential enhancements:
1. Add code quality checks (pylint, flake8)
2. Add security scanning (bandit, safety)
3. Generate coverage badges automatically
4. Set minimum coverage thresholds
5. Add performance benchmarks
6. Deploy to test environment after successful tests

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Codecov Documentation](https://docs.codecov.com/)
