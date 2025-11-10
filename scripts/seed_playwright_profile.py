# scripts/seed_playwright_profile.py
from playwright.sync_api import sync_playwright
from time import sleep
import os

USER_DATA_DIR = r"C:\ChromeProfiles\mycase_pw"
os.makedirs(USER_DATA_DIR, exist_ok=True)

with sync_playwright() as p:
    print(f"📁 Creando nuevo perfil persistente en: {USER_DATA_DIR}")

    context = p.chromium.launch_persistent_context(
        USER_DATA_DIR,
        headless=False,
        channel="chrome",
        args=[
            "--start-maximized",
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--password-store=basic",      # 🔑 asegura guardado local de credenciales
            "--use-mock-keychain",         # 🧱 evita cifrado dependiente del usuario de Windows
        ],
    )

    page = context.new_page()
    page.goto("https://auth.mycase.com/login_sessions/new?login_required=true")

    print("➡️  Se abrió el navegador.")
    print("👉  Inicia sesión en MyCase, completa el 2FA y marca 'Recordar este dispositivo'.")
    input("🟢 Cuando veas el dashboard y hayas terminado, pulsa ENTER aquí para cerrar el script.\n")

    print("💾 Guardando estado de sesión...")
    sleep(5)  # deja tiempo para escribir cookies

    try:
        context.close()
        print("✅ Contexto cerrado correctamente. Tu sesión ha sido guardada.")
    except Exception:
        print("ℹ️ El navegador ya se había cerrado manualmente. No hay problema.")
