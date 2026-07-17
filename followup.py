# followup.py
import asyncio
import re
from playwright.async_api import Page
from config import TANGGAL_AWAL, TANGGAL_AKHIR, FILTER_STATUS, STATUS_MESSAGE_TEMPLATE, DEFAULT_MESSAGE

async def set_filter_tanggal(page: Page):
    print("[*] Mengatur filter tanggal dan status...")
    await page.wait_for_selector("#tgl1", timeout=10000)

    await page.evaluate('''(tanggal) => {
        const input = document.querySelector('#tgl1');
        if (input) {
            input.value = tanggal;
            input.dispatchEvent(new Event('change', { bubbles: true }));
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }''', TANGGAL_AWAL)

    await page.evaluate('''(tanggal) => {
        const input = document.querySelector('#tgl2');
        if (input) {
            input.value = tanggal;
            input.dispatchEvent(new Event('change', { bubbles: true }));
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }''', TANGGAL_AKHIR)

    if FILTER_STATUS:
        for status in FILTER_STATUS:
            await page.locator("#status_perjalanan").selectOption(label=status)
        print(f"[+] Status perjalanan difilter: {', '.join(FILTER_STATUS)}")

    await page.locator("#btncari").click()
    await page.wait_for_timeout(2000)
    print("[+] Filter tanggal dan status berhasil diterapkan.")

def generate_wa_message(status, nama, resi, paket):
    status_lower = status.lower()
    for key, template in STATUS_MESSAGE_TEMPLATE.items():
        if key.lower() in status_lower:
            return template.format(nama=nama, resi=resi, paket=paket, status=status)
    return DEFAULT_MESSAGE.format(nama=nama, resi=resi, paket=paket, status=status)

async def process_tracking(page: Page, resi_list: list, log_callback=None, stop_check=None) -> list:
    hasil = []
    await page.wait_for_selector("#edtcari", timeout=30000)
    await set_filter_tanggal(page)

    for idx, resi in enumerate(resi_list, 1):
        # Cek stop jika ada fungsi stop_check
        if stop_check and stop_check():
            print("[!] Proses dihentikan oleh user.")
            if log_callback:
                log_callback("[!] Proses dihentikan oleh user.\n")
            break

        msg = f"[{idx}/{len(resi_list)}] Memproses Resi: {resi} ... "
        print(msg, end="", flush=True)
        if log_callback:
            log_callback(msg)

        try:
            await page.locator("#edtcari").fill("")
            await page.locator("#edtcari").fill(resi)
            await page.locator("#btncari").click()

            await page.wait_for_selector("#tbldata", timeout=5000)
            await page.wait_for_timeout(1500)

            row_count = await page.locator("#data_body tr").count()
            if row_count == 0:
                print("Tidak Ditemukan (tabel kosong)")
                if log_callback:
                    log_callback("Tidak Ditemukan (tabel kosong)\n")
                hasil.append({
                    "Kode Resi": resi, "Status": "Tidak ditemukan", "Status Terakhir": "",
                    "Nama": "", "HP": "", "Paket": "", "Nilai": "", "Pesan WA": ""
                })
                continue

            resi_link = page.locator(f"#data_body a:has-text('{resi}')").first
            if await resi_link.count() == 0:
                resi_link = page.locator(f"#tbldata a:has-text('{resi}')").first
                if await resi_link.count() == 0:
                    print("Tidak Ditemukan (resi tidak ada di tabel)")
                    if log_callback:
                        log_callback("Tidak Ditemukan (resi tidak ada di tabel)\n")
                    hasil.append({
                        "Kode Resi": resi, "Status": "Tidak ditemukan", "Status Terakhir": "",
                        "Nama": "", "HP": "", "Paket": "", "Nilai": "", "Pesan WA": ""
                    })
                    continue

            row = resi_link.locator("xpath=ancestor::tr")

            # Status Terakhir
            status_terakhir = ""
            try:
                status_note = row.locator(".fu-status-note div").first
                if await status_note.count() > 0:
                    status_terakhir = (await status_note.inner_text()).strip()
                else:
                    note_text = await row.locator(".fu-status-note").inner_text()
                    if note_text:
                        status_terakhir = note_text.replace("Status terakhir", "").strip()
            except:
                pass

            # Status badge
            status_badge = row.locator(".fu-badge").first
            status_text = await status_badge.inner_text() if await status_badge.count() > 0 else "Tidak diketahui"
            status_text = status_text.strip()

            # Klik untuk buka modal
            await resi_link.click()
            modal = page.locator(".modal.show")
            await modal.wait_for(state="visible", timeout=5000)
            await page.wait_for_timeout(500)

            # Ekstrak data modal
            paket_raw = ""
            nilai = ""
            try:
                paket_section = modal.locator(".trk-section:has-text('Paket')")
                values = await paket_section.locator(".trk-value").all_inner_texts()
                if len(values) >= 1:
                    paket_raw = values[0].strip().replace("\n", " ")
                    paket_raw = re.split(r'(?i)(?:Beli|Coba)', paket_raw, maxsplit=1)[0].strip()
                if len(values) >= 2:
                    nilai_elem = paket_section.locator("strong")
                    if await nilai_elem.count() > 0:
                        nilai = (await nilai_elem.inner_text()).strip()
            except:
                pass

            nama = ""
            hp = ""
            try:
                penerima_section = modal.locator(".trk-section:has-text('Penerima')")
                penerima_text = await penerima_section.locator(".trk-value").inner_text()
                penerima_lines = [line.strip() for line in penerima_text.split("\n") if line.strip()]
                if len(penerima_lines) >= 1:
                    nama = penerima_lines[0]
                if len(penerima_lines) >= 2:
                    hp = penerima_lines[1]
            except:
                pass

            pesan_wa = generate_wa_message(status_terakhir, nama, resi, paket_raw)

            print("Sukses Diambil")
            if log_callback:
                log_callback("Sukses Diambil\n")
            hasil.append({
                "Kode Resi": resi,
                "Status": status_text,
                "Status Terakhir": status_terakhir,
                "Nama": nama,
                "HP": hp,
                "Paket": paket_raw,
                "Nilai": nilai,
                "Pesan WA": pesan_wa
            })

            # Tutup modal
            close_btn = modal.locator(".btn-close").first
            if await close_btn.count() > 0:
                await close_btn.click()
            else:
                await page.keyboard.press("Escape")
            await modal.wait_for(state="hidden", timeout=3000)

        except Exception as e:
            err_msg = f"Error: {str(e)}"
            print(err_msg)
            if log_callback:
                log_callback(err_msg + "\n")
            hasil.append({
                "Kode Resi": resi, "Status": "Error System/Timeout", "Status Terakhir": "",
                "Nama": "", "HP": "", "Paket": "", "Nilai": "", "Pesan WA": ""
            })
            try:
                await page.keyboard.press("Escape")
            except:
                pass

    return hasil