import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
    index("routes/home.tsx"),
    route("text-matcher", "routes/text-matcher.tsx"),
    route("spotify-callback", "routes/spotify-callback.tsx"),
] satisfies RouteConfig;
