import styled from "styled-components";
import InputTextForm from "~/components/textMatcher/InputTextForm";
import TextField from "~/components/common/TextField";
import { textMatcherText } from "~/content/texts";
import MusicResults from "~/components/textMatcher/MusicResults";

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

const StyledSecionsContainer = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: top;
    gap: 2rem;
`


const TextMatcher = () => {
    return (
        <StyledMainContainer>
            <TextField title={"Search By Text"} text={textMatcherText}/>
            <StyledSecionsContainer>
                <InputTextForm/>
                <MusicResults/>
            </StyledSecionsContainer>
        </StyledMainContainer>
    );
}

export default TextMatcher;