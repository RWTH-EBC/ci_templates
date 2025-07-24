# EBC CI Templates

This repository provides a centralized GitHub Actions workflow designed to orchestrate multiple reusable workflows for
Python projects.  
It acts as a single entry point to trigger selected CI jobs like linting, building packages, and generating
documentation.
---
## Usage

To use this workflow in your own repository:

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
    with:
      PYTHON_VERSION: "3.13"
      USE_PYLINT: true
      USE_RUFF: true
      BUILD_PACKAGE: true
      GENERATE_DOCUMENTATION: true
      USE_SEMANTIC_RELEASE: false
      EXECUTE_TESTS: true
      EXECUTE_COVERAGE_TEST: true
      CONVERT_EXAMPLES: true
      EXTRA_REQUIREMENTS: '[report]'
      PYTHON_PACKAGE_NAME: 'teaser'

```
## Inputs

| Name                      | Type    | Default                               | Description                                              |
|---------------------------|---------|---------------------------------------|----------------------------------------------------------|
| `PYTHON_VERSION`          | string  | `"3.13"`                              | Python version to use                                    |
| `USE_PYLINT`              | boolean | `false`                               | Run static code analysis using `pylint`                  |
| `USE_RUFF`                | boolean | `false`                               | Run static code analysis using `ruff`                    |
| `BUILD_PACKAGE`           | boolean | `false`                               | Build and verify the Python package                      |
| `GENERATE_DOCUMENTATION`  | boolean | `false`                               | Build Sphinx documentation                               |
| `PYTHON_PACKAGE_NAME`     | string  | `""`                                  | The name of your Python package (optional)               |
| `USE_UV`                  | boolean | `false`                               | Use `uv` instead of `pip` for installing dependencies    |
| `INSTALL_REQUIREMENTS`    | boolean | `true`                                | Install from `requirements.txt` if it exists             |
| `EXTRA_REQUIREMENTS`      | string  | `""`                                  | Extra requirements to pass to pip install (e.g. `[dev]`) |
| `EXECUTE_TESTS`           | boolean | `false`                               | Run the test suite using `pytest` or `unittest`          |
| `EXECUTE_COVERAGE_TEST`   | boolean | `false`                               | Run tests with coverage report and badge                 |
| `TEST_ENGINE`             | string  | `"PYTEST"`                            | Which test engine to use (`PYTEST` or `UNITTEST`)        |
| `TEST_PATH`               | string  | `"tests"`                             | Path to the test folder                                  |
| `COVERAGE_TYPE`           | string  | `"default"`                           | Coverage type, used to distinguish CI environments       |
| `USE_SEMANTIC_RELEASE`    | boolean | `false`                               | Enable automated versioning and changelog generation     |
| `COMMIT_SUBJECT`          | string  | `"chore(release): version {version}"` | Commit message for releases                              |
| `DIRECTORY`               | string  | `"."`                                 | Directory where `pyproject.toml` is located              |
| `GH_PAGES`                | boolean | `false`                               | Enable GitHub Pages deployment                           |
| `GH_PAGES_BRANCH`         | string  | `"gh-pages"`                          | Target branch for GitHub Pages                           |
| `GH_PAGES_DIR`            | string  | `"/tmp/gh-pages"`                     | Temporary folder to stage GitHub Pages files             |
| `DOCS_PATH`               | string  | `"docs"`                              | Directory where documentation output is located          |
| `CREATE_PAGES_ON_FAILURE` | boolean | `false`                               | If `true`, deployment will also run on failed builds     |

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
---
## Artifacts

Depending on which workflows are enabled, the CI run may upload the following artifacts:

- `dist/` — built package distributions
- `pylint-report/` — Pylint output (text, HTML, badge)
- `ruff-report/` — Ruff output (text, HTML, badge)
- `docs/` — Sphinx HTML documentation
---
## Requirements

- Python project with `setup.py` or `pyproject.toml`
- Optional: `requirements.txt` and/or `docs/requirements.txt`
- This workflow assumes conventional project layouts (e.g., code inside a folder named after the repo or explicitly
  passed)
- if you want to use the convert_examples workflow you need a gitlab access token and add is as a repository secret
- if you want to use a workflow that pushes code (e.g github_pages, semantic_release, convert_examples) you need a
  github access token as a repository secret