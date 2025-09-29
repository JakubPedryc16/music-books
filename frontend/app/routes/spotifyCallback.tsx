import { useEffect } from "react";
import { useNavigate } from "react-router";

const SpotifyCallback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    navigate("/")
}, [navigate]);

  return <p>Logging in via Spotify...</p>;
};

export default SpotifyCallback;
