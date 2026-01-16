import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

class ExtelUmiiAPI:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.token = None
        self.base_url = "https://umii.avidsen.one/services"

    async def login(self):
        """Authentification Umii (Login)."""
        url = f"{self.base_url}/login" # Adapté de tes captures
        payload = {
            "login": self.email,
            "password": self.password,
            "stayConnected": "on",
            "deviceID": "99420B8A-38D2-4FF2-8B70-08A3", # ID vu dans ton image
            "deviceOS": "IOS",
            "deviceType": "iPhone13,4",
            "deviceToken": "cxWJvPWm..." # À compléter si besoin
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=DEFAULT_HEADERS) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self.token = data.get("token")
                    return True
                return False

    async def send_command(self, gate_id, action):
        """Envoie une commande (OPEN, CLOSE, STOP, HALF-OPEN)."""
        url = f"{self.base_url}/devices/{gate_id}/action"
        headers = {**DEFAULT_HEADERS, "Authorization": f"Bearer {self.token}"}
        payload = {"actions": [{"name": action}]}

        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=payload, headers=headers) as resp:
                return resp.status == 200

    async def get_status(self, gate_id):
        """Récupère l'état (Open/Closed)."""
        url = f"{self.base_url}/devices/{gate_id}/status"
        headers = {**DEFAULT_HEADERS, "Authorization": f"Bearer {self.token}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # Logique de ton template YAML pour extraire le statut
                    statuses = data.get("resource", {}).get("statuses", [])
                    for s in statuses:
                        if s.get("name") == "status":
                            return s.get("value")
                return "unknown"
