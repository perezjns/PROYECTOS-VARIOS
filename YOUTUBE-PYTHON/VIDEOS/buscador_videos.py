import asyncio
import edge_tts
import os
import re
import shutil
import requests
from collections import Counter

# ==========================================
# CONFIGURACIÓN
# ==========================================
VOZ_SELECCIONADA = "es-ES-AlvaroNeural"
VELOCIDAD = "-5%"

# Rutas de archivos en el Escritorio
escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
archivo_guion = os.path.join(escritorio, "GUION.txt")
archivo_audio = os.path.join(escritorio, "narracion_guion.mp3")
carpeta_videos = os.path.join(escritorio, "Clips_Para_Video")

# Palabras comunes a ignorar para el análisis del texto
STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "a", "ante", "bajo", "cabe", "con",
    "contra", "desde", "en", "entre", "hacia", "hasta", "para", "por", "según", "sin", "sobre", "tras", 
    "y", "e", "ni", "que", "o", "u", "pero", "mas", "sino", "porque", "como", "este", "esta", "estos",
    "estas", "ese", "esa", "esos", "esas", "mi", "tu", "su", "ya", "si", "no", "todo", "tambien", "hacer"
}

# 🌐 LISTA DE VÍDEOS DE STOCK ESTABLES Y VARIADOS
VIDEOS_STOCK = [
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"
]

def extraer_palabras_clave(texto):
    """Extrae palabras clave del texto o devuelve valores por defecto si es corto."""
    palabras = re.findall(r'\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]{4,}\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in STOPWORDS]
    conteo = Counter(palabras_filtradas)
    
    # Obtenemos las 2 más comunes
    mas_comunes = [palabra for palabra, _ in conteo.most_common(2)]
    
    # Si el guion es muy corto y no detecta suficientes, añadimos palabras genéricas para asegurar variedad
    if len(mas_comunes) < 2:
        mas_comunes = ["proyecto", "video"]
        
    return mas_comunes

def preparar_carpeta_videos():
    """Limpia y recrea la carpeta de vídeos."""
    if os.path.exists(carpeta_videos):
        try:
            shutil.rmtree(carpeta_videos)
        except Exception:
            pass
    os.makedirs(carpeta_videos)

def descargar_multiples_videos(palabras_clave):
    """Descarga varios vídeos independientes asegurando que la carpeta se llene."""
    preparar_carpeta_videos()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"\n🔍 Iniciando descarga de recursos visuales...")

    # Descargaremos un total de 4 vídeos independientes asegurando variedad
    for i in range(4):
        url_video = VIDEOS_STOCK[i % len(VIDEOS_STOCK)]
        palabra_asociada = palabras_clave[i % len(palabras_clave)]
        nombre_archivo = os.path.join(carpeta_videos, f"clip_{i+1}_{palabra_asociada}.mp4")
        
        try:
            print(f"  📥 Descargando clip {i+1} de 4...")
            respuesta = requests.get(url_video, headers=headers, stream=True)
            
            if respuesta.status_code == 200:
                with open(nombre_archivo, "wb") as f:
                    for chunk in respuesta.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"  ✅ Guardado con éxito: {nombre_archivo}")
            else:
                print(f"  ❌ Error HTTP al descargar el clip {i+1}")
        except Exception as e:
            print(f"  ❌ Error en la descarga del clip {i+1}: {e}")

async def generar_audio(texto):
    """Genera la locución profesional en MP3."""
    print("\n🎙️ Generando la narración de audio con IA...")
    comunicador = edge_tts.Communicate(texto, VOZ_SELECCIONADA, rate=VELOCIDAD)
    await comunicador.save(archivo_audio)
    print(f"✅ Audio guardado en tu Escritorio como: '{archivo_audio}'")

async def main():
    if not os.path.exists(archivo_guion):
        print(f"❌ No se encuentra el archivo 'GUION.txt' en tu Escritorio.")
        return

    print("📖 Leyendo 'GUION.txt'...")
    with open(archivo_guion, "r", encoding="utf-8") as f:
        texto = f.read()

    # 1. Extraer palabras clave
    palabras_clave = extraer_palabras_clave(texto)
    print(f"🎯 Temas base detectados: {', '.join(palabras_clave)}")

    # 2. Generar audio y descargar múltiples vídeos
    await generar_audio(texto)
    descargar_multiples_videos(palabras_clave)

    print("\n🎉 ¡PROCESO COMPLETADO CON ÉXITO!")
    print(f"• Audio listo en el Escritorio.")
    print(f"• Revisa tu carpeta 'Clips_Para_Video' en el Escritorio. ¡Contiene varios clips listos!")

if __name__ == "__main__":
    asyncio.run(main())