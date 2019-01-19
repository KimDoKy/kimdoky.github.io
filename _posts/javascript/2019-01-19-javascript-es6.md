---
layout: post
section-type: post
title: javascript - ES6
category: javascript
tags: [ 'javascript' ]
---

## ES6

### const, let
- 변수를 선언할 때 사용하는 예약어
- const : 선언후 값이 바뀌지 않는 변수
 - 변수의 용도를 구분함으로 코드의 가독성을 높임

```javascript
let a = 10;
a = 20; // 20

const b = 10;
b = 20; // Uncaught TypeError: Assignment to constant variable.
```

### 블록의 유효범위

```javascript
// ES5
var i = 10;
for (var i = 0; i < 5; i++) {
    console.log(i);  // 0,1,2,3,4
}
console.log(i);  // 5

// ES6
let i = 10;
for (var i = 0; i < 5; i++) {
    console.log(i); // 0,1,2,3,4
}
console.log(i);  // 10
```

### 화살표 함수(Arrow Functions)

```javascript
var sunNumber = function(a, b) {
    return a + b;
};

var sumNumber = (a, b) => {
    return a + b;
}
```

- 구현 속도도 빨라지고 코드의 길이도 짧아짐

### import, export

- import : 다른 파일의 내용을 불러옴
- export : 한 파일의 특정 기능을 다른 파일에서 사용할수 있도록 설정
 - JS는 변수의 유효 범위가 파일 단위로 구분되지 않고, 기본적으로 같은 유효범위를 가짐
 - 복잡한 app을 작성시 정의된 변수를 잘못 재정의하거나 유효범위 충돌이 발생함
 - 이러한 문제를 방지하기 위해 모듈화가 필요

```javascript
// ./login.js
export const id = 'test';

// ./main.js
import {id} from './login.js';
console.log(id);
```

> 출처: [Do it! Vue.js 입문](http://www.yes24.com/24/goods/58206961)
