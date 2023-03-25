"use client";

import Head from "next/head";

export default function Home() {
  return (
    <div>
      <Head>
        <title>Sentry Onboarding</title>
        <meta name="description" content="Make your Next.js ready for Sentry" />
      </Head>

      <main className="w-full flex justify-center">
        <button
          type="button"
          className="mt-32 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          onClick={() => {
            throw new Error("Sentry Frontend Error");
          }}
        >
          Throw Error
        </button>
      </main>
    </div>
  );
}
