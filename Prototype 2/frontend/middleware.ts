import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
    //Nonces offer a way to allow inline scripts to execute if they have the correct nonce.
    const nonce = Buffer.from(crypto.randomUUID()).toString('base64')

    const cspHeader = `
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
    `
    //For style-src 'self' 'nonce-${nonce}'; is wanted not script-src 'self' 'unsafe-eval'  'unsafe-inline';
    //For script-src 'self'  'nonce-${nonce}' 'strict-dynamic'; is wanted
    //Because of EvalError mostly in @next/react-refresh-utils/dist/runtime.js unsafe-eval needs to be set.

    // Replace newline characters and spaces
    const contentSecurityPolicyHeaderValue = cspHeader
        .replace(/\s{2,}/g, ' ')
        .trim()

    const requestHeaders = new Headers(request.headers)
      requestHeaders.set('x-nonce', nonce)

    requestHeaders.set(
        'Content-Security-Policy',
        contentSecurityPolicyHeaderValue
    )

    const response = NextResponse.next({
        request: {
            headers: requestHeaders,
        },
    })
    response.headers.set(
        'Content-Security-Policy',
        contentSecurityPolicyHeaderValue
    )

    response.headers.set('Access-Control-Allow-Origin', 'http://localhost:3000')

    return response
}

export const config = {
    matcher: [
        /*
         * Match all request paths except for the ones starting with:
         * - api (API routes)
         * - _next/static (static files)
         * - _next/image (image optimization files)
         * - favicon.ico (favicon file)
         */
        {
            source: '/((?!api|_next/static|_next/image|favicon.ico).*)',
            missing: [
                { type: 'header', key: 'next-router-prefetch' },
                { type: 'header', key: 'purpose', value: 'prefetch' },
            ],
        },
    ],
}