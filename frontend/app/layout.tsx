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
      <body>
        <div className="min-h-screen flex flex-col bg-white text-gray-800">
          <Navbar />
          {children}
        </div>
      </body>
    </html>
  );
}
