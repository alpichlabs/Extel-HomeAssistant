from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_DEVICE_ID
from .api import ExtelUmiiAPI
from .coordinator import ExtelGateCoordinator
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api = ExtelUmiiAPI(
        entry.data[CONF_EMAIL], 
        entry.data[CONF_PASSWORD],
        entry.data.get(CONF_DEVICE_ID)
    )
    
    await api.login()
    coordinator = ExtelGateCoordinator(hass, api, entry.data["gate_id"])
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }
    
    await hass.config_entries.async_forward_entry_setups(entry, ["cover", "button", "binary_sensor"])
    return True
