import {DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger} from "@/components/ui/dropdown-menu";
import {Button} from "@/components/ui/button";
import {Icons} from "@/components/Icons/icons"

import * as React from "react";
import {auth, signOut} from "@/auth";
import Logout from "@/components/Auth/Logout";
import Login from "@/components/Auth/Login";

export default async function User() {
    const session = await auth()

    if (session)
    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon">
                    <Icons.user className="h-5 w-5"/>
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
                <DropdownMenuItem>
                    {
                        session?.user?.name
                    }
                </DropdownMenuItem>
                <DropdownMenuItem>
                    <Logout/>
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    )
}