import { Tooltip } from "@mantine/core";

import { useData } from "../../../contexts/dataContext";
import { usePreferences } from "../../../contexts/preferencesContext";
import { APITeamYear, EPAPercentiles } from "../../../types/api";
import { classnames, roundSigFigs } from "../../../utils/utils";

function getColorSubTemplate(percentiles: EPAPercentiles, colorOptions: string[], value: number) {
  if (percentiles?.p99 && value > percentiles?.p99) {
    return colorOptions?.[0];
  }
  if (percentiles?.p90 && value > percentiles?.p90) {
    return colorOptions?.[1];
  }
  if (percentiles?.p75 && value > percentiles?.p75) {
    return colorOptions?.[2];
  }
  if (percentiles?.p25 && value < percentiles?.p25) {
    return colorOptions?.[4];
  }
  return colorOptions?.[3];
}

function getColorTemplate(
  colorScheme: string,
  percentiles: EPAPercentiles,
  colorOptions: string[],
  value: number,
) {
  if (colorScheme === "light") {
    return getColorSubTemplate(percentiles, colorOptions, value);
  }
  return getColorSubTemplate(percentiles, colorOptions.slice(5), value);
}

// eslint-disable-next-line import/prefer-default-export
export function EPACellRenderer({
  data,
  epaKey,
  value,
  context,
}: {
  data: APITeamYear;
  epaKey: string;
  value: number;
  context?: any;
}) {
  if (value === undefined || value === null) {
    return <div className="flex h-full w-full items-center justify-center">-</div>;
  }

  const { colorScheme, EPACellFormat } = usePreferences();
  const { yearDataDict } = useData();
  const { year } = context;

  const mean = value;
  const sd = data?.epa?.breakdown?.[epaKey]?.sd || 0;
  const [rawLower, rawUpper] = data?.epa?.conf ?? [0, 0];
  const lower = mean + rawLower * sd;
  const upper = mean + rawUpper * sd;
  const adjSd = (upper - lower) / 2;

  const percentiles: EPAPercentiles = yearDataDict[year]?.percentiles?.[epaKey] ?? {};

  if (EPACellFormat === "Plaintext") {
    return <div>{roundSigFigs(value, 2)}</div>;
  }

  const color = getColorTemplate(
    colorScheme,
    percentiles,
    [
      "bg-blue-200 text-blue-800", // light p99
      "bg-green-200 text-green-800", // light p90
      "bg-green-100 text-green-800", // light p75
      "", // light middle
      "bg-red-200 text-red-700", // light p25
      "bg-blue-500 text-white", // dark p99
      "bg-green-600 text-white", // dark p90
      "bg-green-300 text-green-800", // dark p75
      "", // dark middle
      "bg-red-400 text-white", // dark p25
    ],
    value,
  );

  if (EPACellFormat === "Highlight (mean only)") {
    return (
      <div className="flex h-full w-full items-center justify-center">
        <div className={classnames(color, "flex h-7 w-12 items-center justify-center rounded-lg")}>
          {roundSigFigs(value, 3, 1)}
        </div>
      </div>
    );
  }

  if (EPACellFormat === "Highlight (with interval)") {
    return (
      <div className="flex h-full w-full items-center justify-center">
        <Tooltip
          label={`${roundSigFigs(lower, 2, 2)} - ${roundSigFigs(upper, 2, 2)}`}
          classNames={{
            tooltip: "text-xs",
          }}
        >
          <div
            className={classnames(color, "flex h-7 w-12 items-center justify-center rounded-lg")}
          >
            {roundSigFigs(value, 2, 1)}
            <p className="ml-1 text-xs">±{roundSigFigs(adjSd, 1, 0)}</p>
          </div>
        </Tooltip>
      </div>
    );
  }

  const centerColor = color === "" ? "border border-zinc-500" : color;
  const errorColor = color === "" ? "bg-zinc-500" : color;

  const shifted = EPACellFormat === "Error Bars (shifted)";

  let valueRange = 2 * (context?.[epaKey]?.maxError ?? 10);
  let midValue = 0;
  if (shifted) {
    const minValue = context?.[epaKey]?.minValue ?? 0;
    const maxValue = context?.[epaKey]?.maxValue ?? 100;
    valueRange = maxValue - minValue;
    midValue = minValue + valueRange / 2;
  }

  // multiply by 2 since the element is centered in the remaining space
  const leftMargin = shifted ? (100 * 2 * (value - midValue)) / valueRange : 0;
  // multiply by 100 / (100 - leftMargin) since full width reduced from 100% to (100 - leftMargin)
  const leftBarWidth = (100 * ((100 / (100 - leftMargin)) * (value - lower))) / valueRange;
  const rightBarWidth = (100 * ((100 / (100 - leftMargin)) * (upper - value))) / valueRange;

  return (
    <div
      className="relative flex h-full w-auto min-w-[24px] items-center justify-center"
      style={{ marginLeft: `${leftMargin}%` }}
    >
      <div
        className={classnames(
          "absolute right-1/2 top-1/2 mr-[12px] h-[1.5px] transform",
          errorColor,
        )}
        style={{ width: `calc(${leftBarWidth}% - 12px)` }}
      />
      <Tooltip
        label={`${roundSigFigs(lower, 2, 2)} - ${roundSigFigs(upper, 2, 2)}`}
        classNames={{ tooltip: "text-xs" }}
      >
        <div
          className={classnames(
            "flex h-6 w-6 items-center justify-center rounded-full",
            centerColor,
          )}
        >
          {roundSigFigs(value, 2, 0)}
        </div>
      </Tooltip>
      <div
        className={classnames(
          "absolute left-1/2 top-1/2 ml-[12px] h-[1.5px] transform",
          errorColor,
        )}
        style={{ width: `calc(${rightBarWidth}% - 12px)` }}
      />
    </div>
  );
}

export const EPATotalRankDef = {
  field: "epa.ranks.total.rank",
  headerName: "EPA Rank",
  sortingOrder: ["desc", null],
};

export const UnitlessEPADef = {
  field: "epa.unitless",
  headerName: "Unitless EPA",
  sortingOrder: ["desc", null],
};

export const getEPADef = (epaKey: string, headerName: string) => ({
  field: `epa.breakdown.${epaKey}.mean`,
  headerName,
  minWidth: 120,
  cellRenderer: EPACellRenderer,
  cellRendererParams: { epaKey },
  resizable: true,
  sortingOrder: ["desc", null],
  // filterParams: {
  //   filterOptions: ["greaterThan", "lessThan", "inRange"],
  //   maxNumConditions: 1,
  // },
});
