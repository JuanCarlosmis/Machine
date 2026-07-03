#!/usr/bin/env python3
import os

RAIZ = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(RAIZ, 'static')
AUDIOS = os.path.join(STATIC, 'audios')

print(f"📁 Creando estructura de carpetas...")
print(f"   Ruta base: {RAIZ}")

try:
    os.makedirs(AUDIOS, exist_ok=True)
    print(f"✓ Carpeta static: {os.path.exists(STATIC)}")
    print(f"✓ Carpeta audios: {os.path.exists(AUDIOS)}")
    print(f"\n✅ Estructura de carpetas creada exitosamente")
except Exception as e:
    print(f"❌ Error: {e}")
