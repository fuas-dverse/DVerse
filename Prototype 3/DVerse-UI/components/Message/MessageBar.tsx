import {useState} from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Icons } from "@/components/Icons/icons";
import {HistoryBar} from "@/components/Sidebar/HistoryBar";

interface Proptypes {
    ws: any
    addMessage: (message: string, sender: "user" | "bot") => void
}

export default function MessageBar({ ws, addMessage }: Proptypes) {
    const [newMessage, setNewMessage] = useState<string>("");

    const handleSendMessage = (): void => {
        addMessage(newMessage, "user");
        ws.emit("message", newMessage)
        setNewMessage("");
    };

    return (
        <div className="fixed bottom-0 z-10 p-4 bg-background container left-1/2 transform -translate-x-1/2">
            <div className={"flex justify-between gap-4"}>
                <HistoryBar/>
                <Input
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                    placeholder="Type a message..."
                    className=""
                    type={"text"}
                />
                <Button className={"bg-primary text-primary-foreground px-2"} onClick={handleSendMessage}>
                    <div className={"hidden sm:block"}>
                        Send
                    </div>
                    <div className={"block sm:hidden"}>
                        <Icons.send/>
                    </div>
                </Button>
            </div>
        </div>
    )
}