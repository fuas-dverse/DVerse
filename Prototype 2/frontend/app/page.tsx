"use client"
import Image from "next/image";
import {useState} from "react";
import {Button} from "@/components/ui/button";
import {Input} from "@/components/ui/input";
import {Sidebar} from "@/components/sidebar";
import {siteConfig} from "@/config/site";
export default function Home() {

    const [messages, setMessages] = useState([
        {id: 1, text: 'Hello! How can I help you today?', sender: 'bot'},
        {id: 2, text: 'Can you tell me more about NextUI?', sender: 'user'}
    ]);
    const [newMessage, setNewMessage] = useState('');

    const handleSendMessage = () => {
        if (newMessage.trim() !== '') {
            const newMessageObject = {
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
        <div>
            <Sidebar/>
            <main className="flex h-[calc(100vh-65px)] flex-col items-center justify-center p-12 bg-background">
                <div className="flex flex-1 flex-col w-full max-w-3xl space-y-4 overflow-auto">
                    {messages.map((message) => (
                        <div
                            key={message.id}
                            className={`flex ${message.sender === 'bot' ? 'justify-start' : 'justify-end'}`}>
                            <div
                                className={`p-4 rounded-lg ${message.sender === 'bot' ? 'bg-secondary text-secondary-foreground' : 'bg-primary text-primary-foreground'}`}>
                                {message.text}
                            </div>
                        </div>
                    ))}
                </div>
                <div className="flex w-full max-w-3xl justify-between gap-4">
                    <Input
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                        placeholder="Type a message..."
                        className="flex-1"
                    />
                    <Button className={"bg-primary text-primary-foreground"} onClick={handleSendMessage}>
                        Send
                    </Button>
                </div>
            </main>
        </div>
    );
}
