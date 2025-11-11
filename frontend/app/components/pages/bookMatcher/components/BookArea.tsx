import styled from "styled-components";

const StyledTextArea = styled.div`
    font-size: 18px;
    line-height: 32px;
    max-width: 800px;
    @media (max-width: 768px) {
        font-size: 16px;
        line-height: 24px;
    }
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