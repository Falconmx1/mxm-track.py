#!/usr/bin/env python3
# Mxm-Track - Supera a Ghos-Track
# Autor: TuNombre
# GitHub: tuusuario/Mxm-Track

import os
import sys
import json
import platform
import argparse
import subprocess
from modules.geoipy import get_ip_info
from modules.mapper import ascii_map
from modules.export import export_results

def clear_screen():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def banner():
    banner_text = """
    ╔═══════════════════════════════════════╗
    ║   ███╗   ███╗██╗  ██╗███╗   ███╗     ║
    ║   ████╗ ████║╚██╗██╔╝████╗ ████║     ║
    ║   ██╔████╔██║ ╚███╔╝ ██╔████╔██║     ║
    ║   ██║╚██╔╝██║ ██╔██╗ ██║╚██╔╝██║     ║
    ║   ██║ ╚═╝ ██║██╔╝ ██╗██║ ╚═╝ ██║     ║
    ║   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ║
    ║        Mxm-Track v1.0 - Más potente   ║
    ╚═══════════════════════════════════════╝
    """
    print(banner_text)

def main():
    parser = argparse.ArgumentParser(description="Mxm-Track: Herramienta OSINT de geolocalización")
    parser.add_argument("-t", "--target", help="IP o dominio objetivo")
    parser.add_argument("-o", "--output", help="Exportar resultados (json, csv, html, txt)")
    parser.add_argument("--map", action="store_true", help="Mostrar mapa ASCII")
    parser.add_argument("--silent", action="store_true", help="Modo silencioso (solo datos)")
    args = parser.parse_args()

    if not args.silent:
        clear_screen()
        banner()

    if not args.target:
        target = input("[+] Ingresa IP o dominio: ")
    else:
        target = args.target

    print(f"\n[+] Rastreando: {target}")
    info = get_ip_info(target)

    if info:
        print(json.dumps(info, indent=4))
        if args.map:
            ascii_map(info.get('lat', 0), info.get('lon', 0))
        if args.output:
            export_results(info, args.output)
    else:
        print("[!] No se pudo obtener información.")

if __name__ == "__main__":
    main()
