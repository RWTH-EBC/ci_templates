# EBC CI Templates

---

This repository provides a centralized GitHub Actions workflow designed to orchestrate multiple reusable workflows for
Python projects.  
It acts as a single entry point to trigger selected CI jobs like linting, building packages, and generating
documentation.

## Usage

You need to create the ./.github/workflows/ folder and the ./.github/workflows/ci.yml file in your repository and import
this workflow.

```yaml
name: Python CI

on:
  push:

jobs:
  ci:
    uses: RWTH-EBC/ci_templates/.github/workflows/ci_pipeline.yml@main
```

This is a minimal example that does not include any functionality.


## Requirements

- Python project with `setup.py` or `pyproject.toml`
- Optional: `requirements.txt` and/or `docs/requirements.txt`
- This workflow assumes conventional project layouts (e.g., code inside a folder named after the repo or explicitly
  passed)
- If you want to use the convert_examples workflow, you need a GitLab access token and must add it as a repository
  secret
    - For information on how to create a repository secret,
      read [this guide](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-what-your-workflow-does/using-secrets-in-github-actions)
- If you want to use a workflow that pushes code (e.g., github_pages, semantic_release, or convert_examples), you need a
  GitHub access token as a repository secret
    - For information on how to create a GitHub access token,
      read [this guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- If you want to use the PyPI release workflow, you need PyPI credentials as repository secrets
    - You can use either username/password or API token authentication
    - For information on how to create a PyPI API token,
      read [this guide](https://pypi.org/help/#apitoken)

## Example

```yaml
name: Python CI

on:
  push:

jobs:
  ci:
    uses: RWTH-EBC/ci_templates/.github/workflows/ci_pipeline.yml@main
    secrets:
      GH_TOKEN: ${{ secrets.GH_TOKEN }}
      GITLAB_TOKEN: ${{ secrets.GITLAB_TOKEN }}
      PYPI_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
    with:
      PYTHON_VERSION: "3.13"
      USE_PYLINT: true
      USE_RUFF: true
      BUILD_PACKAGE: true
      GENERATE_DOCUMENTATION: true
      GH_PAGES: true
      EXECUTE_TESTS: true
      EXECUTE_COVERAGE_TEST: true
      CONVERT_EXAMPLES: true
      PYPI_RELEASE: true
      EXTRA_REQUIREMENTS: '[dev]'

```

## Inputs

| Name                       | Type    | Default                                                                                         | Description                                                                                       |
|----------------------------|---------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `PYTHON_VERSION`           | string  | `"3.10"`                                                                                        | Python version to use                                                                             |
| `USE_PYLINT`               | boolean | `false`                                                                                         | Run static code analysis using `pylint`                                                           |
| `USE_RUFF`                 | boolean | `false`                                                                                         | Run static code analysis using `ruff`                                                             |
| `BUILD_PACKAGE`            | boolean | `false`                                                                                         | Build and verify the Python package                                                               |
| `GENERATE_DOCUMENTATION`   | boolean | `false`                                                                                         | Build Sphinx documentation                                                                        |
| `PYTHON_PACKAGE_NAME`      | string  | `""`                                                                                            | The name of your Python package ((needed when the package name is different then the repository)) |
| `USE_UV`                   | boolean | `false`                                                                                         | Use `uv` instead of `pip` for installing dependencies                                             |
| `INSTALL_REQUIREMENTS`     | boolean | `true`                                                                                          | Install from `requirements.txt` if it exists                                                      |
| `EXTRA_REQUIREMENTS`       | string  | `""`                                                                                            | Extra requirements to pass to pip install (e.g. `[dev]`)                                          |
| `EXECUTE_TESTS`            | boolean | `false`                                                                                         | Run unit tests                                                                                    |
| `EXECUTE_COVERAGE_TEST`    | boolean | `false`                                                                                         | Run coverage tests                                                                                |
| `COVERAGE_TYPE`            | string  | `"default"`                                                                                     | Coverage mode: `default` or `Dymola`                                                              |
| `PYTHON_TEST_MATRIX`       | string  | `'["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]'`                                              | List of Python versions to run tests against as a matrix (e.g. `["3.10", "3.11"]`)                |
| `TEST_ENGINE`              | string  | `"PYTEST"`                                                                                      | Test runner engine (`PYTEST`, `unittest`, ...)                                                    |
| `TEST_PATH`                | string  | `"tests"`                                                                                       | Path to test folder                                                                               |
| `FAIL-FAST`                | boolean | `false`                                                                                         | If true and one of the jobs in the python test matrix fails, all other jobs are cancelled         |
| `USE_SEMANTIC_RELEASE`     | boolean | `false`                                                                                         | Use Python Semantic Release for versioning                                                        |
| `DIRECTORY`                | string  | `"."`                                                                                           | Project base directory for semantic release                                                       |
| `COMMIT_SUBJECT`           | string  | `"chore(release): version {version}"`                                                           | Commit message format for release                                                                 |
| `GH_PAGES`                 | boolean | `false`                                                                                         | Enable GitHub Pages deployment                                                                    |
| `GH_PAGES_BRANCH`          | string  | `"gh-pages"`                                                                                    | Target branch for GitHub Pages deployment                                                         |
| `GH_PAGES_DIR`             | string  | `"/tmp/gh-pages"`                                                                               | Temp directory for Pages workflow                                                                 |
| `DOCS_PATH`                | string  | `"docs"`                                                                                        | Path to documentation                                                                             |
| `CREATE_PAGES_ON_FAILURE`  | boolean | `false`                                                                                         | Whether to generate pages even if previous steps failed                                           |
| `CONVERT_EXAMPLES`         | boolean | `false`                                                                                         | Enable automatic example conversion into jupyter notebook                                         |
| `GIT_REPO`                 | string  | `""`                                                                                            | Git repo to push converted files to (only used for example conversion)                            |
| `EXAMPLE_CONVERTER_CONFIG` | string  | `"examples/converter.toml"`                                                                     | Config file for example converter                                                                 |
| `COMMIT_MSG`               | string  | `"chore(examples): Automatic commit of example files in Markdown and Jupyter Notebook format."` | Commit message for example converter                                                              |
| `EXAMPLE_FILE_FOLDER`      | string  | `"converter"`                                                                                   | Folder where the converter repo will be cloned                                                    |
| `PYPI_RELEASE`             | boolean | `false`                                                                                         | Enable PyPI release (only triggered on main branch with "PYPI-RELEASE" in commit message)        |
| `PYTHON_VERSION_NAME`      | string  | `"__version__"`                                                                                 | Name of the version attribute in your Python package                                              |

## Secrets

| Name             | Required | Description                                                      |
|------------------|----------|------------------------------------------------------------------|
| `GH_TOKEN`       | false    | GitHub personal access token (required for releases and pages)  |
| `GITLAB_TOKEN`   | false    | GitLab access token (required for example conversion)           |
| `PYPI_PASSWORD`  | false    | PyPI password or API token (required for PyPI releases)         |

## Included Workflows

This CI workflow can trigger the following individual workflows:

### `build.yml`

- Installs the local repository and its dependencies.
- Optionally uses `uv` as the installer.
- Builds the package using `python -m build`.
- Installs the package to verify its integrity.

### `pylint.yml`

- Runs `pylint` on your codebase.
- Auto-detects the module name if not provided.
- Generates a badge and a linting report as artifacts.

### `ruff.yml`

- Runs the `ruff` linter for fast static code analysis.
- Outputs a text report, HTML version, and a badge with issue count.

### `sphinx_doc.yml`

- Installs documentation dependencies (e.g. `sphinx`, `sphinx-rtd-theme`).
- Runs `sphinx-apidoc` and `sphinx-build`.
- Publishes the generated HTML and a status badge.

### `tests.yml`

- Runs unit tests using `pytest` or `unittest`
- Supports specifying a test directory and engine
- Uploads test results as GitHub Actions logs

### `test-coverage.yml`

- Executes tests with `coverage` tracking
- Generates `HTML` report and `coverage-badge`
- Uploads coverage folder as an artifact

### `semantic-release.yml`

- Uses `python-semantic-release` to automate releases
- Requires conventional commits for version bumps
- Can publish to PyPI and update `CHANGELOG.md`

### `github_pages.yml`

- Deploys built documentation (e.g. Sphinx) to GitHub Pages
- Supports dynamic branch folders (e.g. per-branch previews)
- Automatically cleans up outdated previews

### `examples_converter.yml`

- Clones a template repo and converts `.md` and `.ipynb` example files.
- Commits and pushes the converted files to the current repo or a custom repo.

### `release.yml`

- Builds and releases your Python package to PyPI
- Creates GitHub releases with built distributions
- **Trigger conditions:**
  - Only runs on commits to the `main` branch
  - Only runs when commit message contains `PYPI-RELEASE`
  - Only runs when `PYPI_RELEASE` input is set to `true`
- Automatically detects package version from your Python module
- Prevents duplicate releases (checks if version already exists on PyPI)
- Supports both PyPI username/password and API token authentication

### `fiware_tests.yml`
- Run unittests with a FIWARE platform inside the CI job.
- This workflow is NOT INCLUDED by default
- It requires a `docker-compose.yml` that resides in your project repository. A possible structure in your repository is:
```
.
├── .github/workflows/my_workflow.yml   <-- your workflow that uses the fiware_tests.yml
├── my_project
│   └── docker/
│       └── docker-compose.yml      <-- Your FIWARE configurations
│       └── mosquitto.conf          <-- Your FIWARE configurations

```
- Additional inputs:

| Input              | Required | Default | Description                              |
|--------------------|----------|---------|------------------------------------------|
| FIWARE_DIRECTORY   | Yes      |         | Directory containing docker-compose.yml. |
| TEST_ENV_VARS      | No       | '[ ]'   | List of env vars needed for unittest     |
- An example is provided in the [`.github/workflows/fiware_test_example.yml`](.github/workflows/fiware_test_example.yml)
## PyPI Release Workflow

The PyPI release workflow has special trigger conditions to prevent accidental releases:

### Trigger Requirements
1. **Branch**: Must be a push to the `main` branch
2. **Commit Message**: Must contain the text `PYPI-RELEASE`
3. **Input Parameter**: `PYPI_RELEASE` must be set to `true`
4. **Dependencies**: All other workflows (build, tests, etc.) must complete successfully

### Example Usage
To trigger a PyPI release, make a commit with a message like:
```bash
git commit -m "feat: add new feature PYPI-RELEASE"
```

And ensure your workflow configuration includes:
```yaml
with:
  PYPI_RELEASE: true
  PYTHON_PACKAGE_NAME: "your-package-name"
```

### Version Detection
The workflow automatically detects your package version by:
1. First trying to import your package and read the version attribute (default: `__version__`)
2. Falling back to `setup.py --version` if available
3. Falling back to reading version from `pyproject.toml`
4. Failing if no version can be determined

### PyPI Authentication
You can use either traditional username/password or API tokens:

**Option 1: Username/Password**
```yaml
secrets:
  PYPI_PASSWORD: ${{ secrets.PYPI_PASSWORD }}  # Your PyPI password
```

**Option 2: API Token (Recommended)**
```yaml
secrets:
  PYPI_PASSWORD: ${{ secrets.PYPI_PASSWORD }}  # Your API token
```

For API token usage:
1. Create an API token at https://pypi.org/manage/account/token/
2. Set `PYPI_PASSWORD` to your API token

---

## Artifacts

Depending on which workflows are enabled, the CI run may upload the following artifacts:

- `build/` — build status badge
- `dist/` — built package distributions (from release workflow)
- `pylint/` — Pylint output (text, HTML, badge)
- `ruff/` — Ruff output (text, HTML, badge)
- `docs/` — Sphinx HTML documentation
- `coverage/` — Coverage reports and badges

---