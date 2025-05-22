# Black Metal Transcription Backend

¡Bienvenido al abismo negro! Este repositorio contiene el backend para la herramienta de transcripción del Abismo Negro, que transforma audios en textos malditos usando Whisper. Desplegado en Render, soporta formatos como `.mp3`, `.opus`, `.wav`, y más.

## Archivos
- `app.py` Servidor Flask que maneja la subida y transcripción de audios.
- `Dockerfile` Configura el entorno con `ffmpeg` para soportar múltiples formatos.
- `requirements.txt` Dependencias de Python.
- `render.yaml` Configuración para el despliegue en Render.

## Cómo desplegar
1. Conectá este repositorio a Render como un Web Service.
2. Usá el `Dockerfile` para construir el entorno.
3. Configurá la URL del backend en el frontend (`index.html`).

## Tecnologías
- Flask
- Whisper (OpenAI)
- Render
- ffmpeg