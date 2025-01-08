import { defineConfig } from 'vite';
import fs from 'fs';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    https: {
      key: fs.readFileSync('C:/Users/julia/animal_adoption/localhost1.key'),  // Ścieżka do pliku klucza
      cert: fs.readFileSync('C:/Users/julia/animal_adoption/localhost1.crt'), // Ścieżka do pliku certyfikatu
    },
    port: 5173,
  },
})