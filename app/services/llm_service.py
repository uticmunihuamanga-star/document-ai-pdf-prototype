import logging
import time
from typing import cast
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings
from app.models.document import DatosExtraidosLLM
from app.prompts.extract_prompt import crear_prompt_extraccion_documentos
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GestorLlaves:

    def __init__(self, llaves: list[str]):
        if not llaves:
            raise ValueError('CRÍTICO: No hay GOOGLE_API_KEYS configuradas en el entorno.')
        self.llaves = llaves
        self.indice_actual = 0

    def obtener_llave_actual(self) -> str:
        return self.llaves[self.indice_actual]

    def rotar_llave(self) -> None:
        self.indice_actual = (self.indice_actual + 1) % len(self.llaves)
gestor_llaves = GestorLlaves(settings.lista_llaves)

def get_extractor_chain(api_key: str):
    modelo_base = ChatGoogleGenerativeAI(model=settings.AI_MODEL, google_api_key=api_key, temperature=0.0, max_retries=1, request_timeout=settings.REQUEST_TIMEOUT)
    modelo_estructurado = modelo_base.with_structured_output(DatosExtraidosLLM)
    chat_prompt = crear_prompt_extraccion_documentos()
    return chat_prompt | modelo_estructurado

def extraer_datos_documento(texto_documento: str) -> DatosExtraidosLLM:
    intentos = 0
    max_intentos = len(gestor_llaves.llaves)
    while intentos < max_intentos:
        llave_actual = gestor_llaves.obtener_llave_actual()
        num_llave = gestor_llaves.indice_actual + 1
        try:
            logger.info(f'🧠 Gemini (Llave {num_llave}/{max_intentos}) - Analizando {len(texto_documento)} chars...')
            cadena = get_extractor_chain(llave_actual)
            raw_result = cadena.invoke({'text': texto_documento})
            resultado = cast(DatosExtraidosLLM, raw_result)
            logger.info('✅ Extracción LLM exitosa.')
            return resultado
        except Exception as e:
            intentos += 1
            error_msg = str(e).lower()
            if '429' in error_msg or 'resource_exhausted' in error_msg or 'quota' in error_msg:
                logger.warning(f'⚠️ Llave {num_llave} AGOTADA (Error 429). Rotando a la siguiente API Key...')
            else:
                logger.warning(f'⚠️ Error técnico en Llave {num_llave}: {str(e)}. Reintentando con siguiente llave...')
            gestor_llaves.rotar_llave()
            if intentos < max_intentos:
                time.sleep(2)
                continue
            else:
                logger.error('❌ TODAS LAS LLAVES DE RESPALDO SE HAN AGOTADO O FALLARON.')
                break
    return DatosExtraidosLLM(nombre_norma_opcional=None, contenido_resolutivo='⚠️ ERROR: No se pudo extraer la información. Verifique cuotas o errores del sistema.', resumen_ejecutivo='No disponible.')
