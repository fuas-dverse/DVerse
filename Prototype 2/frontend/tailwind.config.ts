import type {Config} from "tailwindcss";
import {nextui} from "@nextui-org/react";

const config: Config = {
    content: [
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
        "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            backgroundImage: {
                "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
                "gradient-conic":
                    "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
            },
            colors: {}
        },
    },
    plugins: [
        nextui({
            themes: {
                light: {
                    colors: {},
                },
                dark: {
                    colors: {
                        background: "#121212",
                        foreground: "#ffffff",
                        primary: '#0db6ea',
                        secondary: "#0b526f"
                    },
                },
            }
        })
    ],
    darkMode: "class",
};
export default config;
