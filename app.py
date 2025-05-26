from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import os
import uuid
import threading

app = Flask(__name__)
CORS(app)  # <- Sigue habilitando CORS “automáticamente”, aunque no bastó

# —————— Bloque para inyectar encabezados CORS en TODAS las respuestas ——————
@app.after_request
def add_cors_headers(response):
    """
    Cada vez que Flask devuelva una respuesta, este decorador
    agregará manualmente los headers CORS necesarios:
      - Access-Control-Allow-Origin
      - Access-Control-Allow-Methods
      - Access-Control-Allow-Headers
    de modo que el navegador permita cualquier origen a nuestro backend.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response
# ——————————————————————————————————————————————————————————————————————————

tasks = {}

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No se proporcionó un archivo de audio'}), 400

    audio_file = request.files['audio']
    valid_extensions = ['.mp3', '.wav', '.ogg', '.opus', '.flac', '.m4a']
    if not any(audio_file.filename.lower().endswith(ext) for ext in valid_extensions):
        return jsonify({'error': 'Formato de archivo no soportado'}), 400

    task_id = str(uuid.uuid4())
    temp_path = f"/tmp/{task_id}{os.path.splitext(audio_file.filename)[1]}"
    audio_file.save(temp_path)

    tasks[task_id] = {'status': 'pending'}

    def transcribe():
        try:
            model = whisper.load_model("tiny")
            result = model.transcribe(temp_path, language="Spanish")
            tasks[task_id] = {
                'status': 'completed',
                'transcription': result['text']
            }
            os.remove(temp_path)
        except Exception as e:
            tasks[task_id] = {
                'status': 'failed',
                'error': str(e)
            }
            if os.path.exists(temp_path):
                os.remove(temp_path)

    threading.Thread(target=transcribe).start()
    return jsonify({'taskId': task_id, 'debug': 'esto es código nuevo'}), 202

@app.route('/status/<task_id>', methods=['GET'])
def check_status(task_id):
    task = tasks.get(task_id, {'status': 'not_found', 'error': 'Tarea no encontrada'})
    if task['status'] in ['completed', 'failed']:
        tasks.pop(task_id, None)
    return jsonify(task)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
