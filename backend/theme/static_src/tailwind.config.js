module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
        // '!../../**/node_modules',
        // '../../**/*.js',
        // '../../**/*.py'
    ],

    safelist: [
        'translate-x-full',
        'translate-x-0',
        'transition',
        'transform',
        'duration-300',
        'ease-in-out',
        'hidden',
        'fixed',
        'inset-0',
        'inset-y-0',
        'right-0',
        'z-50',
        'bg-black/30',
        'bg-white',
        'shadow-xl',

        'bg-violet-800',
        'bg-violet-700',
        'bg-violet-600',
        'bg-violet-500',
        'hover:bg-violet-300',
        'hover:bg-violet-400',
    ],

    theme: {
        extend: {
            keyframes: {
                wiggle: {
                    '0%, 100%': { transform: 'rotate(-3deg)' },
                    '50%': { transform: 'rotate(3deg)' },
                },
            },
            animation: {
                wiggle: 'wiggle 0.5s ease-in-out infinite',
            },
        },
    },

    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
