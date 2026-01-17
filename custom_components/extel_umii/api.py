import aiohttp
import logging
from .const import DEFAULT_HEADERS

_LOGGER = logging.getLogger(__name__)

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
                        if res.get("className") == "BoardGate":
                            gid = res.get("id")
                            name = res.get("name") or "Portail Jardin"
                            gates[str(gid)] = name
                    return gates
                return {}

    async def send_command(self, gate_id, action):
        """Envoie OPEN, CLOSE, STOP ou HALF-OPEN via PUT."""
        if not self.token: await self.login()
        # URL corrigée selon ton YAML
        url = f"{self.base_url}/durin/my/objects/{gate_id}"
        headers = {**DEFAULT_HEADERS, "Authorization": f"Bearer {self.token}"}
        payload = {"actions": [{"name": action}]}

        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=payload, headers=headers) as resp:
                return resp.status in [200, 204]

    async def get_status(self, gate_id):
        url = f"{self.base_url}/durin/my/objects/{gate_id}"
        headers = {**DEFAULT_HEADERS, "Authorization": f"Bearer {self.token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    res = data.get("resource", {})
                    statuses = res.get("statuses", [])
                    for s in statuses:
                        if s.get("name") == "status":
                            return s.get("value")
                return "unknown"