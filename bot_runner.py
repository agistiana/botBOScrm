# bot_runner.py
import asyncio
import threading
import queue
import os
from playwright.async_api import async_playwright
from config import HEADLESS, RESULTS_FOLDER
from excel import read_resi_list, save_to_excel
from login import login_bos_ampuh
from followup import process_tracking
from models import db, TrackingResult

log_queue = queue.Queue()
stop_flag = False

def send_log(message):
    log_queue.put(message)

def stop_bot():
    global stop_flag
    stop_flag = True
    send_log("[!] Bot dihentikan oleh user.")

class BotThread(threading.Thread):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.is_running = True
        self._stop = False
        
    def stop(self):
        self._stop = True
        global stop_flag
        stop_flag = True
        
    def run(self):
        from app import app
        with app.app_context():
            asyncio.run(self.run_bot())
    
    async def run_bot(self):
        global stop_flag
        stop_flag = False
        send_log("=== BOT FOLLOW UP BOS AMPUH STARTED ===")
        hasil_tracking = []
        output_file = None
        
        try:
            resi_list = read_resi_list(self.file_path)
            send_log(f"[+] Total {len(resi_list)} resi siap diproses.")
            
            async with async_playwright() as p:
                send_log("[*] Membuka browser...")
                browser = await p.chromium.launch(headless=HEADLESS)
                context = await browser.new_context(viewport={'width': 1366, 'height': 768})
                page = await context.new_page()
                
                try:
                    await login_bos_ampuh(page)
                    
                    # Proses tracking
                    hasil_tracking = await process_tracking(
                        page, 
                        resi_list, 
                        log_callback=send_log,
                        stop_check=lambda: stop_flag or self._stop
                    )
                    
                    if not hasil_tracking:
                        send_log("[!] Tidak ada data yang diambil.")
                        return
                    
                    # === SIMPAN KE DATABASE ===
                    try:
                        for data in hasil_tracking:
                            result = TrackingResult(
                                kode_resi=data['Kode Resi'],
                                status=data['Status'],
                                status_terakhir=data['Status Terakhir'],
                                nama=data['Nama'],
                                hp=data['HP'],
                                paket=data['Paket'],
                                nilai=data['Nilai'],
                                pesan_wa=data['Pesan WA']
                            )
                            db.session.add(result)
                        db.session.commit()
                        send_log(f"[+] {len(hasil_tracking)} data berhasil disimpan ke database.")
                    except Exception as db_err:
                        send_log(f"[-] Error database: {str(db_err)}")
                        db.session.rollback()
                    
                    # === SIMPAN KE EXCEL ===
                    try:
                        output_file = save_to_excel(hasil_tracking)
                        if output_file:
                            send_log(f"[+] File hasil: {os.path.basename(output_file)}")
                            # Refresh daftar file di dashboard
                            send_log("REFRESH_FILES")
                        else:
                            send_log("[-] Gagal menyimpan file Excel.")
                    except Exception as excel_err:
                        send_log(f"[-] Error Excel: {str(excel_err)}")
                    
                except Exception as e:
                    send_log(f"[-] Error: {str(e)}")
                finally:
                    await context.close()
                    await browser.close()
                    send_log("[*] Bot selesai.")
                    
        except Exception as e:
            send_log(f"[-] Fatal error: {str(e)}")
        finally:
            self.is_running = False
            stop_flag = False
            # Jika hasil_tracking ada tapi file tidak tersimpan, coba simpan lagi di akhir
            if hasil_tracking and not output_file:
                try:
                    send_log("[*] Mencoba menyimpan file Excel lagi...")
                    output_file = save_to_excel(hasil_tracking)
                    if output_file:
                        send_log(f"[+] File hasil: {os.path.basename(output_file)}")
                        send_log("REFRESH_FILES")
                except Exception as e:
                    send_log(f"[-] Gagal menyimpan file Excel: {str(e)}")