/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["*.html"],
  theme: {
    extend: {
      colors: {
        'brand': '#C2211A'
      },
      screens: {
        'content': '1192px'
      }
    },
    fontFamily: {
      'sans': ['Montserrat', 'ui-sans-serif', 'system-ui'],
    },
  },
  plugins: [],
}

