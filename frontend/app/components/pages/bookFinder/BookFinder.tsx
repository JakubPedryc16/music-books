import styled from "styled-components"
import { colors } from "~/colors"
import TextField from "~/components/common/TextField"
import { bookFinderText, bookMatcherText, textMatcherText } from "~/content/texts"
import UploadBookForm from "./components/UploadBookForm"
import BookSearch from "./components/BookSearch"

const StyledMainContainer = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 80%;
    margin: 0 auto;
    gap: 3rem;
    padding-bottom: 4rem;
    padding-top: 4rem;
    
    @media(max-width: 768px) {
        gap: 2rem;
    }
`

const StyledBookContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4rem;

    background-color: ${colors.darkGrey};
    padding-bottom: 4rem;
    padding-top: 4rem;
    align-self: center;
    width: 100vw;
`



export default function BookFinderPage() {

    return (
        <StyledMainContainer>
            <TextField title={"Search available books or upload your own"} text={bookFinderText}/>
            <UploadBookForm/>
            <BookSearch/>
        </StyledMainContainer>
    )
}