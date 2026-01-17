from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_DEVICE_ID
from .api import ExtelUmiiAPI
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api = ExtelUmiiAPI(
        entry.data[CONF_EMAIL], 
        entry.data[CONF_PASSWORD],
        entry.data.get(CONF_DEVICE_ID)
    )
    
    await api.login()
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = api
    
    # On charge les deux plateformes : cover et button
    await hass.config_entries.async_forward_entry_setups(entry, ["cover", "button"])
    return True