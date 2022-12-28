import React from "react";

import "./dist.css";
import Navbar from "./navbar";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head />
      <body>
        <div className="min-h-screen flex flex-col text-gray-800">
          <Navbar />
          {children}
        </div>
      </body>
    </html>
  );
}
