# ci_templates
This repository defines reoccurring ci-jobs to be used by different repositories.


### Example:

Create a .github/workflows/EXAMPLE.yml file to use a workflow.
The content of the file should be as followed:

```yaml
name: install and build

on:
  push:
    branches: ["main"]

jobs:
  build:
    uses: "RWTH-EBC/ci_templates/.github/workflows/build.yml@main"
    with:
      python-version: "3.10"
      use-uv: false
      install-requirements: true
      extra-requirements: ""
```

## implemented workflows

| Workflow     | Beschreibung                                |
|--------------|---------------------------------------------|
| `install.yml`| installs the local python repositories      |
| `build.yml`  | builds and installs the python repositories |
