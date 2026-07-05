import aiohttp
import logging
from .const import DEFAULT_HEADERS

_LOGGER = logging.getLogger(__name__)

VALID_GATE_STATES = {"closed", "open", "opening", "closing", "unknown"}


class ExtelUmiiAPI:
    def __init__(self, email, password, device_id):
        self.email = email
        self.password = password
        self.device_id = device_id
        self.token = None
        self.base_url = "https://umii.avidsen.one/services"

    async def login(self):
        url = f"{self.base_url}/dain/login"
        payload = {
            "login": self.email,
            "password": self.password,
            "stayConnected": "on",
            "deviceID": self.device_id,
            "deviceOS": "IOS",
            "deviceType": "iPhone13,4"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=DEFAULT_HEADERS) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self.token = data.get("token")
                    return True
                _LOGGER.warning("Extel login failed with HTTP status %s", resp.status)
                return False

    async def get_gates(self):
        url = f"{self.base_url}/durin/my/objects"
        headers = {**DEFAULT_HEADERS, "Authorization": f"Bearer {self.token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    content = data.get("content", [])
                    gates = {}
                    for item in content:
                        res = item.get("resource", {})
                        if res.get("className") in ("BoardGate", "Gate"):
                            gid = res.get("id")
                            name = res.get("name") or "Portail Jardin"
                            gates[str(gid)] = name
                    return gates
                _LOGGER.warning("Extel gate list failed with HTTP status %s", resp.status)
                return {}

    async def send_command(self, gate_id, action):
        """Envoie OPEN, CLOSE, STOP ou HALF-OPEN via PUT."""
        if not self.token:
            await self.login()
        url = f"{self.base_url}/durin/my/objects/{gate_id}"
        payload = {"actions": [{"name": action}]}

        async with aiohttp.ClientSession() as session:
            for attempt in range(2):
                headers = {**DEFAULT_HEADERS, "Authorization": f"Bearer {self.token}"}
                async with session.put(url, json=payload, headers=headers) as resp:
                    ok = resp.status in [200, 204]
                    if ok:
                        return True
                    if resp.status == 401 and attempt == 0 and await self.login():
                        continue
                    _LOGGER.warning(
                        "Extel command %s for gate %s failed with HTTP status %s",
                        action,
                        gate_id,
                        resp.status,
                    )
                    return False

    async def get_status(self, gate_id):
        url = f"{self.base_url}/durin/my/objects/{gate_id}"
        async with aiohttp.ClientSession() as session:
            for attempt in range(2):
                headers = {**DEFAULT_HEADERS, "Authorization": f"Bearer {self.token}"}
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 401 and attempt == 0 and await self.login():
                        continue
                    if resp.status == 200:
                        data = await resp.json()
                        res = data.get("resource", {})
                        statuses = res.get("statuses", [])
                        for status in statuses:
                            if status.get("name") == "status":
                                raw_status = str(status.get("value", "unknown")).strip().lower()
                                _LOGGER.debug("Extel raw status for gate %s: %s", gate_id, raw_status)
                                if raw_status in VALID_GATE_STATES or raw_status.startswith("middle_"):
                                    return raw_status
                                _LOGGER.warning("Unknown Extel status for gate %s: %s", gate_id, raw_status)
                                return "unknown"
                        _LOGGER.warning("Extel status missing for gate %s", gate_id)
                        return "unknown"
                    _LOGGER.warning("Extel status fetch for gate %s failed with HTTP status %s", gate_id, resp.status)
                    return "unknown"