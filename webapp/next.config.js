/** @type {import('next').NextConfig} */
const nextConfig = {}

const isDevelopment = process.env.NODE_ENV !== "production";
const rewritesConfig = isDevelopment
    ? [
        {
            source: "/api/:path*",
            destination: "http://localhost:5000/api/:path*",
        },
    ]
    : [];

module.exports = {
    reactStrictMode: true,
    rewrites: async () => rewritesConfig,
};