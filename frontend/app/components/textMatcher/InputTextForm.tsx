import React, { useState } from "react";
import styled from "styled-components";
import CustomButton from "../common/CustomButton";
import { colors } from "~/colors";
import api from "~/utils/api";
import type { MatchTextParams } from "../models/match";

const StyledForm = styled.form`
    display: flex;
    flex-direction: column;
    align-items: center;
    align-self: center;
    gap: 1rem;
    box-sizing: border-box;
    background-color: ${colors.darkgrey};
    padding: 1rem 0rem 2rem 0;

    width: 100vw;
`

const StyledTextarea = styled.textarea`
    border-radius: 10px;
    border: 2px solid white;
    font-size: 14px;
    line-height: 20px;
    padding: 1rem;
    min-height: 100px;
    min-width: 300px;
    background-color: ${colors.grey};

    @media (max-width: 768px) {
        height: 200px;
        width: 50%;
        min-width: 200px;
    }
`

const StyledTitle = styled.h2`
    font-size: 20px;
    line-height: 32px;
    font-weight: 700;
    text-align: center;
`
const StyledLimitText = styled.div`
    text-align: right;
    font-size: 14px;
    line-height: 20px;
`
type Props = {
    onSubmit: (params: MatchTextParams) => void;
}

const InputTextForm = ({onSubmit}: Props) => {

    const maxLength = 1000;
    const [text, setText] = useState<string>("");

    const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        if (e.target.value.length <= maxLength) {
            setText(e.target.value)
        }
    }

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        onSubmit({
            text: text,
            amount: 5,
            matcher_type: "hybrid_cascade" 
        })
    }
    
    return (
        <StyledForm onSubmit={handleSubmit}>
            <StyledTitle>Input Text Fragment</StyledTitle>
            <StyledTextarea value={text} onChange={handleChange} placeholder="input text fragment"/>
            <StyledLimitText>{text.length} / {maxLength}</StyledLimitText>
            <CustomButton type={"submit"} onClick={() => handleSubmit}>Submit</CustomButton>
        </StyledForm>
    );
};

export default InputTextForm;