from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_ID, CONF_COUNT

class AlarmFeedConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=f"Alarm Feed ({user_input[CONF_ID]})", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_ID): str,
                vol.Required(CONF_COUNT, default=3): vol.All(vol.Coerce(int), vol.Range(min=1, max=10))
            }),
        )
