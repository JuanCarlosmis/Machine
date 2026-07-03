#!/usr/bin/env python3
"""
Script de inicialización - Ejecutar ANTES de python app.py
Asegura que BD y carpetas están correctamente configuradas
"""

import os
import sqlite3
from setup_db import crear_base_datos

RAIZ = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(RAIZ, 'static')
AUDIOS = os.path.join(STATIC, 'audios')
DB_PATH = os.path.join(RAIZ, 'clinica_dislexia.db')

print("\n" + "="*70)
print("⚙️  INICIALIZANDO SISTEMA - TAMIZAJE DE DISLEXIA")
print("="*70)

# 1. Crear carpetas
print("\n📁 Creando estructura de carpetas...")
try:
    os.makedirs(AUDIOS, exist_ok=True)
    print(f"  ✓ Carpeta static/audios existe")
except Exception as e:
    print(f"  ❌ Error: {e}")
    exit(1)

# 2. Crear/verificar BD
print("\n💾 Inicializando base de datos...")
try:
    crear_base_datos()
    print(f"  ✓ Base de datos inicializada")
except Exception as e:
    print(f"  ❌ Error: {e}")
    exit(1)

# 3. Verificar tablas
print("\n📊 Verificando tablas...")
try:
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    
    # Tablas esperadas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = [t[0] for t in cursor.fetchall()]
    
    esperadas = ['Usuarios_Docentes', 'Pacientes', 'Historial_Sesiones']
    faltantes = [t for t in esperadas if t not in tablas]
    
    if faltantes:
        print(f"  ❌ Tablas faltantes: {faltantes}")
        exit(1)
    
    print(f"  ✓ Todas las tablas existen")
    
    # Verificar docente de prueba
    cursor.execute("SELECT COUNT(*) FROM Usuarios_Docentes")
    docentes = cursor.fetchone()[0]
    print(f"  ✓ Docentes: {docentes}")
    
    conexion.close()
except Exception as e:
    print(f"  ❌ Error: {e}")
    exit(1)

print("\n" + "="*70)
print("✅ SISTEMA LISTO - Ejecuta: python app.py")
print("="*70 + "\n")
