"use client"

import Link from "next/link"
import {usePathname} from "next/navigation"

import {cn} from "@/lib/utils"
import {NavItem} from "@/types/nav";
import {Button} from "@/components/ui/button";
import {
    Sheet,
    SheetContent,
    SheetDescription,
    SheetFooter,
    SheetHeader,
    SheetTitle,
    SheetTrigger
} from "@/components/ui/sheet";
import {Separator} from "@/components/ui/separator";
import {Icons} from "@/components/Icons/icons";

export interface DocsSidebarNavProps {
    items: NavItem[]
}

const chats = [
    {id: 1, name: 'Chat 1', message: 'Can you help me with booking a vacation?'},
    {id: 1, name: 'Chat 1', message: 'Can you help me with setting up a business?'},
    {id: 1, name: 'Chat 1', message: 'Can you create a logo for me?'},
    {id: 1, name: 'Chat 1', message: 'Can you help me with booking a vacation?'},
    {id: 1, name: 'Chat 1', message: 'Can you help me with booking a vacation?'},
    // Add more chats as needed
];

export function HistoryBar() {
    const pathname = usePathname()

    return (
        <Sheet>
            <SheetTrigger className={"hidden sm:block"} asChild>
                <Button >
                    Show history
                </Button>
            </SheetTrigger>
            <SheetTrigger className={"block sm:hidden"} asChild>
                <Button className={"px-2"}>
                    <Icons.history/>
                </Button>
            </SheetTrigger>
            <SheetContent side={"left"}>
                <SheetHeader>
                    <SheetTitle className={"text-2xl font-bold mb-4"}>History</SheetTitle>
                    <SheetDescription className={"space-y-2 flex flex-col"}>
                        {
                            chats.map((chat, index) => {
                                return <Button key={index} className={"text-left bg-secondary text-secondary-foreground inline-block whitespace-nowrap overflow-hidden text-ellipsis"}>
                                    {
                                        chat.message
                                    }
                                </Button>
                            })
                        }
                    </SheetDescription>
                </SheetHeader>
            </SheetContent>
        </Sheet>
    );
}