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
      width: {
        "1/9": "11.11111111111111%",
        "2/9": "22.22222222222222%",
        "1/14": "7.142857142857143%",
        "1/7": "14.285714285714286%",
        "3/14": "21.428571428571427%",
        "2/7": "28.57142857142857%",
        "5/14": "35.714285714285715%",
        "3/7": "42.857142857142854%",
      },
      fontSize: {
        xxs: "0.625rem",
        xxxs: "0.5rem",
      },
    },
    screens: {
      xs: "480px",
      sm: "640px",
      md: "768px",
      lg: "1024px",
      xl: "1200px",
    },
  },
  // eslint-disable-next-line global-require
  plugins: [require("@tailwindcss/typography")],
};
export default config;
