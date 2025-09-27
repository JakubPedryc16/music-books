import json
import os

import numpy as np
from app.ml_models.models import (
    embedding_model,
    emotion_model,
    emotion_tokenizer,
    emotion_labels,
    sentiment_model,
    sentiment_tokenizer
)
from app.services.embedding_service import EmbeddingService
from app.core.config import settings

from app.matchers.matcher import Matcher
from app.matchers.matcher_constants import MatcherType
from app.matchers import (
    EmbeddingMatcher,
    EmotionsMatcher,
    TagsMatcher,
    FeaturesMatcher,
    HybridAllMatcher,
    HybridCascadeMatcher
)

embedding_service: EmbeddingService | None = None

def get_embedding_service():
    if embedding_service is None:
        raise RuntimeError("Embedding service not initialized yet")
    return embedding_service

with open(settings.TAGS_FILE, "r") as f:
    TAGS = json.load(f)

tag_embeddings = np.load(settings.EMBEDDINGS_FILE)

def init_embedding_service():
    os.makedirs(settings.CONFIG_DIR, exist_ok=True)
    
    global embedding_service 
    embedding_service = EmbeddingService(
        tags=TAGS,
        tag_embeddings=tag_embeddings,
        embedding_model=embedding_model,
        emotion_model=emotion_model,
        emotion_tokenizer=emotion_tokenizer,
        emotion_labels=emotion_labels,
        sentiment_model=sentiment_model,
        sentiment_tokenizer=sentiment_tokenizer
    )

embedding_matcher: EmbeddingMatcher | None = None
emotions_matcher: EmotionsMatcher | None = None
features_matcher: FeaturesMatcher | None = None
tags_matcher: TagsMatcher | None = None
hybrid_all_matcher: HybridAllMatcher | None = None
hybrid_cascade_matcher: HybridCascadeMatcher | None = None  

def get_matcher(matcher_type: MatcherType) -> Matcher:
    singletons = {
        MatcherType.embedding: embedding_matcher,
        MatcherType.emotions: emotions_matcher,
        MatcherType.features: features_matcher,
        MatcherType.tags: tags_matcher,
        MatcherType.hybrid: hybrid_all_matcher,
        MatcherType.hybrid_cascade: hybrid_cascade_matcher
    }

    matcher = singletons.get(matcher_type)
    if matcher is None:
        raise RuntimeError(f"Matcher {matcher_type} not initialized yet")
    return matcher


def init_matchers():
    global embedding_matcher
    global emotions_matcher
    global features_matcher
    global tags_matcher
    global hybrid_all_matcher
    global hybrid_cascade_matcher

    embedding_matcher = EmbeddingMatcher(embedding_service)
    emotions_matcher = EmotionsMatcher(embedding_service)
    features_matcher = FeaturesMatcher(embedding_service)
    tags_matcher = TagsMatcher(embedding_service)

    hybrid_all_matcher = HybridAllMatcher(
        embedding_matcher=embedding_matcher,
        emotions_matcher=emotions_matcher,
        features_matcher=features_matcher,
        tags_matcher=tags_matcher
    )

    hybrid_cascade_matcher = HybridCascadeMatcher(
        embedding_matcher=embedding_matcher,
        emotions_matcher=emotions_matcher,
        features_matcher=features_matcher,
        tags_matcher=tags_matcher
    )