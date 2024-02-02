import { APIEvent } from "../types/api";
import { EVENT_NAME_MAP } from "./events";

export const truncate = (str: string, length: number) => {
  if (str.length > length) {
    return `${str.substring(0, length - 3)}...`;
  }
  return str;
};

export const capitalize = (str: string) => str.charAt(0).toUpperCase() + str.slice(1);

export const formatEventName = (eventName: string, limit: number = -1) => {
  const name = EVENT_NAME_MAP[eventName] || eventName;
  return limit > 0 ? truncate(name, limit) : name;
};

export const formatOngoingEventStatus = (event: APIEvent) => {
  if (event.status !== "Ongoing") {
    return event.status;
  }
  if (event.qual_matches === 0) {
    return "Scheduled Unreleased";
  }
  if (event.current_match === 0) {
    return "Schedule Released";
  }
  if (event.current_match < event.qual_matches) {
    return `Qual ${event.current_match}`;
  }
  if (event.current_match === event.qual_matches) {
    return "Quals Over";
  }
  return "Elims Ongoing";
};
export const COMP_LEVEL_FULL_NAMES: { [key: string]: string } = {
  qm: "Qualifications",
  ef: "Eighth Finals",
  qf: "Quarterfinals",
  sf: "Semifinals",
  f: "Finals",
};

export const COMP_LEVEL_SHORT_NAMES: { [key: string]: string } = {
  qm: "Quals",
  ef: "Eighths",
  qf: "Quarters",
  sf: "Semis",
  f: "Finals",
};

export const formatMatch = (compLevel: string, matchNum: number, setNum: number) => {
  let displayMatch = `${COMP_LEVEL_SHORT_NAMES[compLevel]} ${matchNum}`;
  if (compLevel !== "qm") {
    displayMatch = `${COMP_LEVEL_SHORT_NAMES[compLevel]} ${setNum}-${matchNum}`;
  }

  return displayMatch;
};
