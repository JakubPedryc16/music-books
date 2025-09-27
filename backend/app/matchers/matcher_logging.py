
from app.utils.logger import logger

def print_best_worst(filtered, min_score, method = ""):

    logger.info(f"[INFO] {method} Dopasowano {len(filtered)} piosenek (min {min_score})")
    if filtered:
        best_id, best_sim = max(filtered, key=lambda x: x[1])
        worst_id, worst_sim = min(filtered, key=lambda x: x[1])
        logger.info(f"[INFO] {method} Najlepsze dopasowanie: {best_id} -> {best_sim:.4f}")
        logger.info(f"[INFO] {method} Najgorsze dopasowanie: {worst_id} -> {worst_sim:.4f}")


def filter_matches(matches, min_score, min_amount, max_amount):
    final_filtered = [(id_, sim) for id_, sim in matches if sim >= min_score]
    if len(final_filtered) < min_amount:
        final_filtered = sorted(matches, key=lambda x: x[1], reverse=True)[:min_amount]
    return final_filtered[:max_amount]

