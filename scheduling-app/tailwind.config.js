/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,ts}'],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#01696f', light: '#00838a', dark: '#004f54' },
        shift: { scheduled:'#FFC107', confirmed:'#4CAF50', alert:'#EF5350', pending:'#FF9800', open:'#90CAF9', cancelled:'#BDBDBD' },
        surface: { page:'#F5F5F5', card:'#FFFFFF', header:'#FAFAFA', today:'#E3F2FD' },
        border: { DEFAULT:'#E0E0E0', strong:'#BDBDBD' },
        text: { primary:'#212121', secondary:'#757575', inverse:'#FFFFFF' }
      },
      fontFamily: { sans: ['Inter','Roboto','sans-serif'] },
      fontSize: { xs:'11px', sm:'12px', base:'13px', md:'14px', lg:'16px', xl:'18px', '2xl':'20px' },
      spacing: { 0:'0', 1:'4px', 2:'8px', 3:'12px', 4:'16px', 5:'20px', 6:'24px', 8:'32px', 10:'40px', 12:'48px' },
      borderRadius: { sm:'4px', DEFAULT:'6px', md:'8px', lg:'12px', full:'9999px' },
      boxShadow: { card:'0 1px 3px rgba(0,0,0,0.12)', hover:'0 4px 8px rgba(0,0,0,0.15)' }
    }
  },
  plugins: []
}
