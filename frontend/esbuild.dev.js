const esbuild = require('esbuild');

const isWatch = process.argv.includes('--watch');

async function build() {
  const ctx = await esbuild.context({
    entryPoints: ['src/main.jsx'],
    outfile: 'dist/bundle.js',
    bundle: true,
    format: 'esm',
    target: 'es2020',
    loader: {
      '.js': 'jsx',
      '.jsx': 'jsx',
      '.css': 'css'
    },
    sourcemap: true,
    outdir: 'dist',
    publicPath: '/',
    define: {
      'process.env.NODE_ENV': '"development"'
    },
    jsx: 'automatic',
    assetNames: 'assets/[name]-[hash]',
    chunkNames: 'chunks/[name]-[hash]',
  });

  if (isWatch) {
    await ctx.watch();
    console.log('🔧 esbuild watching for changes...');
  } else {
    await ctx.rebuild();
    await ctx.dispose();
  }
}

build().catch(() => process.exit(1));