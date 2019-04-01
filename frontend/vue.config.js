// vue.config.js
const fs = require("fs");

module.exports = {
  css: {
    loaderOptions: {
      sass: {
        data: fs.readFileSync("src/variables.scss", "utf-8")
      }
    }
  },
  chainWebpack: config => {
    config.module
      .rule("vue")
      .use("vue-svg-inline-loader")
      .loader("vue-svg-inline-loader")
      .options({
        removeAttributes: ["alt", "src"],
        svgo: {
          plugins: [
            { cleanupIDs: false },
            { removeDoctype: true },
            { removeComments: true }
          ]
        }
      });
  }
};
