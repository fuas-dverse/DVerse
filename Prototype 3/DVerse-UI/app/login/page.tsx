import Image from "next/image"
import Login from "@/components/Auth/Login";

export default function LoginPage() {
	return (
		<div className="w-full h-[calc(100vh-65px)] max-h-screen lg:grid lg:grid-cols-2">
			<div className="flex h-full items-center justify-center">
				<div className="mx-auto grid w-[350px] gap-6">
					<div className="grid gap-2 text-center">
						<h1 className="text-3xl font-bold">Login</h1>
						<p className="text-balance text-muted-foreground">
							Choose your preferred method to login
						</p>
					</div>
					<div className="grid gap-4">
						<Login />
					</div>
				</div>
			</div>
			<div className="hidden bg-muted max-h-[calc(100vh-64px)] lg:flex items-center justify-center">
				<Image
					src={"/images/DVerse_logo.png"}
					alt={"Dverse Logo"}
					loading={"eager"}
					width="768"
					height="768"
					className="object-contain w-[75%] h-[75%]"
				/>
			</div>
		</div>
	)
}