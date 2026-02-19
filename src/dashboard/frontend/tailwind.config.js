/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        panel: '#1a1f2e',
        surface: '#242938',
        border: '#2d3446',
        accent: '#3b82f6',
        critical: '#ef4444',
        warning: '#f59e0b',
        success: '#22c55e',
        muted: '#6b7280',
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
    },
  },
  plugins: [],
}
