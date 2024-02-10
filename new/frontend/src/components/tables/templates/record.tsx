import { round } from "../../../utils/utils";

export const getWLT = (params: any) => {
  const record = params?.data?.record?.season;
  if (!record) {
    return { wins: 0, losses: 0, ties: 0 };
  }
  const wins = record?.wins || 0;
  const losses = record?.losses || 0;
  const ties = record?.ties || 0;
  return { wins, losses, ties };
};

export const recordGetter = (params: any) => {
  const { wins, losses, ties } = getWLT(params);
  return `${wins}-${losses}-${ties}`;
};

export const winRateGetter = (params: any) => {
  const { wins, losses, ties } = getWLT(params);
  const total = wins + losses + ties;
  if (total === 0) return 0;
  return (wins + ties / 2) / total;
};

// COLUMN DEFS

export const recordDef = {
  colId: "record",
  headerName: "Record",
  minWidth: 100,
  valueGetter: recordGetter,
  // sort record by win rate column
  // eslint-disable-next-line no-unused-vars, @typescript-eslint/no-unused-vars
  comparator: (_a: any, _b: any, nodeA: any, nodeB: any, _c: any) => {
    const winRateA = winRateGetter(nodeA);
    const winRateB = winRateGetter(nodeB);
    return winRateA - winRateB;
  },
};

export const winRateDef = {
  colId: "win_rate",
  headerName: "Win Rate",
  // filter: "agNumberColumnFilter",
  valueGetter: winRateGetter,
  valueFormatter: (params: any) => `${round((params?.value ?? 0) * 100, 1)}%`,
};
