# 🎬 Buscador y Descargador Automatizado de Vídeos de Pixabay

## 📌 Descripción del proyecto

Este proyecto consiste en desarrollar una herramienta automatizada en Python capaz de analizar un guion de texto y buscar material audiovisual relacionado con su contenido mediante la API de Pixabay.

El programa identifica palabras relevantes, genera consultas visuales en español e inglés y descarga vídeos de stock para facilitar la creación de contenido audiovisual, documentales y vídeos para YouTube.

El objetivo es reducir el tiempo dedicado a buscar manualmente imágenes y vídeos, automatizando parte del proceso de selección y descarga de recursos audiovisuales.

## 🎯 Objetivos

- Automatizar la búsqueda de vídeos de stock a partir de un guion.
- Identificar palabras clave relevantes mediante procesamiento de texto.
- Ampliar las búsquedas utilizando términos en español e inglés.
- Incorporar sinónimos y conceptos visuales mediante un diccionario temático.
- Consultar diferentes combinaciones de palabras clave.
- Descargar vídeos automáticamente desde Pixabay.
- Evitar descargas duplicadas.
- Optimizar las consultas mediante un sistema de caché.

## ⚙️ Tecnologías utilizadas

| Tecnología | Aplicación |
|---|---|
| Python | Desarrollo del programa |
| Requests | Consultas HTTP a la API de Pixabay y descarga de vídeos |
| Pixabay API | Búsqueda de vídeos de stock |
| Regular Expressions (re) | Extracción y limpieza de palabras |
| JSON | Almacenamiento de resultados y caché |
| OS | Gestión de archivos y directorios |
| Unicode | Normalización de caracteres y eliminación de tildes |
| Datetime | Control temporal de la caché |

## 🔍 Funcionamiento del programa

El proceso se divide en varias etapas:

### 1. Lectura del guion

El programa lee automáticamente un archivo llamado `GUION.txt`, ubicado en el Escritorio del usuario.

Cada línea de texto se procesa individualmente.

### 2. Limpieza y extracción de palabras clave

Se eliminan signos de puntuación, palabras vacías (stopwords) y elementos que no aportan información visual.

También se normalizan los caracteres para facilitar la identificación de términos con y sin acentos.

### 3. Generación de consultas bilingües

El programa utiliza un diccionario de conceptos visuales para relacionar palabras del guion con términos de búsqueda en inglés.

Por ejemplo:

| Palabra del guion | Consulta visual |
|---|---|
| Mente | Human mind psychology |
| Cerebro | Human brain neuroscience |
| Evolución | Human evolution science |
| Civilización | Ancient civilization ruins |
| Economía | Economy financial markets |
| Miedo | Fear anxiety darkness |
| Naturaleza | Nature wildlife landscape |

Se generan diferentes consultas para ampliar las posibilidades de encontrar vídeos relacionados.

### 4. Búsqueda mediante Pixabay API

Se realizan consultas a la API oficial de Pixabay, utilizando los idiomas español e inglés.

La búsqueda contempla:
- Diferentes combinaciones de palabras.
- Hasta 50 resultados por consulta.
- Priorización de resultados populares.
- Filtro de contenido seguro.

### 5. Descarga automática

Los vídeos encontrados se descargan directamente mediante Requests.

Se priorizan las siguientes calidades:

1. Large.
2. Medium.
3. Small.

Los archivos se guardan en formato MP4.

### 6. Control de duplicados

Se utiliza un archivo de registro para identificar los vídeos descargados anteriormente.

De esta manera, el programa evita descargar repetidamente los mismos recursos.

### 7. Sistema de caché

Las búsquedas se almacenan temporalmente en un archivo JSON durante 24 horas.

Esto permite reutilizar resultados anteriores y reducir consultas innecesarias a la API.

## 📁 Estructura de archivos

El programa utiliza la siguiente estructura:

```text
Desktop/
│
├── GUION.txt
│
└── stock videos/
    │
    ├── pixabay_123456.mp4
    ├── pixabay_123457.mp4
    ├── downloaded_archive.txt
    └── pixabay_cache.json
```

## 🛠️ Instalación

### Requisitos

- Python 3.9 o superior.
- Conexión a Internet.
- Una cuenta y clave API de Pixabay.

### Instalación de dependencias

Ejecutar en la terminal:

```bash
pip install requests
```

### Configuración de la API

Obtener una clave API desde:

https://pixabay.com/api/docs/

Configurar la clave en el programa mediante una variable de entorno o un archivo de configuración local.

**Importante:** no publicar claves API ni credenciales personales en repositorios públicos de GitHub.

### Ejecución

Guardar el programa Python y colocar el archivo `GUION.txt` en el Escritorio.

Ejecutar:

```bash
python buscador_pixabay.py
```

Los vídeos descargados aparecerán automáticamente en la carpeta `stock videos`.

## 📊 Parámetros configurables

El programa permite modificar diferentes parámetros:

| Parámetro | Valor inicial | Descripción |
|---|---:|---|
| MAX_QUERIES_PER_LINE | 3 | Número máximo de consultas por línea |
| MAX_DOWNLOADS_PER_LINE | 3 | Número máximo de vídeos descargados por línea |
| RESULTADOS_POR_BUSQUEDA | 50 | Resultados consultados por búsqueda |
| ESPERA_ENTRE_BUSQUEDAS | 1 | Pausa entre consultas, en segundos |
| CACHE_HORAS | 24 | Tiempo de conservación de resultados en caché |

## 🚀 Posibles mejoras futuras

El proyecto tiene posibilidades de ampliación:

- Incorporar procesamiento de lenguaje natural (NLP).
- Utilizar técnicas de análisis semántico para interpretar mejor el contenido del guion.
- Implementar traducción automática de conceptos.
- Identificar escenas y párrafos con mayor precisión.
- Incorporar otras plataformas de vídeos de stock mediante sus API.
- Añadir un sistema de clasificación de vídeos por relevancia.
- Crear una interfaz gráfica para facilitar su utilización.
- Generar informes de búsqueda y descarga.

## ⚠️ Consideraciones

- La disponibilidad de resultados depende de la API y del catálogo de Pixabay.
- No todas las consultas generan vídeos descargables.
- La búsqueda automática no garantiza que cada vídeo represente exactamente el contenido narrado.
- Es necesario respetar los límites de solicitudes y las condiciones de uso de Pixabay.
- Antes de publicar los vídeos, se deben revisar las condiciones de licencia aplicables a cada recurso.

## 👩‍💻 Autora

**Jeanette Pérez Carnota**

Proyecto personal de Python orientado a la automatización de búsquedas audiovisuales, procesamiento de texto y utilización de APIs externas.

GitHub: [jeanette-portfolio](https://github.com/jeanette-portfolio)

---

*Proyecto desarrollado con Python como ejercicio práctico de automatización, procesamiento de texto e integración de servicios mediante APIs.*
