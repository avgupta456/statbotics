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
        "1/13": "7.692%",
        "2/13": "15.384%",
        "3/13": "23.076%",
      },
    },
  },
  plugins: [],
};
