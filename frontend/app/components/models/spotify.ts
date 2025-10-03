export type PlayResponseData = {
    tracks_count: number;
    played_tracks: string[];
}

export type PlayRequestData = {
    tracks_ids: string[];
}