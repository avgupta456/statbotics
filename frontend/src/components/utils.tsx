import { round } from "../utils";

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
