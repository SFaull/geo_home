"""Config flow for Geo Home integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .geohome import GeoHomeHub

_LOGGER = logging.getLogger(__name__)


def options_schema(options: dict = None) -> dict:
    """Return options schema."""
    options = options or {}
    return {
        vol.Required(
            "username",
            default=options.get("username", "admin"),
            description="Geo Home web username",
        ): str,
        vol.Required(
            "password",
            default=options.get("password", "password"),
            description="Geo Home web password",
        ): str,
        vol.Required(
            "polling_interval",
            default=options.get("polling_interval", 10),  # Default polling interval of 10 seconds
            description="Polling interval in seconds",
        ): int,
    }


def new_options(username: str, password: str, polling_interval: int) -> dict:
    """Create a standard options object."""
    return {"username": username, "password": password, "polling_interval": polling_interval}


def options_data(user_input: dict) -> dict:
    """Return options dict."""
    return new_options(
        user_input.get("username", ""),
        user_input.get("password", ""),
        user_input.get("polling_interval", 10),  # Default polling interval of 10 seconds
    )


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    hub = GeoHomeHub(data["username"], data["password"], hass)

    if not await hub.authenticate():
        raise InvalidAuth

    # If you cannot connect:
    # throw CannotConnect
    # If the authentication is wrong:
    # InvalidAuth

    # Return info that you want to store in the config entry.
    return {"title": "Geo Home"}


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Options for the component."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Init object."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(
                title="",
                data=options_data(user_input),
            )
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(options_schema(self.config_entry.options)),
        )


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Geo Home."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlowHandler:
        """Get the options flow."""
        return OptionsFlowHandler(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=vol.Schema(options_schema())
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(options_schema()), errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
