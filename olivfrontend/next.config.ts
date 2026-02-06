import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* Image Optimization */
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

  /* Build Speed Optimizations */
  typescript: {
    // This skips the "Running TypeScript..." step in the build
    ignoreBuildErrors: true, 
  },
  eslint: {
    // This skips the "Linting..." step in the build
    ignoreDuringBuilds: true,
  },
  
  // Ensures the output is lean and optimized for production
  // (Optional: useful if deploying to Vercel/Docker)
  output: 'standalone', 
};

export default nextConfig;