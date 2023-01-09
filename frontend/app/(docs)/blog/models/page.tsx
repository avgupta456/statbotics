import React from "react";

import Link from "next/link";

import SeasonTable from "../table";

const Page = () => {
  return (
    <div className="w-4/5 mx-auto flex-grow">
      <div className="w-full h-full py-16 prose prose-slate max-w-none">
        <h2 className="w-full text-center">Evaluating FRC Rating Models</h2>
        <p className="lead">
          How do you choose between FRC rating models? We compare several models on three
          characteristics: predictive power, interpretability, and accessibility. Expected Points
          Added (EPA) is a new metric deployed on Statbotics that excels in all three categories.
        </p>
        <h3>Summarizing the Options</h3>
        <p>
          Given the importance of match strategy and alliance selection, several models have been
          developed that attempt to quantify an FRC team&apos;s contribution to match outcomes. We
          consider a wins baseline, the popular OPR and Elo rating systems, and the new Expected
          Points Added (EPA) model deployed on Statbotics. A brief summary of each model is included
          below.
        </p>
        <ul>
          <li>
            <strong>Wins Baseline</strong>: This simple model only considers a team&apos;s record.
            The alliance with the most wins that year is predicted to win. This model is roughly how
            a human would intuitively predict the outcome of a match, and is a good baseline for
            evaluating more complex models.
          </li>
          <li>
            <strong>Offensive Power Rating (OPR)</strong>: OPR uses linear algebra to minimize the
            sum of squared errors between the predicted and actual scores. We evaluate a variant of
            OPR called ixOPR that incorporates a prior during ongoing events. TBA Insights and
            Statbotics both incorporate ixOPR.
          </li>
          <li>
            <strong>Elo Rating</strong>: The Elo rating system is a well-known model for predicting
            the outcome of chess matches. In FRC, Elo iteratively updates a team&apos;s rating based
            on the difference between the predicted and observed winning margin. Caleb Sykes
            modified Elo for FRC, and we include both his original mode and the Statbotics
            implementation.
          </li>
          <li>
            <strong>Expected Points Added (EPA)</strong>: EPA attempts to quantify a team&apos;s
            average point contribution to an FRC match. EPA builds upon concepts from the Elo rating
            system, but the units are in points and can be interpreted more analogously to a
            team&apos;s OPR. EPA is highly predictive and separates into components that can be
            interpreted individually. More details are available{" "}
            <Link href="/blog/epa" className="text_link">
              here
            </Link>
            .
          </li>
        </ul>
        <h3>Evaluating models</h3>
        <p>
          When choosing between FRC rating models, multiple factors play a role. In particular, we
          consider the following three:
        </p>
        <ul>
          <li>
            <strong>Predictive Power</strong>: How well does the model predict the outcome of a
            match? We evaluate this by comparing the model&apos;s predictions to the actual
            outcomes.
          </li>
          <li>
            <strong>Interpretability</strong>: How easy is it to understand the model&apos;s
            predictions and incorporate them into a strategy? Ratings in point units and ratings
            that can be separated into components are more interpretable.
          </li>
          <li>
            <strong>Accessibility</strong>: How easy is it to use the model? Models that are
            available on a website or API are more accessible than models that require user
            calculations.
          </li>
        </ul>
        <h3>Predictive Power</h3>
        <p>
          We evaluate predictive power by comparing the model&apos;s predictions to the actual
          outcomes. Accuracy is measured by the percentage of matches that the model correctly
          predicted. Brier Score measures the mean squared error and quantifies calibration and
          reliability. A Brier Score of 0 indicates perfect calibration and a Brier Score of 0.25
          indicates no skill. Going back to 2002, we evaluate models on 160,000 matches, with
          special emphasis on 15,000 champs matches and the 80,000 recent matches since 2016.
        </p>
        <p>
          Simply predicting &quot;Red Alliance&quot; each match results in an accuracy of 50%. To
          approximate the accuracy of an idle spectator, we consider a simple wins baseline that
          predicts the winner based on the alliance with the most combined wins. To evaluate the
          predictive power of a model, we compare its accuracy to the accuracy of the wins baseline.
          This reflects the extent to which the model is able to predict match outcomes beyond the
          eye test.
        </p>
        <p>The table below can be customzied to include and exclude models, metrics, and years.</p>
        <SeasonTable />
        <p>
          The Wins Baseline predicts the outcome of a match with a 65% accuracy on average. In
          comparison, the OPR model has a 68% accuracy, the Elo model has a 69% accuracy, and the
          EPA model has a 70% accuracy. Since 2016, these numbers are 66% (Wins), 70% (OPR), 71%
          (Elo), and 72% (EPA). While the EPA model outperforms the OPR/Elo models by only 1-2%, in
          relation to the wins baseline,{" "}
          <strong>
            the EPA model outperforms the baseline by ~20% more than the OPR/Elo models
          </strong>
          . The EPA model is the best performing model in 15 of the 20 years, including six of the
          last seven. The one exception is 2018, where the EPA model struggles somewhat with the
          nonlinear scoring system.
        </p>
        <p>
          There are two caveats regarding the EPA model&apos;s improved performance. While we
          compare EPA to Elo and OPR individually, Statbotics previously used a combination of both,
          which has improved accuracy compared to either model alone. Still, the EPA model
          individually outperforms this ensemble, and future EPA iterations can ensemble with other
          models to reach even higher performance. Second, while the EPA model significantly
          outperforms other models during the season, this does not translate to champs. EPA
          stabilizes to an accurate prediction faster during the season, but by champs, Elo has
          caught up and is roughly equivalent to EPA.
        </p>
        <h3>Interpretability</h3>
        <p>
          We evaluate interpretability by considering the units of the model and the ability to
          separate the model into components. The OPR and EPA models are in point units, and can be
          separated into auto, teleop, and endgame components. Elo is in arbitrary units (1500 mean,
          ~2000 max) and cannot be separated into components. One benefit of the Elo model is that
          ratings can be roughly compared across years. Using normalized EPA, we can compare EPA
          ratings across years as well (blog post coming soon). In summary, the EPA model combines
          the best of both worlds: point units, separable into components, and comparable across
          years.
        </p>
        <h3>Accessibility</h3>
        <p>
          We evaluate accessibility by considering the availability of the model. Statbotics
          previously included the OPR and Elo models, but has now transitioned to the EPA model. The
          Blue Alliance calculates OPR and their own TBA Insights model. Caleb Sykes publishes a
          comprehensive scouting database on Excel. Statbotics and TBA have APIs that allow for
          integration with external projects. Each model has distribution channels that are more or
          less equally accessible to teams.
        </p>
        <h3>Conclusion</h3>
        <p>
          The EPA model is the best performing model in 15 of the 20 years, including six of the
          last seven. The EPA model is the most interpretable model, with point units, separable
          components, and year-normalized ratings. Finally, the EPA model is highly accessible,
          available on the Statbotics website and through Python API. In summary, we highly
          recommend the EPA model for teams and scouting systems. Please reach out to us if you have
          any questions or feedback.
        </p>
      </div>
    </div>
  );
};

export default Page;
