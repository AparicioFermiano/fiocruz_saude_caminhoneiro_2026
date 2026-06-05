// Configuração compartilhada do Tailwind CSS (Play CDN)
// Este arquivo deve ser carregado após tailwind.js em cada página
tailwind.config = {
  theme: {
    extend: {
      colors: {
        brand: {
          blue:   '#1e40af',
          orange: '#f97316',
          dark:   '#1e293b',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      }
    }
  }
}
