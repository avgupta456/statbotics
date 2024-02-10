import { PROD, TBA_API_KEY, eventNameMap } from "./constants";

export const classnames = (...args: string[]) => args.join(" ");

export const round = (num: number, digits: number = 1) => {
  const factor = 10 ** digits;
  return Math.round(num * factor) / factor;
};

export const truncate = (str: string, length: number) => {
  if (str.length > length) {
    return str.substring(0, length - 3) + "...";
  }
  return str;
};

export const capitalize = (str: string) => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};

export const log = (...args: any[]) => {
  if (!PROD) {
    console.log(...args);
  }
};

export const readTBA = async (url: string) => {
  const response = await fetch("https://www.thebluealliance.com/api/v3" + url, {
    headers: { "X-TBA-Auth-Key": TBA_API_KEY },
  });

  if (response.status === 200) {
    return response.json();
  }

  throw new Error("TBA Error: " + response.status);
};

export const getMediaUrl = async (team: number, year: number) => {
  if (team === 0) return null;
  const data = await readTBA(`/team/frc${team}/media/${year}`);
  const image = data.filter((item: any) => item?.preferred)?.[0];
  if (image?.type === "instagram-image") {
    // if (image?.view_url) {
    //   return `https://www.thebluealliance.com/${image?.direct_url}`;
    // }
    return null;
  } else if (image?.type === "imgur") {
    return image?.direct_url ?? null;
  } else {
    return null;
  }
};

export const getMediaUrls = async (teams: number[], year: number) => {
  const urls = [];
  for (const team of teams) {
    const url = await getMediaUrl(team, year);
    urls.push(url);
  }
  return urls;
};

export const formatEventName = (eventName: string, limit: number = -1) => {
  const name = eventNameMap[eventName] || eventName;
  return limit > 0 ? truncate(name, limit) : name;
};
const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_";

export const compress = (year: number, teams: number[], match: number) => {
  const yearBinary = (year - 2000).toString(2).padStart(6, "0");
  const matchBinary = match.toString(2).padStart(7, "0");
  const prefix = yearBinary + matchBinary;

  teams.sort((a, b) => a - b);
  const teamsBinary = teams.map((team) => parseInt(team.toString(2)));
  const lengths = teamsBinary.map((team) => team.toString().length);
  const lengthCounts = new Array(20).fill(0);
  for (const length of lengths) {
    lengthCounts[length] += 1;
  }

  const posLengthsBinary = lengthCounts.map((x) => (x > 0 ? "1" : "0")).join("");
  const lengthsBinary = lengthCounts
    .filter((x) => x > 0)
    .map((x) => x.toString(2).padStart(7, "0"))
    .join("");

  let binaryString = prefix + posLengthsBinary + lengthsBinary;
  for (const team of teamsBinary) {
    binaryString += team.toString();
  }

  binaryString += "0".repeat(6 - (binaryString.length % 6));

  let string = "";
  for (let i = 0; i < binaryString.length; i += 6) {
    string += chars[parseInt(binaryString.substring(i, i + 6), 2)];
  }

  return string;
};

export const decompress = (str: string) => {
  let binaryString = "";
  for (const char of str) {
    binaryString += chars.indexOf(char).toString(2).padStart(6, "0");
  }

  const prefix = binaryString.substring(0, 13);
  const year = parseInt(prefix.substring(0, 6), 2) + 2000;
  const match = parseInt(prefix.substring(7), 2);

  const posLengthsBinary = binaryString.substring(13, 33);
  const numPositive = posLengthsBinary.split("1").length - 1;
  let lengthsBinary = binaryString.substring(33, 33 + 7 * numPositive);
  let teamsBinary = binaryString.substring(33 + 7 * numPositive);

  const lengths = [];
  for (let i = 0; i < posLengthsBinary.length; i++) {
    if (posLengthsBinary[i] === "1") {
      lengths.push(parseInt(lengthsBinary.substring(0, 7), 2));
      lengthsBinary = lengthsBinary.substring(7);
    } else {
      lengths.push(0);
    }
  }

  const teams = [];
  for (let i = 0; i < lengths.length; i++) {
    for (let j = 0; j < lengths[i]; j++) {
      teams.push(parseInt(teamsBinary.substring(0, i), 2));
      teamsBinary = teamsBinary.substring(i);
    }
  }

  return { year, teams, match };
};

// console.log(decompress(compress(2023, [254, 1323, 1678], 10)));
