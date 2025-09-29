import styled from "styled-components";
import InputTextForm from "~/components/textMatcher/InputTextForm";
import TextField from "~/components/common/TextField";
import { textMatcherText } from "~/content/texts";
import MusicResults from "~/components/textMatcher/MusicResults";
import { useEffect, useState } from "react";
import type { MatchedTracksResponse } from "~/components/models/apiTypes";
import type { MatchTextParams, SongData } from "~/components/models/match";
import api from "~/utils/api";
import { useTextMatcher } from "~/hooks/useTextMatcher";

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
    const {data, error, loading, execute} = useTextMatcher()
        
    const handleSongMatcher = async (params: MatchTextParams) => {
        execute(params)
    }
    return (
        <StyledMainContainer>
            <TextField title={"Search By Text"} text={textMatcherText}/>
            <StyledSecionsContainer>
                <InputTextForm onSubmit={handleSongMatcher}/>
                <MusicResults tracks={data} loading={loading} error={error}/>
            </StyledSecionsContainer>
        </StyledMainContainer>
    );
}

export default TextMatcher;