from homeassistant.components.cover import CoverEntity, DeviceClass
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    api = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ExtelGateCover(api, entry.data["gate_id"], entry.title)])

class ExtelGateCover(CoverEntity):
    def __init__(self, api, gate_id, name):
        self._api = api
        self._gate_id = gate_id
        self._name = name
        self._state = None

    @property
    def name(self): return self._name
    
    @property
    def device_class(self): return DeviceClass.GATE

    @property
    def is_closed(self):
        return self._state == "closed"

    async def async_open_cover(self, **kwargs):
        await self._api.send_command(self._gate_id, "OPEN")

    async def async_close_cover(self, **kwargs):
        await self._api.send_command(self._gate_id, "CLOSE")

    async def async_stop_cover(self, **kwargs):
        await self._api.send_command(self._gate_id, "STOP")

    async def async_update(self):
        """Met à jour l'état depuis l'API."""
        self._state = await self._api.get_status(self._gate_id)
