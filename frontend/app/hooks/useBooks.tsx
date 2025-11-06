import api from "~/utils/api"
import { useApi } from "./useApi"
import type { MatchedTracksResponse } from "~/components/models/apiTypes"
import type { SongData } from "~/components/models/match"

export const useBooks = () => {
    return useApi<SongData[], void> (() => api.get<MatchedTracksResponse>("/books"))
}