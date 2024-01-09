import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        inputBlue: "#2684FF",
        gradientBlue: "#0D37F1",
        gradientRed: "#F50608",
      },
      fontSize: {
        xxs: "0.625rem",
        xxxs: "0.5rem",
      },
    },
  },
  // eslint-disable-next-line global-require
  plugins: [require("@tailwindcss/typography")],
};
export default config;