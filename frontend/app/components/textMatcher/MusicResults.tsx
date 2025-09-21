import styled from "styled-components";
import { colors } from "~/colors";
import DynamicScrollText from "../utils/DynamicScrollText";

const StyledMainContainer = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;   

    border-radius: 10px;
    padding: 2rem;
`

const StyledTitle = styled.div`
    font-size: 20px;
    line-height: 32px;
    text-align: center;
`

const StyledTracksContainer = styled.ul`
    display: flex;
    flex-direction: row;
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

const StyledTrackElement = styled.li`
    display: flex;
    flex-direction: column;
    justify-content: start;
    flex: 1;
    padding: 1rem 2rem;
    background-color: ${colors.darkgrey};
    border-radius: 10px;
    text-align: center;
    min-width: 0; 

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
const ScrollWrapper = styled.div`
  width: 100%;
  overflow: hidden;   /* 🔑 ukrywa wszystko, co wychodzi poza rodzica */
`;

const MusicResults = () => {

    return(
        <StyledMainContainer>
            <StyledTitle>Results</StyledTitle>
            <StyledTracksContainer>
                <StyledTrackElement> {/*TODO: create component for element representation*/}
                    <DynamicScrollText><h3>Title</h3></DynamicScrollText>
                    <DynamicScrollText><p>Author Author</p></DynamicScrollText>
                </StyledTrackElement>
                <StyledTrackElement> 
                    <DynamicScrollText><h3>Title</h3></DynamicScrollText>
                    <DynamicScrollText><p>Some Weird Long Name</p></DynamicScrollText>
                </StyledTrackElement>
                <StyledTrackElement>
                     <DynamicScrollText><h3>Title</h3></DynamicScrollText>
                    <DynamicScrollText><p>Some very long name with some additional random thing</p></DynamicScrollText>
                </StyledTrackElement>
            </StyledTracksContainer>
            
        </StyledMainContainer>
    );
};

export default MusicResults;