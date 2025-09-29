from langdetect import detect
import torch
from app.ml_models.models import language_tokenizer, language_model
from app.schemas.matcher_schema import TranslationResponse
from app.utils.logger import logger
import asyncio
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
async def detect_and_translate(text: str) -> TranslationResponse:
    try:
        lang = await asyncio.to_thread(detect, text)
    except Exception as e:
        logger.warning(f"Language detection failed: {e}")
        return {"success": False, "text": "", "error": "Language detection failed: {e}"}

    try:
        if lang == "pl":
            def translate():
                inputs = language_tokenizer(text, return_tensors="pt", truncation=False, padding=True).to(device)
                outputs = language_model.generate(**inputs, max_length=512)

                return language_tokenizer.decode(outputs[0], skip_special_tokens=True)

            translated_text = await asyncio.to_thread(translate)
            logger.debug("pl " + translated_text)

            return TranslationResponse(success=True, data=translated_text)

        elif lang == "en":
            logger.debug("en " + text)
            return TranslationResponse(success=True, data=text)

        else:
            logger.warning(f"Unknown language detected: {lang}")
            return TranslationResponse(success=False, error=f"Unknown language detected: {lang}")

    except Exception as e:
        logger.error(f"Translation failed: {e}")
        return TranslationResponse(success=False, error=f"Translation failed: {e}")
