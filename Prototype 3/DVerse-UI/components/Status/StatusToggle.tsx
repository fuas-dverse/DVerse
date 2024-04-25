"use client"
import {Bot, CheckIcon, CircleDot, Ellipsis} from "lucide-react";
import {usePathname} from "next/navigation";
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover"
import {useState} from "react";
import {Button} from "@/components/ui/button";
import StatusBar, {StatusBarProps} from "@/components/Status/StatusBar";
import {Separator} from "@/components/ui/separator";


export default function StatusToggle() {
    const router = usePathname()
    const [status, setStatus] = useState<"not_started" | "running" | "error" | "done">("not_started")
    const statusColors = {
        "not_started": "gray",
        "running": "orange",
        "error": "red",
        "done": "green"
    };

    const bots: StatusBarProps[] = [
        {
            name: "Language",
            status: "done",

        },
        {
            name: "Travel",
            status: "running",

        },
        {
            name: "Booking",
            status: "error",
        }
    ]

    if (router == "/chat") {
        return (
            <Popover>
                <PopoverTrigger asChild>
                    <Button variant="ghost" size="icon">
                        {status in statusColors && <Bot color={statusColors[status]} className={"h-5 w-5"} strokeWidth={2}/>}
                    </Button>
                </PopoverTrigger>
                <PopoverContent className={"space-y-1"}>
                    {
                        bots.map((bot, index) => {
                            return (
                                <>
                                    <StatusBar key={index} name={bot.name} status={bot.status}/>
                                    <Separator/>
                                </>
                            )
                        })
                    }
                </PopoverContent>
            </Popover>
        )
    }
}