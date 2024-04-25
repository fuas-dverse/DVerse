"use client"
import {HistoryBar} from "@/components/Sidebar/HistoryBar";
import {Input} from "@/components/ui/input";
import {Button} from "@/components/ui/button";
import {Icons} from "@/components/Icons/icons";
import {useEffect, useState} from "react";
import {MessageBubbleProps} from "@/components/Message/MessageBubble";
import {io} from "socket.io-client";

export default function MessageBar(){
    // const [socket, setSocket] = useState<any>(undefined)
    // const [newMessage, setNewMessage] = useState('');
    //
    // const handleSendMessage = () => {
    //     socket.emit("message", newMessage)
    //
    //     setNewMessage("")
    // };
    //
    // useEffect(() => {
    //     // Code gives error in the terminal, but does work in if connected to the right websocket server
    //     // !! Is tested with a custom server
    //     const socket = io("http://localhost:3001/")
    //     setSocket(socket)
    // }, [])

    return (
        <div
            className="fixed bottom-0 z-10 p-4 bg-background container left-1/2 transform -translate-x-1/2">
            <div className={"flex justify-between gap-4"}>
                <HistoryBar/>
                <Input
                    // value={newMessage}
                    // onChange={(e) => setNewMessage(e.target.value)}
                    // onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    placeholder="Type a message..."
                    className=""
                    type={"text"}
                />
                <Button className={"bg-primary text-primary-foreground px-2"}>
                {/*<Button className={"bg-primary text-primary-foreground px-2"} onClick={handleSendMessage}>*/}
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