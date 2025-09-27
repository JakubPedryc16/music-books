from langdetect import detect
from app.ml_models.models import language_tokenizer, language_model
from app.schemas.matcher_schema import TranslationResult
from app.utils.logger import logger
import asyncio

async def detect_and_translate(text: str) -> TranslationResult:
    try:
        lang = await asyncio.to_thread(detect, text)
    except Exception as e:
        logger.warning(f"Language detection failed: {e}")
        return {"success": False, "text": "", "error": "Language detection failed: {e}"}

    try:
        if lang == "pl":
            def translate():
                inputs = language_tokenizer(text, return_tensors="pt")
                outputs = language_model.generate(**inputs, max_length=200)
                return language_tokenizer.decode(outputs[0], skip_special_tokens=True)

            translated_text = await asyncio.to_thread(translate)
            logger.info("pl " + translated_text)
            return {"success": True, "text": translated_text, "error": None}

        elif lang == "eng":
            logger.info("eng " + text)
            return {"success": True, "text": text, "error": None}

        else:
            logger.warning(f"Unknown language detected: {lang}")
            return {"success": False, "text": "", "error": f"Unknown language detected: {lang}"}

    except Exception as e:
        logger.error(f"Translation failed: {e}")
        return {"success": False, "text": "", "error": "Translation failed: {e}"}
