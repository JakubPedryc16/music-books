import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
    index("routes/home.tsx"),
    route("text-matcher", "routes/textMatcher.tsx"),
    route("spotify-callback", "routes/spotifyCallback.tsx"),
] satisfies RouteConfig;
