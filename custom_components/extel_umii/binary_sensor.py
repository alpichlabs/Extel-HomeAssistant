from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.const import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import get_status_value


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    gate_id = entry.data["gate_id"]
    device_name = entry.title
    async_add_entities(
        [
            ExtelGateConnectivitySensor(coordinator, gate_id, device_name),
            ExtelGateProblemSensor(coordinator, gate_id, device_name),
        ]
    )


class ExtelGateConnectivitySensor(CoordinatorEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_has_entity_name = True
    _attr_name = "Connectivity"

    def __init__(self, coordinator, gate_id, device_name):
        super().__init__(coordinator)
        self._gate_id = gate_id
        self._device_name = device_name
        self._attr_unique_id = f"extel_{gate_id}_connectivity"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._gate_id)},
            "manufacturer": "Extel",
            "name": self._device_name,
        }

    @property
    def is_on(self):
        present = get_status_value(self.coordinator.data or {}, "present")
        if present is None:
            return None
        return str(present) == "1"

    @property
    def extra_state_attributes(self):
        return {
            "present": get_status_value(self.coordinator.data or {}, "present"),
        }


class ExtelGateProblemSensor(CoordinatorEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_has_entity_name = True
    _attr_name = "Problem"

    def __init__(self, coordinator, gate_id, device_name):
        super().__init__(coordinator)
        self._gate_id = gate_id
        self._device_name = device_name
        self._attr_unique_id = f"extel_{gate_id}_problem"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._gate_id)},
            "manufacturer": "Extel",
            "name": self._device_name,
        }

    @property
    def is_on(self):
        board_error = get_status_value(self.coordinator.data or {}, "board_error")
        if board_error is None:
            return None
        return str(board_error) != "0"

    @property
    def extra_state_attributes(self):
        return {
            "board_error": get_status_value(self.coordinator.data or {}, "board_error"),
        }
