import React, { useRef, type ReactNode } from "react";
import styled from "styled-components";

const Container = styled.div`
  position: relative;
  overflow: hidden;
  white-space: nowrap;
  width: 100%;
`;

interface ScrollProps {
    children : ReactNode
}

export const DynamicScrollText = ({ children } : ScrollProps) => {
  const ref = useRef<HTMLDivElement>(null);
  const [style, setStyle] = React.useState<React.CSSProperties>({});

  const speed = 25;
  const pause = 3;

  const updateAnimation = () => {
    if (!ref.current) return;

    const containerWidth = ref.current.parentElement?.offsetWidth || 0;
    const textWidth = ref.current.scrollWidth;
    const scrollDistance = Math.max(textWidth - containerWidth, 0);

    if (scrollDistance === 0) {
      setStyle({ display: "inline-block", whiteSpace: "nowrap" });
      return;
    }

    const moveDuration = scrollDistance / speed;
    const totalDuration = pause * 2 + moveDuration * 2;
    const animName = `scroll-${Math.random().toString(36).slice(2, 11)}`;

    const styleTag = document.createElement("style");
    styleTag.id = animName;
    styleTag.innerHTML = `
      @keyframes ${animName} {
        0% { transform: translateX(0); }
        ${(pause / totalDuration) * 100}% { transform: translateX(0); }
        ${(pause + moveDuration) / totalDuration * 100}% { transform: translateX(-${scrollDistance}px); }
        ${(pause + moveDuration + pause) / totalDuration * 100}% { transform: translateX(-${scrollDistance}px); }
        100% { transform: translateX(0); }
      }
    `;
    document.head.appendChild(styleTag);

    setStyle({
      animation: `${animName} ${totalDuration}s linear infinite`,
      display: "inline-block",
      whiteSpace: "nowrap",
    });

    return () => {
      const oldStyle = document.getElementById(animName);
      if (oldStyle) document.head.removeChild(oldStyle);
    };
  };

  React.useEffect(() => {
    let cleanup = updateAnimation();

    const handleResize = () => {
      if (cleanup) cleanup();
      cleanup = updateAnimation();
    };

    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
      if (cleanup) cleanup();
    };
  }, [children]);

  return (
    <Container>
      <div ref={ref} style={style}>
        {children}
      </div>
    </Container>
  );
};

export default DynamicScrollText;
