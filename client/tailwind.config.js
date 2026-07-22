/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'gotham-bg': '#0A0E1A',
        'gotham-bg-sec': '#111827',
        'gotham-card': '#1C2333',
        'gotham-accent': '#3B82F6',
        'gotham-danger': '#EF4444',
        'gotham-warning': '#F59E0B',
        'gotham-success': '#10B981',
        'gotham-text': '#F9FAFB',
        'gotham-text-sec': '#9CA3AF',
        'gotham-border': '#2D3748',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
