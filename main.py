# main.py
import asyncio
from playwright.async_api import async_playwright
import config
from excel import read_resi_list, save_to_excel
from login import login_bos_ampuh
from followup import process_tracking

async def main():
    print("=== BOT FOLLOW UP BOS AMPUH STARTED ===")

    try:
        resi_list = read_resi_list(config.INPUT_EXCEL)
        print(f"[+] Total {len(resi_list)} resi siap diproses.")
    except Exception as e:
        print(f"[-] Gagal membaca file input: {e}")
        return

    async with async_playwright() as p:
        print("[*] Membuka browser...")
        browser = await p.chromium.launch(headless=config.HEADLESS)
        context = await browser.new_context(viewport={'width': 1366, 'height': 768})
        page = await context.new_page()

        try:
            await login_bos_ampuh(page)
            hasil_tracking = await process_tracking(page, resi_list)
            save_to_excel(hasil_tracking, config.OUTPUT_EXCEL)

        except Exception as e:
            print(f"\n[-] Terjadi kesalahan fatal: {e}")
            await page.screenshot(path="error_screenshot.png")
            print("[*] Screenshot error disimpan sebagai error_screenshot.png")
        finally:
            print("[*] Menutup browser. Selesai.")
            await context.close()
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())