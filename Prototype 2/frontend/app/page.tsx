"use client"
import Image from "next/image";
import {Button, Input} from "@nextui-org/react";
import {useState} from "react";

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
        <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-background">
            <div className="flex flex-1 flex-col w-full max-w-3xl space-y-4 overflow-auto">
                {messages.map((message) => (
                    <div
                        key={message.id}
                        className={`flex ${message.sender === 'bot' ? 'justify-start' : 'justify-end'}`}>
                        <div className={`p-4 rounded-lg ${message.sender === 'bot' ? 'bg-secondary' : 'bg-primary'}`}>
                            {message.text}
                        </div>
                    </div>
                ))}
            </div>
            <div className="flex w-full max-w-3xl justify-between gap-4">
                <Input
                    fullWidth
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    placeholder="Type a message..."
                    className="flex-1"
                />
                <Button color="primary" onClick={handleSendMessage}>
                    Send
                </Button>
            </div>
        </main>
    );
}
