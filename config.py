# config.py

BASE_URL = "https://www.bosampuh.id/app"

USER_EMAIL = "septiantaufik53@gmail.com"
USER_PASSWORD = "AL_Basyaro122"

INPUT_EXCEL = "file resi.xlsx"
OUTPUT_EXCEL = "hasil_followup.xlsx"

HEADLESS = False

# === KONFIGURASI FILTER TANGGAL (format DD/MM/YYYY) ===
TANGGAL_AWAL = "31/05/2026"
TANGGAL_AKHIR = "17/07/2026"
FILTER_STATUS = []   # Contoh: ["Gagal Antar"] atau []

# === TEMPLATE PESAN WHATSAPP ===
# Gunakan placeholder {nama}, {resi}, {paket}, {status}
STATUS_MESSAGE_TEMPLATE = {
    "DITERIMA YANG BERSANGKUTAN": "halo kak {nama}, pesanan produk {paket} dengan resi paket {resi} sudah diterima oleh yang bersangkutan. Terima kasih",
    "DITERIMA ORANG SERUMAH": "halo kak {nama}, pesanan produk {paket} dengan resi paket {resi} sudah diterima oleh orang serumah. Terima kasih",
    "TIDAK DITEMPAT": "halo kak {nama}, pesanan produk {paket} dengan no resi {resi} saat ini terkendala YANG BERSANGKUTAN TIDAK DITEMPAT. kalo boleh tau kapan kakak ada dirumah dan bisa menerima paketnya kak?",
    "DITOLAK": "halo kak {nama}, pesanan produk {paket} dengan no resi {resi} saat ini terkendala KIRIMAN DITOLAK YANG BERSANGKUTAN. kalo boleh tau alasannya kenapa ya kak?",
    "TIDAK DIKENAL": "halo kak {nama}, pesanan produk {paket} dengan no resi {resi} saat ini terkendala YANG BERSANGKUTAN TIDAK DIKENAL. apakah ada alternatif nama lain yang mudah dikenali oleh tetangga kak? itu diperlukan agar mempermudah kurir saat mengantar paketnya",
    "RUMAH/ALAMAT BELUM DIKETEMUKAN": "halo kak {nama}, pesanan produk {paket} dengan no resi {resi} saat ini terkendala RUMAH/ALAMAT TIDAK DITEMUKAN. boleh dikirimkan shareloknya agar mempermudah kurir saat mengantarkan paketnya kak",
    "RUMAH KOSONG": "halo kak {nama}, pesanan produk {paket} dengan no resi {resi} tidak dapat dikirim karena rumah kosong. mohon infokan alamat lain atau jadwal pengantaran ulang.",
}

# Template default jika tidak ada yang cocok
DEFAULT_MESSAGE = "halo kak {nama}, kami informasikan status terakhir paket Anda dengan resi {resi}: {status}. saat ini sedang dikirim ulang. kalo boleh tau kapan kakak ada dirumah dan bisa menerima paketnya kak?"