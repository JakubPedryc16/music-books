import api from "~/utils/api";
import { useApi } from "./useApi"
import type { UploadBookRequest } from "~/components/models/book";
import type { UploadBookResponse } from "~/components/models/apiTypes";

export const useUploadBook = () => {
    return useApi<number, UploadBookRequest> ((body: UploadBookRequest) => 
        api.post<UploadBookResponse>("book/upload", body)
    );
}