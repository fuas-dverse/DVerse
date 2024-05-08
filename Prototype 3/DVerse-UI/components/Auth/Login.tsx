import {signIn} from "@/auth";
import {Button} from "@/components/ui/button";

export default function Login() {
	return (
		<form
			action={async () => {
				"use server"
				await signIn("keycloak")
			}}>
			<Button variant="outline" className="w-full">
				Sign in with Keycloak
			</Button>
		</form>
	)
}