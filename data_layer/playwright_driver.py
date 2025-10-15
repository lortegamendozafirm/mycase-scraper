# ============================================
# data_layer/playwright_driver.py
# ============================================

from playwright.sync_api import sync_playwright
from pathlib import Path
import os
from utils.logger import get_logger

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
        if persistent:
            # 🚀 Sesión persistente (cookies guardadas entre ejecuciones)
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(USER_DATA_DIR),
                headless=HEADLESS,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-extensions",
                    "--disable-blink-features=AutomationControlled",
                    "--start-maximized",
                ],
                channel=CHROME_CHANNEL
            )
            logger.info("🧠 Contexto persistente creado en %s", USER_DATA_DIR)
        else:
            # 🧩 Sesión efímera (sin guardar cookies)
            browser = p.chromium.launch(
                headless=HEADLESS,
                args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"]
            )
            context = browser.new_context()
            logger.info("🚀 Contexto efímero iniciado.")

        page = context.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT)

        # ⚙️ Bloquear recursos no necesarios para velocidad
        page.route("**/*", lambda route, req:
            route.abort() if req.resource_type in BLOCK_RESOURCES else route.continue_()
        )

        logger.info("✅ Playwright listo (headless=%s)", HEADLESS)
        return p, context, page

    except Exception as e:
        logger.exception("❌ Error creando el contexto de Playwright: %s", e)
        raise
