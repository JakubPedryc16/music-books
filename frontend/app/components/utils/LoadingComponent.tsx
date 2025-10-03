import styled, { keyframes } from 'styled-components';
import { colors } from '~/colors';

const spin = keyframes`
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
`;

const Spinner = styled.div`
  width: 60px;
  height: 60px;
  border-radius: 50%;
  position: relative;
  
  animation: ${spin} 1s linear infinite;

  box-shadow:
    inset 0 0 0 1px rgba(0, 0, 0, 0.1),
    0 0 0 2px rgba(0, 0, 0, 0.1);
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 50%;

    background: conic-gradient(
        ${colors.darkGrey} 30%,
        ${colors.light} 45%,
        ${colors.light} 55%,
        ${colors.darkGrey} 70%
    );
  }

  &::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 75%;
    height: 75%;
    background-color: ${colors.grey};
    border-radius: 50%;
  }
`;

const SpinnerWrapper = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 25vh;
`;

function LoadingComponent() {
  return (
    <SpinnerWrapper>
      <Spinner />
    </SpinnerWrapper>
  );
}

export default LoadingComponent;