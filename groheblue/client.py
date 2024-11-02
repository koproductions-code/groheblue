import logging
from datetime import datetime, timedelta

from .tokens import get_refresh_tokens, get_tokens_from_credentials
from .controller import execute_tap_command, get_dashboard_data
from .classes import GroheDevice


class GroheClient:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.access_token = None
        self.refresh_token = None
        self.access_token_expiring_date = None

    async def login(self):
        """
        Asynchronously logs in the user by obtaining access and refresh tokens using provided credentials.

        This method attempts to retrieve tokens using the user's email and password. If successful, it sets the
        access token, its expiration date, and the refresh token for the user. If it fails, it logs an error
        message and raises the exception.

        Raises:
            Exception: If there is an error obtaining the tokens.

        Returns:
            None
        """
        try:
            tokens = await get_tokens_from_credentials(self.email, self.password)
            self.access_token = tokens["access_token"]
            self.access_token_expiring_date = datetime.now() + timedelta(
                seconds=tokens["access_token_expires_in"] - 60
            )
            self.refresh_token = tokens["refresh_token"]
        except Exception as e:
            logging.error(f"Could not get initial tokens: {e}")
            raise e

    async def refresh_tokens(self):
        """
        Refreshes the access and refresh tokens.

        This method asynchronously fetches new access and refresh tokens using the current refresh token.
        It updates the instance's access token, refresh token, and the access token's expiring date.

        Raises:
            Exception: If the token refresh process fails.

        Returns:
            None
        """
        tokens = await get_refresh_tokens(self.refresh_token)
        self.access_token = tokens["access_token"]
        self.refresh_token = tokens["refresh_token"]
        self.access_token_expiring_date = datetime.now() + timedelta(
            seconds=tokens["access_token_expires_in"] - 60
        )

    async def get_access_token(self) -> str:
        """
        Retrieves the current access token. If the access token has expired,
        it refreshes the tokens before returning the access token.

        Returns:
            str: The current access token.
        """
        if datetime.now() > self.access_token_expiring_date:
            await self.refresh_tokens()
        return self.access_token

    async def get_devices(self) -> list[GroheDevice]:
        """
        Asynchronously retrieves a list of GroheDevice objects.

        This method fetches the access token and uses it to get the dashboard data.
        It then extracts the first location and room from the data and iterates over
        the appliances in the room to create GroheDevice instances.

        Returns:
            list[GroheDevice]: A list of GroheDevice objects representing the appliances.
        """
        devices = []

        access_token = await self.get_access_token()
        data = await get_dashboard_data(access_token)

        for location in data["locations"]:
            for room in location["rooms"]:
                for appliance in room["appliances"]:
                    appliance_id = appliance["appliance_id"]
                    device = GroheDevice(location["id"], room["id"], appliance_id, appliance)
                    devices.append(device)

        return devices

    async def dispense(self, device, tap_type, amount):
        """
        Dispenses a specified amount of water from the given device.

        Args:
            device (str): The identifier of the device to dispense water from.
            tap_type (str): The type of tap operation to perform (e.g., still, sparkling).
            amount (int): The amount of water to dispense in milliliters.

        Returns:
            bool: True if the water was successfully dispensed, False otherwise.

        Raises:
            RuntimeError: If the water dispensing operation fails.
        """
        success = await execute_tap_command(
            device, await self.get_access_token(), tap_type, amount
        )

        if not success:
            logging.error("Failed to dispense water.")
            raise RuntimeError("Failed to dispense water.")

        return success
