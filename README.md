# 📄 Document AI - Prototipo de Procesamiento de PDFs

Este proyecto automatiza la extracción de metadatos, clasificación y generación de reportes de resoluciones municipales (PDF) utilizando IA (Gemini) y Pydantic.

## 🚀 Configuración Inicial

### 1. Preparar el entorno

```bash
git clone <url-del-repo>
cd document-ai-pdf-prototype
cp .env.example .env
```

> **Nota:** Edita el archivo `.env` y añade tu `GOOGLE_API_KEY`. El sistema soporta rotación automática si añades varias llaves separadas por comas en `GOOGLE_API_KEYS`.

### 2. Instalación de Dependencias

#### Opción A: Usando `uv` (Recomendado)

```bash
# Sincroniza el entorno y las dependencias automáticamente
uv sync
```

#### Opción B: Usando `pip` (Python estándar)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno:
# Windows: venv\Scripts\activate | Linux/Mac: source venv/bin/activate

# Instalar dependencias
pip install -e .
```

### 3. Requisitos del Sistema (OCR)

Para procesar documentos escaneados localmente:

- **Tesseract OCR** (con datos de idioma español)
- **Poppler** (añadir a la ruta de variables de entorno)

---

## 🐳 Despliegue con Docker

El proyecto está dockerizado para facilitar su despliegue sin configurar dependencias locales como Tesseract o Poppler.

### Uso con Docker Compose (Recomendado)

```bash
# Levantar el contenedor
docker compose up -d
```

### Construcción Manual

```bash
# Construir la imagen localmente
docker build -t document-ai-app .

# Ejecutar el contenedor
docker run -p 8501:8501 --env-file .env document-ai-app
```

---

## 💻 Uso del Proyecto

### Ejecutar la Aplicación

```bash
# Con uv
uv run streamlit run main.py

# Con pip (con el entorno activo)
streamlit run main.py
```

### 📝 Convención de Nombres (Crítico)

Para la clasificación automática, los archivos deben seguir el formato:
`[prefijo]_[número]_[fecha].pdf` (Ej: `rtran_282_15122025.pdf`)

**Prefijos soportados:**

- `ralc`: Alcaldía
- `rtran`: Transporte
- `rgm`: Gerencia Municipal
- `rjefa`: Jefatura

---

## 🔄 Flujo General de Datos

```bash
Subida de PDF
      ↓
Extracción de metadatos del nombre
      ↓
Extracción de texto / OCR
      ↓
Análisis semántico con Gemini
      ↓
Validación con Pydantic
      ↓
Almacenamiento en Supabase
      ↓
Generación de reporte Excel
```

## 🧪 Testing

```bash
# Con uv
uv run pytest

# Con pip
pytest
```

## 👥 Mantenimiento y Soporte

**Entidad responsable:**
Municipalidad Provincial de Huamanga (MP-HUAMANGA)
Unidad de Tecnologías de Información y Comunicaciones (UTIC)

**Contacto técnico:**
📧 [ledvirabp@gmail.com](mailto:ledvirabp@gmail.com)

**Última actualización:**
🔄 Marso de 2026
