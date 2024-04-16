"use client"
import React, {ReactNode, useCallback, useState} from "react";
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


	const handleSocketMessage = useCallback((data: any): void => {
		Object.entries(data.data).forEach(([key, value]): void => {
			if (Array.isArray(value)) {
				const message = (
					<>
						<h2><b>{key}</b></h2><br />
						{value.map((item: any, index: number) => (
							<>
								<Link className={"hover:text-blue-600"} target={"_blank"} key={index} href={item.URL}>{item.Title}</Link><br/>
							</>
						))}
					</>
				);

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