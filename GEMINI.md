# 🤖 Document AI - Gemini Context

This project is an advanced prototype for the automated processing of administrative PDF documents (municipal resolutions) using AI. It leverages **Gemini API** (via LangChain), **Pydantic v2** for structured extraction, and **Streamlit** for the user interface.

## 🏗️ Project Overview

- **Core Purpose:** Automate metadata extraction, classification, and reporting from municipal PDF resolutions.
- **Architecture:**
  - **Frontend:** Streamlit-based UI for uploading, processing, and visualization.
  - **Processing Pipeline:** Prefix-based classification -> Text/OCR Extraction -> LLM Semantic Analysis -> Structured Validation -> Storage/Reporting.
  - **Key Services:**
    - `llm_service.py`: Integrates Gemini with API key rotation and Pydantic structured output.
    - `pdf_service.py`: Orchestrates text extraction and OCR (using Tesseract/Poppler).
    - `excel_service.py`: Generates formatted reports using `pandas` and `openpyxl`.
    - `storage_service.py`: Handles document persistence in Supabase.
- **Primary Technologies:** Python 3.12, LangChain, Gemini 2.5 Flash, Pydantic, Streamlit, Tesseract OCR, Supabase, UV.

## 🚀 Building and Running

### Prerequisites

- Python 3.12+
- **Tesseract OCR** and **Poppler** installed on the system.
- Google Gemini API Key(s).

### Setup

```powershell
# 1. Install dependencies (using uv or pip)
pip install -e ".[dev]"

# 2. Configure environment
copy .env.example .env
# Required: GOOGLE_API_KEYS, TESSERACT_PATH, POPPLER_PATH, SUPABASE_URL/KEY
```

### Running the Application

```powershell
streamlit run main.py
```

### Testing

```powershell
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=app
```

### Docker

```powershell
docker compose up --build
```

## 🛠️ Development Conventions

### File Naming Convention

The system relies on a specific prefix-based naming convention for automatic classification:

- `[prefix]_[number]_[date].pdf` (e.g., `rtran_282_15122025.pdf`).
- Prefixes: `ralc` (Alcaldía), `rtran` (Transporte), `rgm` (Gerencia Municipal), etc.
- **Fe de Erratas:** Files ending in `_fe.pdf` receive special processing logic.

### API Key Management

- Supports multiple Gemini API keys in `.env` (comma-separated).
- `llm_service.py` implements automatic rotation on `429 (Resource Exhausted)` errors.

### Data Validation

- All document data must pass through Pydantic models in `app/models/`.
- **Structured Output:** The LLM is forced to respond in JSON format matching the Pydantic schemas.

### Project Structure

- `app/core/`: Configuration and global settings.
- `app/models/`: Domain models and Pydantic schemas.
- `app/services/`: Business logic and external integrations.
- `app/ui/`: Streamlit components and page layout.
- `app/utils/`: Shared utilities and parsers.

## 📝 Roadmap & Current Status

- [x] Text extraction and prefix classification.
- [x] Gemini integration with structured output.
- [x] Excel report generation.
- [x] API Key rotation.
- [x] OCR support for scanned documents.
- [ ] Dashboard for processing metrics.
- [ ] Async processing for large batches.
