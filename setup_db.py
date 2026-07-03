import sqlite3
import os

def crear_base_datos():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clinica_dislexia.db')
    
    # Si la BD existe y está corrupta, hacer backup y recrear
    if os.path.exists(db_path):
        try:
            conexion_test = sqlite3.connect(db_path)
            conexion_test.execute("SELECT 1 FROM Historial_Sesiones LIMIT 1")
            conexion_test.close()
        except:
            print("⚠️  BD corrupta detectada. Haciendo backup...")
            os.rename(db_path, db_path + '.backup')
    
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()
    
    # Habilitar foreign keys
    cursor.execute('PRAGMA foreign_keys = ON')

    # Crear tabla de docentes
    cursor.execute('''CREATE TABLE IF NOT EXISTS Usuarios_Docentes (
        id_docente INTEGER PRIMARY KEY AUTOINCREMENT, 
        nombre_completo TEXT NOT NULL, 
        usuario TEXT UNIQUE NOT NULL, 
        contrasena TEXT NOT NULL)''')

    # Crear tabla de pacientes
    cursor.execute('''CREATE TABLE IF NOT EXISTS Pacientes (
        id_paciente INTEGER PRIMARY KEY AUTOINCREMENT, 
        nombres TEXT NOT NULL, 
        apellidos TEXT NOT NULL, 
        dni TEXT UNIQUE NOT NULL,
        edad INTEGER NOT NULL,
        id_docente INTEGER NOT NULL,
        fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_docente) REFERENCES Usuarios_Docentes (id_docente))''')

    # Crear tabla de historial con todas las columnas necesarias
    cursor.execute('''CREATE TABLE IF NOT EXISTS Historial_Sesiones (
        id_sesion INTEGER PRIMARY KEY AUTOINCREMENT, 
        id_paciente INTEGER NOT NULL, 
        fecha_evaluacion DATETIME DEFAULT CURRENT_TIMESTAMP,
        tiempo_total_s INTEGER, 
        fijaciones_oculares_anomalas INTEGER, 
        errores_comprension INTEGER, 
        ruta_audio TEXT, 
        diagnostico_ia TEXT,
        FOREIGN KEY (id_paciente) REFERENCES Pacientes (id_paciente) ON DELETE CASCADE)''')

    # Crear índices para mejor rendimiento
    cursor.execute('''CREATE INDEX IF NOT EXISTS idx_historial_paciente 
                     ON Historial_Sesiones(id_paciente)''')
    cursor.execute('''CREATE INDEX IF NOT EXISTS idx_historial_fecha 
                     ON Historial_Sesiones(fecha_evaluacion DESC)''')
    cursor.execute('''CREATE INDEX IF NOT EXISTS idx_pacientes_docente 
                     ON Pacientes(id_docente)''')

    # Insertar docente de prueba
    cursor.execute('''INSERT OR IGNORE INTO Usuarios_Docentes 
                     (id_docente, nombre_completo, usuario, contrasena) 
                     VALUES (1, 'Docente Prueba', 'admin', '12345')''')

    conexion.commit()
    
    # Verificar que las tablas están correctas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = cursor.fetchall()
    
    if tablas:
        print("✓ Base de datos creada exitosamente")
        print(f"✓ Tablas: {[t[0] for t in tablas]}")
    
    conexion.close()

if __name__ == '__main__':
    crear_base_datos()