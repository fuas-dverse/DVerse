import {CircleDot, Dot} from "lucide-react";

export interface StatusBarProps {
    name: string,
    status: "not_started" | "running" | "error" | "done"
}

const statusColors = {
    "not_started": "gray",
    "running": "orange",
    "error": "red",
    "done": "green"
};

export default function StatusBar({name, status}: StatusBarProps) {
    return (
        <div className={"w-full flex flex-row p-2 items-center space-x-2"}>
            <div>
                {status in statusColors && <CircleDot color={statusColors[status]} className={"h-5 w-5"} strokeWidth={4}/>}
            </div>
            <div className={"flex-1"}>
                {name}
            </div>
        </div>
    )
}