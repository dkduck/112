import feedparser
import logging
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_ID, CONF_COUNT

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=10)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coordinator = FeedUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([AlarmFeedSensor(coordinator)], True)

class FeedUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        self.feed_id = entry.data[CONF_ID]
        self.count = entry.data[CONF_COUNT]
        self.hass = hass
        super().__init__(
            hass,
            _LOGGER,
            name="Alarm Feed Coordinator",
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        url = f"https://alarm.example.com/rss?id={self.feed_id}"
        feed = await self.hass.async_add_executor_job(feedparser.parse, url)
        return feed.entries[:self.count]

class AlarmFeedSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Alarm Feed"

    @property
    def state(self):
        entries = self.coordinator.data
        if entries:
            return entries[0].title
        return "Ingen alarmer"

    @property
    def extra_state_attributes(self):
        return {
            f"alarm_{i+1}": e.title for i, e in enumerate(self.coordinator.data)
        }
