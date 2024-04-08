"use client"
import Image from "next/image";
import {useState} from "react";
import {Button} from "@/components/ui/button";
import {Input} from "@/components/ui/input";
import {HistoryBar} from "@/components/Sidebar/HistoryBar";
import {Icons} from "@/components/Icons/icons";
import MessageBubble, {MessageBubbleProps} from "@/components/Message/MessageBubble";

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
        <main className="flex flex-col items-center justify-start p-4 sm:p-12 bg-background overflow-hidden min-h-[calc(100vh-65px)] sm:w-3/4 sm:m-auto md:w-2/3">
            <div className={"w-full"}>
                <div className="flex flex-1 flex-col w-full mb-8">
                    {messages.map((message) => (
                        <MessageBubble key={message.id} id={message.id} sender={message.sender} text={message.text}/>
                    ))}
                </div>
                <div
                    className="flex w-full justify-between gap-4 ">
                    <HistoryBar/>
                    <Input
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                        placeholder="Type a message..."
                        className=""
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
