import { round } from "../utils";

export const formatNumber = (num: number) => {
  if (num > 100000) {
    return round(num / 100000, 0).toString() + String.fromCharCode(65 + (num % 100000));
  }
  return num.toString();
};
