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
        <Script id="google" async src="https://www.googletagmanager.com/gtag/js?id=G-JD14NTTG5M" />
        <Script
          id="gtag"
          dangerouslySetInnerHTML={{
            __html: `window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-JD14NTTG5M', { page_path: window.location.pathname });
          `,
          }}
        />
        <div className="min-h-screen flex flex-col bg-white text-gray-800">
          <Navbar />
          {children}
        </div>
      </body>
    </html>
  );
}
