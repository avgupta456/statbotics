/* eslint-disable @next/next/next-script-for-ga */
import React from "react";

import Script from "next/script";

import "./globals.css";
import Navbar from "./navbar";

export const metadata = {
  title: "Statbotics",
  description: "Modernizing FRC Data Analytics",
  openGraph: {
    title: "Statbotics",
    description: "Modernizing FRC Data Analytics",
    type: "website",
    url: "https://www.statbotics.io",
    images: [
      {
        url: "https://www.statbotics.io/og_spline.png",
        width: 1200,
        height: 630,
      },
    ],
  },
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Script
          id="google"
          async
          src="https://www.googletagmanager.com/gtag/js?id=UA-145490100-3"
        />
        <Script
          id="gtag"
          dangerouslySetInnerHTML={{
            __html: `window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'UA-145490100-3', { page_path: window.location.pathname });
          `,
          }}
        />
        <Script
          id="umami"
          src="https://umami-nine-zeta.vercel.app/umami.js"
          data-website-id="eaf23a65-20a8-40aa-a1a6-730683f5fe10"
          async
          defer
        />
        <div className="min-h-screen flex flex-col bg-white text-gray-800">
          <Navbar />
          {children}
        </div>
      </body>
    </html>
  );
}
