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
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
export default config;
