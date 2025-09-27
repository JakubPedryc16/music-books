import os
from sentence_transformers import SentenceTransformer
import numpy as np
import json

model = SentenceTransformer("all-MiniLM-L6-v2")

TAGS = [
    # Emocje i nastroje
    "happy", "sad", "energetic", "calm", "dark", "motivational",
    "uplifting", "angry", "nostalgic", "mysterious", "lonely", "playful",
    "melancholic", "hopeful", "romantic", "tense", "peaceful", "dramatic tension",
    "whimsical", "dreamy", "tragic", "cheerful", "sentimental", "bittersweet",

    # Gatunki i tematy książek/muzyki
    "mystery", "fantasy", "adventure", "science fiction", "history", "love",
    "friendship", "betrayal", "war", "peace", "thriller", "crime", "drama",
    "philosophy", "psychology", "horror", "comedy", "action",
    "biography", "self-help", "spirituality", "politics", "social issues",
    "environment", "technology", "dystopia", "utopia", "coming of age",
    "romance", "tragedy", "family saga", "epic saga", "detective", "crime noir",
    "mythology", "legend", "folklore", "satirical fiction", "science", "memoir",

    # Motywy, style narracyjne i muzyczne
    "storytelling", "poetry", "dark humor", "satire", "epic", "introspective",
    "cinematic", "instrumental", "vocal", "narrative", "lyrical", "haunting",
    "minimalist", "orchestral", "ambient", "gothic", "romanticism", "baroque",
    "folk", "jazz-inspired", "dramatic arc", "emotional journey", "imaginative",

    # Dodatkowe uniwersalne
    "relaxing", "dramatic", "intense", "emotional", "uplifting", "thought-provoking",
    "atmospheric", "mysterious ambiance", "energetic rhythm", "reflective", "meditative"
]

tag_embeddings = model.encode(TAGS, convert_to_numpy=True, normalize_embeddings=True)

CONFIG_DIR = "data/tags/"
os.makedirs(CONFIG_DIR, exist_ok=True)

TAGS_FILE = os.path.join(CONFIG_DIR, "tags.json")
EMBEDDINGS_FILE = os.path.join(CONFIG_DIR, "tag_embeddings.npy")


np.save(EMBEDDINGS_FILE, tag_embeddings)
with open(TAGS_FILE, "w") as f:
    json.dump(TAGS, f)