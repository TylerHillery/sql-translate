import { nodeResolve } from '@rollup/plugin-node-resolve';

export default {
  input: './src/editor.js',  // The entry point (your source file)
  output: {
    file: './static/js/editor.bundle.js',  // The bundled file output
    format: 'iife',  // IIFE format for browser compatibility
    name: 'cm6'
  },
  plugins: [nodeResolve()],
};
