import React from "react";

import Head from "next/head";

export default function PageLayout({
  title,
  lead,
  children,
}: {
  title: string;
  lead: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <Head>
        <title>{title}</title>
      </Head>
      <div className="mx-auto w-4/5">
        <div className="prose prose-slate h-full w-full max-w-none py-4 pb-16 md:pt-8">
          <h2 className="w-full text-center">{title}</h2>
          <p className="lead">{lead}</p>
          {children}
        </div>
      </div>
    </div>
  );
}
