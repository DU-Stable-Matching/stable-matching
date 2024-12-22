/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'dark-green': '#12664f',
        'myrtle-green': '#307473',
        'cool-gray': '#7a82ab',
        'periwinkle': '#c6d4ff',
        'robin-egg-blue': '#2dc3bd',
      }
    },
  },
  plugins: [],
}