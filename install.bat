@echo off
echo Instalando Mxm-Track en Windows
pip install requests
git clone https://github.com/Falconmx1/Mxm-Track.git
cd Mxm-Track
python mxm-track.py --help
pause
