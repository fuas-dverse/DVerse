import "./globals.css";
import {Inter as FontSans} from "next/font/google"
import {cn} from "@/lib/utils"
import {ThemeProvider} from "@/components/Theme/theme-provider";
import {SiteHeader} from "@/components/Navbar/SiteHeader";

const fontSans = FontSans({
    subsets: ["latin"],
    variable: "--font-sans",
})

export default async function RootLayout(
    {
        children,
    }: Readonly<{
        children: React.ReactNode;
    }>) {
    return (
        <html lang="en" suppressHydrationWarning={true}>
        <head>
            <title>DVerse</title>
            <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"/>
        </head>
        <body className={
            cn(
                "bg-background font-sans antialiased",
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
