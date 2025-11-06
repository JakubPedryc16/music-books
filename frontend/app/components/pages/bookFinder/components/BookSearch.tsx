import { useEffect } from "react";
import styled from "styled-components";
import { colors } from "~/colors";
import BookComponent from "~/components/common/BookComponent";
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

    useEffect (() => {
        bookHook.execute();
    }, [])



    return (
 
        <MainComponent>
            <StyledLabel htmlFor="searchBar">Search Book From Available Ones</StyledLabel>
            <StyledInput placeholder="input book name ..."/>
            {bookHook.loading && <div>Loading ...</div>}
            {bookHook.error && <div>{bookHook.error}</div>}
            
            //TODO : Seperate component for books and maybe generics with MusicResults
            
            <StyledBooksContainer $isLong = {bookHook.data && bookHook.data.length > 0 ? true : false}>
                {(bookHook.data && bookHook.data.length) && bookHook.data.map(book => <BookComponent book={book}/>)}
            </StyledBooksContainer>
            
        </MainComponent>
    );
}

export default BookSearch;