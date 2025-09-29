import type { SongData } from "./match";
import type { PlayResponseData } from "./spotify";

export interface APIResponse<T> {
    success: boolean;
    data?: T;
    error?: string;
}

export type TranslationResponse = APIResponse<string>;

export type PlayResponse = APIResponse<PlayResponseData>

export type MatchedTracksResponse = APIResponse<SongData[]>
