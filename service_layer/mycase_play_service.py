# service_layer/mycase_play_service.py
# CAPAS DE SERVICIO
from config.settings import MYCASE_EMAIL, MYCASE_PASSWORD, LOGIN_URL, DASHBOARD_URL
from data_layer.playwright_driver import create_playwright_context
from parsing_layer.mycase_documents import download_case_pdfs
from utils.logger import get_logger

# Librerias
# Librería para manejar excepciones de Playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeout

logger = get_logger(__name__)

def download_pdfs_for_case(case_id: int, subfolder: str):
    p, context, page = create_playwright_context()
    # Ir a la página de login
    page.goto(DASHBOARD_URL)
    try:
        # Espera y llena los campos
        page.fill("#login_session_email", MYCASE_EMAIL or "")
        page.fill("#login_session_password", MYCASE_PASSWORD or "")

        # Click en el botón de login
        page.click("#login-form-submit")

        # Esperar que la URL cambie a dashboard
        page.wait_for_url("**/dashboard*", timeout=15000)
        logger.info("✅ Login exitoso en MyCase.")
        # Llamar a la función de descarga
        download_case_pdfs(page, case_id, subfolder)
    except PlaywrightTimeout:
        # Si ya estábamos logueados (por cookies), ir directo al dashboard
        page.goto(DASHBOARD_URL)
        logger.warning("ℹ️ Sesión ya activa, saltando login.")



def login_mycase():
    """
    Abre un contexto persistente y asegura que estamos logueados una sola vez.
    Retorna p, context, page (Playwright objects).
    """
    p, context, page = create_playwright_context()
    page.goto(DASHBOARD_URL)
    
    try:
        # Si aparece formulario de login, llenar credenciales
        page.fill("#login_session_email", MYCASE_EMAIL or "")
        page.fill("#login_session_password", MYCASE_PASSWORD or "")
        page.click("#login-form-submit")

        page.wait_for_url("**/dashboard*", timeout=15000)
        logger.info("✅ Login exitoso en MyCase.")
    except PlaywrightTimeout:
        # Ya había sesión (cookies)
        logger.warning("ℹ️ Sesión ya activa, saltando login.")

    return p, context, page


def open_mycase_with_pw():
    p, context, page = create_playwright_context()
    page.goto(DASHBOARD_URL)
    logger.info("✅ MyCase con sesión persistente (Playwright).")
    return p, context, page
