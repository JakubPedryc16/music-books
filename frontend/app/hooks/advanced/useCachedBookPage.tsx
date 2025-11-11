import { useEffect, useRef, useState } from "react";
import { useBookPage } from "../useBookPage";

export const useCachedBookPage = (bookId: number, initialPageIndex: number) => {
  const { execute, loading, error } = useBookPage();
  const cacheRef = useRef<Record<number, string>>({});
  const currentRequestRef = useRef<number | null>(null);
  const [currentIndex, setCurrentIndex] = useState(initialPageIndex);
  const [text, setText] = useState<string>("");

  const loadPage = async (index: number, direction: "next" | "prev" = "next") => {
    if (cacheRef.current[index] !== undefined) {
      setText(cacheRef.current[index]);
      setCurrentIndex(index);
      return;
    }

    currentRequestRef.current = index;
    const res = await execute({ book_id: bookId, page: index + 1 });
    if (currentRequestRef.current !== index) return;

    const pageText = res?.text ?? "";

    if (pageText.trim() === "") {
      const nextIndex = direction === "next" ? index + 1 : index - 1;
      if (nextIndex >= 0) {
        await loadPage(nextIndex, direction);
      }
      return;
    }

    cacheRef.current[index] = pageText;
    setText(pageText);
    setCurrentIndex(index);
  };

  const goNext = () => loadPage(currentIndex + 1, "next");
  const goPrev = () => loadPage(currentIndex - 1, "prev");

  useEffect(() => {
    loadPage(initialPageIndex);
  }, [bookId, initialPageIndex]);

  return { text, loading, error, currentIndex, goNext, goPrev };
};
