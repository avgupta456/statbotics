import axios from "axios";

import { url } from "./index";

/*TEAM EVENT API CALLS*/

export const fetchTeamEvents = async (key) => {
  try {
    const events = await axios.get(`${url}/team_events/event/${key}/by/time`);
    return events.data;
  } catch (error) {
    return error;
  }
};
