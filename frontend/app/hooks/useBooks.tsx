import api from "~/utils/api"
import { useApi } from "./useApi"
import type { MatchedBooksResponse } from "~/components/models/apiTypes"
import type { BookData } from "~/components/models/book"

export const useBooks = () => {
    return useApi<BookData[], void> (() => api.get<MatchedBooksResponse>("/books"))
}