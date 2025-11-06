# 🕸️ MyCase Scraper Automation

Automatización profesional para la extracción de datos y documentos del portal **MyCase** de The Mendoza Law Firm (TMLF), usando **Playwright**, **Polars**, y una arquitectura modular Python.

---

## 🚀 Descripción general

Este proyecto permite:

- Autenticarse de forma segura en MyCase (usando sesión persistente con cookies).
- Extraer información de casos (`Name`, `ID`, `DateOpened`, `TypeOfCase`).
- Descargar documentos PDF asociados a casos o leads.
- Exportar los resultados a CSV, Excel o archivos JSON individuales.
- Reutilizar la sesión sin reautenticarse cada vez (gracias al perfil persistente de Chrome).

El flujo fue diseñado con una **arquitectura por capas**, separando la lógica de scraping, parsing, configuración y servicios.

---

## 🧩 Estructura del proyecto

```

scraper_mycase/
├── .env                          # Contiene las variables de entorno
├── messages.csv                  # csv para main_messages.py con dos columnas, "ID" y "MESSAGE"
├── cases_ids.csv                 # csv para main_datos.py con una sola columna "ID"
├── case_details.csv              # csv para main_datos.py, salida de este módulo
├── cases.csv                     # csv para main.py con dos columnas "ID" y "Nombre del PC"
├── main.py                       # Descarga documentos (por ID)
├── main_datos.py                 # Extrae información de los casos a Excel
├── main_send_messages.py         # Envía mensajes mediante el chat integrado en mycase
├── scripts/
│   └── start_chrome_debug.bat      # Determina como se debe configurar el chrome
│   └── seed_playwright_profile.py  # Genera la semilla de sesión persistente (cookies guardadas)
├── service_layer/
│   └── mycase_play_service.py      # Login y control del flujo de scraping
│   └── mycase_scraper_service.py   # Extracción de datos de casos
├── parsing_layer/
│   └── mycase_documents.py         # Lógica de descarga de PDFs
│   └── mycase_text_messages.py     # Lógica de enviar mensajes mediante mycase
├── data_layer/
│   └── playwright_driver.py        # Configuración y creación del contexto Playwright
├── utils/
│   ├── logger.py                   # Configuración de logs
│   └── text_utils.py               # Utilidades de texto (sanitize, etc.)
├── config/
│   └── settings.py                 # Variables globales y rutas
├── requirements.txt
└── README.md                       # Este archivo

````

---

## ⚙️ Instalación

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/TrackerIA/scraper_mycase 
cd scraper_mycase
````

### 2️⃣ Crear entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Instalar navegadores Playwright

```bash
playwright install
```

---

## 🔐 Variables de entorno (.env)

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```bash
MYCASE_EMAIL=tu_correo@themendozalawfirm.com
MYCASE_PASSWORD=tu_contraseña
PW_USER_DATA_DIR=C:\ChromeProfiles\mycase_pw
PW_HEADLESS=false
PW_TIMEOUT_MS=8000
```

Estas variables controlan tanto el login como el perfil persistente de Chrome.

---

## 🧠 Generar la semilla de sesión (cookies persistentes)

Antes de ejecutar los scrapers, **debes generar una sesión persistente** válida en MyCase.

Ejecuta:

```bash
python -m scripts.seed_playwright_profile
```

Aparecerá una ventana de Chrome.

1. Inicia sesión en MyCase.
2. Completa el 2FA (si aplica).
3. Marca “**Recordar este dispositivo**”.
4. Una vez en el dashboard, vuelve a la consola y presiona ENTER.

Esto generará la carpeta:

```
C:\ChromeProfiles\mycase_pw
```

con las cookies de sesión guardadas.

---

## 🧰 Uso de los scrapers

### 🟢 1. Descargar documentos PDF de leads o casos

```bash
python -m main
```

* Lee `cases.csv` con columnas `ID, CLIENT`
* Descarga todos los documentos en `C:\MyCaseDownloads\<cliente>`

---

### 🟡 2. Extraer información general de casos

```bash
python -m main_datos
```

* Lee `cases_ids.csv` con columna `ID`
* Extrae `Name`, `ID`, `DateOpened`, `TypeOfCase`
* Exporta resultados a `case_details.xlsx`

---

### 🔵 3. Convertir resultados CSV a JSON individuales

```bash
python csv_to_json_splitter.py
```

* Toma `case_details.csv`
* Genera un archivo JSON por registro en `json_output/`

---

## 🧩 Arquitectura por capas

| Capa               | Descripción                                                |
| ------------------ | ---------------------------------------------------------- |
| **data_layer/**    | Configura el navegador y mantiene la sesión persistente.   |
| **service_layer/** | Orquesta el login y la lógica de negocio del scraping.     |
| **parsing_layer/** | Extrae y descarga la información visible en cada página.   |
| **utils/**         | Herramientas de apoyo (logs, sanitización de texto, etc.). |
| **config/**        | Variables globales y parámetros reutilizables.             |

---

## 🧾 Ejemplo de salida

### `case_details.xlsx` / `case_details.csv`

| Name                    | ID       | DateOpened | TypeOfCase |
| ----------------------- | -------- | ---------- | ---------- |
| Leonardo Pablo Ortiz    | 10613406 | 05/04/2020 | VAWA AOS   |
| Maria Isabel Reyes Moya | 10613860 | 05/04/2020 | VAWA DA    |

---

## 🧱 Dependencias clave

* [Playwright](https://playwright.dev/python/) — Navegación y scraping.
* [Polars](https://pola.rs/) — Lectura/escritura eficiente de CSV/Excel.
* [XlsxWriter](https://pypi.org/project/XlsxWriter/) — Exportación a Excel.
* [python-dotenv](https://pypi.org/project/python-dotenv/) — Gestión de variables .env.
* [pathlib](https://docs.python.org/3/library/pathlib.html) — Manejo seguro de rutas.
* [logging](https://docs.python.org/3/library/logging.html) — Sistema de logs integrado.

---

## 🧹 Mantenimiento

* Si cambia tu contraseña o el portal invalida la sesión, borra la carpeta:

  ```
  C:\ChromeProfiles\mycase_pw
  ```

  y vuelve a ejecutar `python -m scripts.seed_playwright_profile`.

* Puedes ajustar `PW_HEADLESS=true` en `.env` para correr en segundo plano sin mostrar el navegador.

---

## 🧩 Autor

**Julio César Vargas Domínguez**
Desarrollador de automatizaciones y BI – *The Mendoza Law Firm*
📧 [julio.vargas@mendozafirm.com](mailto:julio.vargas@mendozafirm.com)

---

## 🧾 Licencia

Proyecto interno de **The Mendoza Law Firm** — uso restringido a fines operativos y de automatización interna.
