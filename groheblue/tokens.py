import httpx
import urllib.parse
from bs4 import BeautifulSoup

AUTH_BASE_URL = "https://idp2-apigw.cloud.grohe.com/v3/iot/oidc/login"
REFRESH_TOKEN_BASE_URL = "https://idp2-apigw.cloud.grohe.com/v3/iot/oidc/refresh"


async def get_tokens_from_credentials(
    grohe_email: str, grohe_password: str, client: httpx.AsyncClient
) -> dict:
    """
    Get the initial access and refresh tokens from the given Grohe credentials.
    Args:
        grohe_email: The Grohe email.
        grohe_password: The Grohe password.

    Returns: A dict with the tokens.
    """
    # Step 1: Get the login page to retrieve the action URL
    response = await client.get(AUTH_BASE_URL, follow_redirects=True)
    response.raise_for_status()
    html = response.text

    # Parse the HTML to extract the form action URL
    soup = BeautifulSoup(html, "html.parser")
    form = soup.find("form")
    if not form or "action" not in form.attrs:
        raise Exception("Login form target URL not found")

    action_url = urllib.parse.urljoin(AUTH_BASE_URL, form["action"])

    # Step 2: Send the login credentials
    payload = {
        "username": grohe_email,
        "password": grohe_password,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": AUTH_BASE_URL,
    }

    response = await client.post(
        action_url, data=payload, headers=headers, follow_redirects=False
    )
    if response.status_code != 302:
        raise Exception(
            "Invalid username/password or unexpected response from Grohe service"
        )

    # Step 3: Follow the redirect to get the token URL
    location = response.headers.get("Location")
    if not location:
        raise Exception("No redirect location found after login")

    tokens_url = location.replace("ondus://", "https://")

    # Step 4: Get the tokens
    response = await client.get(tokens_url)
    response.raise_for_status()
    json_data = response.json()

    tokens = get_tokens_from_json(json_data)
    return tokens


def get_tokens_from_json(json_data: dict) -> dict:
    """
    Get the tokens from the JSON data.
    Args:
        json_data: The JSON data.

    Returns: A dict with the tokens.
    """
    tokens = {
        "access_token": json_data.get("access_token"),
        "access_token_expires_in": json_data.get("expires_in"),
        "refresh_token": json_data.get("refresh_token"),
        "refresh_token_expires_in": json_data.get("refresh_expires_in"),
    }
    return tokens


async def get_refresh_tokens(refresh_token: str, client: httpx.AsyncClient) -> dict:
    """
    Refresh the access and refresh tokens.
    Args:
        refresh_token: The refresh token.

    Returns: A dict with the new tokens.
    """
    data = {"refresh_token": refresh_token, "grant_type": "refresh_token"}
    response = await client.post(REFRESH_TOKEN_BASE_URL, json=data)
    response.raise_for_status()
    json_data = response.json()

    tokens = get_tokens_from_json(json_data)
    return tokens
