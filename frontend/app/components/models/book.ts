export type PageRequest = {
    bookId: number;
    pageIndex: number;
}

export type UploadBookRequest = {
    book: FormData;
}

export type BookData = {
    id: number;
    title: string;
    author: string;
}