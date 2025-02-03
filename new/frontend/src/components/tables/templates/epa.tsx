import { useData } from "../../../contexts/dataContext";
import { usePreferences } from "../../../contexts/preferencesContext";
import { EPAPercentiles } from "../../../types/api";
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
  epaKey,
  value,
  context,
}: {
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

  return (
    <div className="flex h-full w-full items-center justify-center">
      <div className={classnames(color, "flex h-7 w-12 items-center justify-center rounded-lg")}>
        {roundSigFigs(value, 3, 1)}
      </div>
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
  field: `epa.breakdown.${epaKey}`,
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
