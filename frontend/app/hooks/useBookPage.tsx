import type { BookPageData, PageRequest } from "~/components/models/book"
import { useApi } from "./useApi"
import type { BookPageResponse } from "~/components/models/apiTypes";
import api from "~/utils/api";

export const useBookPage = () => {
    return useApi<BookPageData, PageRequest>((params: PageRequest) =>
        api.get<BookPageResponse>("books/page", { params })
    );
};