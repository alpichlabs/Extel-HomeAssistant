from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Initialise le portail après config."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    
    # Ici on pourra ajouter plus tard :
    # hass.async_create_task(hass.config_entries.async_forward_entry_setups(entry, ["button", "binary_sensor"]))
    
    return True
