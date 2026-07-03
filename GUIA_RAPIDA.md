# 🧪 GUÍA RÁPIDA DE PRUEBA

## ¿Qué se corrigió?

Tu aplicación tenía un problema donde **los datos se grababan pero no se mostraban en el historial**. Esto se debía a varios puntos débiles en el flujo de guardado de datos.

### Problemas Identificados y Corregidos:

1. **Falta de validación de datos** - El sistema no verificaba si los datos recibidos eran válidos
2. **Sin logging detallado** - Era imposible ver dónde fallaba el guardado
3. **Conversión de tipos insegura** - El id_paciente podía no convertirse correctamente
4. **Falta de manejo de errores** - Los errores de BD no se reportaban adecuadamente
5. **Nombres de archivo duplicados** - Los audios podían sobrescribirse

---

## 🚀 Cómo Probar (Pasos Rápidos)

### Paso 1: Verificar que todo está listo
```bash
cd "C:\Users\ROG ZEPHYRUS\Desktop\Tamizaje_Dislexia"
python verificar_bd.py
```

**Deberías ver algo como:**
```
✓ Base de datos encontrada
📋 Tablas encontradas: 4
👨‍🏫 DOCENTES: 1 registros
👤 PACIENTES: 1 registros (ca adas)
📊 EVALUACIONES: 0 registros
✅ Base de datos VÁLIDA
```

### Paso 2: Iniciar la aplicación
```bash
python app.py
```

**Deberías ver:**
```
✓ Aplicación iniciada en puerto 5000
 * Running on http://127.0.0.1:5000
```

### Paso 3: Acceder a la aplicación
- Abre en tu navegador: **http://localhost:5000**
- Usuario: **admin**
- Contraseña: **12345**

### Paso 4: Realizar una evaluación
1. Click en "▶ Iniciar Tamizaje" del paciente "ca adas"
2. Completa la prueba de lectura y preguntas
3. Espera a que muestre el resultado
4. Regresa al panel

### Paso 5: Verificar en el historial
1. Click en "📄 Ver Resultados" del paciente
2. **¡AHORA DEBERÍAS VER LA EVALUACIÓN REGISTRADA!**
3. Verás: Fecha, Tiempo Total, Errores, Desviaciones, Audio, Diagnóstico

---

## 📋 Si Algo Falla

### Problema: No aparece nada en el historial
```bash
# 1. Verifica la BD
python verificar_bd.py

# 2. Si dice "0 registros" en EVALUACIONES después de hacer la prueba,
#    el servidor NO está guardando. Revisa la consola del servidor.

# 3. Si ves mensajes de error en la consola, copialos y revisa
```

### Problema: Error al iniciar server
```bash
# El puerto 5000 podría estar en uso. Edita app.py:
# Última línea: app.run(debug=True, port=5001)  # Cambia a otro puerto
```

### Problema: Los audios no se guardan
```bash
# Crea la carpeta si no existe
mkdir static/audios

# Verifica permisos de escritura
```

---

## 🔍 Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| **setup_db.py** | ✓ Mejor manejo de BD, índices, validación |
| **app.py** | ✓ Logging detallado, validación de datos, manejo de errores |
| **templates/index.html** | ✓ Validación en cliente, mejor conversión de tipos |

## 📁 Nuevos Archivos

- **verificar_bd.py** - Para revisar estado de la BD
- **prueba_insercion.py** - Para probar inserciones directas
- **prueba_post.py** - Para simular POST al servidor
- **MEJORAS.md** - Documento completo de cambios

---

## ✅ Checklist Final

- [ ] Ejecutar `python verificar_bd.py` - BD debe estar VÁLIDA
- [ ] Ejecutar `python app.py` - Servidor debe iniciarse sin errores
- [ ] Acceder a http://localhost:5000 - Page debe cargar
- [ ] Login con admin/12345 - Debe funcionar
- [ ] Hacer una evaluación - Debe completarse
- [ ] Ver historial - DEBE mostrar la evaluación guardada
- [ ] Verificar que aparece: fecha, tiempo, errores, desviaciones, diagnóstico

---

## 💡 Nota Importante

El sistema ahora incluye **logging detallado**. Cuando realices una evaluación, verás en la consola del servidor algo como:

```
📊 EVALUACIÓN RECIBIDA:
   ID Paciente: 1
   Tiempo: 35s | Errores: 1 | Desviaciones: 2
   🎙️  Audio guardado: pac_1_20260616_201500.webm
   ✅ Registrado en BD con ID sesión: 1
```

Esto te ayuda a ver exactamente qué está pasando.

---

**¿Tienes dudas?** Revisa los logs en la consola del servidor - ahora son muy descriptivos.

**¿Sigue sin funcionar?** Ejecuta:
```bash
python verificar_bd.py --recrear
```

Esto recreará la BD desde cero.
