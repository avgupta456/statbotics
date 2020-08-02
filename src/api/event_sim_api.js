import axios from "axios";

import { url } from "./index";

/*TEAM EVENT API CALLS*/

export const fetchSimFull = async (key, retries) => {
  try {
    const sim = await axios.get(`${url}/event_sim/event/${key}/full`);
    return sim.data;
  } catch (error) {
    if (retries > 1) {
      return [];
    } else {
      return fetchSimFull(key, retries + 1);
    }
  }
};
