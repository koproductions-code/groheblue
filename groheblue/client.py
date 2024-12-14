import logging
import asyncio
import httpx
from datetime import datetime, timedelta

from .tokens import get_refresh_tokens, get_tokens_from_credentials
from .controller import execute_tap_command, get_dashboard_data, execute_custom_command
from .classes import GroheDevice


class GroheClient:
    def __init__(
        self, email: str, password: str, httpx_client: httpx.AsyncClient = None
    ):
        self.email = email
        self.password = password
        self.access_token = None
        self.refresh_token = None
        self.access_token_expiring_date = None
        self.httpx_client = httpx_client or httpx.AsyncClient()

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
            tokens = await get_tokens_from_credentials(
                self.email, self.password, self.httpx_client
            )
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
        tokens = await get_refresh_tokens(self.refresh_token, self.httpx_client)
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

    async def get_current_measurement(self, device: GroheDevice) -> GroheDevice:
        """
        Retrieves the current measurement of the given device.

        Args:
            device (GroheDevice): The device to get the current measurement from.

        Returns:
            GroheDevice: The device with the new measurement data.
        """
        access_token = await self.get_access_token()
        success = await execute_custom_command(
            device, access_token, self.httpx_client, get_current_measurement=True
        )

        if not success:
            logging.error("Failed to get current measurement.")
            raise RuntimeError("Failed to get current measurement.")

        new_data = False
        counter = 0

        while not (new_data) and counter < 5:
            await asyncio.sleep(2)
            data = await get_dashboard_data(access_token, self.httpx_client)
            for location in data["locations"]:
                for room in location["rooms"]:
                    for appliance in room["appliances"]:
                        if appliance["appliance_id"] == device.appliance_id:
                            device.data_latest.timestamp != appliance["data_latest"][
                                "measurement"
                            ]["timestamp"]
                            new_data = True

            counter += 1

        return GroheDevice(
            device.location_id, device.room_id, device.appliance_id, appliance
        )

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
        data = await get_dashboard_data(access_token, self.httpx_client)

        for location in data["locations"]:
            for room in location["rooms"]:
                for appliance in room["appliances"]:
                    appliance_id = appliance["appliance_id"]
                    device = GroheDevice(
                        location["id"], room["id"], appliance_id, appliance
                    )
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
            device, await self.get_access_token(), self.httpx_client, tap_type, amount
        )

        if not success:
            logging.error("Failed to dispense water.")
            raise RuntimeError("Failed to dispense water.")

        return success

    async def custom_command(self, device, **kwargs):
        """
        Executes a custom command on the given device.
        !!! Only use this if you know what you are doing. !!!

        Args:
            device (GroheDevice): The device to execute the command on.
            **kwargs: The command parameters. Defaults are:
                co2_status_reset: False
                tap_type: None
                cleaning_mode: False
                filter_status_reset: False
                get_current_measurement: False
                tap_amount: None
                factory_reset: False
                revoke_flush_confirmation: False
                exec_auto_flush: False

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        success = await execute_custom_command(
            device, await self.get_access_token(), self.httpx_client, **kwargs
        )

        if not success:
            logging.error("Failed to execute custom command.")
            raise RuntimeError("Failed to execute custom command.")

        return success
