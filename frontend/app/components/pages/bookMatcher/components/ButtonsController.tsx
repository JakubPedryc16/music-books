import styled from "styled-components";
import CustomButton from "~/components/common/CustomButton";

const StyledButtonContainer = styled.div`
    display: flex;
    flex-direction: row;
    gap: 2rem;

    @media (max-width: 768px){
        flex-direction: column;
    }
`

type Props = {
    onPrevious: () => void;
    onNext: () => void;
    onSpotify: () => void;
}

const ButtonsController = ({onPrevious, onNext, onSpotify}: Props) => {

    const handlePrevious = () => {
        onPrevious();
    }

    const handleNext = () => {
        onNext();
    }

    const handleSpotify = () => {
        onSpotify();
    }
    return (
    <StyledButtonContainer>
        <CustomButton type="button" onClick={handlePrevious}> Previous </CustomButton>
        <CustomButton type="button" onClick={handleSpotify}> Spotify </CustomButton>
        <CustomButton type="button" onClick={handleNext}> Next </CustomButton>
    </StyledButtonContainer>
)};

export default ButtonsController;