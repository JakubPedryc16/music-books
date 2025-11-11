import type React from "react";
import { useState } from "react";
import { useNavigate } from "react-router";
import styled from "styled-components";
import { colors } from "~/colors";
import CustomButton from "~/components/common/CustomButton";
import type { BookData, BookPageData, UploadBookRequest } from "~/components/models/book";
import { useUploadBook } from "~/hooks/useUploadBook";

const StyledForm = styled.form`
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
const StyledLabel = styled.label`
    font-size: 20px;
    line-height: 32px;
    font-weight: 700;
    text-align: center;
`

const StyledInputContainer = styled.div`
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
`

const UploadBookForm = () => {

    const [file, setFile] = useState<File | null>(null);
    const [title, setTitle] = useState("");
    const [author, setAuthor] = useState("");
    const {data, loading, error, execute} = useUploadBook();
    const navigate = useNavigate();
    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if(e.target.files && e.target.files.length > 0) {
            setFile(e.target.files[0]);
        }
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!file || !title || !author) return;

        const formData = new FormData();
        formData.append("book", file);
        formData.append("title", title);
        formData.append("author", author);

        const bookId: number | null = await execute(formData);

        if (!error && bookId) {
            navigate(`/book-matcher/${bookId}`);
        }
    }

    return (
       <StyledForm onSubmit={handleSubmit}>
        <StyledInputContainer>
            <StyledInputContainer>
                <StyledLabel htmlFor="titleInput">Book Title</StyledLabel>
                <StyledInput
                    type="text"
                    id="titleInput"
                    value={title}
                    onChange={e => setTitle(e.target.value)}
                    required
                />
            </StyledInputContainer>

            <StyledInputContainer>
                <StyledLabel htmlFor="authorInput">Author</StyledLabel>
                <StyledInput
                    type="text"
                    id="authorInput"
                    value={author}
                    onChange={e => setAuthor(e.target.value)}
                    required
                />
            </StyledInputContainer>
            <StyledLabel htmlFor="fileInput">Upload The Pdf Book File</StyledLabel>
            <StyledInput
                type="file"
                accept="application/pdf"
                id="fileInput"
                onChange={handleFileChange}
            />
        </StyledInputContainer>
        {error}
        <CustomButton type="submit">Upload Your Book</CustomButton>
       </StyledForm> 
    );
}

export default UploadBookForm;