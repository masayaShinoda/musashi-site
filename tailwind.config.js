/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["*.html"],
  theme: {
    extend: {
      colors: {
        'brand': '#C2211A'
      },
    },
    fontFamily: {
      'sans': ['Montserrat', 'ui-sans-serif', 'system-ui'],
    },
    screens: {
      'content': '1192px'
    }
  },
  plugins: [],
}

