const colors = require('tailwindcss/colors');

module.exports = {
  content: [
    '../templates/**/*.html',
    '../../templates/**/*.html',
    '../../**/templates/**/*.html',
    '../../**/*.js',
    '../../**/*.py'
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '##f9aa42',
          DEFAULT: '##f9ad48',
          dark: '#bd6e06',
        },
        secondary: {
          light: '#fef3c7',
          DEFAULT: '#facc15',
          dark: '#854d0e',
        },
        neutral: colors.gray,
        danger: '#ef4444',
        success: '#22c55e',
        warning: '#f59e0b',
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
