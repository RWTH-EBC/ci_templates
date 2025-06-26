# EBC CI Templates

This repository provides a centralized GitHub Actions workflow designed to orchestrate multiple reusable workflows for Python projects.  
It acts as a single entry point to trigger selected CI jobs like linting, building packages, and generating documentation.

## Usage

To use this workflow in your own repository:

```yaml
name: Python CI

on:
  push:
  pull_request:

jobs:
  ci:
    uses: RWTH-EBC/ci_templates/.github/workflows/ci.yml@main
    with:
      PYTHON_VERSION: "3.11"
      USE_PYLINT: true
      USE_RUFF: true
      BUILD_PACKAGE: true
      GENERATE_DOCUMENTATION: true
```

## Inputs

| Name                  | Type    | Default  | Description                                                |
|-----------------------|---------|----------|------------------------------------------------------------|
| `PYTHON_VERSION`      | string  | `"3.10"` | Python version to use                                      |
| `USE_PYLINT`          | boolean | `false`  | Run static code analysis using `pylint`                    |
| `USE_RUFF`            | boolean | `false`  | Run static code analysis using `ruff`                      |
| `BUILD_PACKAGE`       | boolean | `false`  | Build and verify the Python package                        |
| `GENERATE_DOCUMENTATION` | boolean | `false`  | Build Sphinx documentation                                 |
| `PYTHON_PACKAGE_NAME` | string  | `""`     | The name of your Python package (optional)                 |
| `USE_UV`              | boolean | `false`  | Use `uv` instead of `pip` for installing dependencies      |
| `INSTALL_REQUIREMENTS`| boolean | `true`   | Install from `requirements.txt` if it exists               |
| `EXTRA_REQUIREMENTS`  | string  | `""`     | Extra requirements to pass to pip install (e.g. `[dev]`)   |

## Included Workflows

This CI workflow can trigger the following individual workflows:

###  `build.yml`
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

## Artifacts

Depending on which workflows are enabled, the CI run may upload the following artifacts:

- `dist/` — built package distributions
- `pylint-report/` — Pylint output (text, HTML, badge)
- `ruff-report/` — Ruff output (text, HTML, badge)
- `docs/` — Sphinx HTML documentation

## Requirements

- Python project with `setup.py` or `pyproject.toml`
- Optional: `requirements.txt` and/or `docs/requirements.txt`
- This workflow assumes conventional project layouts (e.g., code inside a folder named after the repo or explicitly passed)

---

For any questions or improvements, feel free to open an issue or pull request.