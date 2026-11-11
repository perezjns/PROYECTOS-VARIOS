import asyncio
import edge_tts
import os

# Configuración de la voz y ruta del archivo en el Escritorio
VOZ_SELECCIONADA = "es-ES-AlvaroNeural" 
VELOCIDAD = "-5%"  # Puedes ajustar la velocidad si lo deseas (-10% más lento, +0% normal)

escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
archivo_guion = os.path.join(escritorio, "GUION.txt")
archivo_salida = os.path.join(escritorio, "narracion_guion.mp3")

async def generar_audio_desde_guion():
    # Comprobar si el archivo GUION.txt existe en el Escritorio
    if not os.path.exists(archivo_guion):
        print(f"❌ Error: No se encuentra el archivo 'GUION.txt' en tu Escritorio.")
        print(f"Asegúrate de crear un bloc de notas llamado 'GUION' en tu Escritorio con el texto dentro.")
        return

    print("Leyendo el archivo 'GUION.txt' desde el Escritorio...")
    # Leer el texto usando codificación utf-8 para que reconozca tildes y eñes sin problemas
    with open(archivo_guion, "r", encoding="utf-8") as archivo:
        texto_largo = archivo.read()

    print("Generando el audio con inteligencia artificial (esto puede tardar unos segundos si el texto es muy largo)...")
    
    # Crear el comunicador con el texto del archivo
    comunicador = edge_tts.Communicate(texto_largo, VOZ_SELECCIONADA, rate=VELOCIDAD)
    
    # Guardar el archivo de audio resultante
    await comunicador.save(archivo_salida)
    print(f"¡Listo! Audio guardado con éxito en tu Escritorio como 'narracion_guion.mp3'.")

if __name__ == "__main__":
    asyncio.run(generar_audio_desde_guion())