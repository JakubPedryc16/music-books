from transformers import pipeline
from sentence_transformers import SentenceTransformer 
import numpy as np

from backend.scripts.spotify_features import spotify_features_to_text


classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
model = SentenceTransformer("all-MiniLM-L6-v2")

def create_classic_embedding(text: str) -> bytes:
    embedding_vector = model.encode(text, convert_to_numpy=True)
    return embedding_vector.astype(np.float32).tobytes()

def create_tag_embedding(text: str, candidate_labels: list) -> dict:
    result = classifier(text, candidate_labels)
    tag_probs = dict(zip(result["labels"], result["scores"]))
    return tag_probs

def create_tag_embedding_with_spotify(text: str, spotify_features: dict, candidate_labels: list) -> dict:
    spotify_desc = spotify_features_to_text(spotify_features)
    full_text = f"{text.strip()}\n\n{spotify_desc.strip()}"
    return create_tag_embedding(full_text, candidate_labels)
