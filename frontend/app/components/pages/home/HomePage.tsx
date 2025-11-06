import { useNavigate } from "react-router";
import styled from "styled-components";
import { colors } from "~/colors";
import CustomButton from "~/components/common/CustomButton";
import TextField from "~/components/common/TextField";
import { SpotifyLoginButton } from "~/components/utils/SpotifyLoginButton";
import { homeWelcomeText } from "~/content/texts";

const StyledMainContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 3rem;
  padding-bottom: 4rem;
  width: 80%;
  margin: 0 auto;

  @media(max-width: 768px) {
    gap: 2rem;
  }
`

const StyledBackgroundContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 256px;

  background-image: url("background-image01.webp");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  box-sizing: border-box;
  margin: 0 -12.5%;
  width: 100vw;
  height: 57vw;


  @media (max-width: 1000px) {
    gap: 192px;
  }

  @media (max-width: 768px) {
    gap: 32px;
  }
`

const StyledButtonsContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 5rem;

  @media (max-width: 1000px) {
    gap: 3rem;
  }

  @media (max-width: 768px) {
    flex-direction: column;
    width: 80%;
    gap: 1rem;
  }

`

const StyledTitle = styled.header`
  display: flex;
  justify-content: center;

  font-size: 80px;
  color: white;
  font-weight: 700;
  text-shadow:
    1.5px 1.5px 0.5px ${colors.darkGrey},
   -1.5px -1.5px 0.5px ${colors.darkGrey},
    -1.5px 1.5px 0.5px ${colors.darkGrey},
    1.5px -1.5px 0.5px ${colors.darkGrey};

    @media (max-width: 1000px) {
      font-size: 64px;
    }

    @media (max-width: 768px) {
      font-size: 32px;
    }
`

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <StyledMainContainer>
      <StyledBackgroundContainer>
        <StyledTitle>Music-Books</StyledTitle>
        <StyledButtonsContainer>
          <CustomButton type={"button"} onClick={() => navigate("/text-matcher")}>Match By Fragment</CustomButton>
          {/* <CustomButton type={"button"} onClick={() => navigate("/book-matcher")}>Match By Books</CustomButton> */}
        </StyledButtonsContainer>
      </StyledBackgroundContainer>

      <TextField title={"O Aplikacji Music-Books"} text={homeWelcomeText}/>
    </StyledMainContainer>
  );
};
