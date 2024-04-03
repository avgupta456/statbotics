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
export const CURR_WEEK = 6;

export const YEAR_OPTIONS = [
  "2024",
  "2023",
  "2022",
  // "2021", // TODO: implement 2021
  "2020",
  "2019",
  "2018",
  "2017",
  "2016",
  "2015",
  "2014",
  "2013",
  "2012",
  "2011",
  "2010",
  "2009",
  "2008",
  "2007",
  "2006",
  "2005",
  "2004",
  "2003",
  "2002",
];

export const BREAKDOWN_YEARS = [2023, 2024]; // TODO: implement 2016-2022

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

export const RP_KEYS: { [key: number]: string[] } = {
  2016: ["defenses_rp", "tower_rp"],
  2017: ["rotor_rp", "kpa_rp"],
  2018: ["auto_rp", "climb_rp"],
  2019: ["rocket_rp", "hab_rp"],
  2020: ["cells_rp", "climb_rp"],
  2022: ["cargo_rp", "hangar_rp"],
  2023: ["links_rp", "activation_rp"],
  2024: ["melody_rp", "harmony_rp"],
};

export const RP_NAMES: { [key: number]: string[] } = {
  2016: ["Breach RP", "Capture RP"],
  2017: ["Rotors RP", "Pressure RP"],
  2018: ["Auto RP", "Climb RP"],
  2019: ["Rocket RP", "HAB RP"],
  2020: ["Generator RP", "Hang RP"],
  2022: ["Cargo RP", "Hangar RP"],
  2023: ["Links RP", "Activation RP"],
  2024: ["Melody RP", "Ensemble RP"],
};
