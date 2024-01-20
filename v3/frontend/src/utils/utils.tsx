import { PROD } from "./constants";

export const classnames = (...args: string[]) => args.join(" ");

export const round = (num: number, digits: number = 1) => {
  const factor = 10 ** digits;
  return Math.round(num * factor) / factor;
};

export const roundSigFigs = (num: number, sigFigs: number = 2, maxRound: number = 10) => {
  if (num === 0) return 0;
  const absNum = Math.abs(num);
  const digits = Math.floor(Math.log10(absNum)) + 1;
  // never round to maxRound digits or more (0.xx)
  const factor = 10 ** Math.min(maxRound, sigFigs - digits);
  return Math.round(num * factor) / factor;
};

export const truncate = (str: string, length: number) => {
  if (str.length > length) {
    return `${str.substring(0, length - 3)}...`;
  }
  return str;
};

export const capitalize = (str: string) => str.charAt(0).toUpperCase() + str.slice(1);

export const log = (...args: any[]) => {
  if (!PROD) {
    // eslint-disable-next-line no-console
    console.log(...args);
  }
};

export const loaderProp = ({ src }: any) => src;
