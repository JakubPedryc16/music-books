import api from "~/utils/api"
import { useApi } from "./useApi"
import type { MatchedTracksResponse } from "~/components/models/apiTypes"
import type { PlayRequestData } from "~/components/models/spotify"

export const usePlaySpotify = () => {
    return useApi((body: PlayRequestData) => api.post<MatchedTracksResponse>("/spotify/play", body))
}