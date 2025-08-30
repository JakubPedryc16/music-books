import asyncio
import json
import re
import sys

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from app.models.music import Music
from app.dal.music_dal import MusicDAL
from scripts.matchers.emotions_matcher import match_by_emotions
from scripts.matchers.features_matcher import match_by_spotify_features
from scripts.matchers.hybrid_all_matcher import match_hybrid_all
from scripts.matchers.hybrid_cascade_matcher import match_hybrid_cascade
from scripts.matchers.tag_matcher import match_by_tags
from scripts.matchers.embedding_matcher import match_by_embedding
from scripts.embedding import create_classic_embedding_async, create_tag_embedding_from_embeddings_async
from scripts.utils.spotify_utils import play_playlist
from app.db.db_async import AsyncSessionLocal
from sqlalchemy import select

from scripts.tag import TAGS
from scripts.ml_models.models import model_emotions

from textblob import TextBlob
from transformers import pipeline


import torch
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter

# # upewnij się, że masz pobrane zasoby NLTK
# nltk.download("punkt")
# nltk.download('punkt_tab')
# nltk.download('averaged_perceptron_tagger_eng')
# nltk.download("averaged_perceptron_tagger")

# tokenizer i model sentymentu

# emotion_classifier = pipeline("text-classification", 
#                               model="j-hartmann/emotion-english-distilroberta-base", 
#                               return_all_scores=True)




async def test_book_matching_param(
    text: str,
    method: int = 1,
    top_n: int = 5  # zmieniamy na 5 piosenek
):
    if method == 1:
        matches = await match_by_embedding(text, amount=top_n)
        method_name = "klasyczne embeddingi"
    elif method == 2:
        matches = await match_by_tags(text, amount=top_n)
        method_name = "dopasowanie po tagach"
    elif method == 3:
        matches = await match_by_spotify_features(text, amount=top_n)
        method_name = "heurystyczne dopasowanie Spotify features"
    elif method == 4:
        matches = await match_by_emotions(text, amount=top_n)
        method_name = "dopasowanie po emocjach"
    elif method == 5:
        matches = await match_hybrid_all(text, amount=top_n)
        method_name = "hybrydowe dopasowanie"
    elif method == 6:
        matches = await match_hybrid_cascade(text, amount=top_n)
        method_name = "hybrydowe dopasowanie kaskadowe"

    else:
        print("❌ Niepoprawny parametr metody. Wybierz 1, 2 lub 3.")
        return

    print(f"\n--- Top {top_n} dopasowań metodą: {method_name} ---")
    
    track_uris = []
    async with AsyncSessionLocal() as session:
        for idx, (music_id, score) in enumerate(matches):
            music = await session.get(Music, music_id)
            print(f"\n🎵 {music.title} - {music.author} - {music.id} (similarity: {score:.4f})")
            track_uris.append(f"spotify:track:{music.spotify_id}")  # zakładam pole spotify_id

    # Odtwarzamy wszystkie top utwory jako kolejkę
    play_playlist(track_uris)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: python script.py <metoda:1|2|3>")
        sys.exit(1)

    method_param = int(sys.argv[1])
    TEXT =  """ 
meow meow meow meow meow meow meow cat cat meow meow meow"""
    
    asyncio.run(test_book_matching_param(TEXT, method=method_param, top_n=5))
