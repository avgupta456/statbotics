import React from "react";

import Head from "next/head";

export default function PythonAPIPage() {
  return (
    <div>
      <Head>
        <title>Python API - Statbotics</title>
      </Head>
      <iframe
        src="https://statbotics.readthedocs.io/en/latest/"
        title="Python API"
        className="h-[calc(100vh-60px)] w-full"
      />
    </div>
  );
}
