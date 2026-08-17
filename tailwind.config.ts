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
          border: '#E6E2D8',     // Subtle natural border
          forest: '#0C2920',     // Deep herbal forest green (Primary Text & Accents)
          herbal: '#1B4332',     // Rich herbal green
          emerald: '#059669',    // Vibrant emerald green
          gold: '#C5A059',       // Muted Ayurvedic gold
          goldHover: '#B28C46',  // Darker gold on hover
          sage: '#657A70',       // Soft sage text secondary
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
