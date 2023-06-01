# Cobertura Console Reporter

Cobertura Console Reporter produces an easy to read console output for 
[Coverlet](https://github.com/coverlet-coverage/coverlet) output files (`coverage.cobertura.xml`) when
generated through the `dotnet` cli using the `--collect:"XPlat Code Coverage"` arg.

## Sample Output

![sample output](img/sample.png)

## Usage

As Python module:

```bash
python -m cobertura_console_reporter --coverage-file <path_to_coverage_cobertura_xml_file> [--package <package_name>] [--warning-threshold <number>]
```

As Windows binary:

```powershell
ccr.exe --coverage-file <path_to_coverage_cobertura_xml_file> [--package <package_name>] [--warning-threshold <number>]
```

As Mac/Linux binary:

```bash
ccr --coverage-file <path_to_coverage_cobertura_xml_file> [--package <package_name>] [--warning-threshold <number>]
```

### Args

| Arg                 | Description                                                              |
|---------------------|--------------------------------------------------------------------------|
| --coverage-file     | Path to the `coverage.cobertura.xml` file produced by Coverlet.          |
| --package           | [Optional] Name of the .NET package (project) to display output for.     |
| --warning-threshold | [Optional] Coverage percentage to display as a warning (defaults to 90). |

## Available PowerShell/Bash Scripts

These scripts are aimed to normalize script patterns across projects and platforms (based on [Scripts to Rule Them All](https://github.com/github/scripts-to-rule-them-all)). 

| Script                          | Description                                                                                                                                                                       |
|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `./scripts/setup.{ps1, sh}`     | Deletes the existing `Python` virtual environment if it exists and runs `bootstrap`.                                                                                              |
| `./scripts/bootstrap.{ps1, sh}` | Checks if `Python` is installed at the minimum version.<br>Creates and activates a `Python` virtual environment.<br>Installs `Python` dependencies from the `requirements` files. |
| `./scripts/test.{ps1, sh}`      | Executes unit tests.                                                                                                                                                              |
| `./scripts/build.{ps1, sh}`     | Builds the application as a single executable under the `/dist` directory using PyInstaller.                                                                                      |

## Troubleshooting

When running the `build.sh` script on Linux using `pyenv` to manage Python versions, you 
may need to install Python enabling shared libraries:

```bash
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.9.9
```
