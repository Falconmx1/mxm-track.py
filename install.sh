#!/bin/bash
echo "[+] Instalando Mxm-Track en Termux"
pkg update -y && pkg upgrade -y
pkg install python git -y
pip install requests
git clone https://github.com/Falconmx1/Mxm-Track.git
cd Mxm-Track
python mxm-track.py --help
echo "[+] Listo. Ejecuta: python mxm-track.py -t 8.8.8.8"
