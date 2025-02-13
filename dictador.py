import sounddevice as sd
import queue
import json
import pandas as pd
from vosk import Model, KaldiRecognizer

# Ruta del modelo descargado
model_path = "C:/Vosk/vosk-model-es-0.42"
model = Model(model_path)

# Configurar el micrófono
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# Función para convertir números escritos en palabras a dígitos
def convertir_numeros(texto):
    reemplazos = {"uno": "1", "dos": "2", "tres": "3", "cuatro": "4"}
    for palabra, numero in reemplazos.items():
        texto = texto.replace(palabra, numero)
    return texto

# Iniciar reconocimiento de voz
rec = KaldiRecognizer(model, 16000)

# Estructura para almacenar preguntas y respuestas
preguntas = []
actual_pregunta = ""
opciones = {}
respuesta_correcta = ""

with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                        channels=1, callback=callback):
    print("🎤 Dicta tu pregunta (di 'terminar' para finalizar):")
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            texto = result.get('text', '').lower()
            texto = convertir_numeros(texto)  # Aplicar conversión
            print(f"📢 Reconocido: {texto}")  # Mostrar lo que se reconoce

            if "terminar" in texto:
                print("✅ Dictado finalizado.")
                break

            if "nueva pregunta" in texto:
                if actual_pregunta:
                    # Guardar la pregunta anterior antes de limpiar las variables
                    print(f"✅ Guardando pregunta: {actual_pregunta}")
                    preguntas.append({
                        "Pregunta": actual_pregunta,
                        "Opción 1": opciones.get("1", ""),
                        "Opción 2": opciones.get("2", ""),
                        "Opción 3": opciones.get("3", ""),
                        "Opción 4": opciones.get("4", ""),
                        "Respuesta Correcta": respuesta_correcta
                    })
                
                # Actualizar la nueva pregunta
                actual_pregunta = texto.replace("nueva pregunta", "").strip()
                opciones = {}
                respuesta_correcta = ""
            elif "opción 1" in texto:
                opciones["1"] = texto.replace("opción 1", "").strip()
            elif "opción 2" in texto:
                opciones["2"] = texto.replace("opción 2", "").strip()
            elif "opción 3" in texto:
                opciones["3"] = texto.replace("opción 3", "").strip()
            elif "opción 4" in texto:
                opciones["4"] = texto.replace("opción 4", "").strip()
            elif "respuesta correcta" in texto:
                respuesta_correcta = texto.replace("respuesta correcta", "").strip()

    # Guardar la última pregunta si no fue guardada
    if actual_pregunta:
        print(f"✅ Guardando última pregunta: {actual_pregunta}")
        preguntas.append({
            "Pregunta": actual_pregunta,
            "Opción 1": opciones.get("1", ""),
            "Opción 2": opciones.get("2", ""),
            "Opción 3": opciones.get("3", ""),
            "Opción 4": opciones.get("4", ""),
            "Respuesta Correcta": respuesta_correcta
        })

# Verificar si hay contenido antes de guardar
if preguntas:
    df = pd.DataFrame(preguntas)
    df.to_excel("cuestionario.xlsx", index=False)
    print("📁 Archivo 'cuestionario.xlsx' guardado correctamente.")
else:
    print("⚠️ No se capturaron preguntas, no se generó el archivo Excel.")
