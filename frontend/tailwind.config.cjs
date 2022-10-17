const config = {
  content: ['./src/**/*.{html,js,svelte,ts}', './node_modules/stwui/**/*.{svelte,js,ts,html}'],
  plugins: [require('@tailwindcss/forms')],
  darkMode: 'class',
};

module.exports = config;
