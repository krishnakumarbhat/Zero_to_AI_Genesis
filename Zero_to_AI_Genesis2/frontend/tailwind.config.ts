import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        heading: ['Syne', 'sans-serif'],
        body: ['Manrope', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
        accent: ['Orbitron', 'sans-serif'],
      },
      colors: {
        genesis: {
          bg: '#0a0a0a',
          surface: '#121212',
          surfaceHL: '#18181b',
          border: '#27272a',
          text: '#ededed',
          muted: '#a1a1aa',
          dim: '#52525b',
        },
        season: {
          0: '#4CAF50',
          1: '#2196F3',
          2: '#FF9800',
          3: '#9C27B0',
          4: '#F44336',
          5: '#00BCD4',
          6: '#FF5722',
          7: '#673AB7',
        },
      },
      animation: {
        'pulse-glow': 'pulseGlow 2s ease-in-out infinite',
        'float': 'float 6s ease-in-out infinite',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        pulseGlow: {
          '0%, 100%': { opacity: '0.4' },
          '50%': { opacity: '1' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
    },
  },
  plugins: [],
};
export default config;
