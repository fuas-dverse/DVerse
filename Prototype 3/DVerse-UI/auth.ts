import NextAuth from "next-auth";
import Keycloak from "@auth/core/providers/keycloak";

export const { handlers, signIn, signOut, auth } = NextAuth({
    providers: [Keycloak],
    callbacks: {
        redirect: async () => {
            return "/";
        }
    },
    secret: process.env.AUTH_SECRET,
})