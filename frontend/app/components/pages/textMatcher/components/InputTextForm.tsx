import React, { useState } from "react";
import styled from "styled-components";
import CustomButton from "../../../common/CustomButton";
import { colors } from "~/colors";
import api from "~/utils/api";
import type { MatchTextParams } from "../../../models/match";

const StyledForm = styled.form`
    display: flex;
    flex-direction: column;
    align-items: center;
    align-self: center;
    box-sizing: border-box;
    background-color: ${colors.darkGrey};
    padding: 1rem 0rem 2rem 0;

    width: 100vw;
`
const StyledTextareaContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;

    margin-bottom: 2rem;
`

const StyledInputContainer = styled.div`
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    width: 400px;

    margin-bottom: 2rem;
`

const StyledErrorContainer = styled.div`
    height: 20px;
    font-size: 14px;
    line-height: 20px;
    color: red;

    margin-bottom: 1rem;
`

const StyledTextarea = styled.textarea`
    border-radius: 10px;
    border: 2px solid ${colors.lightGrey};
    font-size: 14px;
    line-height: 20px;
    padding: 1rem;

    height: 300px;
    min-height: 250px;
    max-height: 1600px;

    max-width: 1000px;
    min-width: 500px;

    background-color: ${colors.grey};

    box-sizing: border-box; 
    box-shadow: 0 0 12px rgba(255, 255, 255, 0.04);

    &:focus {
        outline: none;
        border-color: ${colors.light};
    }

    @media (max-width: 768px) {
        max-width: 300px;
        min-width: 500px;
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

const StyledLabel = styled.label`
    font-size: 14px;
    line-height: 20px;
    font-weight: 700;
`

const StyledInput = styled.input`
    padding: 8px;

    background-color: ${colors.grey};
    border-radius: 5px;
    border: 2px solid ${colors.lightGrey};
    box-sizing: border-box; 
    box-shadow: 0 0 4px rgba(255, 255, 255, 0.04);

    &:focus {
        outline: none;
        border-color: ${colors.light};
    }
`

type Props = {
    onSubmit: (params: MatchTextParams) => void;
}

const InputTextForm = ({onSubmit}: Props) => {

    const maxLength = 1000;
    const maxAmount = 10;
    const [text, setText] = useState<string>("");
    const [amount, setAmount] = useState<string>("");
    const [error, setError] = useState<string | null>(null);

    const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setError("")
        if (e.target.value.length <= maxLength) {
            setText(e.target.value)
        } else {
            setError(`Test cannot be longer than ${maxLength} characters`)
        }
    }

const handleAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value: number = Number(e.target.value)
    setError("")
    if (Number.isInteger(value) && value > 0 && value <= maxAmount) {
        setAmount(e.target.value);
    } else {
        setError(`Amount must be a number from 1 and ${maxAmount}`);
        setAmount("");
    }
}

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        onSubmit({
            text: text,
            amount: Number(amount) || 3,
            matcher_type: "hybrid_cascade" 
        })
    }
    
    return (
        <StyledForm onSubmit={handleSubmit}>
            <StyledTextareaContainer>
                <StyledTitle>Input Text Fragment</StyledTitle>
                <StyledTextarea id="text" value={text} onChange={handleTextChange} placeholder="input text fragment"/>
                <StyledLimitText>{text.length} / {maxLength}</StyledLimitText>
            </StyledTextareaContainer>
            <StyledInputContainer>
                <StyledLabel htmlFor="amount">Input Titles Amount:</StyledLabel>
                <StyledInput id="amount" value={amount} onChange={handleAmountChange} placeholder="amount 1-10"/>
            </StyledInputContainer>
            <StyledErrorContainer>{error}</StyledErrorContainer>
            <CustomButton type={"submit"} onClick={() => handleSubmit}>Submit</CustomButton>
        </StyledForm>
    );
};

export default InputTextForm;