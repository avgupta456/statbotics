"use client";

import React, { useEffect } from "react";

import Image from "next/image";
import Link from "next/link";
import Script from "next/script";

import "./globals.css";
import Navbar from "./navbar";

const metadata = {
  title: "Statbotics",
  description: "Modernizing FRC Data Analytics",
  metadataBase: new URL("https://www.statbotics.io"),
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
  useEffect(() => {
    // Helper function to set or create meta tags
    const setMetaTag = (property, content) => {
      let element = document.querySelector(`meta[${property}]`);
      if (!element) {
        element = document.createElement("meta");
        element.setAttribute(property.split("=")[0], property.split("=")[1]);
        document.head.appendChild(element);
      }
      element.setAttribute("content", content);
    };

    document.title = metadata.title;

    // Set or create meta tags
    setMetaTag("name='description'", metadata.description);
    setMetaTag("property='og:title'", metadata.openGraph.title);
    setMetaTag("property='og:description'", metadata.openGraph.description);
    setMetaTag("property='og:type'", metadata.openGraph.type);
    setMetaTag("property='og:url'", metadata.openGraph.url);
    setMetaTag("property='og:image'", metadata.openGraph.images[0].url);
    setMetaTag("property='og:image:width'", metadata.openGraph.images[0].width.toString());
    setMetaTag("property='og:image:height'", metadata.openGraph.images[0].height.toString());

    // Set or create favicon
    let favicon = document.querySelector("link[rel='icon']");
    if (!favicon) {
      favicon = document.createElement("link");
      favicon.setAttribute("rel", "icon");
      document.head.appendChild(favicon);
    }
    favicon.setAttribute("href", metadata.icons.icon);
  }, []);

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
