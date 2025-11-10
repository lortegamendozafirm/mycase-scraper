# ============================================
# data_layer/playwright_driver.py
# ============================================
import os
from playwright.sync_api import sync_playwright
from pathlib import Path
from utils.logger import get_logger
from config.settings import (
    PW_USER_DATA_DIR,
    PW_HEADLESS,
    PW_TIMEOUT_MS,
    PW_BLOCK_RESOURCES,
)

logger = get_logger(__name__)
# 📁 Carpeta persistente para mantener cookies y sesión activa
USER_DATA_DIR = Path(os.getenv("PW_USER_DATA_DIR", r"C:\ChromeProfiles\mycase_pw"))
USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

# 🧠 Configuración global
HEADLESS = os.getenv("PW_HEADLESS", "true").lower() == "true"   # Cambia a False si quieres ver el navegador
DEFAULT_TIMEOUT = int(os.getenv("PW_TIMEOUT_MS", 8000))         # 8 segundos
BLOCK_RESOURCES = ["image", "media", "font", "stylesheet"]      # tipos de recursos que no cargamos
CHROME_CHANNEL = "chrome"

def create_playwright_context(persistent: bool = True):
    """
    Crea un contexto de Playwright optimizado para scraping MyCase.
    Mantiene sesión persistente y bloquea recursos pesados para mejorar velocidad.

    Returns:
        tuple: (p, context, page)
    """
    p = sync_playwright().start()

    try:
        user_data_dir = Path(PW_USER_DATA_DIR)
        user_data_dir.mkdir(parents=True, exist_ok=True)

        if persistent:
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(user_data_dir),
                headless=PW_HEADLESS,
                channel="chrome",
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-extensions",
                    "--disable-blink-features=AutomationControlled",
                    "--start-maximized",
                ],
            )
            logger.info("🧠 Contexto persistente creado en %s", user_data_dir)
        else:
            browser = p.chromium.launch(
                headless=PW_HEADLESS,
                args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"]
            )
            context = browser.new_context()
            logger.info("🚀 Contexto efímero iniciado.")

        page = context.new_page()
        page.set_default_timeout(PW_TIMEOUT_MS)

        # ⚙️ Bloquear recursos no necesarios para velocidad
        if PW_BLOCK_RESOURCES:
            page.route("**/*", lambda route, req:
                route.abort() if req.resource_type in PW_BLOCK_RESOURCES else route.continue_()
            )

        logger.info("✅ Playwright listo (headless=%s)", PW_HEADLESS)
        return p, context, page

    except Exception as e:
        logger.exception("❌ Error creando el contexto de Playwright: %s", e)
        raise
