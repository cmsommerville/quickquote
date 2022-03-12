const defaultTheme = require("tailwindcss/defaultTheme");

/** @type {import("@types/tailwindcss/tailwind-config").TailwindConfig } */
module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter var"', ...defaultTheme.fontFamily.sans],
      },
      colors: {
        theme: {
          primary: "#6d28d9",
        },
      },
      backgroundImage: {
        "grad-violet-indigo":
          "linear-gradient(to right bottom, rgba(109, 40, 217, 0.8), rgba(55,48,163, 0.8))",
        "accident-sm":
          "linear-gradient(to right bottom, rgba(91,33,182, 0.8), rgba(91,33,182, 0.8)), url('/src/assets/img/accident-010.jpg')",
        "stethoscope-sm":
          "linear-gradient(to right bottom, rgba(91,33,182, 0.8), rgba(91,33,182, 0.8)), url('/src/assets/img/stethoscope-010.jpg')",
        "pulse-sm":
          "linear-gradient(to right bottom, rgba(91,33,182, 0.8), rgba(91,33,182, 0.8)), url('/src/assets/img/pulse-010.jpg')",
        "x-ray-sm":
          "linear-gradient(to right bottom, rgba(91,33,182, 0.8), rgba(91,33,182, 0.8)),url('/src/assets/img/x-ray-010.jpg')",
      },
      width: {
        "90%": "90%",
        "50vw": "50vw",
        "60vw": "60vw",
        "70vw": "70vw",
        "80vw": "80vw",
      },
      minWidth: {
        "1/2": "50%",
        "2/3": "67%",
        "3/4": "75%",
        "5/6": "83%",
      },
      minHeight: {
        "1/2": "50%",
        "2/3": "67%",
        "3/4": "75%",
        "5/6": "83%",
      },
      maxWidth: {
        "1/2": "50%",
        "2/3": "67%",
        "3/4": "75%",
        "5/6": "83%",
      },
      maxHeight: {
        "1/2": "50%",
        "2/3": "67%",
        "3/4": "75%",
        "5/6": "83%",
      },
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/line-clamp"),
    require("@tailwindcss/aspect-ratio"),
  ],
};
