/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,htm}", "./static/scripts/**/*.js"],
  theme: {
    extend: {},
  },
  plugins: [require('@tailwindcss/forms')]
}

