module.exports = {
  content: [
    "./templates/**/*.{html,js}",
    "./components/**/*.{html,js}",
    "./static/js/**/*.js",
    "./*.html"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif']
      }
    }
  },
  safelist: [
    'bg-gray-50',
    'bg-white',
    'text-gray-900',
    'text-gray-500',
    'border-indigo-500',
    'text-indigo-600',
    'bg-indigo-600',
    'hover:bg-indigo-700'
  ]
}
