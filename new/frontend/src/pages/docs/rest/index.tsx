import React from "react";

import Head from "next/head";

export default function RESTAPIPage() {
  return (
    <div>
      <Head>
        <title>REST API - Statbotics</title>
      </Head>
      <iframe
        src="https://api.statbotics.io/docs"
        title="REST API"
        className="h-[calc(100vh-60px)] w-full"
      />
    </div>
  );
}
