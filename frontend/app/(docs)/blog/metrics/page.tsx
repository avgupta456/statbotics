"use client";

import React, { useState } from "react";

import { champsData, seasonData } from "./data";

const SeasonTable = () => {
  const orderedMethods = ["wins", "opr", "elo", "combined", "tba", "sykes", "epa"];
  const orderedMetrics = ["acc", "brier"];

  const [methods, setMethods] = useState(orderedMethods);
  const [metrics, setMetrics] = useState(orderedMetrics);
  const [champs, setChamps] = useState(false);

  const methodToName = {
    wins: "Wins Baseline",
    opr: "Statbotics OPR",
    elo: "Statbotics Elo",
    combined: "Statbotics Combined",
    tba: "TBA Insights",
    sykes: "Caleb Sykes Elo",
    epa: "Statbotics EPA",
  };

  const metricsToName = {
    acc: "Accuracy",
    brier: "Brier Score",
  };

  const data = champs ? champsData : seasonData;

  const totalAcc = methods.map((method) => {
    let correct = 0;
    let total = 0;
    data.forEach((season) => {
      correct += (season[method]?.acc || 0) * season.n;
      total += season.n;
    });
    return correct / total;
  });

  const maxTotalAcc = Math.max(...totalAcc);

  const totalBrier = methods.map((method) => {
    let brier = 0;
    let total = 0;
    data.forEach((season) => {
      brier += (season[method]?.brier || 1) * season.n;
      total += season.n;
    });
    return brier / total;
  });

  const minTotalBrier = Math.min(...totalBrier);

  const recentAcc = methods.map((method) => {
    let correct = 0;
    let total = 0;
    data.forEach((season) => {
      if (season.year >= 2016) {
        correct += (season[method]?.acc || 0) * season.n;
        total += season.n;
      }
    });
    return correct / total;
  });

  const maxRecentAcc = Math.max(...recentAcc);

  const recentBrier = methods.map((method) => {
    let brier = 0;
    let total = 0;
    data.forEach((season) => {
      if (season.year >= 2016) {
        brier += (season[method]?.brier || 0) * season.n;
        total += season.n;
      }
    });
    return brier / total;
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
    <div>
      <div className="flex flex-row">
        <div className="font-bold">Include methods: </div>
        {Object.keys(methodToName).map((method) => (
          <div
            key={method}
            className="flex justify-center px-1 ml-2 rounded cursor-pointer hover:bg-blue-100"
            onClick={() => {
              if (methods.includes(method)) {
                setMethods(methods.filter((currMethod) => currMethod !== method));
              } else {
                const newMethods = [...methods, method];
                setMethods(orderedMethods.filter((currMethod) => newMethods.includes(currMethod)));
              }
            }}
          >
            <input
              type="checkbox"
              className="mr-1"
              checked={methods.includes(method)}
              onChange={() => {}}
            />
            <label className="cursor-pointer">{methodToName[method]}</label>
          </div>
        ))}
      </div>
      <div className="flex flex-row">
        <div className="font-bold">Include metrics: </div>
        {["acc", "brier"].map((metric) => (
          <div
            key={metric}
            className="flex justify-center px-1 ml-2 rounded cursor-pointer hover:bg-blue-100"
            onClick={() => {
              if (metrics.includes(metric)) {
                setMetrics(metrics.filter((currMetric) => currMetric !== metric));
              } else {
                const newMetrics = [...metrics, metric];
                setMetrics(orderedMetrics.filter((currMetric) => newMetrics.includes(currMetric)));
              }
            }}
          >
            <input
              type="checkbox"
              className="mr-1"
              checked={metrics.includes(metric)}
              onChange={() => {}}
            />
            <label className="cursor-pointer">{metricsToName[metric]}</label>
          </div>
        ))}
      </div>
      <div className="flex flex-row">
        <div className="font-bold">Show: </div>
        <div
          className="flex justify-center px-1 ml-2 rounded cursor-pointer hover:bg-blue-100"
          onClick={() => setChamps(true)}
        >
          <input type="checkbox" className="mr-1" checked={champs} onChange={() => {}} />
          <label className="cursor-pointer">Only Champs</label>
        </div>
        <div
          className="flex justify-center px-1 ml-2 rounded cursor-pointer hover:bg-blue-100"
          onClick={() => setChamps(false)}
        >
          <input type="checkbox" className="mr-1" checked={!champs} onChange={() => {}} />
          <label className="cursor-pointer">Entire Season</label>
        </div>
      </div>
      <table className="text-center">
        <thead>
          <tr>
            <th colSpan={2}>Year</th>
            {methods.map((method) => (
              <th key={method} colSpan={metrics.length} className="border-l-[1px] border-gray-500">
                {methodToName[method]}
              </th>
            ))}
          </tr>
          <tr>
            <th>Year</th>
            <th>N</th>
            {methods.map(() => (
              <>
                {metrics.includes("acc") && (
                  <th className="border-l-[1px] border-gray-500">Accuracy</th>
                )}
                {metrics.includes("brier") && <th>Brier</th>}
              </>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((season) => {
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
            const minBrier = Math.min(...currMethods.map((currMethod) => currMethod?.brier || 1));

            return (
              <tr key={season.year}>
                <td>{season.year}</td>
                <td>{season.n}</td>
                {currMethods.map((currMethod) => {
                  let dispAcc = formatAcc(currMethod?.acc);
                  let dispBrier = formatBrier(currMethod?.brier);

                  return (
                    <>
                      {metrics.includes("acc") && (
                        <td className="border-l-[1px] border-gray-500">
                          {currMethod?.acc >= maxAcc ? <strong>{dispAcc}</strong> : dispAcc}
                        </td>
                      )}
                      {metrics.includes("brier") && (
                        <td>
                          {currMethod?.brier <= minBrier ? <strong>{dispBrier}</strong> : dispBrier}
                        </td>
                      )}
                    </>
                  );
                })}
              </tr>
            );
          })}
          <tr className="bg-blue-100 border-double border-t-4 border-gray-500">
            <td colSpan={2}>
              <strong>2002 - 2022</strong>
            </td>
            {methods.map((method, i) => {
              const dispAcc = method === "tba" ? "-" : formatAcc(totalAcc[i]);
              const dispBrier = method === "tba" ? "-" : formatBrier(totalBrier[i]);

              return (
                <>
                  {metrics.includes("acc") && (
                    <td className="border-l-[1px] border-gray-500">
                      {totalAcc[i] >= maxTotalAcc ? <strong>{dispAcc}</strong> : dispAcc}
                    </td>
                  )}
                  {metrics.includes("brier") && (
                    <td>
                      {totalBrier[i] <= minTotalBrier ? <strong>{dispBrier}</strong> : dispBrier}
                    </td>
                  )}
                </>
              );
            })}
          </tr>
          <tr className="bg-blue-100">
            <td colSpan={2}>
              <strong>2016 - 2022</strong>
            </td>
            {methods.map((method, i) => {
              const dispAcc = formatAcc(recentAcc[i]);
              const dispBrier = formatBrier(recentBrier[i]);
              return (
                <>
                  {metrics.includes("acc") && (
                    <td className="border-l-[1px] border-gray-500">
                      {recentAcc[i] >= maxRecentAcc ? <strong>{dispAcc}</strong> : dispAcc}
                    </td>
                  )}
                  {metrics.includes("brier") && (
                    <td>
                      {recentBrier[i] <= minRecentBrier ? <strong>{dispBrier}</strong> : dispBrier}
                    </td>
                  )}
                </>
              );
            })}
          </tr>
        </tbody>
      </table>
    </div>
  );
};

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
        <SeasonTable />
      </div>
    </div>
  );
};

export default Page;
