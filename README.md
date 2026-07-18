========================================
LANGKAH-LANGKAH MENJALANKAN PROGRAM
========================================

PERSYARATAN:
- Python 3.11 atau 3.12 (JANGAN PAKAI PYTHON 3.13)
- Koneksi internet
- Akun BOS Ampuh (email & password)

========================================
1. INSTALL PYTHON 3.11 atau 3.12
========================================
Jika belum punya Python 3.11/3.12, download dari:
https://www.python.org/downloads/release/python-3119/

SAAT INSTALL: CENTANG "Add Python to PATH"

Cek versi Python:
py -0

Pastikan muncul Python 3.11 atau 3.12.

========================================
2. BUKA CMD DI FOLDER PROYEK
========================================
- Buka File Explorer ke folder hasil download dari GitHub
- Klik di address bar, ketik "cmd", tekan Enter

Atau:
- Klik kanan di folder, pilih "Open in Terminal"

========================================
3. BUAT VIRTUAL ENVIRONMENT
========================================
py -3.11 -m venv venv

========================================
4. AKTIFKAN VIRTUAL ENVIRONMENT
========================================
venv\Scripts\activate.bat

Terminal akan berubah menjadi:
(venv) C:\Users\...\botBOScrm-main>

========================================
5. INSTALL DEPENDENCIES
========================================
pip install playwright Flask Flask-SQLAlchemy Flask-Cors pandas openpyxl

========================================
6. INSTALL BROWSER PLAYWRIGHT
========================================
playwright install chromium

========================================
7. BUAT FOLDER YANG DIPERLUKAN
========================================
mkdir uploads
mkdir results
mkdir instance

========================================
8. EDIT FILE config.py
========================================
Buka file config.py, sesuaikan isinya:

USER_EMAIL = "emailanda@gmail.com"     # Ganti dengan email login BOS Ampuh
USER_PASSWORD = "passwordanda"         # Ganti dengan password login BOS Ampuh
HEADLESS = False                       # False = browser muncul, True = tidak muncul

TANGGAL_AWAL = "17/07/2026"            # Sesuaikan dengan tanggal yang diinginkan
TANGGAL_AKHIR = "17/07/2026"           # Sesuaikan dengan tanggal yang diinginkan

========================================
9. JALANKAN APLIKASI
========================================
python app.py

========================================
10. BUKA DI BROWSER
========================================
Buka http://localhost:5000 atau http://127.0.0.1:5000

========================================
11. CARA MENGGUNAKAN APLIKASI
========================================
1. Upload file Excel (daftar resi) di halaman utama
2. Klik tombol "Mulai Bot"
3. Tunggu proses selesai (lihat log yang muncul)
4. Download file hasil dari halaman utama atau History

========================================
RINGKASAN PERINTAH (COPY-PASTE)
========================================

# Buka CMD di folder proyek, lalu jalankan satu per satu:

py -3.11 -m venv venv
venv\Scripts\activate.bat
pip install playwright Flask Flask-SQLAlchemy Flask-Cors pandas openpyxl
playwright install chromium
mkdir uploads results instance
python app.py

========================================
TROUBLESHOOTING
========================================

ERROR: greenlet DLL load failed
SOLUSI: Gunakan Python 3.11 atau 3.12, BUKAN Python 3.13

ERROR: No module named 'flask'
SOLUSI: Pastikan virtual environment aktif (ada (venv) di terminal)
       Lalu install ulang: pip install Flask

ERROR: File not found /uploads
SOLUSI: Buat folder manual: mkdir uploads results instance

ERROR: Browser tidak muncul
SOLUSI: Set HEADLESS = False di config.py

ERROR: ModuleNotFoundError: No module named 'playwright'
SOLUSI: pip install playwright && playwright install chromium

ERROR: Cannot activate venv (PowerShell)
SOLUSI: Gunakan CMD (Command Prompt) bukan PowerShell

========================================
MEMBUAT FILE run.bat (UNTUK JALANKAN OTOMATIS)
========================================
Buat file baru bernama "run.bat" di folder proyek, isi dengan:

@echo off
echo Mengaktifkan virtual environment...
call venv\Scripts\activate.bat
echo Menjalankan aplikasi...
python app.py
pause

Setelah itu, double-click file run.bat untuk menjalankan aplikasi.

========================================
STRUKTUR FOLDER
========================================
botBOScrm-main/
├── app.py
├── config.py
├── login.py
├── followup.py
├── excel.py
├── models.py
├── bot_runner.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   └── history.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── uploads/          (folder untuk file upload)
├── results/          (folder untuk file hasil)
└── instance/         (folder untuk database)

========================================
CATATAN PENTING
========================================
- Gunakan Python 3.11 atau 3.12 (Python 3.13 TIDAK DIDUKUNG)
- Pastikan virtual environment aktif (ada (venv) di terminal)
- Pastikan email dan password di config.py benar
- Browser akan muncul saat HEADLESS = False
- File hasil Excel tersimpan di folder results/
- Database SQLite tersimpan di instance/bot_data.db

========================================
SELESAI
========================================
