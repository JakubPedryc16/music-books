import styled from "styled-components";
import { colors } from "~/colors";
import DynamicScrollText from "../utils/DynamicScrollText";
import type { SongData } from "../models/match";

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

type Props = {
    tracks?: SongData[] | null,
    loading: boolean,
    error: string | null
}

const MusicResults = ({tracks, loading, error} : Props) => {
    if (loading) return <p>Loading ...</p>
    if (error) return <p>Error: {error}</p>
    if (!tracks || tracks.length == 0) return <></>

    return(
        <StyledMainContainer>
            <StyledTitle>Results</StyledTitle>
            <StyledTracksContainer>
                <StyledTrackElement> {/*TODO: create component for element representation*/}
                    <DynamicScrollText><h3>{tracks[0].title}</h3></DynamicScrollText>
                    <DynamicScrollText><p>{tracks[0].author}</p></DynamicScrollText>
                </StyledTrackElement>
                <StyledTrackElement> 
                    <DynamicScrollText><h3>{tracks[1].title}</h3></DynamicScrollText>
                    <DynamicScrollText><p>{tracks[1].author}</p></DynamicScrollText>
                </StyledTrackElement>
                <StyledTrackElement>
                     <DynamicScrollText><h3>{tracks[2].title}</h3></DynamicScrollText>
                    <DynamicScrollText><p>{tracks[2].author}</p></DynamicScrollText>
                </StyledTrackElement>
            </StyledTracksContainer>
            
        </StyledMainContainer>
    );
};

export default MusicResults;