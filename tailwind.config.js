module.exports = {
  content: [
    "./templates/**/*.{html,js}",
    "./components/**/*.{html,js}",
    "./static/js/**/*.js",
    "./*.html",
    "./about/**/*.html",
    "./admin/**/*.html",
    "./donate/**/*.html",
    "./store/**/*.html"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif']
      },
      colors: {
        gray: {
          50: 'rgb(249, 250, 251)',
          100: 'rgb(243, 244, 246)',
          200: 'rgb(229, 231, 235)',
          300: 'rgb(209, 213, 219)',
          400: 'rgb(156, 163, 175)',
          500: 'rgb(107, 114, 128)',
          600: 'rgb(75, 85, 99)',
          700: 'rgb(55, 65, 81)',
          800: 'rgb(31, 41, 55)',
          900: 'rgb(17, 24, 39)'
        },
        indigo: {
          50: 'rgb(238, 242, 255)',
          100: 'rgb(224, 231, 255)',
          200: 'rgb(199, 210, 254)',
          300: 'rgb(165, 180, 252)',
          400: 'rgb(129, 140, 248)',
          500: 'rgb(99, 102, 241)',
          600: 'rgb(79, 70, 229)',
          700: 'rgb(67, 56, 202)',
          800: 'rgb(55, 48, 163)',
          900: 'rgb(49, 46, 129)'
        }
      }
    }
  },
  safelist: [
    // Navigation
    'border-transparent',
    'border-indigo-500',
    'text-gray-500',
    'text-gray-700',
    'text-gray-900',
    'hover:text-gray-700',
    'hover:border-gray-300',
    'border-b-2',
    // Backgrounds
    'bg-gray-50',
    'bg-white',
    'bg-indigo-50',
    'bg-indigo-100',
    'bg-indigo-600',
    'hover:bg-indigo-700',
    // Text colors
    'text-indigo-600',
    // Interactive elements
    'hover:bg-gray-100',
    'hover:text-gray-900',
    // Spacing and layout
    'space-x-4',
    'space-x-8',
    'space-y-8',
    // Flexbox
    'flex',
    'flex-col',
    'flex-shrink-0',
    'items-center',
    'justify-center',
    'justify-between',
    // Sizing
    'h-16',
    'w-full',
    'max-w-7xl',
    'min-h-screen',
    // Padding and margin
    'px-4',
    'py-12',
    'pt-1',
    'mt-12',
    'mb-8',
    'ml-3',
    'ml-6',
    // Typography
    'text-sm',
    'text-2xl',
    'font-medium',
    'font-bold',
    // Transitions
    'transition-all',
    'duration-200',
    // States
    'active',
    // Responsive classes
    'sm:px-6',
    'sm:ml-6',
    'sm:flex',
    'sm:space-x-8',
    'lg:px-8',
    // Dynamic classes (used in templates)
    {
      pattern: /^(bg|text|border)-(gray|indigo)-\d00$/,
      variants: ['hover', 'focus', 'active']
    }
  ],
  plugins: []
}
