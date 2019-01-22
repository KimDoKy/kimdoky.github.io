---
layout: post
section-type: post
title: Webpack config description
category: javascript
tags: [ 'javascript' ]
---

```
// output 속성에서 사용한 노드 path 라이브러리와 웹팩 플러그인에서 사용할
// node_modules의 웹팩 라이브러리를 node_modules 폴더에서 로딩하여
// path, webpack 에 각각 저장
var path = require('path')
var webpack = require('webpack')

module.exports = {
  entry: './src/main.js',  // entry 속성. main.js 파일에 정의한 내용에 따라 app의 구성요소와 파일들이 웹팩으로 번들링(빌드)됨
  output: {                // 빌드를 하고 난 결과물 파일의 위치와 이름 지정
    path: path.resolve(__dirname, './dist'),
    publicPath: '/dist/',
    filename: 'build.js'
  },
  module: {
    rules: [
      {
        test: /\.css$/,  // css 파일에 vue-style-loader, css-loader를 적용
        use: [           // css 파일을 모두 js 파일로 변환함.
          'vue-style-loader',  // 최종적으로 index.html에 style 태그로 삽입됨
          'css-loader'
        ],
      },      {
        test: /\.vue$/,  // vue 파일에 vue-loader를 적용
        loader: 'vue-loader', // template, script, style 등이 js로 변환되어 결과물에 포함됨
        options: {
          loaders: {
          }
          // other vue-loader options go here
        }
      },
      {
        test: /\.js$/,  // js 파일에 babel-loader를 적용.
        loader: 'babel-loader',  // js의 es6 문법을 모든 브라우저에서 호환 가능한 js로 변환함
        exclude: /node_modules/
      },
      {
        test: /\.(png|jpg|gif|svg)$/,  // 이미지 파일들을 file-loader를 이용하여 js파일로 변환함
        loader: 'file-loader',
        options: {
          name: '[name].[ext]?[hash]'
        }
      }
    ]
  },
  resolve: {  // 빌드할 때 어떤 뷰 라이브러리를 선택할지 지정
    alias: {  // vue.esm.js는 최신 웹팩 버전을 사용할 수 있는 Full 버전을 의미
      'vue$': 'vue/dist/vue.esm.js'   // 미지정시 vue.rumtime.esm.js 를 사용
    },
    extensions: ['*', '.js', '.vue', '.json']
  },
  devServer: {  
    historyApiFallback: true,  // 뷰 라우터와 함께 사용하기 위해 true로 지정
    noInfo: true,              // 처음 서버 시작시에만 웹팩 빌드 정보를 보여줌. 변경시 안보여줌
    overlay: true              // 빌드시 오류가 있으면 브라우저 화면 전체에 오류를 표시
  },
  performance: {   // true 지정시 빌드파일이 250kb를 넘으면 경고 메시지 표시
    hints: false
  },
  devtool: '#eval-source-map'  // 빌드 파일로 구동시 개발자 도구에서 사용할 디버깅 방식을 지정
}

// 배포시 app의 성능 향상을 위한 추가 설정
if (process.env.NODE_ENV === 'production') {
  module.exports.devtool = '#source-map'  // 개발자 도구 분석 옵션을 #source-map으로 지정
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({     // js 파일의 크기를 줄이는 Uglify 플러그인과 환경 변수 값을 설정
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    })
  ])
}
```

> 출처: [Do it! Vue.js 입문](http://www.yes24.com/24/goods/58206961)
