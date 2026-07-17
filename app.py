# app.py
from flask import Flask, render_template, request, jsonify, Response, stream_with_context, send_from_directory
from flask_cors import CORS
import os
import json
import queue
import glob
from datetime import datetime
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, SQLALCHEMY_DATABASE_URI, BASE_DIR, RESULTS_FOLDER
from models import db, TrackingResult

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Buat folder yang diperlukan
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'instance'), exist_ok=True)

db.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()

# Import bot_runner setelah app didefinisikan
from bot_runner import BotThread, log_queue, stop_bot

bot_thread = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== ROUTE UTAMA ====================
@app.route('/')
def index():
    # Ambil daftar file hasil dari folder results
    result_files = get_result_files()
    return render_template('index.html', result_files=result_files[:5])  # tampilkan 5 terbaru

# ==================== UPLOAD ====================
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'File tidak dipilih'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'message': 'File berhasil diupload', 'filename': filename, 'filepath': filepath}), 200
    return jsonify({'error': 'Format file tidak diizinkan'}), 400

# ==================== BOT CONTROL ====================
@app.route('/start_bot', methods=['POST'])
def start_bot():
    global bot_thread
    if bot_thread and bot_thread.is_running:
        return jsonify({'error': 'Bot sedang berjalan'}), 400
    
    data = request.get_json()
    filepath = data.get('filepath')
    if not filepath or not os.path.exists(filepath):
        return jsonify({'error': 'File tidak ditemukan'}), 400
    
    while not log_queue.empty():
        log_queue.get()
    
    bot_thread = BotThread(filepath)
    bot_thread.start()
    return jsonify({'message': 'Bot dimulai'}), 200

@app.route('/stop_bot', methods=['POST'])
def stop_bot_route():
    global bot_thread
    if bot_thread and bot_thread.is_running:
        stop_bot()
        return jsonify({'message': 'Bot dihentikan'}), 200
    return jsonify({'error': 'Bot tidak berjalan'}), 400

@app.route('/api/status')
def api_status():
    global bot_thread
    if bot_thread and bot_thread.is_running:
        return jsonify({'status': 'running'})
    return jsonify({'status': 'idle'})

# ==================== LOGS ====================
@app.route('/logs')
def logs():
    def generate():
        while True:
            try:
                msg = log_queue.get(timeout=1)
                yield f"data: {json.dumps({'message': msg})}\n\n"
            except queue.Empty:
                yield f"data: {json.dumps({'message': ''})}\n\n"
            if bot_thread and not bot_thread.is_running and log_queue.empty():
                yield f"data: {json.dumps({'message': '[BOT SELESAI]'})}\n\n"
                break
    return Response(stream_with_context(generate()), mimetype="text/event-stream")

# ==================== FUNGSI BANTU ====================
def get_result_files():
    """Ambil daftar file Excel dari folder results dengan metadata"""
    files = []
    for f in glob.glob(os.path.join(RESULTS_FOLDER, "*.xlsx")):
        stat = os.stat(f)
        files.append({
            'name': os.path.basename(f),
            'path': f,
            'size': stat.st_size,
            'size_kb': round(stat.st_size / 1024, 1),
            'modified_timestamp': stat.st_mtime,
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'date': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d'),
            'month': datetime.fromtimestamp(stat.st_mtime).strftime('%m'),
            'year': datetime.fromtimestamp(stat.st_mtime).strftime('%Y')
        })
    files.sort(key=lambda x: x['modified_timestamp'], reverse=True)
    return files

# ==================== HISTORY (DAFTAR FILE DENGAN FILTER) ====================
@app.route('/history')
def history():
    # Ambil parameter filter
    filter_date = request.args.get('date', '')
    filter_month = request.args.get('month', '')
    filter_year = request.args.get('year', '')
    filter_name = request.args.get('name', '').strip().lower()

    # Ambil semua file
    all_files = get_result_files()

    # Terapkan filter
    filtered_files = all_files
    if filter_date:
        filtered_files = [f for f in filtered_files if f['date'] == filter_date]
    if filter_month:
        filtered_files = [f for f in filtered_files if f['month'] == filter_month.zfill(2)]
    if filter_year:
        filtered_files = [f for f in filtered_files if f['year'] == filter_year]
    if filter_name:
        filtered_files = [f for f in filtered_files if filter_name in f['name'].lower()]

    # Ambil daftar tahun dan bulan yang tersedia untuk dropdown
    years = sorted(set(f['year'] for f in all_files), reverse=True)
    months = list(range(1, 13))

    return render_template(
        'history.html',
        files=filtered_files,
        years=years,
        months=months,
        filter_date=filter_date,
        filter_month=filter_month,
        filter_year=filter_year,
        filter_name=filter_name
    )

# ==================== DOWNLOAD & DELETE FILE ====================
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(RESULTS_FOLDER, filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    filepath = os.path.join(RESULTS_FOLDER, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({'success': True, 'message': f'File {filename} berhasil dihapus'})
    return jsonify({'success': False, 'message': 'File tidak ditemukan'}), 404

# ==================== API ====================
@app.route('/api/result_files')
def api_result_files():
    return jsonify(get_result_files())

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)