/** @type {import('next').NextConfig} */

const nextConfig = {
    async headers() {
      return [
        {
          source: '/(.*)', // Use '*' for all routes
          headers: [
            {
              key: 'Permissions-Policy',
              value: 'accelerometer=(), ambient-light-sensor=(), autoplay=(), battery=(), camera=(), cross-origin-isolated=(self), display-capture=(), document-domain=(), encrypted-media=(), execution-while-not-rendered=(), execution-while-out-of-viewport=(), fullscreen=(self), geolocation=(), gyroscope=(), keyboard-map=(), magnetometer=(), microphone=(self), midi=(), navigation-override=(), payment=(), picture-in-picture=(), publickey-credentials-get=(), screen-wake-lock=(), sync-xhr=(), usb=(), web-share=(), xr-spatial-tracking=()',
            },
            {
                key: 'Strict-Transport-Security',
                value: 'max-age=63072000; includeSubDomains; preload'
            },
            {
                key: 'X-Content-Type-Options',
                value: 'nosniff'
            },
            {
                key: 'Referrer-Policy',
                value: 'origin-when-cross-origin'
            },
          ],
        },
        {
          source: '/((?!api|_next/static|_next/image|favicon.ico|mastodon-icon.svg).*)',
          headers: [            
            {
              key: 'X-XSS-Protection',
              value: '1; mode=block'
            },
          ],
        },
      ];
    },
  };
  
  export default nextConfig;
