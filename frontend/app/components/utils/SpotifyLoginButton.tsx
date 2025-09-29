
const CLIENT_BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export const SpotifyLoginButton = () => {
    const handleLogin = () => {
        window.location.href = `${CLIENT_BACKEND_URL}/spotify/login`;
    };

    return (
        <button onClick={handleLogin}>
            Login via Spotify
        </button>
    );
};