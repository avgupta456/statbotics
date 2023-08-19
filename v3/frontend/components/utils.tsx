import { round } from "../utils";

export const formatNumber = (num: number) => {
  if (num > 100000) {
    return round(num / 100000, 0).toString() + String.fromCharCode(65 + (num % 100000));
  }
  return num.toString();
};

export const compLevelFullNames = {
  qm: "Qualifications",
  ef: "Eighth Finals",
  qf: "Quarterfinals",
  sf: "Semifinals",
  f: "Finals",
};

export const compLevelShortNames = {
  qm: "Quals",
  ef: "Eighths",
  qf: "Quarters",
  sf: "Semis",
  f: "Finals",
};

export const formatMatch = (compLevel: string, matchNum: number, setNum: number) => {
  let displayMatch = `${compLevelShortNames[compLevel]} ${matchNum}`;
  if (compLevel !== "qm") {
    displayMatch = `${compLevelShortNames[compLevel]} ${setNum}-${matchNum}`;
  }

  return displayMatch;
};
