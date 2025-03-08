"use client";

/* eslint-disable react/no-children-prop */
import React, { useState } from "react";

import Image from "next/image";
import Link from "next/link";

import { CONDITIONAL_COLORS } from "../../../components/Table/shared";
import PageLayout from "../../../layouts/blogLayout";
import { classnames } from "../../../utils";
import SeasonTable from "../shared/table";

const PageContent = () => {
  const [showComparison, setShowComparison] = useState(false);
  const [showFactors, setShowFactors] = useState(false);
  const [showAdvantages, setShowAdvantages] = useState(false);
  const [showDisadvantages, setShowDisadvantages] = useState(false);

  return (
    <PageLayout
      title="The EPA Model: A Gentle Introduction"
      lead="The math behind EPA can be a bit confusing. This page will help you understand the EPA model, how it works, and how to best use it. No math required!"
    >
      <h3>Welcome to Statbotics</h3>
      <p>
        Hi! I&apos;m Abhijit, and I&apos;m the founder of Statbotics. I&apos;m so glad you&apos;re
        here! My goal with Statbotics is to share FRC data and analysis with a wider audience.
        Hopefully this page will help you better understand the EPA (Expected Points Added) model,
        its advantages and disadvantages, and how to best use it. If you still have any questions
        after reading, feel free to reach out to me on Chief Delphi or via email at{" "}
        <Link
          href="mailto:avgupta456@gmail.com"
          rel="noopener noreferrer"
          target="_blank"
          className="not-prose text_link text-blue-500"
        >
          avgupta456@gmail.com
        </Link>
        . Let&apos;s get started!
      </p>
      <h3>Why do we need the EPA model?</h3>
      <p>
        Two factors make strategy in FRC interesting. First, there is a new game every year, with
        new rules, new strategies, and new robots. Second, teams compete in alliances, making it
        difficult to directly attribute success or failure to a single team. If one alliance beats
        another, did certain teams contribute more or less than others? Should we assume that every
        robot in the winning alliance will win their next match?
      </p>
      <p>
        Scouting is a great way to better understand the strengths and weaknesses of other teams at
        an event, but it is impractical to scout every team at every event in the world.{" "}
        <strong>EPA stands for Expected Points Added</strong> and estimates how much a team scores
        in an average match using a few simple inputs and some statistics. Although it is not
        perfect, it can augment scouting data and reveal insights and trends.
      </p>
      <h3 onClick={() => setShowComparison(!showComparison)} className="cursor-pointer">
        Why not use OPR or Elo?{" "}
        <span className="text-xs text-blue-500">
          (Click to {showComparison ? "hide" : "expand"})
        </span>
      </h3>
      {showComparison && (
        <>
          <p>
            You may have heard about OPR or Elo before. These are two other popular methods for
            estimating a team&apos;s performance at an event. OPR is a method that tries to solve a
            system of linear equations to estimate a team&apos;s performance. You can read more
            about it{" "}
            <Link
              href="https://blog.thebluealliance.com/2017/10/05/the-math-behind-opr-an-introduction/"
              rel="noopener noreferrer"
              target="_blank"
              className="not-prose text_link text-blue-500"
            >
              here
            </Link>
            . Elo is a rating system used in Chess and other games. Although the standard Elo system
            only works for two player games with a binary win/loss outcome, Caleb Sykes successfully
            adapted it to FRC. You can read more about it{" "}
            <Link
              href="https://www.chiefdelphi.com/t/paper-frc-elo-2002-present/154250"
              rel="noopener noreferrer"
              target="_blank"
              className="not-prose text_link text-blue-500"
            >
              here
            </Link>
            .
          </p>
          <p>
            One downside of the OPR model is that it requires a couple matches to be played before
            it can be used. The results can be unstable and noisy in the early stages of an event.
            Unlike OPR, Elo smoothly updates a team&apos;s rating up or down after each match.
            However, Elo is in arbitrary units and does not have a clear interpretation. If you
            really care about predictive power, averaging the two model results improves accuracy.
            However, it now becomes difficult to compare and rank teams.
          </p>
          <p>
            EPA takes the best parts of both OPR and Elo and combines them into a single model.
            Mathematically, EPA is derived from Elo and behaves quite similarly. Instead of using
            arbitrary units, EPA is scaled to reflect a team&apos;s point contributions to their
            alliance. Like OPR, EPA can be separated into components for autonomous, teleoperated,
            and endgame scoring. EPA makes a couple improvements to Elo, improving its accuracy and
            predictive power. As a result, EPA is better than the OPR/Elo average and can be used to
            rank teams globally.
          </p>
        </>
      )}
      <h3>How does the EPA model work?</h3>
      <p>
        At it&apos;s core,{" "}
        <strong>the EPA model is simply a moving average of a team&apos;s performance</strong>.
        Initially, every team starts with an EPA rating (more on this later). To predict a match
        score, simply add up the EPA ratings of each team in the match. The alliance with the higher
        EPA rating is expected to win. After the match, the EPA ratings of the teams are updated.
        The difference between the predicted score and the actual score is called the
        &quot;error&quot;. The EPA ratings of the teams are updated based on the error. Statbotics
        also computes component EPAs, which measures a team&apos;s contribution to autonomous,
        teleoperated, and endgame scoring, and ranking point EPAs, which measures a team&apos;s
        contribution to bonus ranking points.
      </p>
      <p>
        If a team&apos;s EPA rating is too high, it will be penalized for overestimating its
        performance. If a team&apos;s EPA rating is too low, it will be rewarded for underestimating
        its performance. The amount of penalty or reward is proportional to the error. Over time,
        teams&apos; EPA ratings will converge to their true performance. This is the same concept
        behind Elo.
      </p>
      <h3 onClick={() => setShowFactors(!showFactors)} className="cursor-pointer">
        What other factors does the EPA model consider?{" "}
        <span className="text-xs text-blue-500">(Click to {showFactors ? "hide" : "expand"})</span>
      </h3>
      {showFactors && (
        <p>
          We&apos;re simplifying things here, but I wanted to give you a brief overview of some
          other factors the EPA model considers.
          <ul>
            <li>
              <strong>Team history</strong>: The EPA model doesn&apos;t start with a blank slate. At
              the beginning of a season, every team starts with an EPA rating based on their
              performance in the past two seasons. However, just because a team was good in the past
              doesn&apos;t mean they&apos;ll be good in the future. After just a couple matches, a
              team&apos;s EPA is mostly based on its performance in the current season.
            </li>
            <li>
              <strong>Point Units</strong>: The EPA model requires the Week 1 score mean and
              standard deviation to scale ratings and estimate match win probabilities. During Week
              1, the Week 0 statistics are used. After Week 1, the Week 1 statistics are used. No
              other score updates are made during the season.
            </li>
            <li>
              <strong>Quals vs Elims</strong>: The EPA model weighs qualification matches more than
              elimination matches. This is because elimination matches are all played with the same
              alliance, making it difficult to attribute playoff success or failure to a single
              team. Use the eye test to determine which teams perform best when the pressure is on.
            </li>
            <li>
              <strong>Season Progress</strong>: The EPA model is designed to quickly adapt to a
              team&apos;s performance in the early stages of a season. As the season progresses, the
              EPA model becomes more conservative and updates to changes slower. The EPA model also
              starts by measuring a team&apos;s contribution to their alliance&apos;s score, and
              transitions to measuring a team&apos;s contribution to their alliance&apos;s winning
              margin.
            </li>
          </ul>
        </p>
      )}
      <h3>How can I use the EPA model?</h3>
      <p>
        At an event, you can use the EPA model to predict match scores and estimate an
        alliance&apos;s chances of winning a match. You can simulate the outcomes of multiple
        matches to forecast your team&apos;s ranking at the end of the event. You can also compare
        teams at the event to see which teams would be the best alliance partners. As the season
        progresses, you can use the EPA model to compare teams across events and locations. You can
        look ahead to future events and see which teams are likely to perform well. You can also
        access historical data to see past trends and patterns.
      </p>
      <div className="not-prose flex justify-between gap-8">
        <div className="w-1/2">
          <div className="w-full h-[300px] relative">
            <Image src="/bubble.png" alt="Summary" fill quality={100} className="object-contain" />
          </div>
        </div>
        <div className="w-[2px] h-[300px] bg-gray-300" />
        <div className="w-1/2">
          <div className="w-full h-[300px] relative">
            <Image src="/team.png" alt="Summary" fill quality={100} className="object-contain" />
          </div>
        </div>
      </div>
      <p>
        The EPA model will get matches wrong sometimes. This is unavoidable. I have spent time to
        ensure the model is calibrated, meaning a 70% prediction is roughly 70% accurate. But that
        does mean the prediction will be wrong 30% of the time. Take all predictions and ratings
        with a grain of salt.
      </p>
      <h3 onClick={() => setShowAdvantages(!showAdvantages)} className="cursor-pointer">
        Advantages of the EPA model{" "}
        <span className="text-xs text-blue-500">
          (Click to {showAdvantages ? "hide" : "expand"})
        </span>
      </h3>
      {showAdvantages && (
        <p>
          <ul>
            <li>
              <strong>Accurate</strong>: The EPA model is more accurate than OPR and Elo. The EPA
              model is also slightly more accurate than the OPR/Elo average. The EPA model is well
              calibrated and can be used to forecast multiple matches into the future.
              <SeasonTable />
            </li>
            <li>
              <strong>Interpretable</strong>: Similar to OPR, the EPA model is in point units and
              can be easily interpreted. EPA can also be separated into components for auto, teleop,
              and endgame scoring. This makes it easy to see which teams are good at particular
              tasks. EPA also includes Ranking Point scores.
            </li>
            <li>
              <strong>Unbiased</strong>: Compared to manual scouting, EPA is unbiased. By applying
              the same model to every team, you can compare teams across events and locations
              without worrying about data quality and scouting biases. You can also use EPA to find
              teams that might have been overlooked due to team age, past performance, location, or
              other factors.
            </li>
          </ul>
        </p>
      )}
      <h3 onClick={() => setShowDisadvantages(!showDisadvantages)} className="cursor-pointer">
        Disadvantages of the EPA model{" "}
        <span className="text-xs text-blue-500">
          (Click to {showDisadvantages ? "hide" : "expand"})
        </span>
      </h3>
      {showDisadvantages && (
        <p>
          <ul>
            <li>
              <strong>Changes in performance</strong>: The EPA model assumes a team&apos;s
              performance is correlated with its previous performance. If your robot breaks for two
              matches, your EPA rating will likely drop. Even if you fix the problem, it might take
              a few matches for your EPA rating to recover. Similarly, if you add a new feature to
              your robot, it might take a few matches for your rating to increase. Scouting can be
              used to provide the real-world context that the EPA model lacks.
            </li>
            <li>
              <strong>Saturated scoring</strong>: This mainly applies to the top 1% of teams. The
              EPA model assumes that an alliance&apos;s score is the sum of the EPA ratings of each
              team. If two or three exceptionally strong teams are on the same alliance, they might
              saturate the scoring opportunities, leading to a lower score than expected and
              unfairly reducing their EPA ratings.
            </li>
          </ul>
        </p>
      )}
      <h3>Frequently Asked Questions</h3>
      <p>
        <ul>
          <li>
            <strong>Where can I access EPA data?</strong> Congratulations on finding the Statbotics
            website! This is the primary home for everything EPA. Check out the various tabs and
            links to get a feel for the site. There are also{" "}
            <Link
              href="/docs/python"
              rel="noopener noreferrer"
              target="_blank"
              className="not-prose text_link text-blue-500"
            >
              Python
            </Link>{" "}
            and{" "}
            <Link
              href="/docs/rest"
              rel="noopener noreferrer"
              target="_blank"
              className="not-prose text_link text-blue-500"
            >
              REST
            </Link>{" "}
            APIs available for developers to integrate EPA into their own applications.
          </li>
          <li>
            <strong>How much do past seasons affect results?</strong> Using data from past seasons
            helps the EPA model adapt to a team&apos;s performance in the early stages of a season.
            After a few matches, the EPA model will be based primarily on the current season&apos;s
            data. By your second event, your EPA rating will be almost entirely based on the current
            season&apos;s data.
          </li>
          <li>
            <strong>What do the colors mean?</strong> The website uses a color scheme to visually
            represent the percentile of a team&apos;s EPA rating relative to other teams. The blue
            highlight represents the{" "}
            <span className={classnames(CONDITIONAL_COLORS[4], "p-1 rounded")}>
              top 1% of teams
            </span>
            , the dark green highlight represents the{" "}
            <span className={classnames(CONDITIONAL_COLORS[3], "p-1 rounded")}>
              top 10% of teams
            </span>
            , and the light green highlight represents the{" "}
            <span className={classnames(CONDITIONAL_COLORS[2], "p-1 rounded")}>
              top 25% of teams
            </span>
            . Most teams are not highlighted (25% to 75%), and the{" "}
            <span className={classnames(CONDITIONAL_COLORS[0], "p-1 rounded")}>
              bottom 25% of teams
            </span>{" "}
            are highlighted in red.The colors are designed to be easy to read and distinguish
            between teams.
          </li>
          <li>
            <strong>Where can I learn more?</strong> Check out the rest of the blog posts for more
            information on the derivation and implementation of the EPA model. You can also read the{" "}
            <Link
              href="https://www.chiefdelphi.com/t/statbotics-2023-season/423703"
              rel="noopener noreferrer"
              target="_blank"
              className="not-prose text_link text-blue-500"
            >
              Chief Delphi thread
            </Link>{" "}
            to learn more about active development.
          </li>
          <li>
            <strong>How can I report bugs/feature requests?</strong> Feel free to share them on the
            Chief Delphi Thread. You can also use the Canny link in the header dropdown or contact
            me directly (email linked above).
          </li>
        </ul>
      </p>
    </PageLayout>
  );
};

export default PageContent;
