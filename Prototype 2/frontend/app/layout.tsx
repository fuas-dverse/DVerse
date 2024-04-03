import type {Metadata} from "next";
import "./globals.css";
import {Inter as FontSans} from "next/font/google"
import {cn} from "@/lib/utils"
import {ThemeProvider} from "@/components/theme-provider";
import {MainNav} from "@/components/main-nav";
import {siteConfig} from "@/config/site";
import {SiteHeader} from "@/components/site-header";
import {Sidebar} from "@/components/sidebar";

const fontSans = FontSans({
    subsets: ["latin"],
    variable: "--font-sans",
})

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
        <html lang="en" suppressHydrationWarning>
        <body className={
            cn(
                "min-h-screen bg-background font-sans antialiased",
                fontSans.variable
            )}>
        <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
        >
            <div className="min-h-screen">
                <SiteHeader/>
                {children}
            </div>
        </ThemeProvider>
        </body>
        </html>
);
}
