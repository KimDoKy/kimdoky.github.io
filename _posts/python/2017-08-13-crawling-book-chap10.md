---
layout: post
section-type: post
title: crawling - P2. 고급 스크레이핑 _ cahp 10. 자바스크립트 스크레이핑
category: python
tags: [ 'python' ]
---

클라이언트 쪽 스크립트 언어는 웹 서버가 아니라 브라우저 자체에서 동작하는 언어입니다. 클라이언트 쪽 언어의 성공은 브라우저가 그 언어를 얼마나 지원하는지에 달려있습니다.  

온라인에서 자주 마주칠 언어는 플래시 애플리케이션에서 사용하는 액션스크립트와 자바스크립트 둘뿐입니다. 액션스크립트는 10년 전에 비하면 거의 사라졌다시피 하였고, 지금 용도는 주로 온라인 게임에서의 멀티미디어 파일 스트리밍, 업데이트가 되지 않는 오래 된 사이트의 시작페이지 정도입니다. 플래시 페이지를 스크레이핑할 필요는 거의 없기 때문에, 이번 챕터에서는 자바스크립트만 다룹니다.  

자바스크립트는 현재 웹에서 가장 널리 쓰이고 가장 잘 지원되는 클라이언트 스크립트 언어입니다. 자바스크립트는 사용자 추적을 위한 정보 수집, 폼을 새로 고치지 않은 상태에서의 정보 전송, 멀티미디어 파일 등에 쓰이며, 자바스크립트만으로 만든 온라인 게임도 있습니다. 아주 단순해 보이는 페이지에도 자바스크립트가 들어 있는 경우가 자주 있습니다. 자바스크립트는 페이지의 소스 코드에서 <script> 태그 부분에 들어 있습니다.  

```javascript
<script>
  alert("This creates a pop-up using JavaScript");
</script>
```

## 10.1 자바스크립트에 관한 간단한 소개

스크레이핑하는 스크립트에서 무슨 일을 하는지 최소한이라도 이해한다면 아주 큰 도움이 될 겁니다. 따라서 자바스크립트에 익숙해져야 합니다.  

자바스크립트는 약한 타이핑 언어이며 그 문법은 종종 자바나 C++과 비교됩니다. 연산자나 루프, 배열 같은 문법적 요소는 일부 비슷하지만, 약한 타입과 스크립트에서 출발한 성격 때문에 일부 프로그래머들은 자바스크립트를 이해하는게 골치 아플 수 있습니다.  

다음 코드는 재귀적으로 피보나치 수열을 계산한 후 브라우저의 개발자 콘솔에 출력합니다.

```javascript
<script>
function fibonacci(a, b){
  val nextNum = a + b;
  console.log(nextNum+" is in the Fibonacci sequence");
  if(nextNum < 100){
    fibonacci(b, nextNum);
  }
}
fibonacci(1, 1);
</script>
```

모든 변수 앞에 `var`가 있습니다. 이 문법은 PHP의 $ 기호나, 자바와 C++의 int, String, List 등 타입 선언과 비슷합니다. 파이썬은 이렇게 명시적인 변수 선언이 없다는 점에서 독특합니다. 또한 자바스크립트에는 함수를 변수처럼 사용할 수 있다는 대단히 좋은 기능이 좋습니다.

```javascript
<script>
var fibonacci = function() {
  var a = 1;
  var b = 1;
  return function () {
    var temp = b;
    b = a + b;
    a = temp;
    return b;
  }
}
var fibInstance = fibonacci();
console.log(fibInstance()+" is in the Fibonacci sequence");
console.log(fibInstance()+" is in the Fibonacci sequence");
console.log(fibInstance()+" is in the Fibonacci sequence");
</script>
```

이 코드는 언뜻 보기에는 이해가 안되지만, 람다 표현식을 염두해 둔다면 그리 어렵지 않습니다.  
변수 fibonacci 는 함수로 정의됐습니다. 이 함수가 반환하는 값은 함수이며, 반환된 함수는 피보나치 수열에서 점점 커지는 값을 출력합니다. fibonacci 를 호출할 때마다 피보나치 수열을 계산하는 함수를 반환하며, 그 함수를 다시 실행해서 함수에 들어 있는 값을 증가시킵니다.  

언뜻 보기엔 대단히 난해해 보이지만, 피보나치 수열을 계산하는 것 같은 종류의 문제는 대개 이런 패턴을 사용합니다. 함수를 마치 변수처럼 다루는 개념은 사용자의 행동이나 콜백을 처리할 때 대단히 유용하며, 자바스크립트 코드를 읽어야 한다면 이런 프로그래밍 스타일에 익숙해질 필요가 있습니다.

### 10.1.1 널리 쓰이는 자바스크립트 라이브러리

자바스크립트 표준을 이해하는 것도 중요하지만, 라이브러리가 없으면 최신 웹에서 할 수 있는 일은 상당히 제한됩니다. 페이지의 소스 코드를 읽어보면 널리 쓰이는 라이브러리가 하나 이상은 들어 있습니다.  

파이썬을 이용해 자바스크립트를 실행하는건 많은 시간과 프로세스 자원을 소비합니다. 특시 대규모로 실행한다면 더 심할 것입니다.

#### 제이쿼리

제이쿼리(jQuery)는 널리 쓰이는 라이브러리입니다. 제이쿼리를 사용하는 사이트는 코드 어딘가에 다음과 같은 제이쿼리를 불러오는 임포트 문이 있기 때문에 구분하기 쉽습니다.

```HTML
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
```

사이트에서 제이쿼리를 사용한다면 반드시 조심해서 스크랩해야 합니다. 제이쿼리는 자바스크립트가 실행된 다음에 동적으로 HTML 콘텐츠를 생성할 수 있기 때문입니다. 이전 챕터들에서 다룬 방법으로 스크랩하면 자바스크립트로 생성한 콘텐츠는 모두 놓치게 됩니다.  

또한, 제이쿼리를 사용하는 페이지에는 애니메이션이나 대화형 콘텐츠, 미디어 파일 등이 들어 있을 확률이 높고 이런 것들은 스크랩을 어렵게 합니다.

#### 구글 애널리틱스

전체 웹사이트의 50% 이상이 [구글 애널리틱스(Google Analytics)](http://bit.ly/2fBflnQ){:target="`_`blank"}를 사용합니다. 구글 애널리틱스는 아마 인터넷에서 가장 널리 쓰이는 자바스크립트 라이브러리인 동시에, 가장 널리 쓰이는 사용자 추적 도구일 겁니다.  

페이지에서 구글 애널리틱스를 사용하는지 여부는 간단히 알 수 있습니다. 구글 애널리틱스를 사용하는 페이지는 소스 코드 마지막에 다음과 비슷한 자바스크립트가 들어 있습니다.

```HTML
<!-- Google Analytics -->
<script type="text/javascript">
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-4591498-1']);
_gaq.push(['_setDomainName', 'oreilly.com']);
_gaq.push(['_addIgnoredRef', 'oreilly.com']);
_gaq.push(['_setSiteSpeedSampleRate', 50]);
_gaq.push(['_trackPageview']);

(function() { var ga = document.createElement('script'); ga.type =
'text/javascript'; ga.async = true; ga.src = ('https:' ==
document.location.protocol ? 'https://ssl' : 'http://www') +
'.google-analytics.com/ga.js'; var s =
document.getElementsByTagName('script')[0];
s.parentNode.insertBefore(ga, s); })();
</script>
```
> 위 코드는 https://www.oreilly.com/ 에서 가져왔습니다. 해당 코드는 head에 들어 있습니다.

이 스크립트는 페이지에서 페이지로 이동하는 사용자의 움직임을 추적하는 특수한 쿠키를 사용합니다. 챕터 후반에서 셀레니움을 사용해 자바스크립트를 실행하고 쿠키를 처리하는 스크레이퍼를 만들 겠지만, 이런 스크레이퍼에서는 구글 애널리틱스는 문제가 될 수 있습니다.  

사이트에서 구글 애널리틱스나 그와 비슷한 웹 분석 시스템을 사용하고, 그 사이트에서 스크레이퍼가 다녀갔음을 알지 못하게 하고 싶다면 분석에 사용되는 쿠키 또는 모든 쿠키를 비활성화해야 합니다.

#### 구글 지도

구글 지도는 어느 사이트에든 아주 쉽게 지도를 임베드할 수 있는 API를 제공합니다.  

어떤 종류든 위치 데이터를 스크랩할 경우, 구글 지도가 어떻게 작동하는지 이해한다면 위도/경도 좌표, 운이 좋다면 주소까지 수월하게 가져올 수 있습니다. 구글 지도에서 위치를 표시하기 위해 가장 많이 쓰는 방법은 **마커** (핀이라고 부르기도 함)입니다.  

구글 지도에서 마커를 삽입할 때는 다음과 같은 코드를 사용합니다.

```javascript
var marker = new google.maps.Marker({
  position: new google.maps.LatLng(-25.363883,131.044922),
  map: map,
  title: 'Some marker text'
});
```

파이써에서 google.maps.LatLng 사이에 있는 좌표를 모두 추출해 위도/경도 리스트를 만드는건 어렵지 않습니다.  

[구글의 리버스 지오코딩(reverse Geocoding)](https://developers.google.com/maps/documentation/javascript/examples/geocoding-reverse){:target="`_`blank"} API 를 사용하면 이들 좌표 쌍을 저장하고 분석하기 알맞은 형태의 주소로 변환할 수 있습니다.

## 10.2 Ajax와 동적 HTML

### 10.2.1 셀리네움으로 파이썬에서 자바스크립트 실행

## 10.3 리다이렉트 처리
