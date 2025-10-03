import styled from "styled-components";
import { colors } from "~/colors";
import DynamicScrollText from "../utils/DynamicScrollText";
import type { SongData } from "../models/match";

const StyledTrackElement = styled.li`
    display: flex;
    flex-direction: column;
    justify-content: start;
    flex: 1;
    padding: 1rem 2rem;
    background-color: ${colors.darkGrey};
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

type Props = {
    track: SongData
}

const TrackComponent = ({track}: Props) => {
    return (
        <StyledTrackElement>
            <DynamicScrollText><h3>{track.title}</h3></DynamicScrollText>
            <DynamicScrollText><p>{track.author}</p></DynamicScrollText>
        </StyledTrackElement>
    );
}

export default TrackComponent