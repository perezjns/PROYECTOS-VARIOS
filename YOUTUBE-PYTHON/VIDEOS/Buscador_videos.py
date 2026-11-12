import os
import re
import json
import time
import requests
import unicodedata

from datetime import datetime, timedelta

# =====================================================
# CONFIGURACION PIXABAY
# =====================================================

PIXABAY_API_KEY = "26999448-13c68095b19cd0da7db5b8bf1"

MAX_QUERIES_PER_LINE = 3
MAX_DOWNLOADS_PER_LINE = 3
RESULTADOS_POR_BUSQUEDA = 50

ESPERA_ENTRE_BUSQUEDAS = 1
CACHE_HORAS = 24

# =====================================================
# PALABRAS QUE NO APORTAN INFORMACION VISUAL (STOPWORDS)
# =====================================================

STOPWORDS = set("""
el la los las un una unos unas y o de del al
a en por para con sin sobre entre su sus
es son fue era ser estar esta este esto
que como cuando donde porque pero muy mas
the and or of in on at to for with by is are
was were be been this that these those
it its from into about as an unos unas
tambien tambien este esta estos estas lo los le les
mio tuyo suyo mi tu su nos os
""".split())


# =====================================================
# NORMALIZAR TEXTO
# =====================================================

def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )
    return texto


# =====================================================
# EXTRAER PALABRAS RELEVANTES DEL GUION
# =====================================================

def extraer_palabras(texto):
    texto = normalizar(texto)
    palabras = re.findall(
        r"\b[a-zA-Z]{3,}\b",
        texto
    )
    palabras = [
        p for p in palabras
        if p not in STOPWORDS
    ]
    return list(dict.fromkeys(palabras))


# =====================================================
# GENERAR CONSULTAS DINAMICAS DESDE EL TEXTO
# =====================================================

def generar_consultas(texto):
    palabras = extraer_palabras(texto)
    consultas = []

    if not palabras:
        return []

    # CONSULTA 1: Las primeras palabras clave principales de la línea
    consulta_principal = " ".join(palabras[:5])
    if consulta_principal:
        consultas.append((consulta_principal, "es"))

    # CONSULTA 2: Si la línea es larga, tomamos una combinación desplazada o la segunda mitad
    if len(palabras) >= 4:
        # Tomar un fragmento diferente de la misma frase para buscar matices visuales distintos
        mitad = len(palabras) // 2
        consulta_secundaria = " ".join(palabras[mitad:mitad + 5])
        if consulta_secundaria and consulta_secundaria != consulta_principal:
            consultas.append((consulta_secundaria, "es"))

    # CONSULTA 3: Combinación alternada o palabras clave salteadas para ampliar variedad
    if len(palabras) >= 3:
        palabras_alternadas = [p for i, p in enumerate(palabras) if i % 2 == 0]
        consulta_alt = " ".join(palabras_alternadas[:4])
        if consulta_alt:
            consultas.append((consulta_alt, "es"))

    # ELIMINAR DUPLICADOS
    resultado = []
    vistas = set()

    for consulta, idioma in consultas:
        consulta = consulta[:100].strip()
        clave = (consulta.lower(), idioma)

        if consulta and clave not in vistas:
            resultado.append((consulta, idioma))
            vistas.add(clave)

        if len(resultado) >= MAX_QUERIES_PER_LINE:
            break

    return resultado


# =====================================================
# BUSQUEDA PIXABAY CON CACHE
# =====================================================

def buscar_videos_pixabay(query, idioma, cache):
    clave = idioma + "_" + query.lower()

    if clave in cache:
        try:
            fecha = datetime.fromisoformat(
                cache[clave]["fecha"]
            )
            if datetime.now() - fecha < timedelta(
                hours=CACHE_HORAS
            ):
                print(f"    [CACHE] Usando resultados guardados para: '{query}'")
                return cache[clave]["hits"]
        except (ValueError, KeyError, TypeError):
            pass

    url = "https://pixabay.com/api/videos/"
    parametros = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "lang": idioma,
        "per_page": RESULTADOS_POR_BUSQUEDA,
        "safesearch": "true",
        "order": "popular"
    }

    try:
        respuesta = requests.get(
            url,
            params=parametros,
            timeout=30
        )

        if respuesta.status_code == 429:
            print("    [AVISO] Limite de solicitudes alcanzado en Pixabay.")
            return []

        respuesta.raise_for_status()
        datos = respuesta.json()
        hits = datos.get("hits", [])

        cache[clave] = {
            "fecha": datetime.now().isoformat(),
            "hits": hits
        }

        print(f"    [OK] '{query}' -> {len(hits)} videos encontrados")
        return hits

    except requests.RequestException as e:
        print(f"    [ERROR] Pixabay: {e}")
        return []


# =====================================================
# DESCARGAR VIDEOS
# =====================================================

def descargar_video(video, output_dir, descargados):
    video_id = str(video.get("id"))

    if video_id in descargados:
        print(f"    [REPETIDO] Video {video_id} ya descargado anteriormente.")
        return False

    videos = video.get("videos", {})
    video_url = None

    for calidad in ["large", "medium", "small"]:
        if videos.get(calidad, {}).get("url"):
            video_url = videos[calidad]["url"]
            break

    if not video_url:
        return False

    destino = os.path.join(
        output_dir,
        f"pixabay_{video_id}.mp4"
    )
    temporal = destino + ".part"

    try:
        with requests.get(
            video_url,
            stream=True,
            timeout=(20, 180)
        ) as respuesta:
            respuesta.raise_for_status()
            with open(temporal, "wb") as archivo:
                for bloque in respuesta.iter_content(chunk_size=1024):
                    if bloque:
                        archivo.write(bloque)

        os.replace(temporal, destino)
        descargados.add(video_id)
        print(f"    [DESCARGADO] pixabay_{video_id}.mp4")
        return True

    except requests.RequestException as e:
        print(f"    [ERROR] Descarga: {e}")
        if os.path.exists(temporal):
            os.remove(temporal)
        return False


# =====================================================
# PROCESAR GUION
# =====================================================

def procesar_guion_y_descargar():
    desktop = os.path.join(
        os.path.expanduser("~"),
        "Desktop"
    )
    output_dir = os.path.join(
        desktop,
        "stock videos"
    )
    os.makedirs(output_dir, exist_ok=True)

    guion_file = os.path.join(desktop, "GUION.txt")
    archive_path = os.path.join(output_dir, "downloaded_archive.txt")
    cache_path = os.path.join(output_dir, "pixabay_cache.json")

    if not os.path.exists(guion_file):
        print("[ERROR] No se encuentra el archivo GUION.txt en el Escritorio.")
        return

    with open(guion_file, "r", encoding="utf-8") as f:
        lineas = [
            linea.strip()
            for linea in f
            if linea.strip()
        ]

    if not lineas:
        print("[AVISO] El archivo GUION.txt esta vacio.")
        return

    if os.path.exists(archive_path):
        with open(archive_path, "r", encoding="utf-8") as f:
            descargados = set(
                linea.strip() for linea in f if linea.strip()
            )
    else:
        descargados = set()

    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except (json.JSONDecodeError, OSError):
            cache = {}
    else:
        cache = {}

    print("\n====================================")
    print(" BUSCADOR DINAMICO DE VIDEOS (PIXABAY)")
    print("====================================")
    print(f"Lineas del guion: {len(lineas)}")
    print(f"Videos ya registrados: {len(descargados)}")
    print(f"Carpeta destino: {output_dir}")

    total_descargados = 0

    for i, texto in enumerate(lineas, 1):
        print(f"\n--- LINEA {i}/{len(lineas)} ---")
        print("Texto:", texto[:120])

        consultas = generar_consultas(texto)

        if not consultas:
            print("    [AVISO] No se extrajeron palabras relevantes de esta línea.")
            continue

        print("\nCONSULTAS GENERADAS:")
        for query, idioma in consultas:
            print(f" [{idioma.upper()}] {query}")

        videos_candidatos = {}

        for query, idioma in consultas:
            hits = buscar_videos_pixabay(query, idioma, cache)

            for video in hits:
                video_id = str(video.get("id"))
                if (
                    video_id not in descargados
                    and video_id not in videos_candidatos
                ):
                    videos_candidatos[video_id] = video

            time.sleep(ESPERA_ENTRE_BUSQUEDAS)

        print(f"\nVideos candidatos nuevos: {len(videos_candidatos)}")

        descargados_linea = 0

        for video in videos_candidatos.values():
            if descargados_linea >= MAX_DOWNLOADS_PER_LINE:
                break

            resultado = descargar_video(
                video,
                output_dir,
                descargados
            )

            if resultado:
                descargados_linea += 1
                total_descargados += 1

                with open(archive_path, "a", encoding="utf-8") as f:
                    f.write(str(video["id"]) + "\n")

        print(f"\nDescargas realizadas en esta linea: {descargados_linea}")

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)

    print("\n====================================")
    print("PROCESO FINALIZADO")
    print(f"Nuevos videos descargados: {total_descargados}")
    print(f"Total videos registrados: {len(descargados)}")
    print(f"Carpeta: {output_dir}")
    print("====================================")


if __name__ == "__main__":
    procesar_guion_y_descargar()







