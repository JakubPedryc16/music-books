import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
    index("routes/home.tsx"),
    route("text-matcher", "routes/text-matcher.tsx"),
    route("spotify-callback", "routes/spotify-callback.tsx"),
    route("book-matcher/:bookId", "routes/book-matcher.tsx"),
    route("book-finder", "routes/book-finder.tsx"),
] satisfies RouteConfig;
