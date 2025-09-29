import api from "~/utils/api"
import { useApi } from "./useApi"
import type { MatchedTracksResponse } from "~/components/models/apiTypes"
import type { MatchTextParams } from "~/components/models/match"

export const useTextMatcher = () => {
    return useApi((params: MatchTextParams) => api.get<MatchedTracksResponse>("/match/text", {
        params: params
    }))
}