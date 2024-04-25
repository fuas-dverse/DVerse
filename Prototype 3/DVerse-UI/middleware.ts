import { auth } from "@/auth";
import { NextResponse } from "next/server";

export default auth((req) => {
    if (!req.auth) {
        const schema: string = req.nextUrl.protocol;
        const host: string = req.nextUrl.host;

        return NextResponse.redirect(`${schema}//${host}/login`)
    }

    // Content Security Policy generation
    const array = new Uint8Array(16);
    crypto.getRandomValues(array);
    const nonce: string = Buffer.from(array).toString('base64')

    const cspHeader: string = `
        default-src 'self';
        script-src 'self' 'strict-dynamic' 'unsafe-eval' 'nonce-${nonce}';
        script-src-elem 'self' 'unsafe-inline';
        style-src 'self' 'unsafe-inline' ;
        img-src 'self' data: blob:;
        font-src 'self';
        connect-src 'self' http://localhost:5000/ wss://localhost:5000/ ws://localhost:5000/;
        object-src 'none'; 
        frame-ancestors 'none';
        form-action 'self'; 
        upgrade-insecure-requests;
        base-uri 'self'
    `.replace(/\s{2,}/g, ' ').trim()


    const requestHeaders = new Headers(req.headers)
    requestHeaders.set('x-nonce', nonce)
    requestHeaders.set('Content-Security-Policy', cspHeader)


    const response = NextResponse.next({
        request: {
            headers: requestHeaders,
        },
    })
    response.headers.set('Content-Security-Policy', cspHeader)

    return response
});

export const config = {
    matcher: [
        {
            source: '/((?!api|_next/static|_next/image|images|favicon.ico|login).*)',
            missing: [
                { type: 'header', key: 'next-router-prefetch' },
                { type: 'header', key: 'purpose', value: 'prefetch' },
            ],
        },
    ],
}
