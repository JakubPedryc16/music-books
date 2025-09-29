
export type SongData = {
    title: string;
    author: string;
    spotify_id: string;
}

export type MatchTextParams = {
  text: string;
  amount?: number;
  matcher_type?: MatcherType;
};

export type MatcherType =
  | "embedding"
  | "emotions"
  | "features"
  | "tags"
  | "hybrid"
  | "hybrid_cascade";