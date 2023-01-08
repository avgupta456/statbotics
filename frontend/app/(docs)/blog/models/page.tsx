"use client";

import React, { useState } from "react";
import Select from "react-select";

import Link from "next/link";

import { yearOptions } from "../../../../components/filterConstants";
import { classnames } from "../../../../utils";
import { champsData, seasonData } from "./data";

const SeasonTable = () => {
  const orderedMethods = ["wins", "opr", "elo", "combined", "tba", "sykes", "epa"];
  const orderedMetrics = ["acc", "brier"];

  const [methods, setMethods] = useState(["wins", "opr", "sykes", "epa"]);
  const [metrics, setMetrics] = useState(["acc"]);
  const [champs, setChamps] = useState(false);
  const [startYear, setStartYear] = useState(2016);
  const [endYear, setEndYear] = useState(2022);

  const methodToName = {
    wins: "Wins Baseline",
    opr: "OPR",
    elo: "Elo",
    combined: "OPR + Elo",
    tba: "TBA Insights",
    sykes: "Caleb Sykes Elo",
    epa: "EPA",
  };

  const metricsToName = {
    acc: "Accuracy",
    brier: "Brier Score",
  };

  const data: any[] = champs ? champsData : seasonData;

  const totalAcc = methods.map((method) => {
    let correct = 0;
    let total = 0;
    data
      .filter((season) => season.year >= startYear && season.year <= endYear)
      .forEach((season) => {
        correct += (season[method]?.acc || 0) * season.n;
        total += season.n;
      });
    return correct / Math.max(1, total);
  });

  const maxTotalAcc = Math.max(...totalAcc);

  const totalBrier = methods.map((method) => {
    let brier = 0;
    let total = 0;
    data
      .filter((season) => season.year >= startYear && season.year <= endYear)
      .forEach((season) => {
        brier += (season[method]?.brier || 1) * season.n;
        total += season.n;
      });
    return brier / Math.max(1, total);
  });

  const minTotalBrier = Math.min(...totalBrier);

  const recentAcc = methods.map((method) => {
    let correct = 0;
    let total = 0;
    data
      .filter((season) => season.year >= startYear && season.year <= endYear)
      .forEach((season) => {
        if (season.year >= 2016) {
          correct += (season[method]?.acc || 0) * season.n;
          total += season.n;
        }
      });
    return correct / Math.max(1, total);
  });

  const maxRecentAcc = Math.max(...recentAcc);

  const recentBrier = methods.map((method) => {
    let brier = 0;
    let total = 0;
    data
      .filter((season) => season.year >= startYear && season.year <= endYear)
      .forEach((season) => {
        if (season.year >= 2016) {
          brier += (season[method]?.brier || 0) * season.n;
          total += season.n;
        }
      });
    return brier / Math.max(1, total);
  });

  const minRecentBrier = Math.min(...recentBrier);

  const formatAcc = (acc) => {
    let formatAcc = "-";
    if (acc) {
      formatAcc = `${(acc * 100).toFixed(2)}%`;
    }
    return formatAcc;
  };

  const formatBrier = (brier) => {
    let formatBrier = "-";
    if (brier) {
      formatBrier = brier.toFixed(4);
    }
    return formatBrier;
  };

  return (
    <div className="overflow-x-scroll scrollbar-hide">
      <h3 className="w-full text-center mb-8">
        Comparison of Historical Prediction Performance (2002 - Present)
      </h3>
      <div className="not-prose mb-4">
        <table className="text-center table-fixed mx-auto text-sm">
          <thead>
            <tr key="header_1">
              <th colSpan={2}>
                <div className="w-32 py-1">Year</div>
              </th>
              {methods.map((method) => (
                <th
                  key={method}
                  colSpan={metrics.length}
                  className="border-l-[1px] border-gray-500 w-40 py-1"
                >
                  <div className="w-40 py-1">{methodToName[method]}</div>
                </th>
              ))}
            </tr>
            <tr key="header_2" className="border-b-[1px] border-gray-500">
              <th className="w-16 py-1">Year</th>
              <th className="w-16 py-1">N</th>
              {methods.map(() => (
                <>
                  {metrics.includes("acc") && (
                    <th className="border-l-[1px] border-gray-500 w-20 py-1">Acc</th>
                  )}
                  {metrics.includes("brier") && (
                    <th
                      className={classnames(
                        "w-20 py-1",
                        metrics.includes("acc") ? "" : "border-l-[1px] border-gray-500"
                      )}
                    >
                      Brier
                    </th>
                  )}
                </>
              ))}
            </tr>
          </thead>
          <tbody>
            {data
              .filter((season) => season.year >= startYear && season.year <= endYear)
              .map((season) => {
                const currMethods = [
                  methods.includes("wins") ? season?.wins : null,
                  methods.includes("opr") ? season?.opr : null,
                  methods.includes("elo") ? season?.elo : null,
                  methods.includes("combined") ? season?.combined : null,
                  methods.includes("tba") ? season?.tba : null,
                  methods.includes("sykes") ? season?.sykes : null,
                  methods.includes("epa") ? season?.epa : null,
                ].filter((currMethod) => currMethod !== null);

                const maxAcc = Math.max(...currMethods.map((currMethod) => currMethod?.acc || 0));
                const minBrier = Math.min(
                  ...currMethods.map((currMethod) => currMethod?.brier || 1)
                );

                return (
                  <tr key={season.year} className="border-b-[1px] border-gray-200">
                    <td className="w-16 py-1">{season.year}</td>
                    <td className="w-16 py-1">{season.n}</td>
                    {currMethods.map((currMethod) => {
                      let dispAcc = formatAcc(currMethod?.acc);
                      let dispBrier = formatBrier(currMethod?.brier);

                      return (
                        <>
                          {metrics.includes("acc") && (
                            <td
                              className={classnames(
                                "border-l-[1px] border-gray-500",
                                metrics.length === 2 ? "w-20 py-1" : "w-40 py-1"
                              )}
                            >
                              {currMethod?.acc >= maxAcc ? <strong>{dispAcc}</strong> : dispAcc}
                            </td>
                          )}
                          {metrics.includes("brier") && (
                            <td
                              className={classnames(
                                metrics.length === 2 ? "w-20 py-1" : "w-40 py-1",
                                metrics.includes("acc") ? "" : "border-l-[1px] border-gray-500"
                              )}
                            >
                              {currMethod?.brier <= minBrier ? (
                                <strong>{dispBrier}</strong>
                              ) : (
                                dispBrier
                              )}
                            </td>
                          )}
                        </>
                      );
                    })}
                  </tr>
                );
              })}
            <tr key="total" className="bg-blue-100 border-double border-t-4 border-gray-500">
              <td colSpan={2} className="w-32 py-1">
                <strong>
                  {startYear} - {endYear}
                </strong>
              </td>
              {methods.map((method, i) => {
                const dispAcc =
                  method === "tba" && startYear <= 2015 ? "-" : formatAcc(totalAcc[i]);
                const dispBrier =
                  method === "tba" && startYear <= 2015 ? "-" : formatBrier(totalBrier[i]);

                return (
                  <>
                    {metrics.includes("acc") && (
                      <td className="border-l-[1px] border-gray-500 py-1">
                        {totalAcc[i] >= maxTotalAcc ? <strong>{dispAcc}</strong> : dispAcc}
                      </td>
                    )}
                    {metrics.includes("brier") && (
                      <td className="py-1">
                        {totalBrier[i] <= minTotalBrier ? <strong>{dispBrier}</strong> : dispBrier}
                      </td>
                    )}
                  </>
                );
              })}
            </tr>
            {startYear <= 2015 && endYear > 2015 && (
              <tr key="recent" className="bg-blue-100">
                <td colSpan={2} className="w-32 py-1">
                  <strong>2016 - {endYear}</strong>
                </td>
                {methods.map((method, i) => {
                  const dispAcc = formatAcc(recentAcc[i]);
                  const dispBrier = formatBrier(recentBrier[i]);
                  return (
                    <>
                      {metrics.includes("acc") && (
                        <td
                          className={classnames(
                            "border-l-[1px] border-gray-500",
                            metrics.length === 2 ? "w-20 py-1" : "w-40 py-1"
                          )}
                        >
                          {recentAcc[i] >= maxRecentAcc ? <strong>{dispAcc}</strong> : dispAcc}
                        </td>
                      )}
                      {metrics.includes("brier") && (
                        <td
                          className={classnames(metrics.length === 2 ? "w-20 py-1" : "w-40 py-1")}
                        >
                          {recentBrier[i] <= minRecentBrier ? (
                            <strong>{dispBrier}</strong>
                          ) : (
                            dispBrier
                          )}
                        </td>
                      )}
                    </>
                  );
                })}
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <div className="w-full flex flex-wrap lg:justify-center text-xs">
        <div className="flex flex-wrap hover:bg-gray-100 px-4 py-2">
          <div className="font-bold">Include methods: </div>
          {Object.keys(methodToName).map((method) => (
            <div
              key={method}
              className="flex items-center px-1 ml-2 rounded cursor-pointer hover:bg-blue-100"
              onClick={() => {
                if (methods.includes(method)) {
                  setMethods(methods.filter((currMethod) => currMethod !== method));
                } else {
                  const newMethods = [...methods, method];
                  setMethods(
                    orderedMethods.filter((currMethod) => newMethods.includes(currMethod))
                  );
                }
              }}
            >
              <input
                type="checkbox"
                className="mr-1"
                checked={methods.includes(method)}
                onChange={() => {}}
              />
              <div className="cursor-pointer">{methodToName[method]}</div>
            </div>
          ))}
        </div>
        <div className="flex items-center hover:bg-gray-100 px-4 py-2">
          <div className="font-bold">Include metrics: </div>
          {["acc", "brier"].map((metric) => (
            <div
              key={metric}
              className="flex items-center px-1 ml-2 rounded cursor-pointer hover:bg-blue-100"
              onClick={() => {
                if (metrics.includes(metric)) {
                  setMetrics(metrics.filter((currMetric) => currMetric !== metric));
                } else {
                  const newMetrics = [...metrics, metric];
                  setMetrics(
                    orderedMetrics.filter((currMetric) => newMetrics.includes(currMetric))
                  );
                }
              }}
            >
              <input
                type="checkbox"
                className="mr-1"
                checked={metrics.includes(metric)}
                onChange={() => {}}
              />
              <div className="cursor-pointer">{metricsToName[metric]}</div>
            </div>
          ))}
        </div>
        <div className="flex items-center hover:bg-gray-100 px-4 py-2">
          <div className="font-bold">Show: </div>
          <div
            className="flex items-center px-1 ml-2 rounded cursor-pointer hover:bg-blue-100"
            onClick={() => setChamps(true)}
          >
            <input type="checkbox" className="mr-1" checked={champs} onChange={() => {}} />
            <div className="cursor-pointer">Only Champs</div>
          </div>
          <div
            className="flex items-center px-1 ml-2 rounded cursor-pointer hover:bg-blue-100"
            onClick={() => setChamps(false)}
          >
            <input type="checkbox" className="mr-1" checked={!champs} onChange={() => {}} />
            <div className="cursor-pointer">Entire Season</div>
          </div>
        </div>
        <div className="flex items-center hover:bg-gray-100 px-4 py-2">
          <div className="font-bold">Start Year: </div>
          <Select
            instanceId="start-year-select"
            menuPlacement="top"
            className="w-24 ml-1"
            styles={{
              menu: (provided) => ({ ...provided, zIndex: 9999 }),
            }}
            options={yearOptions}
            onChange={(e) => setStartYear((e?.value ?? 2002) as number)}
            value={{
              value: startYear.toString(),
              label: startYear.toString(),
            }}
          />
        </div>
        <div className="flex items-center hover:bg-gray-100 px-4 py-2">
          <div className="font-bold">End Year: </div>
          <Select
            instanceId="end-year-select"
            menuPlacement="top"
            className="w-24 ml-1"
            styles={{
              menu: (provided) => ({ ...provided, zIndex: 9999 }),
            }}
            options={yearOptions}
            onChange={(e) => setEndYear((e?.value ?? 2002) as number)}
            value={{
              value: endYear.toString(),
              label: endYear.toString(),
            }}
          />
        </div>
      </div>
      <div className="w-full text-sm text-center mb-4">
        Google Sheets Link:{" "}
        <Link
          className="text_link"
          rel="noopener noreferrer"
          target="_blank"
          href="https://docs.google.com/spreadsheets/d/1NlhOeU78uuPqqbcNh_v2WlLlDwF41wl8gzj3Elx38KM/edit?usp=sharing"
        >
          here
        </Link>
      </div>
    </div>
  );
};

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
