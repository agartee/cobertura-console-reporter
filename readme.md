# Cobertura Console Reporter

Cobertura Console Reporter produces an easy to read console output for 
[Coverlet](https://github.com/coverlet-coverage/coverlet) output files (`coverage.cobertura.xml`) when
generated through the `dotnet` cli using the `--collect:"XPlat Code Coverage"` arg.

## Usage

```bash
python -m cobertura_console_reporter <path_to_coverage_cobertura_xml_file> [package_name]
```

### Args

| Arg                                 | Description                                                             |
|-------------------------------------|-------------------------------------------------------------------------|
| path_to_coverage_cobertura_xml_file | Path to the `coverage.cobertura.xml` file produced by Coverlet.         |
| package_name                        | (Optional) Name of the .NET package (project) to display in the output. |

## Available PowerShell/Bash Scripts

These scripts are aimed to normalize script patterns across projects and platforms (based on [Scripts to Rule Them All](https://github.com/github/scripts-to-rule-them-all)). 

| Script                          | Description                                                                                                                                                                       |
|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `./scripts/bootstrap.{ps1, sh}` | Checks if `Python` is installed at the minimum version.<br>Creates and activates a `Python` virtual environment.<br>Installs `Python` dependencies from the `requirements` files. |
| `./scripts/build.{ps1, sh}`     | Builds the application as a single executable under the `/dist` directory using PyInstaller.                                                                                      |
| `./scripts/setup.{ps1, sh}`     | Deletes the existing `Python` virtual environment if it exists and runs `bootstrap`.                                                                                              |
| `./scripts/test.{ps1, sh}`      | Executes unit tests.                                                                                                                                                              |

## Troubleshooting

When running the `build.sh` script on Linux using `pyenv` to manage Python versions, you 
may need to install Python enabling shared libraries:

```bash
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.9.9
```
