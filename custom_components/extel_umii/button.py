from homeassistant.components.button import ButtonEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    async_add_entities([ExtelPedestrianButton(api, entry.data["gate_id"], entry.title)])

class ExtelPedestrianButton(ButtonEntity):
    def __init__(self, api, gate_id, device_name):
        self._api = api
        self._gate_id = gate_id
        self._device_name = device_name
        self._attr_name = "Ouverture Piéton"
        self._attr_unique_id = f"{gate_id}_pedestrian"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._gate_id)},
            "manufacturer": "Extel",
            "name": self._device_name,
        }

    async def async_press(self):
        """Action lors de l'appui sur le bouton."""
        await self._api.send_command(self._gate_id, "HALF-OPEN")
