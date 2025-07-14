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
