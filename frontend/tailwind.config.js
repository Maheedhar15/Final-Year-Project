/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme');
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'background-1': 'var(./src/assets/b1.jpg)',
      },
      colors: {
        'Dark-black': '#282828',
        'white-blur': 'rgba(243, 244, 246, 0.6)',
      },
      fontFamily: {
        inter: ['Inter var', ...defaultTheme.fontFamily.sans],
        poppins: ['Poppins', ...defaultTheme.fontFamily.sans],
      },
      screens: {
        xs: '250px',
      },
    },
  },

  plugins: [],
};
