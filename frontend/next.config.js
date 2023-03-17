/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false, // Recommended for the `pages` directory, default in `app`.
  experimental: {
    // Required:
    appDir: true,
  },
  images: {
    domains: [
      // imgur
      "i.imgur.com",
    ],
  },
  env: {
    PROD: process.env.PROD,
  },
};

module.exports = nextConfig;
