function setWithExpiry(key, value, ttl) {
  const now = new Date();

  // `item` is an object which contains the original value
  // as well as the time when it's supposed to expire
  const item = {
    value: value,
    expiry: now.getTime() + 1000 * ttl,
  };

  try {
    localStorage.setItem(key, JSON.stringify(item));
  } catch (e) {
    // Clear localStorage if it's full except the 'key' item
    if (e.name === "QuotaExceededError") {
      const fullTeamList = localStorage.getItem("full_team_list");
      localStorage.clear();

      // Re-add "full_team_list" item, but do not re-catch errors
      try {
        localStorage.setItem(
          "full_team_list",
          JSON.stringify({ value: fullTeamList, expiry: 60 * 60 * 24 * 7 })
        ); // 1 week expiry
      } catch (e) {
        console.log("Error clearing localStorage");
      }
    } else {
      throw e;
    }
  }
}

function getWithExpiry(key) {
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
