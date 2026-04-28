import requests
import math

def haversine(lat1, lon1, lat2, lon2):
    """Calcular distancia entre dos coordenadas"""
    R = 6371  # Radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def get_cell_towers(lat, lon, radius_km=10):
    """Buscar torres celulares cercanas (simulado con datos públicos)"""
    # Datos de torres celulares simulados (en realidad se usaría API de OpenCelliD)
    simulated_towers = [
        {"operator": "Movistar", "lat": lat + 0.01, "lon": lon + 0.01, "technology": "4G"},
        {"operator": "Claro", "lat": lat - 0.02, "lon": lon + 0.015, "technology": "5G"},
        {"operator": "Personal", "lat": lat + 0.015, "lon": lon - 0.01, "technology": "4G"},
        {"operator": "Movistar", "lat": lat - 0.01, "lon": lon - 0.02, "technology": "3G"},
        {"operator": "Claro", "lat": lat + 0.025, "lon": lon + 0.02, "technology": "4G"},
    ]
    
    nearby_towers = []
    for tower in simulated_towers:
        distance = haversine(lat, lon, tower['lat'], tower['lon'])
        if distance <= radius_km:
            nearby_towers.append(f"{tower['operator']} - {tower['technology']} (a {distance:.2f} km)")
    
    return nearby_towers
