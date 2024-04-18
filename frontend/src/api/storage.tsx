import { del, get, set } from "idb-keyval";
import pako from "pako";

import { BACKEND_URL } from "../constants";
import { log, round } from "../utils";

export const version = "v3.2";

async function setWithExpiry(key: string, value: any, ttl: number) {
  const now = new Date();

  try {
    await set(`${key}_expiry`, now.getTime() + 1000 * ttl);
    await set(key, value);
  } catch (e: any) {
    log("Error setting", e);
  }
}

async function getWithExpiry(key: string) {
  const expiry = await get(`${key}_expiry`);
  if (!expiry) {
    return null;
  }
  const now = new Date();
  if (now.getTime() > expiry) {
    await del(`${key}_expiry`);
    await del(key);
    return null;
  }
  return get(key);
}

// function decompress(buffer: any) {
//   const strData = pako.inflate(buffer, { to: "string" });
//   const data = JSON.parse(strData);
//   return data;
// }

async function query(storageKey: string, apiPath: string, minLength: number, expiry: number) {
  const cacheRawData = await getWithExpiry(storageKey);
  // const cacheData = cacheRawData ? decompress(cacheRawData) : null;
  const cacheData = cacheRawData;
  if (cacheData && (minLength === 0 || cacheData?.length > minLength)) {
    log(`Used Local Storage: ${storageKey}`);
    return cacheData;
  }

  const start = performance.now();
  const res = await fetch(`${BACKEND_URL}${apiPath}`, { next: { revalidate: 0 } });
  log(`${apiPath} took ${round(performance.now() - start, 0)}ms`);

  if (!res.ok) {
    return undefined;
  }

  // const buffer = await res.arrayBuffer();
  const buffer = await res.json();
  setWithExpiry(storageKey, buffer, expiry);
  return buffer;
  // return decompress(buffer);
}

export default query;
