# main_datos.py
import polars as pl
from service_layer.mycase_play_service import login_mycase
from service_layer.mycase_scraper_service import get_case_details
from utils.logger import get_logger

logger = get_logger(__name__)

def main():
    input_csv = "cases_ids.csv"
    output_excel = "case_details.csv"

    df = pl.read_csv(input_csv)
    results = []

    # 🔐 Una sola sesión persistente
    p, context, page = login_mycase()

    for case_id in df["ID"]:
        logger.info(f"🔍 Procesando ID {case_id}")
        data = get_case_details(page, int(case_id))
        results.append(data)

    # Exportar resultados
    df_out = pl.DataFrame(results)
    df_out.write_csv(output_excel)
    logger.info(f"✅ Archivo generado: {output_excel}")

    # 🔚 Cerrar Playwright solo una vez
    context.close()
    p.stop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(f"❌ Error inesperado: {e}")