const defaultTheme = require("tailwindcss/defaultTheme");

/** @type {import("@types/tailwindcss/tailwind-config").TailwindConfig } */
module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter var"', ...defaultTheme.fontFamily.sans],
      },
    },
    backgroundImage: {
      "accident-sm":
        "linear-gradient(to right bottom, rgba(239,68,68, 0.8), rgba(239,68,68, 0.8)), url('/src/assets/img/accident-010.jpg')",
      "stethoscope-sm":
        "linear-gradient(to right bottom, rgba(239,68,68, 0.8), rgba(239,68,68, 0.8)), url('/src/assets/img/stethoscope-010.jpg')",
      "pulse-sm":
        "linear-gradient(to right bottom, rgba(239,68,68, 0.8), rgba(239,68,68, 0.8)), url('/src/assets/img/pulse-010.jpg')",
      "x-ray-sm":
        "linear-gradient(to right bottom, rgba(239,68,68, 0.8), rgba(239,68,68, 0.8)),url('/src/assets/img/x-ray-010.jpg')",
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/line-clamp"),
    require("@tailwindcss/aspect-ratio"),
  ],
};
