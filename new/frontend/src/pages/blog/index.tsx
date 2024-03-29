import React from "react";

import Head from "next/head";
import Link from "next/link";

export default function BlogPage() {
  const posts = [
    {
      title: "Statbotics V2",
      lead: "Statbotics has gone through some major changes this season. Let's take a look at what's new!",
      url: "/blog/v2",
      date: "2023-01-09",
    },
    {
      title: "The EPA Model",
      lead: "The Expected Points Added (EPA) model builds upon the Elo rating system, but transforms ratings to point units and makes several modifications.",
      url: "/blog/epa",
      date: "2023-01-09",
    },
    {
      title: "Evaluating FRC Rating Models",
      lead: "How do you choose between FRC rating models? We compare several models on three characteristics: predictive power, interpretability, and accessibility.",
      url: "/blog/models",
      date: "2023-01-09",
    },
    {
      title: "The EPA Model: A Gentle Introduction",
      lead: "The math behind EPA can be a bit confusing. This page will help you understand the EPA model, how it works, and how to best use it. No math required!",
      url: "/blog/intro",
      date: "2023-03-16",
    },
    {
      title: "Strength of Schedule",
      lead: "How can we use EPA to measure strength of schedule? We propose three metrics and briefly explore some results.",
      url: "/blog/sos",
      date: "2023-03-23",
    },
  ];

  return (
    <div>
      <Head>
        <title>Blog - Statbotics</title>
      </Head>
      <div className="w-full flex-grow">
        <div className="h-full w-full p-4 md:pt-8">
          <div className="w-full text-center text-3xl">Statbotics Blog</div>
          <div className="grid p-8 lg:grid-cols-2">
            {posts.reverse().map((post) => (
              <div key={`post_${post.url}`} className="w-full p-2">
                <Link href={post.url}>
                  <div className="h-full w-full rounded-lg bg-gray-100 p-8 hover:bg-blue-100">
                    <div className="w-full text-2xl">{post.title}</div>
                    <div className="mb-4 w-full text-sm text-gray-500">{post.date}</div>
                    <div className="w-full text-base">{post.lead}</div>
                  </div>
                </Link>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
