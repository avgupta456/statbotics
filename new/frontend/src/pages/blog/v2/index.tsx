import React from "react";

import Image from "next/image";
import Link from "next/link";

import PageLayout from "../../../components/blog/pageLayout";
import SeasonTable from "../table";

export default function V2BlogPage() {
  return (
    <PageLayout
      title="Statbotics V2"
      lead="Statbotics has gone through some major changes this season. Let's take a look at what's new!"
    >
      <h3>Background</h3>
      <p>
        My name is Abhijit Gupta, and I&apos;m a student at Yale and former member of FRC Team 5511
        Cortechs Robotics. Cortechs competed at IRI in 2019, where Zebra Motionworks robot tracking
        was first introduced. I became interested in FRC data analysis and eventually built
        Statbotics to analyze historical FRC data. In 2022, I modified Statbotics to support ongoing
        events. Thousands of users engaged with the site, but the slow data refresh reduced the
        total impact. This year, I have rebuilt everything from the ground up, with an increased
        focus on performance and scalability, and a broader vision of creating a platform for both
        realtime and historical FRC data analysis. I&apos;m excited to share the new Statbotics
        platform with the community!
      </p>
      <h3>Welcome to Statbotics V2</h3>
      <p>
        Statbotics V2 is a complete rewrite of the original Statbotics platform. This includes
        changes to the rating model, backend infrastructure, website, and Python API.
      </p>
      <div className="not-prose mx-auto w-4/5 p-8">
        <div className="relative h-[400px] w-full">
          <Image
            src="/spline.png"
            alt="Summary"
            fill
            quality={100}
            priority
            className="object-contain"
          />
        </div>
      </div>
      <p>
        The new Expected Points Added (EPA) model is a significant improvement over the previous Elo
        and OPR based rating models, providing increased prediction accuracy, interpretability, and
        accessibility. Read more about the EPA model{" "}
        <Link className="text_link" rel="noreferer noopener" target="_blank" href="/blog/epa">
          here
        </Link>{" "}
        and read how it compares to existing approaches{" "}
        <Link className="text_link" rel="noreferer noopener" target="_blank" href="/blog/models">
          here
        </Link>
        .
      </p>
      <SeasonTable />
      <p>
        The new backend infrastructure better interfaces with the TBA API and is designed to support
        realtime data analysis. During the competition season,{" "}
        <strong>match results will be updated every minute</strong>, compared to every couple hours
        last year. The website has been rewritten to reduce loading time and provide a stronger
        foundation upon which to continue building. Already, some new features have been added, such
        as bubble plots, match breakdowns, and a revamped team page.
      </p>
      <div className="not-prose">
        <div className="mx-auto w-4/5 p-8">
          <div className="relative h-[400px] w-full">
            <Image src="/bubble.png" alt="Summary" fill quality={100} className="object-contain" />
          </div>
        </div>
        <div className="mx-auto w-4/5 p-8">
          <div className="relative h-[400px] w-full">
            <Image src="/match.png" alt="Summary" fill quality={100} className="object-contain" />
          </div>
        </div>
        <div className="mx-auto w-4/5 p-8">
          <div className="relative h-[400px] w-full">
            <Image src="/team.png" alt="Summary" fill quality={100} className="object-contain" />
          </div>
        </div>
      </div>
      <p>
        The Python API has been rewritten to support the new EPA model and use the new backend
        infrastructure.
      </p>
      <h3>What&apos;s next?</h3>
      <p>
        Given the complete overhaul, most of my effort was spent recreating the existing
        functionality. I expect to add new features and improve the platform over the coming months.
        I am very open to community feedback and feature requests. I plan to maintain this blog and
        use the EPA model to answer interesting questions. Thanks for reading, and I hope you enjoy
        the new Statbotics!
      </p>
    </PageLayout>
  );
}
