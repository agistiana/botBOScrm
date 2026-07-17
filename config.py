# config.py
import os

BASE_URL = "https://www.bosampuh.id/app"

USER_EMAIL = "septiantaufik53@gmail.com"
USER_PASSWORD = "AL_Basyaro122"

HEADLESS = False

# === KONFIGURASI FILTER TANGGAL (format DD/MM/YYYY) ===
TANGGAL_AWAL = "31/05/2026"
TANGGAL_AKHIR = "17/07/2026"
FILTER_STATUS = []

# === TEMPLATE PESAN WHATSAPP ===
STATUS_MESSAGE_TEMPLATE = {
    "DITERIMA YANG BERSANGKUTAN": "halo kak {nama}, paket dengan resi {resi} sudah diterima oleh yang bersangkutan. Terima kasih sudah berbelanja!",
    "DITERIMA ORANG SERUMAH": "halo kak {nama}, paket dengan resi {resi} sudah diterima oleh orang serumah. Terima kasih sudah berbelanja!",
    "TIDAK DITEMPAT": "halo kak {nama}, pesanan produk {paket} dengan no resi {resi} saat ini terkendala karena penerima tidak ditempat. mohon infokan waktu yang tepat untuk pengantaran ulang.",
    "DITOLAK": "halo kak {nama}, pesanan produk {paket} dengan no resi {resi} ditolak oleh penerima. mohon konfirmasi apakah pesanan tetap dilanjutkan atau dibatalkan?",
    "TIDAK DIKENAL": "halo kak {nama}, pesanan produk {paket} dengan no resi {resi} tidak dapat dikirim karena penerima tidak dikenal. mohon cek kembali data penerima ya kak.",
    "RUMAH/ALAMAT BELUM DIKETEMUKAN": "halo kak {nama}, pesanan produk {paket} dengan no resi {resi} saat ini terkendala RUMAH/ALAMAT TIDAK DITEMUKAN. boleh dikirimkan shareloknya agar mempermudah kurir saat mengantarkan paketnya kak",
    "RUMAH KOSONG": "halo kak {nama}, pesanan produk {paket} dengan no resi {resi} tidak dapat dikirim karena rumah kosong. mohon infokan alamat lain atau jadwal pengantaran ulang.",
}
DEFAULT_MESSAGE = "halo kak {nama}, kami informasikan status terakhir paket Anda dengan resi {resi}: {status}. Mohon konfirmasi."

# === FOLDER ===
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
RESULTS_FOLDER = os.path.join(BASE_DIR, 'results')
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# === DATABASE ===
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'bot_data.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False