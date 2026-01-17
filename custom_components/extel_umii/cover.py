from homeassistant.components.cover import (
    CoverEntity, 
    CoverDeviceClass, 
    CoverEntityFeature
)
from .const import DOMAIN

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

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return f"extel_{self._gate_id}"

    @property
    def device_class(self):
        # Correction ici : CoverDeviceClass au lieu de DeviceClass
        return CoverDeviceClass.GATE

    @property
    def supported_features(self):
        """Définit les boutons disponibles (Ouvrir, Fermer, Stop)."""
        return CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.STOP

    @property
    def is_closed(self):
        if self._state is None:
            return None
        return self._state == "closed"

    async def async_open_cover(self, **kwargs):
        """Action d'ouverture."""
        await self._api.send_command(self._gate_id, "OPEN")
        self._state = "opening"
        self.async_write_ha_state()

    async def async_close_cover(self, **kwargs):
        """Action de fermeture."""
        await self._api.send_command(self._gate_id, "CLOSE")
        self._state = "closing"
        self.async_write_ha_state()

    async def async_stop_cover(self, **kwargs):
        """Action d'arrêt."""
        await self._api.send_command(self._gate_id, "STOP")
        self.async_write_ha_state()

    async def async_update(self):
        """Récupère l'état réel depuis l'API."""
        self._state = await self._api.get_status(self._gate_id)