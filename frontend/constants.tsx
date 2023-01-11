export const PROD = process.env.PROD === "True";

// undici bug requires 127.0.0.1 instead of localhost
export const BACKEND_URL = PROD ? "https://api.statbotics.io/api" : "http://127.0.0.1:8000/api";

console.log(PROD, BACKEND_URL);

export const CURR_YEAR = 2023;
export const CURR_WEEK = 1;

export const MAX_TEAM = 9311; // above is offseason

export const CORRECT_COLOR = "#86CFA3";
export const INCORRECT_COLOR = "#F77F84";

export const Category10Colors = [
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

export const RPMapping = {
  2016: ["Breach RP", "Capture RP"],
  2017: ["Rotors RP", "Pressure RP"],
  2018: ["Auto RP", "Climb RP"],
  2019: ["Rocket RP", "HAB RP"],
  2020: ["Generator RP", "Hang RP"],
  2022: ["Cargo RP", "Hanger RP"],
  2023: ["Links RP", "Activation RP"],
};
