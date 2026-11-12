
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

# Se conserva tu clave API original
PIXABAY_API_KEY = "26999448-13c68095b19cd0da7db5b8bf1"

MAX_QUERIES_PER_LINE = 3
MAX_DOWNLOADS_PER_LINE = 3
RESULTADOS_POR_BUSQUEDA = 50

ESPERA_ENTRE_BUSQUEDAS = 1
CACHE_HORAS = 24

# =====================================================
# PALABRAS QUE NO APORTAN INFORMACION VISUAL
# =====================================================

STOPWORDS = set("""
el la los las un una unos unas y o de del al
a en por para con sin sobre entre su sus
es son fue era ser estar esta este esto
que como cuando donde porque pero muy mas
the and or of in on at to for with by is are
was were be been this that these those
it its from into about as an
""".split())

# =====================================================
# DICCIONARIO DE CONCEPTOS VISUALES
# =====================================================

MAPA_VISUAL = {

    # PSICOLOGIA Y EMOCIONES

    "mente": "human mind psychology",
    "cerebro": "human brain neuroscience",
    "psicologia": "psychology human behavior",
    "emocion": "human emotions facial expressions",
    "emociones": "human emotions facial expressions",
    "miedo": "fear anxiety darkness",
    "ansiedad": "anxiety stress mental health",
    "tristeza": "sadness loneliness",
    "felicidad": "happiness smiling people",
    "amor": "love couple romantic relationship",
    "soledad": "loneliness isolated person",
    "pensamiento": "thinking human mind",
    "decision": "decision making person thinking",
    "sesgo": "cognitive bias psychology",
    "memoria": "human memory brain",
    "comportamiento": "human behavior psychology",
    "manipulacion": "psychological manipulation",
    "sociedad": "society people crowds",
    "sociedades": "society people crowds",
    "relacion": "human relationship interaction",
    "relaciones": "human relationships interaction",

    # HISTORIA

    "origen": "ancient origins history",
    "origenes": "ancient history evolution",
    "civilizacion": "ancient civilization ruins",
    "civilizaciones": "ancient civilizations archaeology",
    "historia": "historical documentary archive",
    "antiguo": "ancient historical ruins",
    "antigua": "ancient historical ruins",
    "imperio": "ancient empire historical",
    "guerra": "war history military",
    "revolucion": "historical revolution",
    "arqueologia": "archaeology ancient discoveries",
    "evolucion": "human evolution science",
    "humanidad": "human civilization history",
    "pasado": "historical archive old photographs",
    "culturas": "world cultures traditions",

    # CIENCIA Y TECNOLOGIA

    "ciencia": "science laboratory research",
    "investigacion": "scientific research laboratory",
    "experimento": "science experiment laboratory",
    "energia": "energy electricity power",
    "tecnologia": "modern technology digital",
    "sistema": "technology digital system",
    "universo": "universe galaxy space",
    "planeta": "planet earth space",
    "espacio": "outer space astronomy",
    "naturaleza": "nature wildlife landscape",
    "animales": "wildlife animals nature",
    "agua": "water ocean river",
    "clima": "weather climate storm",
    "digital": "digital technology computer",
    "robot": "robot artificial intelligence",
    "inteligencia": "artificial intelligence technology",

    # ECONOMIA Y NEGOCIOS

    "economia": "economy financial markets",
    "mercado": "stock market finance trading",
    "dinero": "money finance banking",
    "riqueza": "wealth luxury finance",
    "pobreza": "poverty social inequality",
    "consumo": "consumerism shopping economy",
    "empresa": "business corporate office",
    "trabajo": "workplace business employees",
    "finanzas": "financial markets investment",
    "bancos": "banking financial institution",
    "inversion": "investment stock market",
    "crisis": "economic crisis financial market",

    # TRUE CRIME Y MISTERIO

    "crimen": "crime investigation police",
    "asesinato": "crime investigation detective",
    "asesino": "criminal investigation police",
    "misterio": "mystery dark atmosphere",
    "desaparicion": "missing person investigation",
    "investigador": "detective investigation",
    "policia": "police investigation crime scene",
    "prision": "prison jail bars",
    "juicio": "courtroom justice trial",
    "evidencia": "forensic investigation evidence",
    "paranormal": "paranormal haunted mysterious",
    "fantasma": "ghost mysterious dark",
    "secreto": "mystery secret hidden",
    "documental": "documentary cinematic footage",
    "sangre": "crime investigation forensic",
    "cadaver": "forensic investigation crime scene",
    "sospechoso": "police detective investigation",

    # IMAGENES GENERALES

    "persona": "human person portrait",
    "personas": "people human crowd",
    "ciudad": "city urban buildings",
    "noche": "night city dark",
    "dia": "daylight landscape",
    "camino": "road journey landscape",
    "montana": "mountain landscape nature",
    "mar": "sea ocean waves",
    "playa": "beach ocean coastline",
    "bosque": "forest trees nature",
    "lluvia": "rain storm weather",
    "fuego": "fire flames burning",
    "luz": "light cinematic lighting",
    "sombra": "shadows dark cinematic",
    "casa": "house home interior",
    "habitacion": "bedroom interior",
    "ventana": "window sunlight interior",
    "reloj": "clock time passing",
    "camara": "cinematic camera filming",
    "avion": "airplane airport aviation",
    "carretera": "highway traffic road",
    "tren": "train railway transport",
    "hospital": "hospital medical healthcare",
    "medico": "doctor medical hospital",
    "enfermedad": "medical healthcare hospital",
    "familia": "family people relationship",
    "infancia": "childhood children playing",
    "anciano": "elderly person aging",
    "joven": "young people lifestyle"
}


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
# EXTRAER PALABRAS RELEVANTES
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
# GENERAR CONSULTAS EN ESPAÑOL E INGLES
# =====================================================

def generar_consultas(texto):

    palabras = extraer_palabras(texto)

    consultas = []

    # BUSQUEDA 1: PALABRAS ORIGINALES EN ESPAÑOL

    if palabras:

        consulta_es = " ".join(palabras[:6])

        consultas.append(
            (consulta_es, "es")
        )

    # BUSQUEDA 2: CONCEPTOS VISUALES EN INGLES

    conceptos = []

    for palabra in palabras:

        if palabra in MAPA_VISUAL:

            conceptos.extend(
                MAPA_VISUAL[palabra].split()
            )

    conceptos = list(dict.fromkeys(conceptos))

    if conceptos:

        consulta_en = " ".join(conceptos[:8])

        consultas.append(
            (consulta_en, "en")
        )

    # BUSQUEDA 3: COMBINACIONES ALTERNATIVAS

    if len(conceptos) >= 4:

        consulta_alternativa = " ".join(
            conceptos[4:8]
        )

        consultas.append(
            (consulta_alternativa, "en")
        )

    elif len(conceptos) >= 2:

        consultas.append(
            (" ".join(conceptos[:4]), "en")
        )

    # ELIMINAR DUPLICADOS

    resultado = []
    vistas = set()

    for consulta, idioma in consultas:

        consulta = consulta[:100]

        clave = (
            consulta.lower(),
            idioma
        )

        if consulta and clave not in vistas:

            resultado.append(
                (consulta, idioma)
            )

            vistas.add(clave)

        if len(resultado) >= MAX_QUERIES_PER_LINE:

            break

    return resultado


# =====================================================
# BUSQUEDA PIXABAY CON CACHE
# =====================================================

def buscar_videos_pixabay(query, idioma, cache):

    clave = idioma + "_" + query.lower()

    # COMPROBAR CACHE DE 24 HORAS

    if clave in cache:

        try:

            fecha = datetime.fromisoformat(
                cache[clave]["fecha"]
            )

            if datetime.now() - fecha < timedelta(
                hours=CACHE_HORAS
            ):

                print(
                    "    [CACHE] Busqueda guardada"
                )

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

            print(
                "    [AVISO] Limite de solicitudes alcanzado."
            )

            return []

        respuesta.raise_for_status()

        datos = respuesta.json()

        hits = datos.get("hits", [])

        # GUARDAR RESULTADOS

        cache[clave] = {

            "fecha": datetime.now().isoformat(),

            "hits": hits
        }

        print(
            f"    [OK] {len(hits)} videos encontrados"
        )

        return hits

    except requests.RequestException as e:

        print(
            f"    [ERROR] Pixabay: {e}"
        )

        return []


# =====================================================
# DESCARGAR VIDEOS
# =====================================================

def descargar_video(video, output_dir, descargados):

    video_id = str(video.get("id"))

    if video_id in descargados:

        print(
            f"    [REPETIDO] Video {video_id}"
        )

        return False

    videos = video.get("videos", {})

    video_url = None

    # PRIORIZAR CALIDAD

    for calidad in [
        "large",
        "medium",
        "small"
    ]:

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

            with open(
                temporal,
                "wb"
            ) as archivo:

                for bloque in respuesta.iter_content(
                    chunk_size=1024 * 1024
                ):

                    if bloque:

                        archivo.write(bloque)

        os.replace(
            temporal,
            destino
        )

        descargados.add(video_id)

        print(
            f"    [DESCARGADO] pixabay_{video_id}.mp4"
        )

        return True

    except requests.RequestException as e:

        print(
            f"    [ERROR] Descarga: {e}"
        )

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

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    guion_file = os.path.join(
        desktop,
        "GUION.txt"
    )

    archive_path = os.path.join(
        output_dir,
        "downloaded_archive.txt"
    )

    cache_path = os.path.join(
        output_dir,
        "pixabay_cache.json"
    )

    # COMPROBAR GUION

    if not os.path.exists(guion_file):

        print(
            "[ERROR] No se encuentra GUION.txt"
        )

        return

    with open(
        guion_file,
        "r",
        encoding="utf-8"
    ) as f:

        lineas = [
            linea.strip()
            for linea in f
            if linea.strip()
        ]

    if not lineas:

        print(
            "[AVISO] El guion esta vacio."
        )

        return

    # CARGAR REGISTRO DE DESCARGAS

    if os.path.exists(archive_path):

        with open(
            archive_path,
            "r",
            encoding="utf-8"
        ) as f:

            descargados = set(
                linea.strip()
                for linea in f
                if linea.strip()
            )

    else:

        descargados = set()

    # CARGAR CACHE

    if os.path.exists(cache_path):

        try:

            with open(
                cache_path,
                "r",
                encoding="utf-8"
            ) as f:

                cache = json.load(f)

        except (
            json.JSONDecodeError,
            OSError
        ):

            cache = {}

    else:

        cache = {}

    print("\n====================================")

    print(
        " BUSCADOR BILINGUE PIXABAY"
    )

    print("====================================")

    print(
        f"Lineas del guion: {len(lineas)}"
    )

    print(
        f"Videos registrados: {len(descargados)}"
    )

    print(
        f"Carpeta: {output_dir}"
    )

    total_descargados = 0

    # PROCESAR CADA LINEA

    for i, texto in enumerate(
        lineas,
        1
    ):

        print(
            f"\n--- LINEA {i}/{len(lineas)} ---"
        )

        print(
            "Texto:",
            texto[:120]
        )

        consultas = generar_consultas(
            texto
        )

        if not consultas:

            print(
                "No se encontraron palabras relevantes."
            )

            continue

        print(
            "\nCONSULTAS GENERADAS:"
        )

        for query, idioma in consultas:

            print(
                f" [{idioma.upper()}] {query}"
            )

        videos_candidatos = {}

        # REALIZAR LAS BUSQUEDAS

        for query, idioma in consultas:

            hits = buscar_videos_pixabay(
                query,
                idioma,
                cache
            )

            for video in hits:

                video_id = str(
                    video.get("id")
                )

                if (
                    video_id not in descargados
                    and video_id not in videos_candidatos
                ):

                    videos_candidatos[video_id] = video

            time.sleep(
                ESPERA_ENTRE_BUSQUEDAS
            )

        print(
            f"\nVideos candidatos: {len(videos_candidatos)}"
        )

        # DESCARGAR RESULTADOS

        descargados_linea = 0

        for video in videos_candidatos.values():

            if (
                descargados_linea
                >= MAX_DOWNLOADS_PER_LINE
            ):

                break

            resultado = descargar_video(
                video,
                output_dir,
                descargados
            )

            if resultado:

                descargados_linea += 1

                total_descargados += 1

                # ACTUALIZAR ARCHIVO DE CONTROL

                with open(
                    archive_path,
                    "a",
                    encoding="utf-8"
                ) as f:

                    f.write(
                        str(video["id"]) + "\n"
                    )

        print(
            f"\nDescargas de esta linea: {descargados_linea}"
        )

        # GUARDAR CACHE

        with open(
            cache_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                cache,
                f,
                ensure_ascii=False
            )

    print("\n====================================")

    print(
        "PROCESO FINALIZADO"
    )

    print(
        f"Nuevos videos descargados: {total_descargados}"
    )

    print(
        f"Total registrados: {len(descargados)}"
    )

    print(
        f"Carpeta: {output_dir}"
    )

    print("====================================")


# =====================================================
# EJECUCION
# =====================================================

if __name__ == "__main__":

    procesar_guion_y_descargar()







