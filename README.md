🎯 Cómo usar las nuevas features
# 1. Modo servidor API REST
python mxm-track.py --server

# 2. Escaneo con Shodan (necesitas API key gratis en shodan.io)
python mxm-track.py -t 8.8.8.8 --shodan TU_API_KEY

# 3. Buscar torres celulares
python mxm-track.py -t 190.12.45.6 --towers

# 4. Generar reporte PDF
python mxm-track.py -t google.com --output reporte.pdf

# 5. Modo anónimo con Tor
python mxm-track.py -t 1.1.1.1 --tor --proxy

# 6. Todo junto (máximo poder)
python mxm-track.py -t objetivo.com --shodan API_KEY --towers --map --output full_report.pdf --tor
