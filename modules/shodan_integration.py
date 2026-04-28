import requests

def check_shodan(ip, api_key):
    """Consultar puertos abiertos con Shodan"""
    try:
        url = f"https://api.shodan.io/shodan/host/{ip}?key={api_key}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            ports = list(set([service['port'] for service in data.get('data', [])]))
            return sorted(ports)
        return []
    except:
        return []
