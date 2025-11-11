import type { AxiosResponse } from "axios";
import { useState } from "react";
import type { APIResponse } from "~/components/models/apiTypes";

type RequestFunction<T, P = void> = (data: P) => Promise<AxiosResponse<APIResponse<T>>>;

export const useApi = <T, P>(request: RequestFunction<T, P>) => {
    const [data, setData] = useState<T | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(false);

    const execute = async (payload: P): Promise<T | null> => {
        setError(null);
        setLoading(true);

        try {
            const { data: response } = await request(payload);

            if (response.success) {
                setData(response.data || null);
                return response.data || null;
            } else {
                setError(response.error || "Unknown error");
                return null;
            }
        } catch (err: any) {
            setError(err.response?.data?.error || err.message || "Network error");
            return null;
        } finally {
            setLoading(false);
        }
    };

    return { data, error, loading, execute };
};
