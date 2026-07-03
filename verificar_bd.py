#!/usr/bin/env python3
"""
Script para verificar y limpiar la base de datos de Tamizaje de Dislexia
Uso: python verificar_bd.py [--limpiar] [--recrear]
"""

import sqlite3
import os
from datetime import datetime

RUTA_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clinica_dislexia.db')

def verificar_bd():
    """Verifica el estado de la base de datos"""
    print("\n" + "="*70)
    print("VERIFICACIÓN DE BASE DE DATOS")
    print("="*70)
    
    if not os.path.exists(RUTA_DB):
        print(f"❌ Base de datos NO existe en: {RUTA_DB}")
        return False
    
    print(f"✓ Base de datos encontrada: {RUTA_DB}")
    print(f"  Tamaño: {os.path.getsize(RUTA_DB)} bytes")
    
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        
        # Verificar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = cursor.fetchall()
        print(f"\n📋 Tablas encontradas: {len(tablas)}")
        for tabla in tablas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla[0]}")
            cantidad = cursor.fetchone()[0]
            print(f"  • {tabla[0]}: {cantidad} registros")
        
        # Verificar docentes
        print("\n👨‍🏫 DOCENTES:")
        cursor.execute("SELECT id_docente, nombre_completo, usuario FROM Usuarios_Docentes")
        docentes = cursor.fetchall()
        if docentes:
            for doc in docentes:
                print(f"  ID={doc[0]}: {doc[1]} (usuario: {doc[2]})")
        else:
            print("  ⚠️  No hay docentes registrados")
        
        # Verificar pacientes
        print("\n👤 PACIENTES:")
        cursor.execute("""
            SELECT id_paciente, nombres, apellidos, edad, grado_escolar 
            FROM Pacientes 
            ORDER BY id_docente, apellidos
        """)
        pacientes = cursor.fetchall()
        if pacientes:
            for pac in pacientes:
                print(f"  ID={pac[0]}: {pac[1]} {pac[2]} (Edad: {pac[3]}, Grado: {pac[4]})")
        else:
            print("  ⚠️  No hay pacientes registrados")
        
        # Verificar evaluaciones
        print("\n📊 EVALUACIONES:")
        cursor.execute("""
            SELECT h.id_sesion, p.nombres, p.apellidos, h.fecha_evaluacion, 
                   h.tiempo_total_s, h.errores_comprension, h.diagnostico_ia
            FROM Historial_Sesiones h
            JOIN Pacientes p ON h.id_paciente = p.id_paciente
            ORDER BY h.fecha_evaluacion DESC
            LIMIT 20
        """)
        evaluaciones = cursor.fetchall()
        if evaluaciones:
            for eval in evaluaciones:
                print(f"  Sesión {eval[0]}: {eval[1]} {eval[2]}")
                print(f"    Fecha: {eval[3]} | Tiempo: {eval[4]}s | Errores: {eval[5]} | Dx: {eval[6]}")
        else:
            print("  ⚠️  No hay evaluaciones registradas")
        
        conexion.close()
        print("\n✅ Base de datos VÁLIDA")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en base de datos: {e}")
        return False

def limpiar_evaluaciones():
    """Elimina todas las evaluaciones pero mantiene docentes y pacientes"""
    print("\n" + "="*70)
    print("LIMPIANDO EVALUACIONES")
    print("="*70)
    
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        
        cursor.execute("DELETE FROM Historial_Sesiones")
        conexion.commit()
        
        print("✅ Todas las evaluaciones han sido eliminadas")
        conexion.close()
        return True
    except Exception as e:
        print(f"❌ Error al limpiar: {e}")
        return False

def recrear_bd():
    """Recrea la base de datos desde cero"""
    print("\n" + "="*70)
    print("RECREANDO BASE DE DATOS")
    print("="*70)
    
    try:
        # Hacer backup
        if os.path.exists(RUTA_DB):
            backup_path = RUTA_DB + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(RUTA_DB, backup_path)
            print(f"✓ Backup guardado: {backup_path}")
        
        # Recrear
        from setup_db import crear_base_datos
        crear_base_datos()
        
        print("✅ Base de datos recreada exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error al recrear: {e}")
        return False

if __name__ == '__main__':
    import sys
    
    print("\n🔍 HERRAMIENTA DE VERIFICACIÓN - TAMIZAJE DE DISLEXIA")
    print("Iniciado:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    if '--recrear' in sys.argv:
        recrear_bd()
    elif '--limpiar' in sys.argv:
        limpiar_evaluaciones()
    else:
        verificar_bd()
    
    print("\n" + "="*70 + "\n")
