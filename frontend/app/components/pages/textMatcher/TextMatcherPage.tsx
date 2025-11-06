import styled from "styled-components";
import InputTextForm from "~/components/pages/textMatcher/components/InputTextForm";
import TextField from "~/components/common/TextField";
import { textMatcherText } from "~/content/texts";
import MusicResults from "~/components/pages/textMatcher/components/MusicResults";
import type { MatchTextParams, SongData } from "~/components/models/match";
import api from "~/utils/api";
import { useTextMatcher } from "~/hooks/useTextMatcher";
import { usePlaySpotify } from "~/hooks/usePlaySpotify";
import type { PlayRequestData } from "~/components/models/spotify";

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


const TextMatcherPage = () => {
    const textMatcher = useTextMatcher()
    const spotifyPlayer = usePlaySpotify()

    const handleSongMatcher = async (params: MatchTextParams) => {
        textMatcher.execute(params)
    }

    const handlePlaySpotify = async (data: SongData[]) => {
        const ids: PlayRequestData = { tracks_ids: data.map((elem) => elem.spotify_id)}
        spotifyPlayer.execute(ids)
    }

    return (
        <StyledMainContainer>
            <TextField title={"Search By Text"} text={textMatcherText}/>
            <StyledSecionsContainer>
                <InputTextForm onSubmit={handleSongMatcher}/>
                <MusicResults 
                    tracks={textMatcher.data}
                    loading={textMatcher.loading} 
                    error={textMatcher.error} 
                    onClick={handlePlaySpotify}
                />
            </StyledSecionsContainer>
        </StyledMainContainer>
    );
}

export default TextMatcherPage;