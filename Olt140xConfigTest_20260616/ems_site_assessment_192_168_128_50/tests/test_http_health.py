import pytest


@pytest.mark.http
def test_https_endpoint_responds(config, http_session):
    response = http_session.get(
        config["base_url"],
        timeout=config["timeout_seconds"],
        allow_redirects=True,
    )

    assert response.status_code < 500
    assert response.url.startswith("https://")
    assert response.text.strip(), "Response body should not be empty."


@pytest.mark.http
def test_login_page_has_expected_controls(config, http_session):
    response = http_session.get(
        config["base_url"],
        timeout=config["timeout_seconds"],
        allow_redirects=True,
    )
    body = response.text.lower()

    login_signals = [
        'id="name"',
        'name="user"',
        'id="passwd"',
        'name="pass"',
        'id="signin"',
        'value="login"',
        "netatlasems",
    ]
    assert any(signal in body for signal in login_signals), (
        "Landing page did not expose expected EMS login signals."
    )


@pytest.mark.security
def test_security_headers_are_present(config, http_session):
    response = http_session.get(
        config["base_url"],
        timeout=config["timeout_seconds"],
        allow_redirects=True,
    )
    headers = {key.lower(): value for key, value in response.headers.items()}

    expected_headers = [
        "strict-transport-security",
        "x-frame-options",
        "x-content-type-options",
        "content-security-policy",
    ]
    missing = [header for header in expected_headers if header not in headers]
    assert not missing, f"Missing recommended security headers: {missing}"

