import styled from "styled-components";
import { colors } from "~/colors";
import DynamicScrollText from "../../../utils/DynamicScrollText";
import type { SongData } from "../../../models/match";
import TrackComponent from "~/components/common/TrackComponent";
import CustomButton from "~/components/common/CustomButton";
import type { ButtonHTMLAttributes } from "react";
import LoadingComponent from "~/components/utils/LoadingComponent";

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

const StyledTracksContainer = styled.ul<{$isLong: boolean}>`
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
type Props = {
    tracks?: SongData[] | null,
    loading: boolean,
    error: string | null,
    onClick: (data: SongData[]) => void
}

const MusicResults = ({tracks, loading, error, onClick} : Props) => {

    if (loading) return <LoadingComponent/>
    if (error) return <p>Error: {error}</p>
    if (!tracks || tracks.length == 0) return <></>

    const handleClick = () => {
        onClick(tracks);
    }

    return(
        <StyledMainContainer>
            <StyledTitle>Results</StyledTitle>
            <StyledTracksContainer $isLong={tracks.length > 3}>
               {tracks.map((track) => (
                <TrackComponent key={track.spotify_id} track={track}/>
               ))}
            </StyledTracksContainer>
            <CustomButton type="button" onClick={handleClick}>Play</CustomButton>
        </StyledMainContainer>
    );
};

export default MusicResults;