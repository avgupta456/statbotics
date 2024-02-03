"use client";

import React, { useState } from "react";

import Link from "next/link";

import { Select } from "../../components/select";
import { YEAR_OPTIONS } from "../../utils/constants";
import { classnames } from "../../utils/utils";
import { champsData, seasonData } from "./data";

export default function SeasonTable() {
  const orderedMethods = ["wins", "opr", "elo", "combined", "tba", "sykes", "epa"];
  const orderedMetrics = ["acc", "brier"];

  const [methods, setMethods] = useState(["wins", "opr", "sykes", "epa"]);
  const [metrics, setMetrics] = useState(["acc"]);
  const [champs, setChamps] = useState(false);
  const [startYear, setStartYear] = useState(2016);
  const [endYear, setEndYear] = useState(2022);

  const methodToName: { [key: string]: string } = {
    wins: "Wins Baseline",
    opr: "OPR",
    elo: "Elo",
    combined: "OPR + Elo",
    tba: "TBA Insights",
    sykes: "Caleb Sykes Elo",
    epa: "EPA",
  };

  const metricsToName: { [key: string]: string } = {
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

  const formatAcc = (acc: number) => {
    let formattedAcc = "-";
    if (acc) {
      formattedAcc = `${(acc * 100).toFixed(2)}%`;
    }
    return formattedAcc;
  };

  const formatBrier = (brier: number) => {
    let formattedBrier = "-";
    if (brier) {
      formattedBrier = brier.toFixed(4);
    }
    return formattedBrier;
  };

  return (
    <div className="scrollbar-hide overflow-x-scroll">
      <h3 className="mb-8 w-full text-center">
        Comparison of Historical Prediction Performance (2002 - Present)
      </h3>
      <div className="not-prose mb-4">
        <table className="mx-auto table-fixed text-center text-sm">
          <thead>
            <tr key="header_1">
              <th colSpan={2}>
                <div className="w-32 py-1">Year</div>
              </th>
              {methods.map((method) => (
                <th
                  key={method}
                  colSpan={metrics.length}
                  className="w-40 border-l-[1px] border-gray-500 py-1"
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
                    <th className="w-20 border-l-[1px] border-gray-500 py-1">Acc</th>
                  )}
                  {metrics.includes("brier") && (
                    <th
                      className={classnames(
                        "w-20 py-1",
                        metrics.includes("acc") ? "" : "border-l-[1px] border-gray-500",
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
                  ...currMethods.map((currMethod) => currMethod?.brier || 1),
                );

                return (
                  <tr key={season.year} className="border-b-[1px] border-gray-200">
                    <td className="w-16 py-1">{season.year}</td>
                    <td className="w-16 py-1">{season.n}</td>
                    {currMethods.map((currMethod) => {
                      const dispAcc = formatAcc(currMethod?.acc);
                      const dispBrier = formatBrier(currMethod?.brier);

                      return (
                        <>
                          {metrics.includes("acc") && (
                            <td
                              className={classnames(
                                "border-l-[1px] border-gray-500",
                                metrics.length === 2 ? "w-20 py-1" : "w-40 py-1",
                              )}
                            >
                              {currMethod?.acc >= maxAcc ? <strong>{dispAcc}</strong> : dispAcc}
                            </td>
                          )}
                          {metrics.includes("brier") && (
                            <td
                              className={classnames(
                                metrics.length === 2 ? "w-20 py-1" : "w-40 py-1",
                                metrics.includes("acc") ? "" : "border-l-[1px] border-gray-500",
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
            <tr key="total" className="border-t-4 border-double border-gray-500 bg-blue-100">
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
                            metrics.length === 2 ? "w-20 py-1" : "w-40 py-1",
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
      <div className="flex w-full flex-wrap text-xs lg:justify-center">
        <div className="flex flex-wrap px-4 py-2 hover:bg-gray-100">
          <div className="font-bold">Include methods: </div>
          {Object.keys(methodToName).map((method) => (
            <div
              key={method}
              className="ml-2 flex cursor-pointer items-center rounded px-1 hover:bg-blue-100"
              onClick={() => {
                if (methods.includes(method)) {
                  setMethods(methods.filter((currMethod) => currMethod !== method));
                } else {
                  const newMethods = [...methods, method];
                  setMethods(
                    orderedMethods.filter((currMethod) => newMethods.includes(currMethod)),
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
        <div className="flex items-center px-4 py-2 hover:bg-gray-100">
          <div className="font-bold">Include metrics: </div>
          {["acc", "brier"].map((metric) => (
            <div
              key={metric}
              className="ml-2 flex cursor-pointer items-center rounded px-1 hover:bg-blue-100"
              onClick={() => {
                if (metrics.includes(metric)) {
                  setMetrics(metrics.filter((currMetric) => currMetric !== metric));
                } else {
                  const newMetrics = [...metrics, metric];
                  setMetrics(
                    orderedMetrics.filter((currMetric) => newMetrics.includes(currMetric)),
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
        <div className="flex items-center px-4 py-2 hover:bg-gray-100">
          <div className="font-bold">Show: </div>
          <div
            className="ml-2 flex cursor-pointer items-center rounded px-1 hover:bg-blue-100"
            onClick={() => setChamps(true)}
          >
            <input type="checkbox" className="mr-1" checked={champs} onChange={() => {}} />
            <div className="cursor-pointer">Only Champs</div>
          </div>
          <div
            className="ml-2 flex cursor-pointer items-center rounded px-1 hover:bg-blue-100"
            onClick={() => setChamps(false)}
          >
            <input type="checkbox" className="mr-1" checked={!champs} onChange={() => {}} />
            <div className="cursor-pointer">Entire Season</div>
          </div>
        </div>
        <div className="flex items-center px-4 py-2 hover:bg-gray-100">
          <div className="font-bold">Start Year: </div>
          <Select
            className="ml-1 w-24"
            data={YEAR_OPTIONS}
            onChange={(v) => setStartYear((v ?? 2002) as number)}
            value={startYear.toString()}
          />
        </div>
        <div className="flex items-center px-4 py-2 hover:bg-gray-100">
          <div className="font-bold">End Year: </div>
          <Select
            className="ml-1 w-24"
            data={YEAR_OPTIONS}
            onChange={(v) => setEndYear((v ?? 2002) as number)}
            value={endYear.toString()}
          />
        </div>
      </div>
      <div className="mb-4 w-full text-center text-sm">
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
}
