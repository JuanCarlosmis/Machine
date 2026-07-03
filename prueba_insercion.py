#!/usr/bin/env python3
"""
Script para hacer una prueba de inserción en la base de datos
"""

import sqlite3
import os
from datetime import datetime

RUTA_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clinica_dislexia.db')

print("\n🧪 PRUEBA DE INSERCIÓN - TAMIZAJE DE DISLEXIA")
print("="*70)

try:
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    
    # Habilitar foreign keys
    cursor.execute('PRAGMA foreign_keys = ON')
    
    print("\n✓ Conexión a base de datos establecida")
    
    # Insertar una evaluación de prueba
    print("\n📝 Insertando evaluación de prueba...")
    
    cursor.execute('''INSERT INTO Historial_Sesiones 
        (id_paciente, tiempo_total_s, fijaciones_oculares_anomalas, errores_comprension, ruta_audio, diagnostico_ia) 
        VALUES (?, ?, ?, ?, ?, ?)''', 
        (1, 45, 3, 1, '/static/audios/prueba.webm', 'Riesgo Clínico Detectado'))
    
    conexion.commit()
    nuevo_id = cursor.lastrowid
    
    print(f"✅ Evaluación insertada con ID: {nuevo_id}")
    
    # Verificar que se insertó
    print("\n🔍 Verificando inserción...")
    cursor.execute("""
        SELECT id_sesion, id_paciente, fecha_evaluacion, tiempo_total_s, 
               errores_comprension, diagnostico_ia
        FROM Historial_Sesiones 
        WHERE id_sesion = ?
    """, (nuevo_id,))
    
    resultado = cursor.fetchone()
    if resultado:
        print(f"✅ Registro encontrado:")
        print(f"   ID Sesión: {resultado[0]}")
        print(f"   ID Paciente: {resultado[1]}")
        print(f"   Fecha: {resultado[2]}")
        print(f"   Tiempo: {resultado[3]}s")
        print(f"   Errores: {resultado[4]}")
        print(f"   Diagnóstico: {resultado[5]}")
    else:
        print("❌ Registro NO encontrado después de insertar")
    
    conexion.close()
    print("\n✅ Prueba completada exitosamente")
    
except Exception as e:
    print(f"\n❌ Error durante la prueba: {e}")
    import traceback
    traceback.print_exc()

print("="*70 + "\n")
