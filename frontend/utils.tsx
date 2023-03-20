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
