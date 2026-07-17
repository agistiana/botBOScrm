# login.py
import asyncio
from playwright.async_api import Page
from config import USER_EMAIL, USER_PASSWORD, BASE_URL

async def login_bos_ampuh(page: Page):
    """Melakukan login ke platform BOS Ampuh"""
    print("[*] Mengakses halaman login...")
    
    # Buka halaman login (BASE_URL = https://www.bosampuh.id/app)
    await page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
    
    # Tunggu form login muncul
    await page.wait_for_selector("#username_operator", timeout=15000)
    print("[+] Form login ditemukan.")
    
    # Isi email
    await page.locator("#username_operator").fill(USER_EMAIL)
    
    # Isi password
    await page.locator("#userPassword").fill(USER_PASSWORD)
    
    print("[*] Menekan tombol login...")
    
    # Klik tombol login dan tunggu navigasi
    async with page.expect_navigation(wait_until="networkidle", timeout=30000):
        await page.locator("button[type='submit']").click()
    
    # Tunggu sebentar agar session tersimpan
    await page.wait_for_timeout(2000)
    
    # Cek apakah login berhasil
    current_url = page.url
    print(f"[*] URL saat ini: {current_url}")
    
    if "login" in current_url.lower() or "app" in current_url.lower():
        error_element = page.locator(".alert-danger, .error-message, .alert")
        if await error_element.count() > 0:
            error_text = await error_element.first.inner_text()
            raise Exception(f"Login gagal: {error_text.strip()}")
        else:
            raise Exception("Login gagal: kemungkinan username/password salah.")
    
    print("[+] Login berhasil!")
    
    if "follow_up_monitor" not in page.url:
        print("[*] Mengarahkan ke halaman Follow Up Monitor...")
        await page.goto("https://www.bosampuh.id/follow_up_monitor", wait_until="load", timeout=30000)
        await page.wait_for_selector("#edtcari", timeout=15000)
        print("[+] Halaman monitor siap.")
    else:
        print("[+] Sudah berada di halaman monitor.")