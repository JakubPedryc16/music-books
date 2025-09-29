from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer

import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
import torch
print(torch.__version__)
print(torch.version.cuda)
print(torch.backends.cudnn.enabled)
print(torch.cuda.is_available())
embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device=device)

emotion_model_name = "j-hartmann/emotion-english-distilroberta-base"
emotion_tokenizer = AutoTokenizer.from_pretrained(emotion_model_name)
emotion_model = AutoModelForSequenceClassification.from_pretrained(emotion_model_name).to(device)
emotion_labels = emotion_model.config.id2label

sentiment_tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
sentiment_model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english").to(device)

language_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-pl-en")
language_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-pl-en").to(device)
