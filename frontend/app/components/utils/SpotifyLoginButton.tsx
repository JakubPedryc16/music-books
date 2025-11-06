import type { ReactNode } from "react";
import CustomButton from "../common/CustomButton";

const CLIENT_BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

type SpotifyProps = {
    $variant?: "primary" | "secondary";
    $size?: "small" | "normal" | "big";
    children?: ReactNode;
}

export const SpotifyLoginButton = ({$variant = "primary", $size = "normal", children = "Login via Spotify"} : SpotifyProps) => {
    const handleLogin = () => {
        window.location.href = `${CLIENT_BACKEND_URL}/spotify/login`;
    };

    return (
        <CustomButton $variant={$variant} type={'button'} onClick={handleLogin} $size={$size}>
            {children}
        </CustomButton>
    );
};