import polars as pl

from utils.text_utils import sanitize_folder_name
from service_layer.mycase_play_service import login_mycase
from parsing_layer.mycase_documents import download_leads_pdfs
from utils.logger import get_logger

logger = get_logger(__name__)

def main():
    # Ruta a tu CSV con columnas: ID, CLIENT
    csv_path = "cases.csv"

    # Leer el CSV con Polars (usa latin1 si viene de Excel/Windows)
    df = pl.read_csv(
        csv_path,
        encoding="latin1",
        ignore_errors=True
    )


    # Abrir una sola sesión y loguear
    p, context, page = login_mycase()

    # Iterar por cada fila
    for row in df.iter_rows():
        case_id = int(str(row[0]).strip().lstrip("/")) if str(row[0]).strip().lstrip("/").isdigit() else None
        client_name = str(row[1]).strip() if row[1] else "Unknown_Client"
        # Crear nombre de carpeta seguro para Windows
        safe_folder = sanitize_folder_name(client_name)

        logger.info(f"\n========== Procesando {safe_folder} (ID {case_id}) ==========")
        try:
            download_leads_pdfs(page, case_id, safe_folder)
        except Exception as e:
            logger.error(f"Error al procesar {case_id} - {e}")

    # Cerrar sesión de Playwright al final
    context.close()
    p.stop()


if __name__ == "__main__":
    main()
