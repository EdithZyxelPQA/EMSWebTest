# EMS Site Assessment - 192.168.128.50:9116

This is a standalone pytest project for assessing `https://192.168.128.50:9116/`.
It does not import or modify any existing project modules.

## Test Items

1. HTTPS connectivity: target host and port are reachable, TLS handshake completes, and the response status is not a server error.
2. Login page availability: the landing page contains expected login controls or redirects to an EMS login path.
3. Basic security headers: check for common hardening headers such as `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`, and `Content-Security-Policy`.
4. Login form validation: submit empty credentials and verify the user is not logged in.
5. Valid login smoke test: login with configured credentials and verify an authenticated UI indicator appears.
6. Authenticated navigation smoke test: after login, verify core page content/menu elements are visible and the page is not blank.
7. About/version smoke test: if an About dialog is available, open it and capture the displayed EMS version.
8. Screenshot evidence: UI tests save screenshots in `artifacts/` for later review.

## Configuration

Default settings are in `config.json`.

Environment variables override sensitive or runtime values:

- `EMS_BASE_URL`
- `EMS_USERNAME`
- `EMS_PASSWORD`
- `EMS_HEADLESS`
- `EMS_BROWSER`

## Run

Install dependencies in an environment that has Python:

```powershell
python -m pip install -r requirements.txt
```

Run tests and generate reports:

```powershell
python -m pytest --junitxml reports/junit.xml
python tools/generate_report.py reports/junit.xml reports/assessment_report.md reports/assessment_report.html
```

