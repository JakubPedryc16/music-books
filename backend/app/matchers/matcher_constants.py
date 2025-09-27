
from enum import Enum

class MatcherType(str, Enum):
    embedding = "embedding"
    emotions = "emotions"
    features = "features"
    tags = "tags"
    hybrid = "hybrid"
    hybrid_cascade = "hybrid_cascade"