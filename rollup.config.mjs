import { nodeResolve } from '@rollup/plugin-node-resolve';

export default {
  input: './editor.mjs',  // The entry point (your source file)
  output: {
    file: './static/js/editor.bundle.js',  // The bundled file output
    format: 'iife',  // IIFE format for browser compatibility
  },
  plugins: [nodeResolve()],
};
