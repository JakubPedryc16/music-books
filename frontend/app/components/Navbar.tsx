import { useState } from "react";
import { NavLink } from "react-router-dom";
import styled from "styled-components";
import { colors } from "app/colors" 
import { SpotifyLoginButton } from "./utils/SpotifyLoginButton";


const StyledNav = styled.nav`
    display: flex;
    flex-direction: row;
    align-items: center;

    background-color: ${colors.darkGrey};
    padding: 0.75rem 10vw 0.5rem 10vw;

    @media (max-width: 768px) {
        flex-direction: column;
        padding: 1rem 10vw 1rem 10vw;
    }
`

interface LinksContainerProps {
  $isVisible?: boolean;
}

const StyledLinksContainer = styled.div<LinksContainerProps>`
    display: flex;
    flex-direction: row;
    box-sizing: border-box;

    @media (max-width: 768px) {
        flex-direction: column;
        align-items: center;

        background-color: ${colors.darkGrey};
        display: ${props => (props.$isVisible ? "flex" : "none")};

        width: 100%;
        padding: 2rem 3rem 2rem 3rem;
        border-radius: 10px;
    }
`

const StyledNavLink = styled(NavLink)`
    justify-content: start;
    text-decoration: none;
    color: white;

    padding: 1rem 2rem;
    border-radius: 5px;

    &:hover {
        background-color: ${colors.grey};
    }

    @media (max-width: 768px) {
        width: 100%;
        padding: 1rem 0rem;
        border-bottom: 2px solid ${colors.grey};
        border-radius: 0;
    }
`

const StyledIconsContainer = styled.div`
    width: auto;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 32px;

    @media (max-width: 768px) {
        width: 100%;
    }
`

const StyledImage = styled.img`
    width: 64px;
    height: auto;

    @media (max-width: 768px) {
        width: 48px;
    }
`

const Burger = styled.div`
    display: none;
    flex-direction: column;
    gap: 5px;

    cursor: pointer;

    span {
        width: 25px;
        height: 3px;
        background: white;
    }

    @media (max-width: 768px) {
        display: flex;
    }
`;

const StyledLoginContainer = styled.div`
    
`


const Navbar = () => {
    const [isMobile, setIsMobile] = useState<boolean>(false)

    return (
        <StyledNav>
            <StyledIconsContainer>
                <StyledImage src="logo.webp"></StyledImage>
                <SpotifyLoginButton $variant="secondary" $size="small">Login Spotify</SpotifyLoginButton>
                <Burger onClick={() => setIsMobile(!isMobile)}>
                    <span></span>
                    <span></span>
                    <span></span>
                </Burger>
            </StyledIconsContainer>
           
            <StyledLinksContainer $isVisible={isMobile}>
                <StyledNavLink to="/">Home</StyledNavLink>
                <StyledNavLink to="/text-matcher">Find By Text</StyledNavLink>
                {/* <StyledNavLink to="/">Find By Book</StyledNavLink> */}
            </StyledLinksContainer>

        </StyledNav>
    );
};

export default Navbar;