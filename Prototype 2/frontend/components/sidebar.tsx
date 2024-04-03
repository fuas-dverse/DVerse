"use client"

import Link from "next/link"
import {usePathname} from "next/navigation"

import {cn} from "@/lib/utils"
import {NavItem} from "@/types/nav";
import {Button} from "@/components/ui/button";

export interface DocsSidebarNavProps {
    items: NavItem[]
}

const chats = [
    {id: 1, name: 'Chat 1', message: 'This is the first message fmlkwhjoifhwerf'},
    {id: 1, name: 'Chat 1', message: 'This is the first message fmlkwhjoifhwerf'},
    {id: 1, name: 'Chat 1', message: 'This is the first message fmlkwhjoifhwerf'},
    {id: 1, name: 'Chat 1', message: 'This is the first message fmlkwhjoifhwerf'},
    {id: 1, name: 'Chat 1', message: 'This is the first message fmlkwhjoifhwerf'},
    // Add more chats as needed
];

export function Sidebar() {
    const pathname = usePathname()

    return (
        <div className="w-64 float-left">
            <div className="py-2 px-3 h-[calc(100vh-65px)] flex flex-col space-y-3 border-r-2">
                <h2 className={"font-bold text-xl"}>History</h2>
                {chats.map((chat, key) => (
                    <Button key={key} className={"inline-block text-nowrap overflow-hidden overflow-ellipsis "} variant={"secondary"}>
                        {
                            chat.message
                        }
                    </Button>
                ))}
            </div>
        </div>
    );
}