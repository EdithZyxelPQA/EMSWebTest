# EMSNewCaseTest_20260616

This pytest project is the landing area for new NetAtlas EMS automated test cases.
The existing projects remain for legacy maintenance:

- `../GlobalTest_20260616`
- `../Olt140xConfigTest_20260616`
- `../ChassisConfigTest_260616`

Do not add new test cases to the legacy project folders. They are independent projects and should be changed only when explicitly requested for small maintenance work.

If a new case needs a helper or pattern from a legacy project, copy the needed code into this project first and then adjust it here. Do not share imports directly with the legacy folders.

## Structure

- `conftest.py` loads `environment_parameter.json` and provides `test_config`.
- `tests/` contains new pytest cases.
- `libs/` contains shared helpers for new cases.
- `report/` and `download/` are runtime output folders and should not be committed.

## Run

Run one node:

```powershell
pytest -v -s --cmdopt=NODE1
```

Run a specific case:

```powershell
pytest tests/test_environment.py::TestEnvironment::test_environment_file_loaded -v -s --cmdopt=NODE1
```

Run with another environment file:

```powershell
pytest -v -s --env-file=environment_parameter.json --cmdopt=NODE1
```

## Add New Cases

1. Add a new `test_*.py` file under `tests/`.
2. Use the `test_config` fixture for EMS/DUT parameters.
3. Add shared Selenium or REST helpers under `libs/` when multiple cases need them.
4. Keep test data in `environment_parameter.json` instead of hard-coding IPs, accounts, or device values.
