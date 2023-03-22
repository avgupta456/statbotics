/* eslint-disable @next/next/next-script-for-ga */

export default function Head() {
  return (
    <>
      <meta content="width=device-width, initial-scale=1" name="viewport" />
      <meta name="title" content="Statbotics" />
      <meta name="description" content="Modernizing FRC Data Analytics" />
      <meta name="og:type" content="website" />
      <meta name="og:url" content="https://www.statbotics.io" />
      <meta name="og:title" content="Statbotics" />
      <meta name="og:description" content="Modernizing FRC Data Analytics" />
      <meta name="og:image" content="https://www.statbotics.io/og_spline.png" />
      <link rel="icon" href="/favicon.ico" />

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
    </>
  );
}
