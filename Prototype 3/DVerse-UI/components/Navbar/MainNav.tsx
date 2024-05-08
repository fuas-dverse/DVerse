import * as React from "react"
import Link from "next/link"

import { NavItem } from "@/types/nav"
import { siteConfig } from "@/config/site"
import { cn } from "@/lib/utils"
import Image from "next/image";

interface MainNavProps {
    items?: NavItem[]
}

export function MainNav({ items }: MainNavProps) {
    return (
        <div className="flex gap-6 md:gap-10 ">
            <Link href="/" className=" items-center space-x-2 hidden sm:flex">
                <Image src={"/images/DVerse_logo.png"} alt={"DVerse Logo"} width={24} height={24} className={"object-contain"}/>
                <span className="sm:inline-block font-bold hidden">{siteConfig.name}</span>
            </Link>
            {items?.length ? (
                <nav className="flex gap-3 sm:gap-6">
                    {items?.map(
                        (item, index) =>
                            item.href && (
                                <Link
                                    key={index}
                                    href={item.href}
                                    className={cn(
                                        "flex items-center text-sm font-medium text-muted-foreground",
                                        item.disabled && "cursor-not-allowed opacity-80"
                                    )}
                                >
                                    {item.title}
                                </Link>
                            )
                    )}
                </nav>
            ) : null}
        </div>
    )
}