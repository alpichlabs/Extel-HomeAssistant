import aiohttp
import asyncio

class ExtelAPI:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.token = None

    async def authenticate(self):
        """Authentification et récupération du token."""
        url = "https://api.extel.com/login" # À remplacer par ta vraie URL
        payload = {"email": self.email, "password": self.password}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    self.token = data.get("token")
                    return True
                return False

    async def get_gates(self):
        """Récupère la liste des portails (ton fameux GET)."""
        if not self.token:
            await self.authenticate()
            
        url = "https://api.extel.com/devices" # À remplacer
        headers = {"Authorization": f"Bearer {self.token}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    devices = await response.json()
                    # On crée un dict { "id_objet": "Nom du portail" }
                    return {d["id"]: d["name"] for d in devices}
                return {}
