from langdetect import detect
import torch
from app.ml_models.models import language_tokenizer, language_model
from app.schemas.matcher_schema import TranslationResponse
from app.utils.logger import logger
import asyncio
from fastapi import HTTPException

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

async def detect_and_translate(text: str) -> str:

    try:
        lang = await asyncio.to_thread(detect, text)
    except Exception as e:
        logger.warning(f"Language detection failed (Client Error): {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Cannot detect language from the provided text. Ensure the text is not empty or too short."
        )

    try:
        if lang == "pl":
            def translate_sync():
                inputs = language_tokenizer(text, return_tensors="pt", truncation=False, padding=True).to(device)
                
                with torch.no_grad():
                    outputs = language_model.generate(**inputs, max_length=512)

                return language_tokenizer.decode(outputs[0], skip_special_tokens=True)

            translated_text = await asyncio.to_thread(translate_sync)
            logger.debug(f"Translated from pl to en: {translated_text}")

            return translated_text

        elif lang == "en":
            logger.debug(f"Language is already English: {text}")
            return text

        else:
            logger.warning(f"Unknown or unsupported language detected: {lang}")
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language detected: '{lang}'. Only Polish (pl) and English (en) are supported for matching."
            )

    except RuntimeError as e:
        logger.error(f"ML Model (Translation) error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal translation service error. Model failure: {e}"
        )
    except Exception as e:
        logger.exception(f"Unexpected error during translation process.")
        raise HTTPException(
            status_code=500,
            detail="An unexpected server error occurred during translation."
        )
