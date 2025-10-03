import type { ReactNode } from "react";
import styled from "styled-components"
import { colors } from "~/colors";


interface ButtonProps {
    children: ReactNode;
    type: "button" | "submit";
    onClick?: () => void;
    $variant?: "primary" | "secondary";
}

const StyledButton = styled.button<{$variant?: "primary" | "secondary"}>`
    padding: 16px 32px;
    line-height: 32px;
    font-size: 20px;
    font-weight: 700;
    background-color: ${colors.darkGrey};
    border: ${ ({$variant }) => $variant == "primary" ? `2px solid ${colors.light}` : "none"} ;
    justify-content: center;

    border-radius: 10px;
    display: inline-flex;
    min-width: 256px;
    height: fit-content;

    &:hover {
        background-color: ${colors.grey};
    }
    
    &:active {
        background-color: ${colors.lightGrey};
    }
    
    &:focus-visible {
        border: solid 2px #3DDC97;
        outline: none;
    }

    @media (max-width: 768px) {
        padding: 8px 32px;
        line-height: 24px;
        font-size: 16px;
    }

`

const CustomButton = ({children, type, onClick, $variant = "primary"} : ButtonProps) => {
    return (
        <StyledButton type={type} onClick={onClick} $variant={$variant}>{children} </StyledButton>
    );
};

export default CustomButton;