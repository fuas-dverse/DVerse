"use client"
import {Fragment, ReactNode, useCallback, useState} from "react";
import {Message} from "@/types/message";
import {useSocket} from "@/hooks/useSocket";
import Link from "next/link";
import MessagePage from "@/components/Message/MessagePage";
import MessageBar from "@/components/Message/MessageBar";

export default function Home() {
    const [messages, setMessages] = useState<Message[]>([{
        id: 1, text: 'Hello! How can I help you today?', sender: 'bot'
    }]);

    const handleMessage = ((text: ReactNode, sender: "bot" | "user"): void => {
        setMessages((prevMessages: Message[]) => {
            const id: number = prevMessages.length + 1;
            return [...prevMessages, {id, text, sender}];
        });
    });

    const DynamicLink = ({ item, index }: { item: any, index: number }) => {
        const properties = Object.keys(item);
        return (
            <Link className={"hover:text-blue-600"} target={"_blank"} key={index} href={item.URL}>
                {properties.map((prop, i) => item[prop] && (
                    <Fragment key={i}>
                        {i !== 0 && <br />}
                        {prop === 'Title' ? item[prop] : `${prop}: ${item[prop]}`}
                    </Fragment>
                ))}
            </Link>
        );
    };

    const handleSocketMessage = useCallback((data: any): void => {
        Object.entries(data.data).forEach(([key, value]): void => {
            if (Array.isArray(value)) {
                const message = (<div key={key}>
                    <h2><b>{key}</b></h2><br/>
                    {value.map((item: any, index: number) => (
                        <Fragment key={index}>
                            <DynamicLink item={item} index={index} />
                            <br/>
                            <br />
                        </Fragment>
                    ))}
                </div>);

                handleMessage(message, 'bot');
            }
        });
    }, []);


    const socket = useSocket(handleSocketMessage);

    return (
        <main className="flex relative flex-col bg-background overflow-hidden sm:container p-4">
            <MessagePage messages={messages}/>
            <MessageBar ws={socket} addMessage={handleMessage}/>
        </main>
    );
}