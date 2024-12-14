import logging
import httpx

from .classes import GroheDevice
from .utils import (
    create_command_url_from_device,
    check_tap_params,
    get_auth_header,
)


async def execute_command(
    device: GroheDevice, token: str, command: dict, client: httpx.AsyncClient
) -> bool:
    """
    Executes the command for the given device.

    Args:
        device: The device to execute the command on.
        token: The access token to use.
        command: The command to execute.

    Returns: True if the command was executed successfully, False otherwise.
    """

    async def send_command():
        command_url = create_command_url_from_device(device)

        headers = {
            "Content-Type": "application/json",
            "Authorization": get_auth_header(token),
        }
        data = {
            "type": None,
            "appliance_id": device.appliance_id,
            "command": command,
            "commandb64": None,
            "timestamp": None,
        }

        try:
            response = await client.post(command_url, headers=headers, json=data)
            response.raise_for_status()

            if (response.status_code - 200) >= 0 and (response.status_code - 200) < 100:
                return True

            logging.error(f"Failed to execute tap command. Response: {response.text}")

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


async def execute_tap_command(
    device: GroheDevice,
    token: str,
    client: httpx.AsyncClient,
    tap_type: int,
    amount: int,
) -> bool:
    """
    Executes the command for the given tap type and amount.

    Args:
        device: The device to execute the command on.
        token: The access token to use.
        tap_type: The type of tap. 1 for still, 2 for medium, 3 for sparkling.
        amount: The amount of water to be dispensed in ml in steps of 50ml.

    Returns: True if the command was executed successfully, False otherwise.
    """
    check_tap_params(tap_type, amount)

    command = {
        "co2_status_reset": False,
        "tap_type": tap_type,
        "cleaning_mode": False,
        "filter_status_reset": False,
        "get_current_measurement": False,
        "tap_amount": amount,
        "factory_reset": False,
        "revoke_flush_confirmation": False,
        "exec_auto_flush": False,
    }

    success = await execute_command(device, token, command, client=client)

    return success


async def execute_custom_command(
    device: GroheDevice,
    token: str,
    client: httpx.AsyncClient,
    co2_reset=False,
    filter_reset=False,
    flush=False,
    tap_type=None,
    tap_amount=None,
    clean_mode=False,
    get_current_measurement=False,
    revoke_flush_confirmation=False,
    factory_reset=False,
) -> bool:
    """
    Executes a custom command for the given device.

    Returns: True if the command was executed successfully, False otherwise.
    """
    command = {
        "co2_status_reset": co2_reset,
        "tap_type": tap_type,
        "cleaning_mode": clean_mode,
        "filter_status_reset": filter_reset,
        "get_current_measurement": get_current_measurement,
        "tap_amount": tap_amount,
        "factory_reset": factory_reset,
        "revoke_flush_confirmation": revoke_flush_confirmation,
        "exec_auto_flush": flush,
    }

    success = await execute_command(device, token, command, client=client)

    return success


async def get_dashboard_data(access_token, client: httpx.AsyncClient) -> dict:
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
        response = await client.get(appliance_info_url, headers=headers)
        response.raise_for_status()
        logging.info("Appliance information retrieved successfully.")
        return response.json()

    except httpx.HTTPStatusError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except httpx.RequestError as err:
        logging.error(f"Request error occurred: {err}")

    return {}
