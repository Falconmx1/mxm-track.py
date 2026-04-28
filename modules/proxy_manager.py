import requests
import random

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.tor_proxy = None
    
    def get_free_proxies(self):
        """Obtener proxies gratuitos (actualizar periódicamente)"""
        try:
            url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
            resp = requests.get(url, timeout=10)
            proxies = resp.text.strip().split('\r\n')
            return [{'http': f'http://{p}', 'https': f'http://{p}'} for p in proxies[:50]]
        except:
            return []
    
    def get_proxy(self):
        """Obtener un proxy aleatorio"""
        if not self.proxies:
            self.proxies = self.get_free_proxies()
        
        if self.proxies:
            return random.choice(self.proxies)
        return None
    
    def enable_tor(self):
        """Configurar Tor proxy"""
        # Asume que Tor está instalado y corriendo en localhost:9050
        self.tor_proxy = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        print("[+] Tor habilitado. Asegúrate que 'tor' esté corriendo (systemctl start tor)")
    
    def get_proxy(self):
        """Sobrescribir para usar Tor si está habilitado"""
        if self.tor_proxy:
            return self.tor_proxy
        if not self.proxies:
            self.proxies = self.get_free_proxies()
        if self.proxies:
            return random.choice(self.proxies)
        return None
