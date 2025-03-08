"use client";

import React from "react";

import Image from "next/image";
import Link from "next/link";
import Script from "next/script";

import "./globals.css";
import Navbar from "./navbar";

const Meta = () => {
  return (
    <head>
      <title>Statbotics</title>
      <meta name="description" content="Modernizing FRC Data Analytics" />

      {/* Open Graph Tags */}
      <meta property="og:title" content="Statbotics" />
      <meta property="og:description" content="Modernizing FRC Data Analytics" />
      <meta property="og:type" content="website" />
      <meta property="og:url" content="https://www.statbotics.io" />
      <meta property="og:image" content="https://www.statbotics.io/og_spline.png" />
      <meta property="og:image:width" content="1200" />
      <meta property="og:image:height" content="630" />
      <meta property="og:logo" content="https://www.statbotics.io/circ_favicon.ico" />

      {/* Favicon */}
      <link rel="icon" href="/favicon.ico" />
    </head>
  );
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <Meta />
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
          <footer className="w-full border-t border-gray-300 text-gray-600 text-center pt-3 pb-2">
            <p className="h-4 sm:h-5 lg:h-6 flex justify-center items-center gap-1 text-xs sm:text-sm lg:text-base">
              Powered by{" "}
              <Link
                href="https://www.thebluealliance.com/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 hover:underline"
              >
                The Blue Alliance
              </Link>
              <Link
                href="https://www.thebluealliance.com/"
                target="_blank"
                rel="noopener noreferrer"
                className="relative h-4 sm:h-5 lg:h-6 w-4 sm:h-5 lg:w-6 mx-1"
              >
                <Image src="/tba.png" alt="TBA" unoptimized fill className="object-contain" />
              </Link>
            </p>
          </footer>
        </div>
      </body>
    </html>
  );
}
