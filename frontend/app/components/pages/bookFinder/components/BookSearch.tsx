import { useEffect, useMemo, useState } from "react";
import styled from "styled-components";
import { colors } from "~/colors";
import BookComponent from "~/components/common/BookComponent";
import type { BookData } from "~/components/models/book";
import { useBooks } from "~/hooks/useBooks";

const MainComponent = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4rem;
`

const StyledLabel = styled.label`
    font-size: 20px;
    line-height: 32px;
    font-weight: 700;
    text-align: center;
`

const StyledInput = styled.input`
    padding: 8px;

    background-color: ${colors.grey};
    border-radius: 5px;
    border: 2px solid ${colors.lightGrey};
    box-sizing: border-box; 
    box-shadow: 0 0 4px rgba(255, 255, 255, 0.04);

    &:focus {
        outline: none;
        border-color: ${colors.light};
    }
`

const StyledBooksContainer = styled.ul<{$isLong: boolean}>`
    display: flex;
    flex-direction: ${(props) => (props.$isLong ? "column" : "row")};
    justify-content: center;
    width: 100%;
    max-width: 800px;
    padding: 0;
    gap: 1rem;
    background-color: ${colors.grey};
    border-radius: 10px;

    @media (max-width: 768px) {
        flex-direction: column;
    }
`


const BookSearch = () => {

    const bookHook = useBooks()
    const [query, setQuery] = useState<string>("");

    useEffect(() => {
        bookHook.execute();
    }, []);


    const filteredBooks = useMemo(() => {
        if (!bookHook.data) return [];
        return bookHook.data.filter(book =>
            book.title.toLowerCase().includes(query.toLowerCase())
        );
    }, [bookHook.data, query]);

    
    return (
 
        <MainComponent>
            <StyledLabel htmlFor="searchBar">Search Book From Available Ones</StyledLabel>
            <StyledInput
                id="searchBar"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="input book name ..."
            />
            {bookHook.loading && <div>Loading ...</div>}
            {bookHook.error && <div>{bookHook.error}</div>}
                        
            {/* TODO: Separate component for books and maybe generics with MusicResults */}


            <StyledBooksContainer $isLong={filteredBooks.length > 0}>
            {filteredBooks.length > 0 ? (
                filteredBooks.map(book => <BookComponent key={book.id} book={book} />)
            ) : (
                !bookHook.loading && <div>No books found</div>
            )}
            </StyledBooksContainer>

            
        </MainComponent>
    );
}

export default BookSearch;