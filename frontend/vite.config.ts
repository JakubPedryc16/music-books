import { reactRouter } from "@react-router/dev/vite";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [tailwindcss(), reactRouter(), tsconfigPaths()],
  build: {
    cssMinify: true,
    ssr: false,
  },
  ssr: {
    noExternal: ["styled-components"]
  },
  server: {
    host: '127.0.0.1',
    port: 5173,
    proxy: {
      '/spotify/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
        '/match/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
        '/books/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  } 
});