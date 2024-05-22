import {useEffect, useState} from "react";
import {io, Socket as IOSocket} from "socket.io-client";

// Define a type for the socket
type SocketType = IOSocket | undefined;

export function useSocket(onMessage: (data: { text: string, sender: "bot" | "user" }) => void): SocketType {
	const SERVER_URL = process.env.SERVER_URL || "http://localhost:19256";

	const [socket, setSocket] = useState<SocketType>();

	useEffect(() => {
		const ws = io(SERVER_URL);

		ws.on("connect", (): void => {
			console.log("Connected to server");
		});

		ws.on('message', onMessage);

		ws.on('error', (error: any): void => {
			console.error("Socket error:", error);
		});

		setSocket(ws);

		// Cleanup function
		return (): void => {
			ws.disconnect();
		};
	}, [SERVER_URL, onMessage]);

	return socket;
}