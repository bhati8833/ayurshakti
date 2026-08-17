import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        ayur: {
          bg: '#FAF9F5',         // Warm organic alabaster background
          surface: '#FFFFFF',    // Clean white surface
          card: '#F5F3ED',       // Soft organic sand card background
          border: '#D8D4C8',     // Subtle natural border
          forest: '#0C2920',     // Deep herbal forest green (Primary Text & Accents)
          herbal: '#1B4332',     // Rich herbal green
          emerald: '#047857',    // Deep vibrant emerald green (Contrast ratio >= 5.2:1)
          gold: '#855B14',       // Rich deep Ayurvedic gold (Contrast ratio >= 5.6:1)
          goldHover: '#6E490E',  // Darker gold on hover
          sage: '#3B4E46',       // Deep slate sage text secondary (Contrast ratio >= 7.5:1)
          sand: '#EFECE6',       // Light sand container
        },
      },
      fontFamily: {
        serif: ['var(--font-playfair)', 'Georgia', 'serif'],
        sans: ['var(--font-jakarta)', 'Inter', 'sans-serif'],
      },
      boxShadow: {
        'soft-glow': '0 20px 40px -15px rgba(12, 41, 32, 0.08)',
        'card-hover': '0 25px 50px -12px rgba(12, 41, 32, 0.12)',
        'glass': '0 8px 32px 0 rgba(12, 41, 32, 0.04)',
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
    },
  },
  plugins: [],
};

export default config;
