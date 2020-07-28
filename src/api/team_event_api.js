import axios from "axios";

import { url } from "./index";

/*TEAM EVENT API CALLS*/

export const fetchTeamEvents = async (key, method) => {
  try {
    const events = await axios.get(
      `${url}/team_events/event/${key}/by/${method}`
    );
    return events.data;
  } catch (error) {
    return error;
  }
};
