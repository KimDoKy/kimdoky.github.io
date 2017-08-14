---
layout: post
section-type: post
title: crawling - P2. 고급 스크레이핑 _ chap 10. 자바스크립트 스크레이핑
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

지금까지 다룬 웹서버와의 통신은 페이지를 가져올 때 일종의 HTTP 요청을 보낸 것 뿐이었습니다. 페이지를 새로 고치지 않고 폼을 전송하거나 서버에서 정보를 가져온 경험이 있다면 그건 아마 **Ajax** 를 통한 것이었을 겁니다.  

일부 오해하는 사람도 있지만, Ajax는 언어가 아니라 특정 작업을 하기 위해 사용하는 기술의 묶음입니다. Ajax는 비동기 자바스크립트와 XML의 약자이며, 서버에 별도의 페이지를 요청하지 않고 정보를 주고 받기 위해 사용됩니다. '이 폼은 Ajax를 써서 웹 서버와 통신합니다'라고 말할 수 있습니다.  

Ajax와 마찬가지로, **DHTML(Dynamic HTML)** 도 같은 목적을 위해 함께 사용하는 기술을 묶어부르는 말입니다. DHTML은 클라이언트 쪽 스크립트가 페이지의 HTML 요소 바뀜에 따라 바뀌는 HTML이나 CSS입니다. 사용자가 커서를 움직여야만 버튼이 나타나거나, 클릭에 따라 배경색이 바뀌거나, Ajax 요청으로 새로운 콘텐츠가 나타날 수도 있습니다.  

'동적(Dynamic)'이란 단어는 일반적으로 '움직이는', '변하는' 같은 뜻을 떠올리게 하지만, 대화형 HTML 콘텐츠나 움직이는 이미지가 들어 있다 해서 그 페이지가 DHTML은 아닙니다. 인터넷에서 가장 따분하고 정적으로 보이는 페이지라 하더라도 이면에서 자바스크립트로 HTML과 CSS를 조작하는 DHTML이 있을 수 있습니다.  

다양한 웹사이트에서 아주 많이 스크랩한다면 곧 브라우저에 보이는 콘텐츠가 사이트에서 스크랩한 소스 코드와 맞지 않는 상황이 발생할 겁니다. 스크레이퍼가 내놓은 결과를 보고 브라우저에서 보던 내용이 없는 것을 볼 수도 있습니다. 또한 페이지에서 리다이렉트가 일어나서 다른 페이지로 이동했지만, 페이지 URL은 그대로일 수도 있습니다.  

이런 모든 상황은 자바스크립트가 페이지에서 하는 일을 스크레이퍼는 하지 못하기 때문에 일어나는 현상입니다.  

페이지가 Ajax나 DHTML을 써서 콘텐츠를 바꾸거나 불러온다는 사실을 알아챌 방법은 여러가지가 있지만, 이런 상황의 해결책은 두 가지뿐입니다. 하나는 자바스크립트를 분석해 콘텐츠를 직접 스크랩하는 것이고, 다른 하나는 자바스크립트 자체를 실행할 수 있는 파이썬 패키지를 써서 웹사이트를 브라우저에 보이는 그대로 스크랩하는 것입니다.

### 10.2.1 셀리네움으로 파이썬에서 자바스크립트 실행

[셀리니움](http://www.seleniumhq.org/){:target="`_`blank"}은 웹사이트 테스트 목적으로 개발됐지만, 강력한 웹 스크레이핑 도구로 사용할 수 있습니다. 최근에는 웹사이트가 브라우저에 어떻게 보이는지 정확하게 알 필요가 있을 때도 사용합니다.  
> [TDD 참조](https://kimdoky.github.io/categories/tdd.html){:target="`_`blank"}

셀레니움은 브라우저가 웹사이트를 불러오고, 필요한 데이터를 가져오고, 스크린샷을 찍거나 특정 행동이 웹사이트에 일어난다고 단언하는 등을 자동화합니다.  

셀레니움에는 자체적인 웹 브라우저가 들어있지 않으므로 다른 브라우저가 있어야 동작합니다. 예를 들어 셀레니움을 크롬과 함께 사용하면 말 그대로 크롬을 실행하고 웹사이트를 이동해서 코드에 명시한 동작을 수행합니다. 이렇게 하면 어떤 일이 일어나는지 지켜보기 편하지만, 여기서는 백그라운드에서 조용히 실행되는 [팬텀JS](http://phantomjs.org/){:target="`_`blank"}라는 도구를 사용하겠습니다.  

팬텀JS는 인터페이스가 없는(headless) 브라우저입니다. 팬텀JS는 웹사이트를 메모리에 불러오고 페이지의 자바스크립를 실행하지만, 그래픽은 렌더링하지 않습니다. 셀레니움과 팬텀JS를 결합하면 쿠키와 자바스크립트, 헤더, 그 외의 필요한 모든 것을 쉽게 처리할 수 있습니다.  

셀레니움 라이브러리는 pip로 설치하면 됩니다.

```
pip install selenium
```

팬텀JS는 pip 같은 패키지 관리자로는 설치가 불가하며, [웹사이트](http://phantomjs.org/download.html){:target="`_`blank"}에서 직접 내려 받아야 합니다.  

Ajax를 이용해 데이터를 불러오는 페이지는 아주 많지만(대표적으로 구글), 스크레이퍼를 테스트할 수 있는 샘플 페이지가 있습니다.(http://pythonscraping.com/pages/javascript/ajaxDemo.html) 이 페이지에는 HTML에 직접 입력한 샘플 텍스트가 있는데, 이 텍스트는 2초 뒤에 Ajax로 가져온 콘텐츠로 교체됩니다. 이전에 쓰던 방식대로 이 페이지의 데이터를 스크랩하려 하면, 실제 원하는 데이터가 아니라 로딩 페이지의 데이터만 가지고 오게 됩니다.  

다음 코드는 테스트 페이지에서 Ajax의 '벽' 뒤에 있는 텍스트를 가져옵니다.

```python
from selenium import webdriver
import time

driver = webdriver.PhantomJS()
driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
time.sleep(3)
print(driver.find_element_by_id("content").text)
driver.close()
```
> `selenium.common.exceptions.WebDriverException: Message: 'phantomjs' executable needs to be in PATH.` 에러가 일어난다면..  
팬텀JS 바이너리를 파이썬이나 가상환경이 찾을 수 있는 경로에 설치하는 것을 권장합니다. 즉 현재 작업중인 가상환경이 있다면 `usr/local/var/pyenv/versions/scrapingEnv/bin`안에 팬텀JS 바이너리(`phantomjs`파일)를 두면 됩니다.

셀레니움 라이브러리는 **웹드라이버(WebDriver)** 위에서 호출되는 API입니다. 웹드라이버는 웹사이트를 불러올 수 있다는 점에서 브라우저와 비슷하지만 BeautifulSoup 객체와 마찬가지로 페이지 요소를 찾는 데 쓸 수 있고, 텍스트를 보내거나 클릭하는 등 페이지 요소를 조작할 수 있으며, 그 외에도 웹 스크레이퍼를 작동할 때 필요한 행동을 할 수 있습니다.

> #### 셀레니움 선택자  
이전의 챕터들에서는 find와 find_all과 같은 BeautifulSoup 선택자를 써서 페이지 요소를 선택했습니다. 셀레니움은 웹드라이버의 DOM에서 요소를 찾을 때 완전히 새로운 선택자를 사용합니다. (Document Object Model,DOM : HTML 및 XML 문서를 처리하는 API입니다. 문서의 구조적 형태를 제공하므로 JS와 같은 스크립트 언어를 사용하여 문서 내용과 시작적 표현을 수정할 수 있습니다.)  
예제에서는 선택자 `find_element_by_id`를 사용했지만, 다음과 같이 다른 선택자를 사용하여도 같은 결과를 얻을 수 있습니다.  
```python
driver.find_element_by_css_selector("#content")
driver.find_element_by_tag_name("div")
```
페이지 요소를 여러 개 선택해야 할 때는, 이들 요소 선택자에서 `element`를 `elements`로 바꾸기만 하면 파이썬 리스트를 반환합니다.
```python
driver.find_elements_by_css_selector("#content")
driver.find_elements_by_css_selector("div")
```
물론 이 콘텐츠를 BeautifulSoup로 파싱하는 것도 가능합니다. 웹드라이버의 `page_source`함수는 현 시점의 DOM을 문자열로 반환합니다.
```python
pageSource = driver.page_source
bsObj = BeautifulSoup(pageSource)
print(bsObj.find(id="content").get_text())
```

이 코드는 팬텀JS 라이브러리를 사용해서 셀레니움 웹드라이버를 만듭니다. 팬텀JS는 웹드라이버가 페이지를 불러온 다음 3초 동안 기다리고, 그 다음 콘텐츠를 가져옵니다.  

팬텀JS가 설치된 위치에 따라 새 팬텀JS 웹드라이버를 만들 때 그 위치를 명시적으로 지적해야 할 수도 있습니다.
```python
driver = webdriver.PhantomJS(executable_path='/path/to/bin/phantomjs')
```

모든 것이 정확히 설치됐다면 스크립트를 실행하고 몇 초 뒤에 다음과 같은 텍스트를 출력할 것입니다.

```
Here is some important text you want to retrieve!
A button to click!
```

페이지 자체에는 HTML 버튼이 있지만, 셀레니움의 `.text` 함수는 다른 콘텐츠를 가져오는 방식과 마찬가지로 버튼의 텍스트만 읽어왔습니다.  

위 코드는 time.sleep에서 3초로 지정했지만, 1초만 지정했다면 바뀌기 전의 텍스트를 불러왔을 것입니다.

```
This is some content that will appear on the page while it's loading. You don't care about scraping this.
```

이 방법은 잘 동작하긴 하지만 좀 비효율적이고, 큰 프로젝트에서 사용한다면 문제가 생길 수 있습니다. 페이지를 불러오는 시간은 일정하지 않습니다. 불러오는 순간에 서버가 바쁘거나, 연결 속도에 따라서 시간이 바뀔겁니다. 더 효율적인 방법은 페이지를 완전히 불러왔을 때만 존재하는 요소를 계속해서 확인하다가, 그 요소가 존재할 때만 데이터를 가져오는 겁니다.  

다음 코드는 페이지를 완전히 불러왔을 때만 존재하는, `id`가 `loadedButton`인 버튼을 검사합니다.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.PhantomJS()
driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
try:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "loadedButton"))
    )
finally:
    print(driver.find_element_by_id("content").text)
    driver.close()
```
위 코드에서 **WebDriverWait** 와 **expected_conditions** 을 결합하면 셀레니움에서 **묵시적 대기**(implicit wait)라고 하는 기능을 사용할 수 있습니다.  

묵시적 대기는 DOM이 어떤 상태로 바뀔 때까지 기다린다는 점에서 명시적 대기와는 다릅니다. 앞에서 `time.sleep(3)`으로 명시적 대기를 사용했습니다. 묵시적 대기에서 우리가 기다릴 DOM의 상태는 `expected_conditions`(예상 조건)으로 정의합니다. 셀레니움은 여러가지 예상 조건을 사용할 수 있는데, 그중에서도 자주 쓰이는 것은 다음과 같습니다.

- 알림(alert) 박스 팝업
- 요소(텍스트 박스 등)가 '선택(selected)' 상태로 바뀜
- 페이지 타이틀이 바뀌거나, 어떤 텍스트가 페이지 또는 특정 요소 안에 표시됨
- 보이지 않던 요소가 DOM 상에 보이게 되거나, 반대로 어떤 요소가 DOM에서 사라짐

물론 예상 조건을 사용하려면 어떤 요소를 지켜볼지 지정해야 합니다. 지켜볼 요소는 **위치 지정자(locator)** 로 정합니다. 위치 지정자는 선택자와 다릅니다. 위치 지정자는 `By` 객체를 사용하는 추상 쿼리 언어입니다. By 객체는 다양한 방법으로 사용할 수 있는데, 선택자로 만들 떄도 쓸 수 있습니다.  

다음 예제 코드에서는 위치 지정자를 사용해 id가 loadedButton인 요소를 찾습니다.

```python
EC.presence_of_element_located((By.ID, "loadedButton"))
```
위치 지정자와 `find_element` 함수를 함께 쓰면 선택자를 만들 수 있습니다.
```python
print(driver.find_element("content").text)
```
물론 위 코드는 예제에서 사용한 코드와 같은 일을 합니다.
```python
print(driver.find_element_by_id("content").text)
```
위치 지정자가 필요하지 않다면 쓰지 않아도 됩니다. 임포트 문도 하나 아낄 수 있습니다. 하지만 위치 지정자는 다양한 애플리케이션에서 쓸 수 있고, 매우 유연한 도구입니다.  

`By` 객체와 함께 쓸 수 있는 위치 지정자는 다음과 같습니다.  

#### `ID`
id 속성으로 요소를 찾습니다.
#### `CLASS_NAME`
class 속성으로 요소를 찾습니다. 이 함수의 이름을 `CLASS_NAME`이라고 정한 것은, 셀레니움의 자바 라이브러리에서 class를 예약된 메서드로 사용하므로 `object.CLASS` 형식을 사용하면 문제가 생깁니다. 모든 언어에서 일관된 문법을 쓰기 위해 `CLASS_NAME`이란 이름으로 정해졌습니다.
#### `CSS_SELECTOR`
class, id, tag 이름으로 요소를 찾습니다. 표기법은 각각 `#idName`, `.classNmae`, `tagName` 입니다.
#### `LINK_TEXT`
링크 텍스트로 `<a>` 태그를 찾습니다. 예를 들어 링크 텍스트가 'Next'이면 `(By.LINK_TEXT, "Next")`로 선택할 수 있습니다.
#### `PARTIAL_LINK_TEXT`
`LINK_TEXT`와 비슷하지만 문자열 일부에 일치하는 텍스트를 찾습니다.
#### `NAME`
name 속성으로 요소를 찾습니다. 폼을 다룰 때 편리합니다.
#### `TAG_NAME`
태그 이름으로 요소를 찾습니다.
#### `XPATH`
XPATH 표현식을 써서 요소를 찾습니다.

> #### XPath 문법  
XPath(XML Path)는 XML 문서의 일부분을 탐색하고 선택하는 데 사용하는 쿼리 언어입니다. 파이썬, 자바, C# 등의 언어에서 XML 문서를 다룰 때 이용되곤 합니다.  
BeautifulSoup은 XPath를 지원하지 않지만, 다른 여러 라이브러리는 XPath를 지원합니다. XPath는 CSS 선택자를 사용하는 것과 같은 방식으로 사용할 수 있을 때가 많습니다.(ex: `myTag#idname`) 원래는 HTML보다는 더 범용적인 XML 문서를 다루기 위해 설계되었습니다.  
XPath 문법은 크게 4 가지 개념으로 이루어집니다.  
- 루트 노드 대 루트가 아닌 노드
  - `/div`는 오직 문서의 루트에 있는 div 노드만 선택합니다.
  - `//div`는 문서의 어디에 있든 모든 div 노드를 선택합니다.
- 속성 선택
  - `//@href`는 href 속성이 있는 모든 노드를 선택합니다.
  - `//a[@href='http://google.com']`는 문서에서 구글을 가리키는 모든 링크를 선택합니다.
- 위치에 따른 노드 선택
  - `(//a)[3]`는 문서의 세 번째 링크를 선택합니다.
  - `(//table)[last()]`는 문서의 마지막 테이블을 선택합니다.
  - `(//a)[position() < 3]`는 문서의 처음 두 링크를 선택합니다.
- 아스테라크(`*`)는 어떤 문자나 노드의 집합이든 선택하므로, 다양한 상황에서 사용할 수 있습니다.
  - `//table/tr/*`는 모든 테이블에서 모든 자식 tr 태그를 선택합니다.(th와 td를 같이 쓰는 테이블에서 모든 셸을 선택할 때 유용합니다.)
  - `//div[@*]`는 속성이 하나라도 있는 모든 div 태그를 선택합니다.  
물론 XPath 문법에는 더 고급 기능도 많이 있습니다. 시간의 흐름에 따라 XPath는 다소 복잡한 쿼리 언어로 발전했습니다. boolean 논리 함수(예를 들어 `position()`), 그 밖의 다양한 연산자를 포함하게 되었습니다.  
다른 문법이 필요하다면 [마이크로소프트의 XPath 문법 페이지](http://bit.ly/1HEMbd3){:target="`_`blank"}를 참고하세요.

## 10.3 리다이렉트 처리

클라이언트 쪽 리다이렉트는 페이지 콘텐츠를 보내기 전에 서버에서 실행하는 리다이렉트와는 달리 브라우저에서 자바스크립를 통해 실행되는 리다이렉트입니다. 웹 브라우저에서 페이지를 방문할 때는 그 차이를 구분하기 어렵습니다. 리다이렉트가 워낙 빨리 일어나서 지연 시간을 전혀 느끼지 못하므로 서버 리다이렉트라고 생각할 수도 있습니다.  

하지만 웹 스크레이핑에서는 차이가 큽니다. 서버 쪽 리다이렉트의 경우, 셀레니움을 전혀 쓰지 않고 파이썬의 `urllib` 라이브러리만으로도 쉽게 처리할 수 있습니다. 반면 클라이언트쪽 리다이렉트는 자바스크립트를 실행하지 않으면 전혀 처리할 수 없습니다.  

셀레니움은 자바스크립트 리다이렉트를 다른 자바스크립트와 같은 방법으로 처리합니다. 하지만 이런 리다이렉트에서 중요한 점은 페이지가 리다이렉트를 끝낸 시점이 언제인지 파악하는 것입니다.
http://pythonscraping.com/pages/javascript/redirectDemo1.html 페이지에 이런 파입의 리다이렉트 예제가 있습니다. 이 페이지는 2초후 리대이렉트가 일어납니다.  

이런 리다이렉트를 감지하려면 페이지를 처음 불러올 때 있었던 DOM 요소 하나를 주시하고 있어야 합니다. 그러다가 셀레니움이 `NoSuchElementException` 예외를 일으킬 때, 즉 그 요소가 페이지의 DOM에 더는 존재하지 않을 때가 바로 리다이렉트가 일어난 시점입니다.

```python
from selenium import webdriver
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name("div")
        except NoSuchElementException:
            return

driver = webdriver.PhantomJS()
driver.get("http://pythonscraping.com/pages/javascript/redirectDemo1.html")
waitForLoad(driver)
print(driver.page_source)
```
이 스크립트는 0.5초마다 페이지를 체크하면서 총 10초를 기다립니다.

실행 결과입니다.

```
<html><head>
<title>The Destination Page!</title>

</head>
<body>
This is the page you are looking for!

</body></html>
```
