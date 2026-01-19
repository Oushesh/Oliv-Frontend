import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'www.olvlimits.com',
        pathname: '**',
      },
      {
        protocol: 'https',
        hostname: 'blueprint.bryanjohnson.com',
        pathname: '**',
      },
    ],
  },
};

export default nextConfig;
