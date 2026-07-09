from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=15)


class ExtelGateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api, gate_id):
        super().__init__(
            hass,
            _LOGGER,
            name=f"Extel gate {gate_id}",
            update_interval=SCAN_INTERVAL,
        )
        self.api = api
        self.gate_id = gate_id

    async def _async_update_data(self):
        resource = await self.api.get_gate_resource(self.gate_id)
        if not resource:
            raise UpdateFailed(f"Unable to fetch Extel gate {self.gate_id}")
        return resource


def get_status_value(resource, name, default=None):
    for status in resource.get("statuses", []):
        if status.get("name") == name:
            return status.get("value", default)
    return default
