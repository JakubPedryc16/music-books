
from scripts.matchers.embedding_matcher import match_by_embedding
from scripts.matchers.emotions_matcher import match_by_emotions
from scripts.matchers.features_matcher import match_by_spotify_features
from scripts.matchers.tag_matcher import match_by_tags


async def match_hybrid_all(
    text: str,
    amount: int = 5,
    w_embedding: float = 0.25,
    w_tags: float = 0.25,
    w_spotify: float = 0.25,
    w_emotions: float = 0.25
):
    classic = await match_by_embedding(text, amount=None)
    tags = await match_by_tags(text, amount=None)
    spotify = await match_by_spotify_features(text, amount=None)
    emotions = await match_by_emotions(text, amount=None)

    scores = {}
    for music_id, score in classic:
        scores[music_id] = w_embedding * score
    for music_id, score in tags:
        scores[music_id] = scores.get(music_id, 0) + w_tags * score
    for music_id, score in spotify:
        scores[music_id] = scores.get(music_id, 0) + w_spotify * score
    for music_id, score in emotions:
        scores[music_id] = scores.get(music_id, 0) + w_emotions * score

    music_scored = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return music_scored[:amount]
