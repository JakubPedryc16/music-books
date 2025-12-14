
from app.utils.logger import logger
from app.dal.music_dal import MusicDAL
from typing import Dict, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

def print_best_worst(filtered_matches: List[Tuple[int, float]], requested_min_score: float, matcher_name: str):
    
    amount = len(filtered_matches)
    
    if not filtered_matches:
        logger.info(f"{matcher_name}: Dopasowano 0 piosenek (min {requested_min_score})")
        return

    best_score = filtered_matches[0][1]
    worst_id = filtered_matches[-1][0]
    worst_score = filtered_matches[-1][1]
    
    logger.info(f"{matcher_name}: Dopasowano {amount} piosenek (min {requested_min_score})")
    logger.info(f"{matcher_name}: Najlepsze dopasowanie: {filtered_matches[0][0]} -> {best_score:.4f}")
    
    if worst_score < requested_min_score:
        logger.warning(f"{matcher_name}: UWAGA AWARYJNA: Najgorsze dopasowanie: {worst_id} -> {worst_score:.4f} (Wymagane: {requested_min_score})")
    else:
        logger.info(f"{matcher_name}: Najgorsze dopasowanie: {worst_id} -> {worst_score:.4f}")

def filter_matches(matches: List[Tuple[int, float]], min_score: float, min_amount: int, max_amount: int) -> List[Tuple[int, float]]:
    
    filtered_by_score = [(id_, score) for id_, score in matches if score >= min_score]
    
    if len(filtered_by_score) < min_amount:
        return matches[:min_amount]
    else:
        return filtered_by_score[:max_amount]
   