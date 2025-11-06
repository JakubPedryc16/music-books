import { useEffect, useRef } from "react";
import { useBookPage } from "../useBookPage";

export const useCachedBookPage = (bookId: number, pageIndex: number) => {
    const { data, loading, error, execute } = useBookPage();
    const cacheRef = useRef<Record<number, string>>({});

    useEffect(() => {
        async function loadPage() {
            if (cacheRef.current[pageIndex]) return;
            await execute({bookId, pageIndex});
            if (data) cacheRef.current[pageIndex] = data;
        }

        loadPage();
    }, [bookId, pageIndex])

    const text = cacheRef.current[pageIndex] ?? data ?? "";

    return {text, loading, error};
}