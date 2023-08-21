export const PROD = process.env.PROD === "True";

// undici bug requires 127.0.0.1 instead of localhost
export const BACKEND_URL = PROD
  ? "https://api.statbotics.io/v3/site"
  : "http://127.0.0.1:8000/v3/site";
// export const BACKEND_URL = "https://api.statbotics.io/v3/site";

export const TBA_API_KEY = "XeUIxlvO4CPc44NlLE3ncevDg7bAhp6CRy6zC9M2aQb2zGfys0M30eKwavFJSEJr";

export const CURR_YEAR = 2023;
export const CURR_WEEK = 8;

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

export const eventNameMap = {
  "FIRST in Michigan State Championship presented by DTE Foundation": "FiM Champs - Overall",
  "FIRST in Michigan State Championship presented by DTE Foundation - DTE ENERGY FOUNDATION Division":
    "FiM Champs - DTE Energy Foundation Division",
  "FIRST in Michigan State Championship presented by DTE Foundation - FORD Division":
    "FiM Champs - Ford Division",
  "FIRST in Michigan State Championship presented by DTE Foundation - APTIV Division":
    "FiM Champs - Aptiv Division",
  "FIRST in Michigan State Championship presented by DTE Foundation - CONSUMERS ENERGY Division":
    "FiM Champs - Consumers Energy Division",
  "New England FIRST District Championship": "NE Champs - Overall",
  "New England FIRST District Championship - WILSON Division": "NE Champs - Wilson Division",
  "New England FIRST District Championship - MEIR Division": "NE Champs - Meir Division",
  "FIRST In Texas District Championship presented by Phillips 66": "FIT Champs - Overall",
  "FIRST In Texas District Championship presented by Phillips 66 - APOLLO Division":
    "FIT Champs - Apollo Division",
  "FIRST In Texas District Championship presented by Phillips 66 - MERCURY Division":
    "FIT Champs - Mercury Division",
  "FIRST Ontario Provincial Championship": "Ontario Champs - Overall",
  "FIRST Ontario Provincial Championship - SCIENCE Division": "Ontario Champs - Science Division",
  "FIRST Ontario Provincial Championship - TECHNOLOGY Division":
    "Ontario Champs - Technology Division",
};

export const divisionToMainEvent = {
  "2023micmp": "2023micmp",
  "2023micmp1": "2023micmp",
  "2023micmp2": "2023micmp",
  "2023micmp3": "2023micmp",
  "2023micmp4": "2023micmp",
  "2023necmp": "2023necmp",
  "2023necmp1": "2023necmp",
  "2023necmp2": "2023necmp",
  "2023txcmp": "2023txcmp",
  "2023txcmp1": "2023txcmp",
  "2023txcmp2": "2023txcmp",
  "2023oncmp": "2023oncmp",
  "2023oncmp1": "2023oncmp",
  "2023oncmp2": "2023oncmp",
  "2023cmptx": "2023cmptx",
  "2023arc": "2023cmptx",
  "2023cur": "2023cmptx",
  "2023dal": "2023cmptx",
  "2023gal": "2023cmptx",
  "2023hop": "2023cmptx",
  "2023joh": "2023cmptx",
  "2023mil": "2023cmptx",
  "2023new": "2023cmptx",
};

export const mainEventToDivisions = {
  "2023micmp": [
    { name: "Overall", key: "2023micmp" },
    { name: "DTE Energy Foundation", key: "2023micmp1" },
    { name: "Ford", key: "2023micmp2" },
    { name: "Aptiv", key: "2023micmp3" },
    { name: "Consumers Energy", key: "2023micmp4" },
  ],
  "2023necmp": [
    { name: "Overall", key: "2023necmp" },
    { name: "Meir", key: "2023necmp1" },
    { name: "Wilson", key: "2023necmp2" },
  ],
  "2023txcmp": [
    { name: "Overall", key: "2023txcmp" },
    { name: "Apollo", key: "2023txcmp1" },
    { name: "Mercury", key: "2023txcmp2" },
  ],
  "2023oncmp": [
    { name: "Overall", key: "2023oncmp" },
    { name: "Technology", key: "2023oncmp1" },
    { name: "Science", key: "2023oncmp2" },
  ],
  "2023cmptx": [
    { name: "Overall", key: "2023cmptx" },
    { name: "Archimedes", key: "2023arc" },
    { name: "Curie", key: "2023cur" },
    { name: "Daly", key: "2023dal" },
    { name: "Galileo", key: "2023gal" },
    { name: "Hopper", key: "2023hop" },
    { name: "Johnson", key: "2023joh" },
    { name: "Milstein", key: "2023mil" },
    { name: "Newton", key: "2023new" },
  ],
};
