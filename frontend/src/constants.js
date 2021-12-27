export const PROD = process.env.REACT_APP_PROD === "true";

export const BACKEND_URL = PROD
  ? "https://api.statbotics.io/v1"
  : "http://localhost:8000/v1";
