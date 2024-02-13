/*
INFRASTRUCTURE
*/

export const PROD = process.env.NEXT_PUBLIC_PROD === "True";

export const BACKEND_URL = PROD
  ? "https://api.statbotics.io/v3/site"
  : "http://localhost:8000/v3/site";

/*
SEASON CONFIG
*/

export const START_YEAR = 2002;
export const CURR_YEAR = 2024;
export const CURR_WEEK = 1;

export const YEAR_OPTIONS = Array.from({ length: CURR_YEAR - START_YEAR + 1 }, (_, i) =>
  (CURR_YEAR - i).toString(),
);

/*
COLORS
*/

export const CORRECT_COLOR = "#86CFA3";
export const INCORRECT_COLOR = "#F77F84";

// TODO: Update to visx colors
export const CAT_10_COLORS = [
  "#1f77b4",
  "#ff7f0e",
  "#2ca02c",
  "#d62728",
  "#9467bd",
  "#8c564b",
  "#e377c2",
  "#7f7f7f",
  "#bcbd22",
  "#17becf",
];

/*
HISTORICAL MAPPINGS
*/

export const RP_MAPPINGS = {
  2016: ["Breach RP", "Capture RP"],
  2017: ["Rotors RP", "Pressure RP"],
  2018: ["Auto RP", "Climb RP"],
  2019: ["Rocket RP", "HAB RP"],
  2020: ["Generator RP", "Hang RP"],
  2022: ["Cargo RP", "Hanger RP"],
  2023: ["Links RP", "Activation RP"],
  2024: ["RP 1", "RP 2"],
};
