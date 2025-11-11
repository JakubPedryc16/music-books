import styled from "styled-components";
import { colors } from "~/colors";
import DynamicScrollText from "../utils/DynamicScrollText";
import type { BookData } from "../models/book";

const StyledBookComponent = styled.li`
    display: flex;
    flex-direction: column;
    justify-content: start;
    flex: 1;
    padding: 1rem 2rem;
    background-color: ${colors.darkGrey};
    text-align: center;
    min-width: 0; 

    border: 2px solid ${colors.lightGrey};
    border-radius: 10px;

    &:hover {
        background-color: ${colors.grey};
    }
    
    &:active {
        background-color: ${colors.lightGrey};
    }
    
    &:focus-visible {
        border: solid 2px #3DDC97;
        outline: none;
    }

    h3 {
        font-size: 20px;
        line-height: 32px;
        margin: 0;
    }

    p {
        font-size: 14px;
        line-height: 22px;
    }

`
type Props = {
    book: BookData
    onClick: (bookId: number) => void
}

const BookComponent = ({book, onClick}: Props) => {

    function handleClick() {
        onClick(book.id);
    }

    return (
        <StyledBookComponent onClick={handleClick}>
            <DynamicScrollText><h3>{book.title}</h3></DynamicScrollText>
            <DynamicScrollText><p>{book.author}</p></DynamicScrollText>
        </StyledBookComponent>
    );
}

export default BookComponent