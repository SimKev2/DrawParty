const path = require('path');
const webpack = require("webpack");
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');


module.exports = {
    entry: {
        app: path.join(__dirname, "js/index.js"),
    },
    output: {
        filename: "app.js",
        path: path.join(__dirname)
    },
    plugins: [
        new webpack.optimize.CommonsChunkPlugin({
            names: ['vendor', 'manifest'],
            filename: 'vendor.js',
            minChunks: function (module) {
                return module.context && module.context.indexOf('node_modules') !== -1;
            }
        })
    ],
    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                loader: 'babel-loader',
                include: path.join(__dirname, 'js')
            }
        ]
    },
    devtool: (process.env.NODE_ENV === 'production') ? 'nosources-source-map' : 'eval-source-map'
};
