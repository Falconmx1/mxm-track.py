import requests
import socket

def get_ip_info(target):
    # Si es dominio, resolver IP
    try:
        ip = socket.gethostbyname(target)
    except:
        return None

    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,lat,lon,isp,org,as,query", timeout=10)
        data = resp.json()
        if data.get('status') == 'success':
            return {
                'ip': data['query'],
                'pais': data['country'],
                'region': data['regionName'],
                'ciudad': data['city'],
                'lat': data['lat'],
                'lon': data['lon'],
                'isp': data['isp'],
                'org': data['org'],
                'as': data['as']
            }
        else:
            return None
    except:
        return None
