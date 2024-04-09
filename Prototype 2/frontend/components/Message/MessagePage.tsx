import MessageBubble, {MessageBubbleProps} from "@/components/Message/MessageBubble";
import {useEffect, useState} from "react";
import {io} from "socket.io-client"

export default function MessagePage() {
    const [messages, setMessages] = useState<MessageBubbleProps[]>([
        {id: 1, text: 'Hello! How can I help you today?', sender: 'bot'},
        {id: 2, text: 'Can you tell me more about NextUI?', sender: 'user'},
        {id: 3, text: 'Can you tell me more about NextUI?', sender: 'user'},
        {id: 4, text: 'Can you tell me more about NextUI?', sender: 'user'},
        {id: 5, text: 'Can you tell me more about NextUI?', sender: 'user'},
        {id: 6, text: 'Can you tell me more about NextUI?', sender: 'user'},
        {id: 7, text: 'Can you tell me more about NextUI?', sender: 'user'},
        {id: 8, text: 'Can you tell me more about NextUI?', sender: 'user'},
        {id: 9, text: 'Can you tell me more about NextUI?', sender: 'user'},
        {id: 10, text: 'Can you tell me more about NextUI?', sender: 'bot'},
    ]);

    const [socket, setSocket] = useState<any>(undefined)

    useEffect(() => {
        const socket = io("http://localhost:3001/");

        socket.on("message", (message) => {
            setMessages((currentMessages) => [
                ...currentMessages,
                {
                    id: currentMessages.length + 1,
                    text: message,
                    sender: "user",
                },
            ]);
        });

        setSocket(socket);

        // Cleanup on component unmount
        return () => {
            socket.disconnect()
        }
    }, []);


    return (
        <div className="flex flex-1 flex-col overflow-y-auto mb-12">
            {messages.map((message) => (
                <MessageBubble key={message.id} id={message.id} sender={message.sender} text={message.text}/>
            ))}
        </div>
    )
}