/* eslint-disable @next/next/next-script-for-ga */
import React from "react";

import "./globals.css";
import Navbar from "./navbar";

export const metadata = {
  title: "Statbotics",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-145490100-3" />
        <script
          id="gtag"
          dangerouslySetInnerHTML={{
            __html: `window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'UA-145490100-3', { page_path: window.location.pathname });
        `,
          }}
        />
        <script
          async
          defer
          data-website-id="eaf23a65-20a8-40aa-a1a6-730683f5fe10"
          src="https://umami-nine-zeta.vercel.app/umami.js"
        />
      </head>
      <body>
        <div className="min-h-screen flex flex-col bg-white text-gray-800">
          <Navbar />
          {children}
        </div>
      </body>
    </html>
  );
}
