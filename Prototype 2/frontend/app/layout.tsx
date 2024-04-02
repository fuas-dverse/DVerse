import type {Metadata} from "next";
import {Inter} from "next/font/google";
import "./globals.css";
import Providers from "@/app/Providers";
import AppNavbar from "@/app/components/AppNavbar";

const inter = Inter({subsets: ["latin"]});

export const metadata: Metadata = {
    title: "DVerse - UI",
};

export default function RootLayout(
    {
        children,
    }: Readonly<{
        children: React.ReactNode;
    }>) {
    return (
        <html lang="en">
        <body>
        <Providers>
            <AppNavbar/>
            {children}
        </Providers>
        </body>
        </html>
    );
}
