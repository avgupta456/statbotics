/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontSize: {
        xxs: ".625rem",
      },
      colors: {
        inputBlue: "#2684FF",
        gradientBlue: "#0D37F1",
        gradientRed: "#F50608",
      },
      width: {
        "1/15": "6.666666666666667%",
        "2/15": "13.333333333333334%",
      },
    },
  },
  plugins: [require("daisyui"), require("@tailwindcss/typography")],
  daisyui: { themes: false },
};
