import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from .const import DOMAIN, CONF_GATE_ID
from .api import ExtelAPI

class ExtelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._email = None
        self._password = None

    async def async_step_user(self, user_input=None):
        """Étape 1 : Email et Mot de passe."""
        errors = {}
        if user_input is not None:
            api = ExtelAPI(user_input[CONF_EMAIL], user_input[CONF_PASSWORD])
            if await api.authenticate():
                self._email = user_input[CONF_EMAIL]
                self._password = user_input[CONF_PASSWORD]
                return await self.async_step_select_gate()
            errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_EMAIL): str,
                vol.Required(CONF_PASSWORD): str,
            }),
            errors=errors
        )

    async def async_step_select_gate(self, user_input=None):
        """Étape 2 : Choix du portail trouvé via l'API."""
        api = ExtelAPI(self._email, self._password)
        gates = await api.get_gates()

        if user_input is not None:
            return self.async_create_entry(
                title=gates[user_input[CONF_GATE_ID]],
                data={**user_input, CONF_EMAIL: self._email, CONF_PASSWORD: self._password}
            )

        return self.async_show_form(
            step_id="select_gate",
            data_schema=vol.Schema({
                vol.Required(CONF_GATE_ID): vol.In(gates)
            })
        )
