import React from "react";

import { champsData, seasonData } from "./data";

const Page = () => {
  return (
    <div className="w-full flex-grow p-8">
      <div className="w-full h-full prose max-w-none">
        <h3>Evaluating the EPA Metric</h3>
        <h4>What is EPA</h4>
        Expected Points Added, or EPA for short, attempts to quantify a team&apos;s average point
        contribution to an FRC match. EPA builds upon concepts from the Elo rating system, but the
        output can be interpreted more analogously to a team&apos;s OPR (Offensive Power Rating).
        EPA is highly predictive, separates into components that can be interpreted individually,
        and is intuitive to understand. Statbotics provides realtime and historical EPA data and
        analysis tools to help teams understand and predict robot performance. You can read more
        about the EPA metric here. <br />
        In this article, we will evaluate the predictive power of EPA on historical data. We will
        compare EPA to other metrics, including OPR, Elo, ranking points, and random baselines.
        <table className="text-center">
          <thead>
            <tr>
              <th colSpan={2}>Year</th>
              <th colSpan={2}>Wins Baseline</th>
              <th colSpan={2}>Statbotics OPR</th>
              <th colSpan={2}>Statbotics Elo</th>
              <th colSpan={2}>Statbotics Combined</th>
              <th colSpan={2}>TBA Insights</th>
              <th colSpan={2}>Sykes Elo</th>
              <th colSpan={2}>EPA</th>
            </tr>
            <tr>
              <th>Year</th>
              <th>N</th>
              <th>Acc</th>
              <th>Brier</th>
              <th>Acc</th>
              <th>Brier</th>
              <th>Acc</th>
              <th>Brier</th>
              <th>Acc</th>
              <th>Brier</th>
              <th>Acc</th>
              <th>Brier</th>
              <th>Acc</th>
              <th>Brier</th>
              <th>Acc</th>
              <th>Brier</th>
            </tr>
          </thead>
          <tbody>
            {seasonData.map((season) => (
              <tr key={season.year}>
                <td>{season.year}</td>
                <td>{season.n}</td>
                <td>{season?.wins?.acc || "-"}</td>
                <td>{season?.wins?.brier || "-"}</td>
                <td>{season?.opr?.acc || "-"}</td>
                <td>{season?.opr?.brier || "-"}</td>
                <td>{season?.elo?.acc || "-"}</td>
                <td>{season?.elo?.brier || "-"}</td>
                <td>{season?.combined?.acc || "-"}</td>
                <td>{season?.combined?.brier || "-"}</td>
                <td>{season?.tba?.acc || "-"}</td>
                <td>{season?.tba?.brier || "-"}</td>
                <td>{season?.sykes?.acc || "-"}</td>
                <td>{season?.sykes?.brier || "-"}</td>
                <td>{season?.epa?.acc || "-"}</td>
                <td>{season?.epa?.brier || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Page;
