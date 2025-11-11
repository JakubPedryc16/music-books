import api from "~/utils/api";
import { useApi } from "./useApi"
import type { UploadBookResponse } from "~/components/models/apiTypes";

export const useUploadBook = () => {
    return useApi<number, FormData>((formData: FormData) =>
        api.post<UploadBookResponse>("books/upload", formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
    );
}
