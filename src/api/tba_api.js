import axios from "axios";

const pre_url = "https://cors-anywhere.herokuapp.com/"; //for bypassing CORS
const url = "https://www.thebluealliance.com/api/v3/";
const access_token =
  "XeUIxlvO4CPc44NlLE3ncevDg7bAhp6CRy6zC9M2aQb2zGfys0M30eKwavFJSEJr";

export const fetchRankings = async (key) => {
  try {
    let data = await axios.get(`${pre_url}${url}/event/${key}/rankings`, {
      headers: { "X-TBA-Auth-Key": `${access_token}` },
    });
    data = data.data["rankings"];
    let rankings = {};
    for (var i = 0; i < data.length; i++) {
      rankings[parseInt(data[i]["team_key"].substring(3))] = i + 1;
    }
    return rankings;
  } catch (error) {
    return error;
  }
};
