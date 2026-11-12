# 🎬 Buscador y Descargador Dinámico de Videos Stock (Pixabay)

Este script en Python automatiza la búsqueda y descarga de videos de stock gratuitos desde la API de **Pixabay** a partir de un archivo de texto con tu guion (`GUION.txt`). 

A diferencia de los buscadores basados en diccionarios estáticos, este script analiza cada línea del guion de forma **100% dinámica**, extrayendo las palabras clave relevantes y generando múltiples combinaciones de búsqueda para obtener material visual variado y evitar repetir siempre los mismos clips.

---

## ✨ Características Principales

* **Extracción Dinámica de Palabras Clave:** Limpia el texto de acentos, signos de puntuación y palabras vacías (*stopwords* como artículos, preposiciones y conectores) para quedarse únicamente con los conceptos importantes de cada línea.
* **Consultas Variadas por Línea:** Para evitar resultados repetitivos, genera hasta 3 búsquedas distintas por cada párrafo o línea del guion (fragmento inicial, fragmento medio y palabras alternadas).
* **Historial de Descargas (`downloaded_archive.txt`):** Registra los IDs de todos los videos descargados previamente para no volver a bajar el mismo archivo en futuras ejecuciones.
* **Sistema de Caché Local (`pixabay_cache.json`):** Guarda los resultados de las búsquedas durante 24 horas para acelerar el proceso y respetar los límites de peticiones de la API de Pixabay.
* **Prioridad de Calidad:** Selecciona automáticamente la mejor resolución disponible (`large`, `medium` o `small`) y realiza descargas seguras mediante archivos temporales (`.part`) para evitar videos corruptos si se interrumpe la conexión.

---

## 📋 Requisitos Previos

* **Python 3.7** o superior.
* Una clave de API gratuita de [Pixabay API](https://pixabay.com/api/docs/).
* Librería `requests` instalada.

### Instalación de dependencias

Ejecuta el siguiente comando en tu terminal para instalar la única dependencia externa necesaria:

```bash
pip install requests
```

---

## 🚀 Cómo Usarlo

1. **Prepara tu guion:**
   Crea un archivo llamado `GUION.txt` en tu **Escritorio** (`Desktop`). Escribe cada escena, párrafo o frase en una línea diferente.

2. **Configura tu API Key:**
   Abre el archivo `.py` y asegúrate de colocar tu clave en la variable correspondiente (o utiliza variables de entorno si vas a subir el código a un repositorio público):
   ```python
   PIXABAY_API_KEY = "TU_CLAVE_API_DE_PIXABAY"
   ```

3. **Ejecuta el script:**
   ```bash
   python nombre_de_tu_script.py
   ```

4. **Revisa tus videos:**
   El programa creará automáticamente una carpeta llamada **`stock videos`** en tu Escritorio, donde guardará todos los clips descargados en formato `.mp4` junto con los archivos de control.

---

## ⚙️ Configuración Personalizable

Al inicio del script puedes ajustar fácilmente los siguientes parámetros según tus necesidades:

| Variable | Valor por defecto | Descripción |
| :--- | :---: | :--- |
| `MAX_QUERIES_PER_LINE` | `3` | Número máximo de búsquedas distintas que se harán por cada línea del guion. |
| `MAX_DOWNLOADS_PER_LINE` | `3` | Cantidad máxima de videos nuevos que se descargarán por cada línea. |
| `RESULTADOS_POR_BUSQUEDA` | `50` | Cantidad de resultados que se solicitan a Pixabay por consulta (máx. 200). |
| `ESPERA_ENTRE_BUSQUEDAS` | `1` | Segundos de pausa entre peticiones para evitar bloqueos por límite de velocidad. |
| `CACHE_HORAS` | `24` | Tiempo en horas que se guardan los resultados en la caché local. |

---

## 📁 Estructura de Archivos Generados

```text
Desktop/
├── GUION.txt                   # Tu archivo de entrada con el texto del guion
└── stock videos/               # Carpeta generada automáticamente
    ├── pixabay_12345.mp4       # Videos descargados identificados por su ID
    ├── downloaded_archive.txt  # Registro histórico para evitar duplicados
    └── pixabay_cache.json      # Caché temporal de consultas a la API
```

---

## ⚠️ Nota de Seguridad para GitHub

Si vas a publicar este proyecto en un repositorio **público** en GitHub, recuerda **borrar o reemplazar tu `PIXABAY_API_KEY`** antes de hacer `git push` para que nadie más utilice tu cuota de peticiones.
