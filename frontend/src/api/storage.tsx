import { del, get, set } from "idb-keyval";
import pako from "pako";

import { BACKEND_URL, BUCKET_URL } from "../constants";
import { log, round } from "../utils";

export const version = "v3";

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

export function decompress(buffer: any) {
  const strData = pako.inflate(buffer, { to: "string" });
  const data = JSON.parse(strData);
  return data;
}

async function query(
  storageKey: string,
  apiPath: string,
  checkBucket: boolean,
  minLength: number,
  expiry: number
) {
  const cacheData = await getWithExpiry(storageKey);
  if (cacheData && (minLength === 0 || cacheData?.length > minLength)) {
    log(`Used Local Storage: ${storageKey}`);
    return cacheData;
  }

  const start = performance.now();

  let buffer = null;
  try {
    if (!checkBucket) {
      throw new Error("Skip bucket check");
    }
    const fileName = apiPath.replace("?", ".").replace("&", ".");
    const res = await fetch(`${BUCKET_URL}${fileName}`, {
      next: { revalidate: 0 },
      headers: {
        "Cache-Control": "no-cache",
        "Content-Type": "application/octet-stream",
      },
    });
    log(`${fileName} (bucket) took ${round(performance.now() - start, 0)}ms`);
    if (res.ok) {
      buffer = decompress(await res.arrayBuffer());
    } else {
      throw new Error(`Failed to fetch from bucket: ${res.status}`);
    }
  } catch (e) {
    const res = await fetch(`${BACKEND_URL}${apiPath}`, { next: { revalidate: 0 } });
    log(`${apiPath} (backend) took ${round(performance.now() - start, 0)}ms`);
    if (res.ok) {
      buffer = await res.json();
    }
  }

  if (buffer) {
    await setWithExpiry(storageKey, buffer, expiry);
    return buffer;
  }
}

export default query;
