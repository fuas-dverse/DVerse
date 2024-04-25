import MessagePage from "@/components/Message/MessagePage";
import MessageBar from "@/components/Message/MessageBar";

export default async function Home() {

    return (
        <main className="flex relative flex-col bg-background overflow-hidden sm:container p-4">
            <h1>DVerse</h1>
            <p>Welcome to the DVerse UI.</p>
        </main>
    );
}
