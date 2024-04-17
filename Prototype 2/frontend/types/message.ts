import {ReactNode} from "react";

export interface Message {
	id: number;
	text: ReactNode;
	sender: "bot" | "user";
}