"use client"
import MessagePage from "@/components/Message/MessagePage";
import MessageBar from "@/components/Message/MessageBar";

export default function Home() {


    return (
        <main
            className="flex relative flex-col bg-background overflow-hidden sm:container p-4">

            {/*Chat section*/}
            <MessagePage/>

            {/*Bottom bar for sending data*/}
            <MessageBar/>
        </main>
    );
}
