/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./components/**/*.{js,ts,jsx,tsx,html}",
    "./dev/**/*.{js,ts,jsx,tsx,html}",
    "./server/**/*.{js,ts,jsx,tsx,html}",
    "./www/**/*.{js,ts,jsx,tsx,html}",
    "./docs/**/*.{js,ts,jsx,tsx,html}"
  ],
  theme: {
    screens: {
      'mobile': {'max': '768px'},
      'desktop': {'min': '769px'},
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px',
    },
    extend: {
      colors: {
        // Dev domain colors - Blue theme
        'dev': {
          50: '#eff6ff',
          100: '#dbeafe', 
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554'
        },
        // Server domain colors - Green theme
        'server': {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0', 
          300: '#86efac',
          400: '#4ade80',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
          800: '#166534',
          900: '#14532d',
          950: '#052e16'
        },
        // WWW domain colors - Purple theme
        'www': {
          50: '#faf5ff',
          100: '#f3e8ff',
          200: '#e9d5ff',
          300: '#d8b4fe',
          400: '#c084fc',
          500: '#a855f7',
          600: '#9333ea',
          700: '#7c3aed',
          800: '#6b21a8',
          900: '#581c87',
          950: '#3b0764'
        },
        // Common colors
        'primary': {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe', 
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554'
        }
      },
      spacing: {
        // Touch-friendly spacing
        'touch': '44px',
        'touch-sm': '40px',
        'touch-lg': '48px',
        // Component-specific spacing
        'navbar-height': '64px',
        'ticker-height': '32px',
        'footer-padding': '2rem'
      },
      fontSize: {
        // Mobile-optimized text sizes
        'mobile-xs': ['0.75rem', { lineHeight: '1rem' }],
        'mobile-sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'mobile-base': ['1rem', { lineHeight: '1.5rem' }],
        'mobile-lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'mobile-xl': ['1.25rem', { lineHeight: '1.75rem' }],
        // Desktop-optimized text sizes
        'desktop-xs': ['0.75rem', { lineHeight: '1rem' }],
        'desktop-sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'desktop-base': ['1rem', { lineHeight: '1.5rem' }],
        'desktop-lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'desktop-xl': ['1.25rem', { lineHeight: '1.75rem' }]
      },
      animation: {
        'ticker': 'ticker 30s linear infinite',
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out'
      },
      keyframes: {
        ticker: {
          '0%': { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(-100%)' }
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        }
      },
      boxShadow: {
        'navbar': '0 2px 4px -1px rgba(0, 0, 0, 0.06), 0 1px 2px -1px rgba(0, 0, 0, 0.1)',
        'card': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'card-hover': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
      },
      zIndex: {
        'navbar': '1000',
        'ticker': '999',
        'dropdown': '1001'
      }
    },
  },
  plugins: [
    // Custom plugin for component-specific utilities
    function({ addUtilities, addComponents, theme }) {
      // Touch-friendly utilities
      addUtilities({
        '.touch-target': {
          minHeight: theme('spacing.touch'),
          minWidth: theme('spacing.touch'),
        },
        '.touch-target-sm': {
          minHeight: theme('spacing.touch-sm'),
          minWidth: theme('spacing.touch-sm'),
        },
        '.touch-target-lg': {
          minHeight: theme('spacing.touch-lg'),
          minWidth: theme('spacing.touch-lg'),
        }
      });

      // Component base styles
      addComponents({
        '.navbar-base': {
          height: theme('spacing.navbar-height'),
          position: 'fixed',
          top: '0',
          left: '0',
          right: '0',
          zIndex: theme('zIndex.navbar'),
          backgroundColor: 'white',
          boxShadow: theme('boxShadow.navbar'),
        },
        '.ticker-base': {
          height: theme('spacing.ticker-height'),
          position: 'fixed',
          top: theme('spacing.navbar-height'),
          left: '0',
          right: '0',
          zIndex: theme('zIndex.ticker'),
          overflow: 'hidden',
          whiteSpace: 'nowrap',
        },
        '.dropdown-menu': {
          position: 'absolute',
          top: '100%',
          left: '0',
          right: '0',
          backgroundColor: 'white',
          boxShadow: theme('boxShadow.card'),
          borderRadius: theme('borderRadius.md'),
          zIndex: theme('zIndex.dropdown'),
        }
      });
    }
  ],
}