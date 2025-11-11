export type PageRequest = {
    book_id: number;
    page: number;
}

export type UploadBookRequest = {
    book: FormData;
}

export type BookData = {
    id: number;
    title: string;
    author: string;
}

export type BookPageData = {
    id: number;
    page: number;
    text: string;
}