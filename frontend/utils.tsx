import { PROD, TBA_API_KEY } from "./constants";

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
