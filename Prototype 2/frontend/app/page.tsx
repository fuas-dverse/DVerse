"use client"
import Image from "next/image";
import {useState} from "react";
import {Button} from "@/components/ui/button";
import {Input} from "@/components/ui/input";
import {HistoryBar} from "@/components/Sidebar/HistoryBar";
import {Icons} from "@/components/Icons/icons";
import MessageBubble, {MessageBubbleProps} from "@/components/Message/MessageBubble";
import {Separator} from "@/components/ui/separator";

export default function Home() {

    const [messages, setMessages] = useState<MessageBubbleProps[]>([
        {id: 1, text: 'Hello! How can I help you today?', sender: 'bot'},
        {id: 2, text: 'Can you tell me more about NextUI?', sender: 'user'},
        {id: 2, text: 'Can you tell me more about NextUI?', sender: 'user'},
        {id: 2, text: 'Can you tell me more about NextUI?', sender: 'user'},
        {id: 2, text: 'Can you tell me more about NextUI?', sender: 'user'},
        {id: 2, text: 'Can you tell me more about NextUI?', sender: 'user'},
        {id: 2, text: 'Can you tell me more about NextUI?', sender: 'user'},
        {id: 2, text: 'Can you tell me more about NextUI?', sender: 'user'},
        {id: 2, text: 'Can you tell me more about NextUI?', sender: 'user'},
        {id: 2, text: 'Can you tell me more about NextUI?', sender: 'bot'},
    ]);
    const [newMessage, setNewMessage] = useState('');

    const handleSendMessage = () => {
        if (newMessage.trim() !== '') {
            const newMessageObject: MessageBubbleProps = {
                id: messages.length + 1,
                text: newMessage,
                sender: 'user',
            };
            setMessages([...messages, newMessageObject]);
            setNewMessage('');
            // Here you would typically also handle sending the message to your backend or service
        }
    };
    return (
        <main
            className="flex relative flex-col bg-background overflow-hidden sm:container p-4">
            {/*Chat section*/}
            <div className="flex flex-1 flex-col overflow-y-auto mb-12">
                {messages.map((message) => (
                    <MessageBubble key={message.id} id={message.id} sender={message.sender} text={message.text}/>
                ))}
            </div>

            {/*Bottom bar for sending data*/}
            <div
                className=" fixed bottom-0 z-10 pb-4 pt-4 bg-background w-full px-2 left-1/2 transform -translate-x-1/2">
                <div className={"flex justify-between gap-4"}>
                    <HistoryBar/>
                    <Input
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
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
        </main>
    );
}
