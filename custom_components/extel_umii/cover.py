import re

from homeassistant.components.cover import (
    CoverEntity,
    CoverDeviceClass,
    CoverEntityFeature,
)
from .const import DOMAIN

MIDDLE_STATUS_PATTERN = re.compile(r"^middle_(\d{1,3})$")


async def async_setup_entry(hass, entry, async_add_entities):
    """Configuration des entités cover à partir d'une entrée de configuration."""
    api = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ExtelGateCover(api, entry.data["gate_id"], entry.title)])


class ExtelGateCover(CoverEntity):
    """Représentation du portail Extel."""

    def __init__(self, api, gate_id, name):
        self._api = api
        self._gate_id = gate_id
        self._name = name
        self._state = None
        self._position = None
        self._last_raw_status = None
        self._last_command = None
        self._last_command_success = None

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return f"extel_{self._gate_id}"

    @property
    def device_class(self):
        return CoverDeviceClass.GATE

    @property
    def supported_features(self):
        """Définit les boutons disponibles (Ouvrir, Fermer, Stop)."""
        return CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.STOP

    @property
    def is_closed(self):
        if self._state is None or self._state == "unknown":
            return None
        return self._state == "closed"

    @property
    def is_opening(self):
        return self._state == "opening"

    @property
    def is_closing(self):
        return self._state == "closing"

    @property
    def current_cover_position(self):
        return self._position

    @property
    def extra_state_attributes(self):
        return {
            "last_raw_status": self._last_raw_status,
            "last_command": self._last_command,
            "last_command_success": self._last_command_success,
        }

    async def async_open_cover(self, **kwargs):
        """Action d'ouverture."""
        success = await self._api.send_command(self._gate_id, "OPEN")
        self._last_command = "OPEN"
        self._last_command_success = success
        if success:
            self._state = "opening"
        self.async_write_ha_state()

    async def async_close_cover(self, **kwargs):
        """Action de fermeture."""
        success = await self._api.send_command(self._gate_id, "CLOSE")
        self._last_command = "CLOSE"
        self._last_command_success = success
        if success:
            self._state = "closing"
        self.async_write_ha_state()

    async def async_stop_cover(self, **kwargs):
        """Action d'arrêt."""
        success = await self._api.send_command(self._gate_id, "STOP")
        self._last_command = "STOP"
        self._last_command_success = success
        self.async_write_ha_state()

    async def async_update(self):
        """Récupère l'état réel depuis l'API."""
        raw_status = await self._api.get_status(self._gate_id)
        self._apply_status(raw_status)

    def _apply_status(self, raw_status):
        self._last_raw_status = raw_status
        if raw_status == "closed":
            self._state = "closed"
            self._position = 0
            return
        if raw_status == "open":
            self._state = "open"
            self._position = 100
            return
        if raw_status in ("opening", "closing"):
            self._state = raw_status
            return

        middle_match = MIDDLE_STATUS_PATTERN.match(raw_status or "")
        if middle_match:
            self._state = raw_status
            self._position = max(0, min(100, int(middle_match.group(1))))
            return

        self._state = "unknown"