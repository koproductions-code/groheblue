class GroheDevice:
    """
    Represents a Grohe device with various configurations, parameters, states, and statuses.

    Attributes:
        location_id (str): The ID of the location where the device is installed.
        room_id (str): The ID of the room where the device is installed.
        appliance_id (str): The ID of the appliance.
        installation_date (str): The installation date of the device.
        name (str): The name of the device.
        serial_number (str): The serial number of the device.
        type (str): The type of the device.
        version (str): The version of the device.
        tdt (str): The TDT of the device.
        timezone (str): The timezone of the device.
        role (str): The role of the device.
        registration_complete (bool): Indicates if the registration is complete.
        presharedkey (str): The pre-shared key for the device.
        config (Config): The configuration settings of the device.
        params (Params): The parameters of the device.
        error (Error): The error information of the device.
        state (State): The state information of the device.
        status (list of Status): The status information of the device.
        notifications (list): The notifications related to the device.
        data_latest (DataLatest): The latest data measurements of the device.

    Inner Classes:
        Config:
            Represents the configuration settings of the Grohe device.

            Attributes:
                co2_type (str): The type of CO2 used.
                co2_consumption_medium (float): The medium CO2 consumption.
                co2_consumption_carbonated (float): The carbonated CO2 consumption.
                guest_mode_active (bool): Indicates if guest mode is active.
                auto_flush_active (bool): Indicates if auto flush is active.
                flush_confirmed (bool): Indicates if flush is confirmed.
                hose_length (float): The length of the hose.
                f_parameter (float): The F parameter.
                l_parameter (float): The L parameter.
                flow_rate_still (float): The flow rate for still water.
                flow_rate_medium (float): The flow rate for medium water.
                flow_rate_carbonated (float): The flow rate for carbonated water.

        Params:
            Represents the parameters of the Grohe device.

            Attributes:
                water_hardness (float): The hardness of the water.
                carbon_hardness (float): The hardness of the carbon.
                filter_type (str): The type of filter used.
                variant (str): The variant of the device.
                auto_flush_reminder_notif (bool): Indicates if auto flush reminder notification is enabled.
                consumables_low_notif (bool): Indicates if consumables low notification is enabled.
                product_information_notif (bool): Indicates if product information notification is enabled.

        Error:
            Represents the error information of the Grohe device.

            Attributes:
                Dynamic attributes based on the error data provided.

        State:
            Represents the state information of the Grohe device.

            Attributes:
                start_time (str): The start time of the device.
                APPLIANCE_SUCCESSFUL_CONFIGURED (bool): Indicates if the appliance is successfully configured.
                co2_empty (bool): Indicates if the CO2 is empty.
                co2_20l_reached (bool): Indicates if 20 liters of CO2 have been reached.
                filter_empty (bool): Indicates if the filter is empty.
                filter_20l_reached (bool): Indicates if 20 liters of filter usage have been reached.
                cleaning_mode_active (bool): Indicates if cleaning mode is active.
                cleaning_needed (bool): Indicates if cleaning is needed.
                flush_confirmation_required (bool): Indicates if flush confirmation is required.
                System_error_bitfield (int): The system error bitfield.

        Status:
            Represents the status information of the Grohe device.

            Attributes:
                type (str): The type of status.
                value (str): The value of the status.

        DataLatest:
            Represents the latest data measurements of the Grohe device.

            Attributes:
                cleaning_count (int): The count of cleanings.
                date_of_cleaning (str): The date of the last cleaning.
                date_of_co2_replacement (str): The date of the last CO2 replacement.
                date_of_filter_replacement (str): The date of the last filter replacement.
                filter_change_count (int): The count of filter changes.
                max_idle_time (int): The maximum idle time.
                open_close_cycles_carbonated (int): The count of open/close cycles for carbonated water.
                open_close_cycles_still (int): The count of open/close cycles for still water.
                operating_time (int): The operating time of the device.
                power_cut_count (int): The count of power cuts.
                pump_count (int): The count of pump operations.
                pump_running_time (int): The running time of the pump.
                remaining_co2 (float): The remaining CO2.
                remaining_filter (float): The remaining filter.
                time_since_last_withdrawal (int): The time since the last withdrawal.
                time_since_restart (int): The time since the last restart.
                timeoffset (int): The time offset.
                timestamp (str): The timestamp of the latest data.
                water_running_time_carbonated (int): The running time for carbonated water.
                water_running_time_medium (int): The running time for medium water.
                water_running_time_still (int): The running time for still water.
                remaining_filter_liters (float): The remaining filter liters.
                remaining_co2_liters (float): The remaining CO2 liters.
    """

    def __init__(self, location_id: str, room_id: str, appliance_id: str, data: dict):
        self.location_id = location_id
        self.room_id = room_id
        self.appliance_id = appliance_id
        self.installation_date = data.get("installation_date")
        self.name = data.get("name")
        self.serial_number = data.get("serial_number")
        self.type = data.get("type")
        self.version = data.get("version")
        self.tdt = data.get("tdt")
        self.timezone = data.get("timezone")
        self.role = data.get("role")
        self.registration_complete = data.get("registration_complete")
        self.presharedkey = data.get("presharedkey")

        self.config = self.Config(data.get("config", {}))
        self.params = self.Params(data.get("params", {}))
        self.error = self.Error(data.get("error", {}))
        self.state = self.State(data.get("state", {}))
        self.status = [self.Status(status) for status in data.get("status", [])]
        self.notifications = data.get("notifications", [])
        self.data_latest = self.DataLatest(
            data.get("data_latest", {}).get("measurement", {})
        )

    class Config:
        def __init__(self, config):
            self.co2_type = config.get("co2_type")
            self.co2_consumption_medium = config.get("co2_consumption_medium")
            self.co2_consumption_carbonated = config.get("co2_consumption_carbonated")
            self.guest_mode_active = config.get("guest_mode_active")
            self.auto_flush_active = config.get("auto_flush_active")
            self.flush_confirmed = config.get("flush_confirmed")
            self.hose_length = config.get("hose_length")
            self.f_parameter = config.get("f_parameter")
            self.l_parameter = config.get("l_parameter")
            self.flow_rate_still = config.get("flow_rate_still")
            self.flow_rate_medium = config.get("flow_rate_medium")
            self.flow_rate_carbonated = config.get("flow_rate_carbonated")

    class Params:
        def __init__(self, params):
            self.water_hardness = params.get("water_hardness")
            self.carbon_hardness = params.get("carbon_hardness")
            self.filter_type = params.get("filter_type")
            self.variant = params.get("variant")
            self.auto_flush_reminder_notif = params.get("auto_flush_reminder_notif")
            self.consumables_low_notif = params.get("consumables_low_notif")
            self.product_information_notif = params.get("product_information_notif")

    class Error:
        def __init__(self, error):
            for key, value in error.items():
                setattr(self, key, value)

    class State:
        def __init__(self, state):
            self.start_time = state.get("start_time")
            self.APPLIANCE_SUCCESSFUL_CONFIGURED = state.get(
                "APPLIANCE_SUCCESSFUL_CONFIGURED"
            )
            self.co2_empty = state.get("co2_empty")
            self.co2_20l_reached = state.get("co2_20l_reached")
            self.filter_empty = state.get("filter_empty")
            self.filter_20l_reached = state.get("filter_20l_reached")
            self.cleaning_mode_active = state.get("cleaning_mode_active")
            self.cleaning_needed = state.get("cleaning_needed")
            self.flush_confirmation_required = state.get("flush_confirmation_required")
            self.System_error_bitfield = state.get("System_error_bitfield")

    class Status:
        def __init__(self, status):
            self.type = status.get("type")
            self.value = status.get("value")

    class DataLatest:
        def __init__(self, measurement):
            self.cleaning_count = measurement.get("cleaning_count")
            self.date_of_cleaning = measurement.get("date_of_cleaning")
            self.date_of_co2_replacement = measurement.get("date_of_co2_replacement")
            self.date_of_filter_replacement = measurement.get(
                "date_of_filter_replacement"
            )
            self.filter_change_count = measurement.get("filter_change_count")
            self.max_idle_time = measurement.get("max_idle_time")
            self.open_close_cycles_carbonated = measurement.get(
                "open_close_cycles_carbonated"
            )
            self.open_close_cycles_still = measurement.get("open_close_cycles_still")
            self.operating_time = measurement.get("operating_time")
            self.power_cut_count = measurement.get("power_cut_count")
            self.pump_count = measurement.get("pump_count")
            self.pump_running_time = measurement.get("pump_running_time")
            self.remaining_co2 = measurement.get("remaining_co2")
            self.remaining_filter = measurement.get("remaining_filter")
            self.time_since_last_withdrawal = measurement.get(
                "time_since_last_withdrawal"
            )
            self.time_since_restart = measurement.get("time_since_restart")
            self.timeoffset = measurement.get("timeoffset")
            self.timestamp = measurement.get("timestamp")
            self.water_running_time_carbonated = measurement.get(
                "water_running_time_carbonated"
            )
            self.water_running_time_medium = measurement.get(
                "water_running_time_medium"
            )
            self.water_running_time_still = measurement.get("water_running_time_still")
            self.remaining_filter_liters = measurement.get("remaining_filter_liters")
            self.remaining_co2_liters = measurement.get("remaining_co2_liters")
