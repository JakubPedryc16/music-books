import styled from "styled-components"
import { colors } from "~/colors"
import TextField from "~/components/common/TextField"
import { bookMatcherText, textMatcherText } from "~/content/texts"
import BookArea from "./components/BookArea"
import ButtonsController from "./components/ButtonsController"
import { useCachedBookPage } from "~/hooks/advanced/useCachedBookPage"
import { useState } from "react"
import { usePlaySpotify } from "~/hooks/usePlaySpotify"
import { useTextMatcher } from "~/hooks/useTextMatcher"
import type { MatchTextParams, SongData } from "~/components/models/match"
import type { PlayRequestData } from "~/components/models/spotify"

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

const StyledBookContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4rem;

    background-color: ${colors.darkGrey};
    padding-bottom: 4rem;
    padding-top: 4rem;
    align-self: center;
    width: 100vw;
`
type Props = {
    bookId?: string;
}
export default function BookMatcherPage({ bookId }: Props) {

    const numericBookId = bookId ? Number(bookId): undefined;
    if (!numericBookId) { 
        console.error("Invalid bookId in URL:", bookId)
        return <p>Invalid book ID</p>
    }

    const [index, setIndex] = useState<number>(0)
    const {text, loading, error} = useCachedBookPage(numericBookId, 0);
    const textMatcher = useTextMatcher();
    const spotify = usePlaySpotify();

    function handleNext() {
        setIndex(index + 1);
    }

    function handlePrevious() {
        setIndex(Math.max(index - 1, 0));
    }

    async function handleSpotify() {
        const matchTextParams: MatchTextParams = {
            text: text,
            amount: 5,
            matcher_type: "hybrid_cascade"
        }
        await textMatcher.execute(matchTextParams);
        if (!textMatcher.error && textMatcher.data) {
            const playSpotifyParams: PlayRequestData = {
                tracks_ids: textMatcher.data.map(tracks => tracks.spotify_id)
            }

            await spotify.execute(playSpotifyParams);
        }
    }

    return (
        <StyledMainContainer>
            <TextField title={"Search By Text"} text={bookMatcherText}/>
            <StyledBookContainer>
                    <BookArea text={loading ? "Loading..." : text} />
                    <ButtonsController
                        onNext={handleNext}
                        onPrevious={handlePrevious}
                        onSpotify={handleSpotify}
                    />
           
                {textMatcher.loading || (spotify.loading && <div>Loading Music ...</div>)}
                {(spotify.error || textMatcher.error) && (
                    <div style={{ color: "red" }}>
                        {spotify.error || textMatcher.error}
                    </div>
                )}

            </StyledBookContainer>
        </StyledMainContainer>
    )
}