# VOSK-Excel-MockExamGenerator
✅ 1. Requisitos Previos
- Asegúrate de tener Python instalado. Puedes verificarlo con:
```sh
python --version
```
Si no lo tienes, descarga e instala desde python.org.

## ⚙️ 2. Instalación de VOSK
- Abre la terminal de comandos (CMD) como administrador.
- Ejecuta este comando para instalar VOSK y sus dependencias:
```sh
pip install vosk
pip install sounddevice
pip install pandas openpyxl
```
## 📥 3. Descarga del Modelo de Español
VOSK necesita un modelo de lenguaje para funcionar. Descarga uno desde VOSK Models:
- Busca “vosk-model-small-es-0.42” (modelo en español, ligero).
- Extrae la carpeta en una ubicación fácil, por ejemplo: C:/Vosk/vosk-model-small-es-0.42

## ▶️ 4. Ejecutar el Programa
- Guarda el archivo.
- Abre la terminal, navega a la carpeta donde guardaste dictador.py, y ejecuta:
```sh
python dictador.py
```
## 🔹 Ejemplo de dictado:

"Nueva pregunta ¿Cuál es la capital de Perú?"
- "Opción uno: Lima" → Se registrará como Opción 1: Lima
- "Opción dos: Cusco" → Se registrará como Opción 2: Cusco
- "Respuesta correcta: uno" → Se guardará como 1
- Cuando termines, di "terminar" y el archivo Excel estará listo. 🚀
