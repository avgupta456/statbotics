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
      <div className="w-full flex flex-wrap lg:justify-center text-xs mb-4">
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
            <strong>OPR</strong>: OPR attempts to calculate a team&aspos;s contribution to their
            alliance&aspos;s final score. OPR uses linear algebra to minimize the sum of squared
            errors between the predicted and actual scores. We evaluate a variant of OPR called
            ixOPR that incorporates a prior during ongoing events. TBA Insights and Statbotics both
            incorporate ixOPR.
          </li>
          <li>
            <strong>Elo</strong>: The Elo rating system is a well-known model for predicting the
            outcome of chess matches. Elo iteratively updates a team&apos;s rating based on the
            difference between the predicted and observed winning margin. Caleb Sykes modified Elo
            for FRC, and we include both his original mode and the Statbotics implementation.
          </li>
          <li>
            <strong>EPA</strong>: EPA attempts to quantify a team&apos;s average point contribution
            to an FRC match. EPA builds upon concepts from the Elo rating system, but the output can
            be interpreted more analogously to a team&apos;s OPR (Offensive Power Rating). EPA is
            highly predictive, separates into components that can be interpreted individually, and
            is intuitive to understand. More details are available{" "}
            <Link href="/blog/epa" className="text_link">
              here
            </Link>
            .
          </li>
        </ul>
        <h3>Evaluating models</h3>
        <p></p>
        <SeasonTable />
      </div>
    </div>
  );
};

export default Page;
