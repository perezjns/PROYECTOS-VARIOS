# 🎬 Pipeline Automático de Producción para YouTube

Este repositorio contiene un pipeline programático en Python diseñado para automatizar la creación de recursos audiovisuales a partir de un script de texto local (`GUION.txt`). El sistema permite generar tanto la narración en audio como la recopilación de vídeos de stock en carpetas locales sin requerir claves API ni procesos de registro.

---

## 📁 Estructura del Repositorio

```text
YOUTUBE-PYTHON/
│
├── AUDIO/
│   └── generador_voz.py     # Módulo de locución e IA de voz
│
├── VIDEOS/
│   └── buscador_videos.py   # Módulo de procesamiento de guion y descarga de recursos visuales
│
└── README.md
```

---

## ⚙️ Descripción de Módulos

### 1. 🎙️ Módulo de Audio (`AUDIO/generador_voz.py`)
Genera una locución en formato `.mp3` utilizando síntesis de voz neuronal.

* **Motor TTS:** Integración con `edge-tts` para generar voz en español de alta claridad (`es-ES-AlvaroNeural`).
* **Entrada:** Lee el contenido del archivo `GUION.txt` ubicado en el Escritorio.
* **Salida:** Exporta el archivo de audio `narracion_guion.mp3` directamente al Escritorio.

### 2. 🎥 Módulo de Vídeos (`VIDEOS/buscador_videos.py`)
Analiza el guion, extrae las palabras clave temáticas y descarga clips de vídeo de stock libres de derechos.

* **Análisis de Texto:** Procesa el guion descartando conectores y artículos (*stopwords*) mediante expresiones regulares (`re`) y recuento de frecuencia (`Counter`).
* **Gestión de Descargas:** Realiza peticiones HTTP HTTP-safe inyectando cabeceras de navegador (`User-Agent`) para evitar bloqueos 403.
* **Mantenimiento Limpio:** Gestiona el directorio de destino `Clips_Para_Video` recreándolo en cada ejecución para asegurar un entorno de edición organizado.
* **Salida:** Descarga recursos en formato `.mp4` en la carpeta `Clips_Para_Video` del Escritorio.

---

## 🛠️ Requisitos e Instalación

Es necesario disponer de **Python 3.10** o superior. Puedes instalar las dependencias necesarias ejecutando:

```bash
pip install edge-tts requests
```

---

## 🚀 Modo de Uso

1. Coloca tu archivo de guion **`GUION.txt`** en el **Escritorio** de tu equipo.
2. Ejecuta el módulo de generación de audio:
   ```bash
   python AUDIO/generador_voz.py
   ```
3. Ejecuta el módulo de descarga de vídeos:
   ```bash
   python VIDEOS/buscador_videos.py
   ```

Una vez completada la ejecución, los recursos listos para la edición (`narracion_guion.mp3` y la carpeta `Clips_Para_Video`) estarán disponibles en tu Escritorio.

---

## 📝 Licencia

Proyecto de uso libre desarrollado para la automatización de flujos de trabajo en creación de contenido audiovisual.
