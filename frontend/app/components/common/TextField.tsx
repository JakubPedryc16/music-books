import styled from "styled-components";

interface TextFieldProps {
    title: String,
    text: String
}

const StyledFieldContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 1100px;
    align-self: center;
    max-width: 800px;
`

const StyledFieldTitle = styled.h1`
    font-size: 32px;
    line-height: 42px;
    margin: 0;
    
    @media (max-width: 768px) {
        font-size: 20px;
        line-height: 32px;
    }
`
const StyledFieldText = styled.p`
    font-size: 18px;
    line-height: 28px;
    @media (max-width: 768px) {
        font-size: 16px;
        line-height: 24px;
    }
`

const TextField = ({title, text} : TextFieldProps) => {
    return (
        <StyledFieldContainer>
            <StyledFieldTitle>{title}</StyledFieldTitle>
            <StyledFieldText>{text}</StyledFieldText>
        </StyledFieldContainer>
    );
}

export default TextField