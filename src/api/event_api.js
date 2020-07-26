import axios from "axios";

import { url } from "./index";

/*EVENT API CALLS*/

export const fetchEvents = async (year) => {
  try {
    const events = await axios.get(`${url}/events/year/${year}/by/time`);
    return events.data;
  } catch (error) {
    return error;
  }
};

export const fetchEvents_byWeek = async (year, week) => {
  try {
    const events = await axios.get(
      `${url}/events/year/${year}/week/${week}/by/time`
    );
    return events.data;
  } catch (error) {
    return error;
  }
};

export const fetchEvents_byCountry = async (year, country) => {
  try {
    const events = await axios.get(
      `${url}/events/year/${year}/country/${country}/by/time`
    );
    return events.data;
  } catch (error) {
    return error;
  }
};

export const fetchEvents_byCountryWeek = async (year, country, week) => {
  try {
    const events = await axios.get(
      `${url}/events/year/${year}/week/${week}/country/${country}/by/time`
    );
    return events.data;
  } catch (error) {
    return error;
  }
};

export const fetchEvents_byState = async (year, country, state) => {
  try {
    const events = await axios.get(
      `${url}/events/year/${year}/country/${country}/state/${state}/by/time`
    );
    return events.data;
  } catch (error) {
    return error;
  }
};

export const fetchEvents_byStateWeek = async (year, country, state, week) => {
  try {
    const events = await axios.get(
      `${url}/events/year/${year}/week/${week}/country/${country}/state/${state}/by/time`
    );
    return events.data;
  } catch (error) {
    return error;
  }
};

export const fetchEvents_byDistrict = async (year, district) => {
  try {
    const events = await axios.get(
      `${url}/events/year/${year}/district/${district}/by/time`
    );
    return events.data;
  } catch (error) {
    return error;
  }
};

export const fetchEvents_byDistrictWeek = async (year, district, week) => {
  try {
    const events = await axios.get(
      `${url}/events/year/${year}/week/${week}/district/${district}/by/time`
    );
    return events.data;
  } catch (error) {
    return error;
  }
};
