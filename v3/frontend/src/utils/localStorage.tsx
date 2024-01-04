import { log } from "./utils";

function setWithExpiry(key: string, value: any, ttl: number) {
  const now = new Date();

  // `item` is an object which contains the original value
  // as well as the time when it's supposed to expire
  const item = {
    value,
    expiry: now.getTime() + 1000 * ttl,
  };

  try {
    localStorage.setItem(key, JSON.stringify(item));
  } catch (e1: any) {
    // Clear localStorage if it's full except the 'key' item
    if (e1.name === "QuotaExceededError") {
      const fullTeamList = localStorage.getItem("full_team_list");
      localStorage.clear();

      // Re-add "full_team_list" item, but do not re-catch errors
      try {
        localStorage.setItem(
          "full_team_list",
          JSON.stringify({ value: fullTeamList, expiry: 60 * 60 * 24 * 7 }),
        ); // 1 week expiry
      } catch (e2: any) {
        log("Error setting localStorage", e2);
      }
    } else {
      log("Error setting localStorage", e1);
    }
  }
}

function getWithExpiry(key: string) {
  const itemStr = localStorage.getItem(key);
  // if the item doesn't exist, return null
  if (!itemStr) {
    return null;
  }
  const item = JSON.parse(itemStr);
  const now = new Date();
  // compare the expiry time of the item with the current time
  if (!item.expiry || now.getTime() > item.expiry) {
    // If the item is expired, delete the item from storage
    // and return null
    localStorage.removeItem(key);
    return null;
  }
  return item.value;
}

export { setWithExpiry, getWithExpiry };
