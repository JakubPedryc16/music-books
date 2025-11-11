import styled from "styled-components";

const StyledTextArea = styled.div`
  font-size: 18px;
  line-height: 32px;
  max-width: 1000px;
  min-height: 1000px;
  white-space: pre-wrap;
  word-wrap: break-word;

  @media (max-width: 768px) {
    font-size: 16px;
    line-height: 24px;
  }
`;

type Props = {
  text: string;
}

const normalizeText = (text: string) => {
  return text
    .replace(/\r\n|\r/g, '\n')
    .split('\n')
    .map(line => line.trim())
    .filter(line => line !== '')
    .map((line, idx, arr) => {
      if (line.length === 1 && arr[idx + 1]) {
        arr[idx + 1] = line + arr[idx + 1];
        return null;
      }
      return line;
    })
    .filter(Boolean)
    .join('\n');
}



const BookArea = ({ text }: Props) => {
  const formattedText = normalizeText(text);

  return <StyledTextArea>{formattedText}</StyledTextArea>;
}

export default BookArea;
