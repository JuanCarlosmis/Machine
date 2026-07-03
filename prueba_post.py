#!/usr/bin/env python3
"""
Script para simular una evaluación POST al servidor Flask
"""

import requests
import json

print("\n🧪 PRUEBA DE SOLICITUD POST AL SERVIDOR")
print("="*70)

# Datos de prueba
datos = {
    'tiempo_s': '35',
    'desviaciones': '2',
    'errores': '1',
    'id_paciente': '1'
}

url = 'http://localhost:5000/evaluar'

print(f"\n📤 Enviando POST a {url}")
print(f"   Datos: {datos}")

try:
    # Hacer la solicitud POST
    response = requests.post(url, data=datos, timeout=5)
    
    print(f"\n📥 Respuesta recibida:")
    print(f"   Status: {response.status_code}")
    print(f"   Headers: {response.headers}")
    
    # Intentar parsear JSON
    try:
        json_data = response.json()
        print(f"\n✅ JSON recibido:")
        print(json.dumps(json_data, indent=2, ensure_ascii=False))
    except:
        print(f"\n📄 Texto recibido:")
        print(response.text[:500])
        
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: No se pudo conectar al servidor")
    print("   ¿Está el servidor Flask ejecutándose en puerto 5000?")
except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("\n" + "="*70 + "\n")
