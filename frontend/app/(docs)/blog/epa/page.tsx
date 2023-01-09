/* eslint-disable react/no-children-prop */
import "katex/dist/katex.min.css";
import rehypeKatex from "rehype-katex";
import remarkMath from "remark-math";

import React from "react";
import ReactMarkdown from "react-markdown";

const renderMath = (str: string) => {
  return (
    <ReactMarkdown
      //inline
      className="inline-block m-0 not-prose"
      children={`$${str}$`}
      remarkPlugins={[remarkMath]}
      rehypePlugins={[rehypeKatex]}
    />
  );
};

const renderMathBlock = (str: string) => {
  return (
    <ReactMarkdown
      className="w-full text-center"
      children={`$$${str}$$`}
      remarkPlugins={[remarkMath]}
      rehypePlugins={[rehypeKatex]}
    />
  );
};

const Page = () => {
  return (
    <div className="w-4/5 mx-auto">
      <div className="w-full h-full py-16 prose prose-slate max-w-none">
        <h2 className="w-full text-center">The EPA Model</h2>
        <p className="lead">
          The Expected Points Added (EPA) model builds upon the Elo rating system, and provides
          improved prediction accuracy, interpretability, and accessibility. Let&apos;s dive into
          the details!
        </p>
        <h3>Motivation</h3>
        <p>
          Prior to 2023, Statbotics displayed both Elo and OPR ratings for each team. OPR was
          separated into Auto, Teleop, and Endgame components, while sorting was primarily done on
          Elo, the more predictive model. Match predictions were made by averaging the win
          probabilities from each model, which slightly outperformed either model individually. The
          complexity of this setup was not ideal, and resulted in reduced data freshness and
          inconsistent sorting/component contributions. The EPA model was developed to replace both
          Elo and OPR with a single unified system. At a high level, the EPA model converts Elo into
          point contributions, and then makes several modifications to improve accuracy and
          interpretability. In this article, I&apos;ll dive into the details of the EPA model, and
          how it compares to existing approaches.
        </p>
        <h3>Derivation from Elo</h3>
        <p>
          As alluded to above, the EPA model builds upon the Elo rating system. But what is Elo, and
          how exactly does it work, especially for FRC? The Elo rating system is a well-known method
          for ranking chess players, and has been adapted to many other domains. Each player is
          given an initial rating, and then the rating is updated after each game depending on the
          predicted and actual outcome. Several modifications have been made to adapt Elo for use in
          FRC, specifically to handle alliances, incorporate winning margin, and account for a new
          game each year.
        </p>
        <p>
          Each team starts with an Elo rating of 1500. An alliance&apos;s rating is the sum of the
          ratings of its three teams. To predict the winner of a match, the Elo ratings of the two
          alliances are compared. The win probability is a logistic function of the difference
          between the two ratings:
        </p>
        {renderMathBlock("P_{win} = \\frac{1}{1 + 10^{\\frac{d}{400}}}")}
        <p>where {renderMath("d")} is the difference between the two ratings.</p>
        <p>
          After the match, the rating of each team on the winning alliance is increased, and the
          rating of each team on the losing alliance is decreased. The amount of change is
          proportional to the surprise of the outcome. Since each year is a new game, scoring must
          be standardized into consistent units. This is done by dividing by the standard deviation
          of Week 1 scores. The predicted score margin is defined as 0.004 times the difference in
          ratings, and the actual score margin is the difference between actual scores divided by
          the standard deviation. The amount of change is then proportional to the difference
          between the predicted and actual score margins:
        </p>
        {renderMathBlock(
          "\\text{predicted score margin} = 0.004 \\times (\\text{red rating} - \\text{blue rating})"
        )}
        {renderMathBlock(
          "\\text{actual score margin} = \\frac{\\text{red score} - \\text{blue score}}{\\sigma}"
        )}
        {renderMathBlock(
          "\\Delta R = K \\times (\\text{actual score margin} - \\text{predicted score margin})"
        )}
        <p>
          where {renderMath("K")} is a constant that controls the amount of change. K is set to 12
          for qualification matches and 3 for playoff matches. Small adjustments are made to
          penalize rookie teams and apply mean reversion year over year. For its relative
          simplicity, Elo has proven to be a very effective model for FRC.
        </p>
        <p>
          I set out to convert Elo ratings from arbitrary units into year-specific points. Instead
          of setting the initial rating to 1500, I set it to one third of the average score in Week
          1. The alliance rating is the sum of the team ratings, and doubles as the predicted
          alliance score. The predicted score margin is then the difference between the two alliance
          scores, and the actual score margin is the difference between the actual scores. Both
          require no additional scaling, and are in the same units as the scores. All that is left
          is to update the ratings after each match.
        </p>
        <p>
          Suppose two alliances have a rating difference of X, but play a match consistent with a
          rating difference of Y. The predicted score margin is {renderMath("0.004 \\times X")}, and
          the actual score margin is {renderMath("0.004 \\times Y")}. The surprise of the outcome,
          measured in standard deviations is {renderMath("\\frac{(Y - X)}{250}")}. Each team&apos;s
          rating is updated by {renderMath("K \\times \\frac{(Y - X)}{250}")} With three teams on
          each alliance, the new rating difference is{" "}
          {renderMath("X + 6 \\times K \\times \\frac{(Y - X)}{250}")}. The difference between the
          new and old rating difference is {renderMath("6 \\times K \\times \\frac{(Y - X)}{250}")}.
          Substituting {renderMath("K=12")}, Elo updates ratings by{" "}
          {renderMath("\\frac{72}{250}\\approx29\\%")} of the difference between the current and
          observed ratings.
        </p>
        <p>
          Extending this approach to the EPA model, each team&apos;s EPA is updated according to the
          equations below:
        </p>
        {renderMathBlock("\\text{predicted score margin} = \\text{red EPA} - \\text{blue EPA}")}
        {renderMathBlock("\\text{actual score margin} = \\text{red score} - \\text{blue score}")}
        {renderMathBlock(
          "\\Delta EPA = \\frac{72}{250} \\times (\\text{actual score margin} - \\text{predicted score margin})"
        )}
        <p>
          So far, the EPA model is identical to the Elo model, with the only modification being a
          unit conversion.{" "}
        </p>
        <h3>Modifications</h3>
        <h3>Component EPA</h3>
        <h3>Ranking Point Predictions</h3>
        <h3>Year Normalized EPA</h3>
      </div>
    </div>
  );
};

export default Page;
