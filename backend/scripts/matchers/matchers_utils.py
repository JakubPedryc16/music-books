
def print_best_worst(filtered, min_score):
    print(f"[TAGS] Dopasowano {len(filtered)} piosenek (min {min_score})")
    if filtered:
        best_id, best_sim = max(filtered, key=lambda x: x[1])
        worst_id, worst_sim = min(filtered, key=lambda x: x[1])
        print(f"[TAGS] Najlepsze dopasowanie: {best_id} -> {best_sim:.4f}")
        print(f"[TAGS] Najgorsze dopasowanie: {worst_id} -> {worst_sim:.4f}")

def filter_matches(matches, min_score, min_amount, max_amount):
    final_filtered = [(id_, sim) for id_, sim in matches if sim >= min_score]
    if len(final_filtered) < min_amount:
        final_filtered = sorted(matches, key=lambda x: x[1], reverse=True)[:min_amount]
    return final_filtered[:max_amount]

