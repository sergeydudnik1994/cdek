/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./*.html", 
    "./src/components/*.html", 
    "./blog/*.html", 
    "./geo/*.html"
  ],
  theme: { 
    extend: { 
      colors: { cdek: '#8de21a', dark: { 900: '#0b101d' } } 
    } 
  },
  plugins: [],
}
