import MessageBubble from "@/components/Message/MessageBubble";
import {Message} from "@/types/message";

export default function MessagePage({ messages } : {messages: Message[]}) {
    return (
        <div className="flex flex-1 flex-col overflow-y-auto mb-12">
            {
                messages.map((message: Message) => (
                    <MessageBubble key={message.id} id={message.id} sender={message.sender} text={message.text} />
                ))
            }
        </div>
    )
}