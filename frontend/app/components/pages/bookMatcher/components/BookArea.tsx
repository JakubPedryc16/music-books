import styled from "styled-components";

const StyledTextArea = styled.div`
    
`

type Props = {
    text: String;
}

const BookArea = ({text}: Props) => {
    return (
        <StyledTextArea>{text}</StyledTextArea>
    )
}

export default BookArea;