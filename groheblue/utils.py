from .classes import GroheDevice


def create_command_url_from_device(device: GroheDevice):
    """
    Generates a command URL for a given GroheDevice.

    Args:
        device (GroheDevice): An instance of GroheDevice containing the necessary identifiers.

    Returns:
        str: A formatted URL string for sending commands to the specified device.
    """
    return (
        f"https://idp2-apigw.cloud.grohe.com/v3/iot"
        f"/locations/{device.location_id}"
        f"/rooms/{device.room_id}"
        f"/appliances/{device.appliance_id}"
        f"/command"
    )


def get_command(tap_type: int, amount: int) -> dict:
    """
    Returns the command to execute for the given tap type and amount.
    Args:
        tap_type: The type of tap. 1 for still, 2 for medium, 3 for sparkling.
        amount: The amount of water to be dispensed in ml.

    Returns: The command to execute.

    """
    return {
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


def check_tap_params(tap_type: int, amount: int) -> None:
    """
    Checks the given tap parameters.
    Args:
        tap_type: The type of tap. 1 for still, 2 for medium, 3 for sparkling.
        amount: The amount of water to be dispensed in ml.

    Raises: ValueError if the parameters are invalid.

    """
    # check if the tap type is valid
    if tap_type not in [1, 2, 3]:
        raise ValueError(f"Invalid tap type: {tap_type}. Valid values are 1, 2 and 3.")
    # check if the amount is valid
    if amount % 50 != 0 or amount <= 0 or amount > 2000:
        raise ValueError(
            "The amount must be a multiple of 50, greater than 0 and less or equal to 2000."
        )


def get_auth_header(access_token: str) -> str:
    """
    Returns the authorization header for the given access token.
    Args:
        access_token: The access token to use.

    Returns: The authorization header.

    """
    return f"Bearer {access_token}"
