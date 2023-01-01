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
      },
      width: {
        "1/14": "7.142857142857143%",
        "1/7": "14.285714285714286%",
        "3/14": "21.428571428571427%",
      },
    },
  },
  plugins: [],
};
