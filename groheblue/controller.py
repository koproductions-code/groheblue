import logging
import httpx

from .classes import GroheDevice
from .utils import (
    create_command_url_from_device,
    get_command,
    check_tap_params,
    get_auth_header,
)


async def execute_tap_command(
    device: GroheDevice, token: str, tap_type: int, amount: int
) -> bool:
    """
    Executes the command for the given tap type and amount.

    Args:
        tap_type: The type of tap. 1 for still, 2 for medium, 3 for sparkling.
        amount: The amount of water to be dispensed in ml in steps of 50ml.
        tries: The number of tries to execute the command.

    Returns: True if the command was executed successfully, False otherwise.
    """
    check_tap_params(tap_type, amount)

    async def send_command():
        command_url = create_command_url_from_device(device)

        headers = {
            "Content-Type": "application/json",
            "Authorization": get_auth_header(token),
        }
        data = {
            "type": None,
            "appliance_id": device.appliance_id,
            "command": get_command(tap_type, amount),
            "commandb64": None,
            "timestamp": None,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(command_url, headers=headers, json=data)
                response.raise_for_status()

                if (response.status_code - 200) >= 0 and (
                    response.status_code - 200
                ) < 100:
                    return True

                logging.error(
                    f"Failed to execute tap command. Response: {response.text}"
                )

                if response.status_code >= 500:
                    raise RuntimeError("Server error.")
                elif response.status_code == 401:
                    raise ValueError("Token expired")

            except httpx.RequestError as e:
                logging.error(f"Request failed: {e}")

            except Exception as e:
                logging.error(f"An error occurred: {e}")

        return False

    return await send_command()


async def get_dashboard_data(access_token) -> dict:
    """
    Retrieves information about the appliance from the Grohe API.

    Returns:
        A dictionary containing the appliance information if successful,
        or an empty dictionary if the request fails.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": get_auth_header(access_token),
    }

    appliance_info_url = "https://idp2-apigw.cloud.grohe.com/v3/iot/dashboard"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(appliance_info_url, headers=headers)
            response.raise_for_status()
            logging.info("Appliance information retrieved successfully.")
            return response.json()

    except httpx.HTTPStatusError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except httpx.RequestError as err:
        logging.error(f"Request error occurred: {err}")

    return {}
