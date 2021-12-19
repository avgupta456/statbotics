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
      console.log(error);
      return fetchSimFull(key, retries + 1);
    }
  }
};

export const fetchSimIndex = async (key, index, retries) => {
  try {
    const sim = await axios.get(
      `${url}/event_sim/event/${key}/index/${index}/full`
    );
    return sim.data;
  } catch (error) {
    console.log(error);
    console.log(retries);
    if (retries > 1) {
      return [];
    } else {
      console.log(error);
      return fetchSimIndex(key, index, retries + 1);
    }
  }
};
