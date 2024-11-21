const colors = require('tailwindcss/colors');

module.exports = {
  content: [
    '../templates/**/*.html',
    '../../templates/**/*.html',
    '../../**/templates/**/*.html'
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#f9aa42',
          DEFAULT: '#f9ad48',
          dark: '#bd6e06',
          100: '#fde7ca',
          200: '#fcd7a7',
          300: '#fbc884',
          400: '#fab860',
          500: '#f9a83d',
          600: '#f7981a',
          700: '#e58608',
          800: '#c27106',
          900: '#9f5d05'
        },
        secondary: {
          light: '#fef3c7',
          DEFAULT: '#facc15',
          dark: '#854d0e'
        },
        neutral: colors.gray,
        danger: '#ef4444',
        success: '#22c55e',
        warning: '#f59e0b'
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/line-clamp'),
    require('@tailwindcss/aspect-ratio')
  ]
};
