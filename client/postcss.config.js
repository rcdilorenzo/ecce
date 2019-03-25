const tailwindcss = require('tailwindcss');
const precss = require('precss');

module.exports = {
  plugins: [
    precss(),
    tailwindcss('./tailwind.config.js'),
    require('autoprefixer'),
  ]
};
