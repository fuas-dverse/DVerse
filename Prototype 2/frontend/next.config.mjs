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
          ],
        },
      ];
    },
  };
  
  export default nextConfig;
