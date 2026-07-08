import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3
import joblib
import numpy as np
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura'

RAIZ_PROYECTO = os.path.dirname(os.path.abspath(__file__))
RUTA_STATIC = os.path.join(RAIZ_PROYECTO, 'static')
RUTA_AUDIOS = os.path.join(RUTA_STATIC, 'audios')
RUTA_DB = os.path.join(RAIZ_PROYECTO, 'clinica_dislexia.db')

try:
    if not os.path.exists(RUTA_AUDIOS): os.makedirs(RUTA_AUDIOS)
except Exception as e: print("Error creando carpetas:", e)

try:
    modelo = joblib.load(os.path.join(RAIZ_PROYECTO, 'modelo_dislexia_rf.pkl'))
except:
    modelo = None
    print("⚠️  Modelo IA no encontrado. Usando lógica clínica.")

def obtener_conexion():
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory = sqlite3.Row
    conexion.execute('PRAGMA foreign_keys = ON')  # Habilitar foreign keys
    return conexion

@app.route('/')
def home():
    if 'id_docente' in session: return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        conexion = obtener_conexion()
        docente = conexion.execute('SELECT * FROM Usuarios_Docentes WHERE usuario = ? AND contrasena = ?', (request.form['usuario'], request.form['contrasena'])).fetchone()
        conexion.close()
        if docente:
            session['id_docente'], session['nombre_docente'] = docente['id_docente'], docente['nombre_completo']
            return redirect(url_for('dashboard'))
        error = 'Credenciales incorrectas.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'id_docente' not in session: return redirect(url_for('login'))
    conexion = obtener_conexion()
    pacientes = conexion.execute('SELECT * FROM Pacientes WHERE id_docente = ? ORDER BY apellidos', (session['id_docente'],)).fetchall()
    conexion.close()
    return render_template('dashboard.html', nombre_docente=session['nombre_docente'], pacientes=pacientes)

@app.route('/registrar_paciente', methods=['POST'])
def registrar_paciente():
    if 'id_docente' not in session: return redirect(url_for('login'))
    try:
        nombres = request.form['nombres'].strip()
        apellidos = request.form['apellidos'].strip()
        dni = request.form['dni'].strip()
        edad = int(request.form['edad'])
        
        # Validaciones
        if not all([nombres, apellidos, dni, edad]):
            return redirect(url_for('dashboard'))
        if len(dni) != 8 or not dni.isdigit():
            print(" DNI debe tener exactamente 8 dígitos")
            return redirect(url_for('dashboard'))
        if edad < 6 or edad > 8:
            print(" La edad debe estar entre 6 y 8 años")
            return redirect(url_for('dashboard'))
        
        conexion = obtener_conexion()
        cursor = conexion.execute('INSERT INTO Pacientes (nombres, apellidos, dni, edad, id_docente) VALUES (?, ?, ?, ?, ?)',
            (nombres, apellidos, dni, edad, session['id_docente']))
        conexion.commit()
        nuevo_id = cursor.lastrowid
        print(f"✓ Paciente registrado: ID={nuevo_id}, DNI={dni}, Nombres={nombres} {apellidos}, Edad={edad}")
        conexion.close()
    except Exception as e:
        print(f" Error registrando paciente: {e}")
    return redirect(url_for('dashboard'))

@app.route('/editar_paciente/<int:id_paciente>', methods=['GET', 'POST'])
def editar_paciente(id_paciente):
    if 'id_docente' not in session: return redirect(url_for('login'))
    conexion = obtener_conexion()
    paciente = conexion.execute('SELECT * FROM Pacientes WHERE id_paciente = ?', (id_paciente,)).fetchone()
    
    if not paciente or paciente['id_docente'] != session['id_docente']:
        conexion.close()
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            nombres = request.form['nombres'].strip()
            apellidos = request.form['apellidos'].strip()
            dni = request.form['dni'].strip()
            edad = request.form['edad'].strip()
            
            # Validar DNI: exactamente 8 dígitos
            if not dni.isdigit() or len(dni) != 8:
                print(f" Error: DNI debe tener exactamente 8 dígitos numéricos")
                return render_template('editar_paciente.html', paciente=paciente, error="DNI debe tener exactamente 8 dígitos")
            
            edad_int = int(edad)
            if edad_int < 6 or edad_int > 8:
                print(" Error: Edad debe estar entre 6 y 8 años")
                return render_template('editar_paciente.html', paciente=paciente, error="Edad debe estar entre 6 y 8 años")

            if nombres and apellidos and dni and edad:
                conexion.execute('UPDATE Pacientes SET nombres = ?, apellidos = ?, dni = ?, edad = ? WHERE id_paciente = ?',
                    (nombres, apellidos, dni, edad_int, id_paciente))
                conexion.commit()
                print(f"✓ Paciente actualizado: ID={id_paciente}")
        except Exception as e:
            print(f" Error actualizando paciente: {e}")
        conexion.close()
        return redirect(url_for('dashboard'))
    
    conexion.close()
    return render_template('editar_paciente.html', paciente=paciente)

@app.route('/historial/<int:id_paciente>')
def historial(id_paciente):
    if 'id_docente' not in session: return redirect(url_for('login'))
    conexion = obtener_conexion()
    
    # Obtener paciente
    paciente = conexion.execute('SELECT * FROM Pacientes WHERE id_paciente = ?', (id_paciente,)).fetchone()
    
    # Obtener evaluaciones ordenadas por fecha descendente
    evaluaciones = conexion.execute(
        '''SELECT * FROM Historial_Sesiones 
           WHERE id_paciente = ? 
           ORDER BY fecha_evaluacion DESC''', (id_paciente,)).fetchall()
    
    # Calcular reporte
    reporte = {
        'total_evaluaciones': len(list(evaluaciones)),
        'evaluaciones_ultimas': list(evaluaciones)[:5] if evaluaciones else [],
        'riesgo_detectado': False,
        'evaluaciones_con_riesgo': 0
    }
    
    if evaluaciones:
        evaluaciones_list = list(evaluaciones)
        for eval in evaluaciones_list:
            if 'Riesgo' in eval['diagnostico_ia']:
                reporte['evaluaciones_con_riesgo'] += 1
        reporte['riesgo_detectado'] = reporte['evaluaciones_con_riesgo'] >= 2
    
    conexion.close()
    
    print(f"📋 Historial para paciente {id_paciente}:")
    print(f"   Paciente: {paciente['nombres'] if paciente else 'NO ENCONTRADO'}")
    print(f"   Evaluaciones encontradas: {reporte['total_evaluaciones']}")
    
    return render_template('historial.html', paciente=paciente, evaluaciones=reporte['evaluaciones_ultimas'], reporte=reporte)

@app.route('/evaluacion/<int:id_paciente>')
def evaluacion(id_paciente):
    if 'id_docente' not in session: return redirect(url_for('login'))
    return render_template('index.html', id_paciente=id_paciente)

@app.route('/evaluar', methods=['POST'])
def evaluar():
    try:
        # Obtener y validar datos
        tiempo_s = int(request.form.get('tiempo_s', 0))
        desviaciones = int(request.form.get('desviaciones', 0))
        errores = int(request.form.get('errores', 0))
        id_paciente = int(request.form.get('id_paciente', 0))
        audio_file = request.files.get('audio')
        
        print(f"\n EVALUACIÓN RECIBIDA:")
        print(f"   ID Paciente: {id_paciente}")
        print(f"   Tiempo: {tiempo_s}s | Errores: {errores} | Desviaciones: {desviaciones}")
        
        # Validar ID paciente
        if id_paciente <= 0:
            print(" ID de paciente inválido")
            return jsonify({'error': 'ID de paciente inválido', 'diagnostico': 'Error: Paciente no válido', 'codigo': 2}), 400
        
        # Asegurar que la carpeta de audios existe
        try:
            os.makedirs(RUTA_AUDIOS, exist_ok=True)
        except Exception as e:
            print(f"  Error al crear carpeta de audios: {e}")
        
        ruta_audio_db = None
        if audio_file and audio_file.filename:
            try:
                nombre_archivo = f"pac_{id_paciente}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.webm"
                ruta_completa = os.path.join(RUTA_AUDIOS, nombre_archivo)
                audio_file.save(ruta_completa)
                ruta_audio_db = f"/static/audios/{nombre_archivo}"
                print(f"   🎙️  Audio guardado: {nombre_archivo}")
            except Exception as e:
                print(f" Error guardando audio: {e}")
                # Continuar sin audio si hay error        
        # Sistema de diagnóstico con IA o lógica clínica
        resultado = ""
        codigo_ia = 0
        try:
            if modelo:
                carac = np.array([[tiempo_s * 1000, (errores/3)*100]]) 
                prediccion = modelo.predict(carac)[0]
                codigo_ia = int(prediccion)
                resultado = "Riesgo Detectado (IA)" if codigo_ia == 1 else "Típico (IA)"
            else:
                raise Exception("Sin modelo")
        except Exception as e:
            print(f"   ⚠️  IA no disponible: {e}, usando lógica clínica")
            riesgo = (tiempo_s > 40) or (desviaciones > 4) or (errores >= 2)
            codigo_ia = 1 if riesgo else 0
            resultado = "Riesgo Clínico Detectado" if riesgo else "Desarrollo Típico"
        
        print(f"   💡 Diagnóstico: {resultado}")
        
        # Guardar en base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute('''INSERT INTO Historial_Sesiones 
            (id_paciente, tiempo_total_s, fijaciones_oculares_anomalas, errores_comprension, ruta_audio, diagnostico_ia) 
            VALUES (?, ?, ?, ?, ?, ?)''', 
            (id_paciente, tiempo_s, desviaciones, errores, ruta_audio_db, resultado))
        
        conexion.commit()
        nuevo_id = cursor.lastrowid
        
        print(f"   ✅ Registrado en BD con ID sesión: {nuevo_id}")
        conexion.close()
        
        return jsonify({
            'diagnostico': resultado, 
            'codigo': codigo_ia,
            'id_sesion': nuevo_id,
            'mensaje': 'Datos guardados correctamente'
        })
        
    except Exception as e:
        print(f"\n❌ ERROR EN EVALUACIÓN: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e), 
            'diagnostico': 'Error al guardar', 
            'codigo': 2
        }), 500

if __name__ == '__main__':
    # Inicializar BD
    from setup_db import crear_base_datos
    crear_base_datos()
    print("✓ Aplicación iniciada en puerto 5000")
    app.run(debug=True, port=5000)