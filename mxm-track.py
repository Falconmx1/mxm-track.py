#!/usr/bin/env python3
# Mxm-Track v2.0 - Modo Dios Activado
# Características: API REST, Shodan, torres celulares, PDF, proxies, Tor

import os
import sys
import json
import platform
import argparse
import threading
import webbrowser
from flask import Flask, request, jsonify
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import requests
import socket
import subprocess
import tempfile
from datetime import datetime

# Importar módulos personalizados
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from modules.shodan_integration import check_shodan
from modules.cell_towers import get_cell_towers
from modules.proxy_manager import ProxyManager

app = Flask(__name__)
proxy_manager = ProxyManager()

def clear_screen():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def banner():
    banner_text = """
    ╔═══════════════════════════════════════════════════════════╗
    ║   ███╗   ███╗██╗  ██╗███╗   ███╗     ████████╗██████╗     ║
    ║   ████╗ ████║╚██╗██╔╝████╗ ████║     ╚══██╔══╝██╔══██╗    ║
    ║   ██╔████╔██║ ╚███╔╝ ██╔████╔██║        ██║   ██████╔╝    ║
    ║   ██║╚██╔╝██║ ██╔██╗ ██║╚██╔╝██║        ██║   ██╔══██╗    ║
    ║   ██║ ╚═╝ ██║██╔╝ ██╗██║ ╚═╝ ██║        ██║   ██║  ██║    ║
    ║   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝        ╚═╝   ╚═╝  ╚═╝    ║
    ║     Mxm-Track v2.0 - Modo Servidor + Shodan + Torres       ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner_text)

def get_ip_info(target, use_proxy=False):
    """Obtener información de IP con soporte para proxy"""
    try:
        ip = socket.gethostbyname(target)
    except:
        return None
    
    proxies = proxy_manager.get_proxy() if use_proxy else None
    
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}", 
                          proxies=proxies, timeout=15)
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
                'as': data['as'],
                'timestamp': datetime.now().isoformat()
            }
        return None
    except:
        return None

def generate_pdf_report(info, shodan_data, towers_data, filename="reporte_mxm.pdf"):
    """Generar reporte PDF profesional"""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Título
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "Mxm-Track Report")
    
    # Fecha
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Información IP
    y = height - 120
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Información del Target")
    y -= 30
    
    c.setFont("Helvetica", 12)
    for key, value in info.items():
        c.drawString(50, y, f"{key.upper()}: {value}")
        y -= 20
    
    # Datos Shodan
    if shodan_data:
        y -= 20
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "Puertos Abiertos (Shodan)")
        y -= 30
        c.setFont("Helvetica", 10)
        for port in shodan_data[:10]:  # Top 10 puertos
            c.drawString(50, y, f"• Puerto {port}")
            y -= 15
    
    # Torres celulares
    if towers_data:
        y -= 20
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "Torres Celulares Cercanas")
        y -= 30
        c.setFont("Helvetica", 10)
        for tower in towers_data[:5]:
            c.drawString(50, y, f"• {tower}")
            y -= 15
    
    c.save()
    return filename

def create_map_html(lat, lon, ip):
    """Crear mapa HTML con OpenStreetMap"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mxm-Track - Mapa de {ip}</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
        <style>
            #map {{ height: 100vh; }}
            body {{ margin: 0; padding: 0; }}
            .info {{
                position: absolute;
                top: 10px;
                right: 10px;
                background: white;
                padding: 10px;
                border-radius: 5px;
                z-index: 1000;
                font-family: Arial;
                box-shadow: 0 0 10px rgba(0,0,0,0.5);
            }}
        </style>
    </head>
    <body>
        <div class="info">
            <strong>Mxm-Track</strong><br>
            IP: {ip}<br>
            Lat: {lat}<br>
            Lon: {lon}
        </div>
        <div id="map"></div>
        <script>
            var map = L.map('map').setView([{lat}, {lon}], 13);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '© OpenStreetMap'
            }}).addTo(map);
            L.marker([{lat}, {lon}]).addTo(map)
                .bindPopup('Target: {ip}')
                .openPopup();
        </script>
    </body>
    </html>
    """
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False)
    temp_file.write(html_content)
    temp_file.close()
    return temp_file.name

# API REST endpoints
@app.route('/api/track', methods=['POST'])
def api_track():
    """Endpoint para rastrear IPs remotamente"""
    data = request.json
    target = data.get('target')
    use_proxy = data.get('use_proxy', False)
    
    if not target:
        return jsonify({'error': 'Target required'}), 400
    
    info = get_ip_info(target, use_proxy)
    if info:
        return jsonify(info)
    return jsonify({'error': 'Could not track target'}), 404

@app.route('/api/shodan/<ip>', methods=['GET'])
def api_shodan(ip):
    """Endpoint para consultar Shodan"""
    shodan_key = request.headers.get('X-Shodan-Key')
    if not shodan_key:
        return jsonify({'error': 'Shodan API key required'}), 401
    
    result = check_shodan(ip, shodan_key)
    return jsonify(result)

@app.route('/api/towers', methods=['POST'])
def api_towers():
    """Endpoint para buscar torres celulares"""
    data = request.json
    lat = data.get('lat')
    lon = data.get('lon')
    
    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude required'}), 400
    
    towers = get_cell_towers(lat, lon)
    return jsonify({'towers': towers})

def start_api_server():
    """Iniciar servidor API REST"""
    print("[+] Iniciando API REST en http://localhost:5000")
    print("[+] Endpoints disponibles:")
    print("    POST /api/track - Rastrear IP")
    print("    GET /api/shodan/<ip> - Consultar Shodan")
    print("    POST /api/towers - Buscar torres")
    app.run(host='0.0.0.0', port=5000, debug=False)

def main():
    parser = argparse.ArgumentParser(description="Mxm-Track v2.0 - Herramienta OSINT Avanzada")
    parser.add_argument("-t", "--target", help="IP o dominio objetivo")
    parser.add_argument("-o", "--output", help="Exportar resultados (json, pdf, html)")
    parser.add_argument("--shodan", help="API key de Shodan para escanear puertos")
    parser.add_argument("--towers", action="store_true", help="Buscar torres celulares cercanas")
    parser.add_argument("--map", action="store_true", help="Generar mapa interactivo")
    parser.add_argument("--proxy", action="store_true", help="Usar proxies anónimos")
    parser.add_argument("--tor", action="store_true", help="Usar Tor (requiere tor instalado)")
    parser.add_argument("--server", action="store_true", help="Iniciar modo servidor API REST")
    parser.add_argument("--silent", action="store_true", help="Modo silencioso")
    
    args = parser.parse_args()
    
    if args.server:
        start_api_server()
        return
    
    if args.tor:
        proxy_manager.enable_tor()
    
    if not args.silent:
        clear_screen()
        banner()
    
    if not args.target:
        target = input("[+] Ingresa IP o dominio: ")
    else:
        target = args.target
    
    print(f"\n[+] Rastreando: {target}")
    
    # Obtener información geográfica
    info = get_ip_info(target, args.proxy or args.tor)
    if not info:
        print("[!] No se pudo obtener información")
        return
    
    print(json.dumps(info, indent=2))
    
    # Consultar Shodan si se proporcionó API key
    shodan_data = None
    if args.shodan:
        print("\n[+] Consultando Shodan...")
        shodan_data = check_shodan(info['ip'], args.shodan)
        if shodan_data:
            print(f"[+] Puertos abiertos encontrados: {', '.join(map(str, shodan_data[:10]))}")
    
    # Buscar torres celulares
    towers_data = None
    if args.towers:
        print("\n[+] Buscando torres celulares cercanas...")
        towers_data = get_cell_towers(info['lat'], info['lon'])
        if towers_data:
            print(f"[+] Se encontraron {len(towers_data)} torres")
            for tower in towers_data[:5]:
                print(f"    • {tower}")
    
    # Generar mapa
    if args.map:
        print("\n[+] Generando mapa interactivo...")
        map_file = create_map_html(info['lat'], info['lon'], info['ip'])
        webbrowser.open(f'file://{map_file}')
        print(f"[+] Mapa guardado en: {map_file}")
    
    # Exportar resultados
    if args.output:
        if args.output.endswith('.pdf'):
            filename = generate_pdf_report(info, shodan_data, towers_data, args.output)
            print(f"[+] Reporte PDF generado: {filename}")
        elif args.output.endswith('.json'):
            with open(args.output, 'w') as f:
                json.dump({'info': info, 'shodan': shodan_data, 'towers': towers_data}, f, indent=2)
            print(f"[+] Datos exportados a {args.output}")
        else:
            print("[!] Formato no soportado. Usa .json o .pdf")

if __name__ == "__main__":
    main()
