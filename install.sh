#!/bin/bash
echo "[+] Instalando Mxm-Track v2.0 - Modo Experto"

# Instalar dependencias
if command -v pkg &> /dev/null; then
    # Termux
    pkg update -y
    pkg install python git tor -y
elif command -v apt &> /dev/null; then
    # Linux
    sudo apt update
    sudo apt install python3 python3-pip git tor -y
fi

# Instalar módulos Python
pip install -r requirements.txt

# Clonar repositorio
git clone https://github.com/tuusuario/Mxm-Track.git
cd Mxm-Track

# Dar permisos
chmod +x mxm-track.py

echo "[✓] Instalación completada"
echo ""
echo "Ejemplos de uso:"
echo "  python mxm-track.py -t 8.8.8.8 --map"
echo "  python mxm-track.py -t google.com --shodan TU_API_KEY --towers"
echo "  python mxm-track.py --server  # Iniciar API REST"
echo "  python mxm-track.py -t 1.1.1.1 --tor --proxy  # Máximo anonimato"
