import type { ReactNode } from "react";
import styled, { css } from "styled-components"
import { colors } from "~/colors";

type StyledButtonProps = {
    $variant: "primary" | "secondary";
    $size: "small" | "normal" | "big"
}

const sizeStyles = {
    small: css`
        line-height: 24px;
        font-size: 16px;
        font-weight: 500;
        min-width: 128px;
    `,
    
    normal: css`
        line-height: 32px;
        font-size: 20px;

    `,

    big: css`
        line-height: 40px;
        font-size: 24px;
    `
}

const StyledButton = styled.button<StyledButtonProps>`
    padding: 16px 32px;
    font-weight: 700;
    background-color: ${colors.darkGrey};
    border: ${ ({$variant }) => $variant == "primary" ? `2px solid ${colors.light}` : "none"} ;
    justify-content: center;

    border-radius: 10px;
    display: inline-flex;
    min-width: 256px;
    height: fit-content;

    ${(props) => sizeStyles[props.$size]}

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
type ButtonProps = {
    children: ReactNode;
    type: "button" | "submit";
    onClick?: () => void;
    $variant?: "primary" | "secondary";
    $size?: "small" | "normal" | "big"
}

const CustomButton = ({children, type, onClick, $variant = "primary", $size = "normal"} : ButtonProps) => {
    return (
        <StyledButton type={type} onClick={onClick} $variant={$variant} $size={$size}> {children} </StyledButton>
    );
};

export default CustomButton;