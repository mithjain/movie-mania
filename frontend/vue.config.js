const path = require('path');
const webpack = require('webpack');

module.exports = {
  transpileDependencies: [
    'vue-echarts',
    'resize-detector',
    'vue-jest'
  ],
  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: 'all'
      }
    },
    resolve: {
      alias: {
        '@': path.resolve('src'),
      }
    },
    plugins: [
      new webpack.ProvidePlugin({
        introJs: ['intro.js']
      })
    ]
  },
  lintOnSave: 'error',
  runtimeCompiler: true,
  productionSourceMap: false,
  outputDir: path.resolve(__dirname, '../static/'),
  publicPath: process.env.VUE_PUB_PATH,
  indexPath: path.resolve(__dirname, '../static/index.html'),
};

