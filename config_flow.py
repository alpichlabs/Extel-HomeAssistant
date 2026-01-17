import voluptuous as vol
import uuid
from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from .const import DOMAIN, CONF_GATE_ID, CONF_DEVICE_ID
from .api import ExtelUmiiAPI

class ExtelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._email = None
        self._password = None
        # On génère un ID unique pour le store
        self._device_id = str(uuid.uuid4()).upper()

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            self._email = user_input[CONF_EMAIL]
            self._password = user_input[CONF_PASSWORD]
            api = ExtelUmiiAPI(self._email, self._password, self._device_id)
            if await api.login():
                return await self.async_step_select_gate()
            errors["base"] = "Login incorrect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_EMAIL): str,
                vol.Required(CONF_PASSWORD): str,
            }),
            errors=errors
        )

    async def async_step_select_gate(self, user_input=None):
        api = ExtelUmiiAPI(self._email, self._password, self._device_id)
        await api.login()
        gates = await api.get_gates()

        if not gates:
            return self.async_abort(reason="Pas de portail trouvé")

        if user_input is not None:
            gate_id = user_input[CONF_GATE_ID]
            return self.async_create_entry(
                title=gates[gate_id],
                data={
                    CONF_EMAIL: self._email,
                    CONF_PASSWORD: self._password,
                    CONF_GATE_ID: gate_id,
                    CONF_DEVICE_ID: self._device_id
                }
            )

        return self.async_show_form(
            step_id="select_gate",
            data_schema=vol.Schema({
                vol.Required(CONF_GATE_ID): vol.In(gates)
            })
        )