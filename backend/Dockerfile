FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Skopiuj plik z wymaganiami i zainstaluj paczki
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj cały projekt
COPY . /app

# Pobranie zasobów NLTK podczas builda
RUN python -m nltk.downloader punkt averaged_perceptron_tagger

# Pobranie modeli Hugging Face podczas builda
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline; \
    AutoTokenizer.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english'); \
    AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english'); \
    pipeline('text-classification', model='j-hartmann/emotion-english-distilroberta-base', return_all_scores=True)"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
