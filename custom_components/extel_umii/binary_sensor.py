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
    async_add_entities(
        [
            ExtelGatePresentSensor(coordinator, gate_id),
            ExtelGateBoardErrorSensor(coordinator, gate_id),
        ]
    )


class ExtelGatePresentSensor(CoordinatorEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_name = "Present"

    def __init__(self, coordinator, gate_id):
        super().__init__(coordinator)
        self._gate_id = gate_id
        self._attr_unique_id = f"extel_{gate_id}_present"

    @property
    def is_on(self):
        present = get_status_value(self.coordinator.data or {}, "present")
        if present is None:
            return None
        return str(present) == "1"


class ExtelGateBoardErrorSensor(CoordinatorEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_name = "Board Error"

    def __init__(self, coordinator, gate_id):
        super().__init__(coordinator)
        self._gate_id = gate_id
        self._attr_unique_id = f"extel_{gate_id}_board_error"

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
