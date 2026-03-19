from functools import lru_cache
from pathlib import Path
from pydantic import Field, field_validator, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
import sys

class Settings(BaseSettings):
    GOOGLE_API_KEYS: str = Field(..., min_length=1)
    AI_MODEL: str = Field(default='gemini-2.5-flash-lite', min_length=1)
    LOG_LEVEL: str = 'INFO'
    MAX_RETRIES: int = 2
    REQUEST_TIMEOUT: int = 60
    TESSERACT_PATH: Path
    POPPLER_PATH: Path
    SUPABASE_URL: HttpUrl
    SUPABASE_KEY: str
    SUPABASE_BUCKET: str = 'documentos'

    @property
    def lista_llaves(self) -> list[str]:
        return [llave.strip() for llave in self.GOOGLE_API_KEYS.split(',') if llave.strip()]

    @field_validator('TESSERACT_PATH')
    @classmethod
    def validar_tesseract(cls, v: Path):
        if sys.platform.startswith('win'):
            if not v.exists():
                raise ValueError(f'TESSERACT_PATH no existe: {v}')
            if not v.is_file():
                raise ValueError('TESSERACT_PATH debe ser un archivo .exe')
        elif not v.exists():
            raise ValueError(f"TESSERACT_PATH no existe: {v}. Instala con 'apt-get install tesseract-ocr'")
        return v

    @field_validator('POPPLER_PATH')
    @classmethod
    def validar_poppler(cls, v: Path):
        if sys.platform.startswith('win'):
            if not v.exists():
                raise ValueError(f'POPPLER_PATH no existe: {v}')
            if not v.is_dir():
                raise ValueError('POPPLER_PATH debe ser un directorio')
        elif not v.exists():
            raise ValueError(f"POPPLER_PATH no existe: {v}. Instala con 'apt-get install poppler-utils'")
        return v
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True, extra='forbid')

@lru_cache
def get_settings() -> Settings:
    return Settings()
settings = get_settings()
