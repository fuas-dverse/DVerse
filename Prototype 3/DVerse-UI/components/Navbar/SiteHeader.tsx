import Link from "next/link"
import {siteConfig} from "@/config/site"
import {buttonVariants} from "@/components/ui/button"
import {Icons} from "@/components/Icons/icons"
import {MainNav} from "@/components/Navbar/MainNav"
import {ThemeSwitcher} from "@/components/Theme/theme-switcher";
import User from "@/components/Auth/User";
import StatusToggle from "@/components/Status/StatusToggle";
import {usePathname} from "next/navigation";

export async function SiteHeader() {

    return (
        <header className="sticky top-0 z-40 w-full border-b bg-background">
            <div className="container flex h-16 items-center space-x-4 sm:justify-evenly sm:space-x-0">
                <MainNav items={siteConfig.mainNav}/>
                <div className="flex flex-1 items-center justify-end space-x-4">
                    <nav className="flex items-center space-x-0 sm:space-x-1">
                        <StatusToggle/>
                        <Link
                            href={siteConfig.links.github}
                            target="_blank"
                            rel="noreferrer"
                        >
                            <div
                                className={buttonVariants({
                                    size: "icon", variant: "ghost",
                                })}
                            >
                                <Icons.gitHub className="h-5 w-5"/>
                                <span className="sr-only">GitHub</span>
                            </div>
                        </Link>
                        <Link
                            href={siteConfig.links.docs}
                            target="_blank"
                            rel="noreferrer"
                        >
                            <div
                                className={buttonVariants({
                                    size: "icon", variant: "ghost",
                                })}
                            >
                                <Icons.docs className="h-5 w-5"/>
                                <span className="sr-only">Documentation</span>
                            </div>
                        </Link>
                        <ThemeSwitcher/>
                        <User/>
                    </nav>
                </div>
            </div>
        </header>
    )
}