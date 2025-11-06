import type { PageRequest } from "~/components/models/book"
import { useApi } from "./useApi"
import type { BookPageResponse } from "~/components/models/apiTypes";
import api from "~/utils/api";

export const useBookPage = () => {
    return useApi<string, PageRequest> ((body: PageRequest) => 
        api.post<BookPageResponse>("books/page", body)
    );
}