'use client'
import {signOut} from "next-auth/react";
import {Button} from "@/components/ui/button";

export default function Logout() {
    return (
        <button onClick={() => {signOut()}}>
            Sign out
        </button>
    )
}