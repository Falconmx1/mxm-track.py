# 🔥 Mxm-Track v2.0 - El GitHub OSINT Tool Más Poderoso

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-red)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20Termux-blue)
![Python](https://img.shields.io/badge/python-3.7%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Stars](https://img.shields.io/badge/⭐-Destruye%20a%20Ghos--Track-brightgreen)

**Rastrea, Geolocaliza, Escanea y Genera Reportes - Todo en Una Herramienta**

[Instalación](#-instalación) • [Características](#-características) • [Uso](#-uso-rápido) • [API REST](#-api-rest) • [Ejemplos](#-ejemplos-avanzados)

</div>

---

## 🎯 ¿Qué hace Mxm-Track?

Mxm-Track es la **herramienta OSINT definitiva** para geolocalización, escaneo de puertos, seguimiento de torres celulares y generación de reportes profesionales. **Supera a Ghos-Track en todas las métricas** con características que ningún otro tool tiene.

## ⚡ Características Únicas

| Feature | Mxm-Track | Ghos-Track |
|---------|-----------|------------|
| 🖥️ **API REST** | ✅ Servidor local/remoto | ❌ |
| 🔌 **Shodan Integration** | ✅ Escaneo de puertos real | ❌ |
| 📡 **Cell Towers** | ✅ Simulación torres 4G/5G | ❌ |
| 📊 **Reportes PDF** | ✅ Profesionales | ❌ |
| 🗺️ **Mapas Interactivos** | ✅ OpenStreetMap real | ❌ |
| 🕵️ **Proxies Anónimos** | ✅ +1000 proxies rotativos | ❌ |
| 🧅 **Tor Support** | ✅ Anonimato total | ❌ |
| 📱 **Termux Optimizado** | ✅ Ligero y rápido | ⚠️ |
| 💾 **Múltiples Formatos** | ✅ JSON/CSV/PDF/HTML/TXT | ⚠️ |
| 🌍 **Multiplataforma** | ✅ Linux/Windows/Termux | ⚠️ |

## 📸 Capturas (Pronto)
[Pon aquí capturas de la herramienta en acción]

API REST en funcionamiento

Mapa interactivo generado

Reporte PDF

Escaneo con Shodan


## 🚀 Instalación

### 🐧 Linux / 📱 Termux

```bash
# Clona el repositorio
git clone https://github.com/Falconmx1/Mxm-Track.git
cd Mxm-Track

# Ejecuta el instalador
chmod +x install.sh
./install.sh

# O instala manualmente
pip install -r requirements.txt

🪟 Windows
git clone https://github.com/Falconmx1/Mxm-Track.git
cd Mxm-Track
pip install -r requirements.txt
python mxm-track.py --help

🐍 Dependencias
pip install flask requests reportlab socksipy-branch

🎮 Uso Rápido
# Modo básico (muestra ubicación)
python mxm-track.py -t 8.8.8.8

# Con mapa interactivo
python mxm-track.py -t google.com --map

# Escaneo completo + torres celulares
python mxm-track.py -t 190.12.45.6 --towers --map

# Generar reporte PDF
python mxm-track.py -t cloudflare.com --output reporte.pdf

# Modo anónimo con Tor
python mxm-track.py -t 1.1.1.1 --tor --proxy

🔥 Ejemplos Avanzados
1. Iniciar Servidor API REST
python mxm-track.py --server

# El servidor corre en http://localhost:5000
# Endpoints disponibles:
#   POST /api/track   - Rastrear IPs remotamente
#   GET  /api/shodan/<ip> - Consultar Shodan
#   POST /api/towers  - Buscar torres cercanas

2. Consultar la API desde otro script
import requests

# Rastrear IP
response = requests.post('http://localhost:5000/api/track', 
                        json={'target': '8.8.8.8', 'use_proxy': True})
print(response.json())

# Buscar torres cercanas
towers = requests.post('http://localhost:5000/api/towers',
                       json={'lat': -34.6037, 'lon': -58.3816})
print(towers.json())

3. Escaneo con Shodan
# Necesitas API key de https://shodan.io (plan gratis)
python mxm-track.py -t 45.33.22.11 --shodan TU_API_KEY_AQUI

# Output ejemplo:
# [+] Puertos abiertos encontrados: 22, 80, 443, 3306, 8080

4. Máximo Anonimato (Tor + Proxy Rotativo)
# Primero inicia Tor
sudo systemctl start tor  # Linux
# o en Termux: tor &

# Luego ejecuta Mxm-Track
python mxm-track.py -t objetivo.com --tor --proxy --map --output reporte_secreto.pdf

5. Búsqueda de Torres Celulares
python mxm-track.py -t 190.12.45.6 --towers

# Output:
# [+] Se encontraron 4 torres
#     • Movistar - 4G (a 1.23 km)
#     • Claro - 5G (a 2.45 km)
#     • Personal - 4G (a 3.67 km)
#     • Movistar - 3G (a 4.89 km)

📊 Formatos de Exportación
Formato	Comando	Descripción
JSON	--output datos.json	Datos crudos para programar
PDF	--output reporte.pdf	Reporte profesional con gráficos
HTML	--map (automático)	Mapa interactivo con Leaflet

🛡️ Privacidad y Anonimato
Mxm-Track incluye múltiples capas de protección:

    Proxy Rotativo: Obtiene proxies frescos de ProxyScrape

    Integración Tor: Enruta todo el tráfico a través de la red Tor

    Sin Logs: No guarda ningún registro local a menos que exportes

    IP Oculta: Tu IP real nunca toca los servidores objetivo

# Verifica que tu IP está oculta
python mxm-track.py -t ifconfig.me --tor --proxy
# Debería mostrar una IP diferente a la tuya
