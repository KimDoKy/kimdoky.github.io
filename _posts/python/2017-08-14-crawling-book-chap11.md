---
layout: post
section-type: post
title: crawling - P2. 고급 스크레이핑 _ chap 11. 이미지 처리와 텍스트 인식
category: python
tags: [ 'python' ]
---

구글의 자율주행 자동차부터 위조지폐 인식하는 자판기까지, 컴퓨터에 눈을 다는 방대한 작업은 우리에게 큰 영향을 미치는 분야입니다. 이번 챕터에서는 이 분야의 작은 일부인 텍스트 인식에 집중합니다. 그중에서도, 온라인에서 가져온 텍스트 기반 이미지를 다양한 파이썬 라이브러리로 인식하고 사용하는 방법에 대해 다룹니다.  

텍스트 대신 이미지를 쓰는 건 봇이 텍스트를 읽는 것을 막기위해 사용하는 방법 중 하나입니다. 연락처에서 이메일 주소나 전체부분을 이미지 처리된 경우들이 있습니다. 정교하게 처리하면 사람조차도 이미지인지 텍스트인지 구분하기 어렵고, 봇은 그런 이미지 때문에 스팸을 뿌려대는 사람들로부터 이메일 주소를 보호할 수 있습니다.  

자동 가입 방지 문자(CAPTCHA) 역시 사용자가 보안 이미지를 읽을 수 있지만 대부분의 못은 읽지 못한다는 점을 이용합니다.  

하지만 웹 스크레이퍼가 이미지를 텍스트로 인식해야 하는 분야는 CAPTCHA만이 아닙니다. 최근에는 문서를 그냥 스캔해서 업로드 하는 경우가 많습니다. 이런 문서는 인터넷이라는 관점에서 보기엔 접근이 불가능한 것이나 마찬가지입니다. 이미지를 텍스트로 인식하는 기능이 없다면 이들 문서에 접근할 수 있는 방법은 사람이 손으로 타이핑하는 것 뿐입니다.  

이미지를 텍스트로 바꾸는 작업을 **광학 문자 인식(OCR)** 이라고 합니다. OCR 기능이 있는 주요 라이브러리는 그리 많지 않지만, 이들을 지원하거나 이들을 기반으로 만들어진 라이브러리는 여러가지입니다.

## 11.1 라이브러리 개관

파이썬은 이미지 처리와 읽기, 이미지 기반 머신 러닝, 심지어 이미지 생성에도 매우 뛰어난 언어입니다. 이미지 처리에 사용할 수 있는 라이브러리는 다양하지만, 이번 챕터에서는 필로(pillow)와 테서랙트(tesseract) 두 가지만 사용합니다.

### 11.1.1 필로

필로는 가장 많은 기능을 갖춘 이미지 처리 라이브러리는 아니지만, 파이썬으로 포토샵 같은 것을 만들거나 연구할 목적이 아닌 이상 필로정도면 충분합니다. 문서화도 잘 되어 있고, 사용하기도 쉽습니다.  

설치는 pip를 통해 하면 됩니다.

```
pip install pillow
```

필로는 파이썬 2.x용 파이썬 이미지 라이브러리인 PIL에서 갈려져 나와 파이썬 3.x 지원을 추가했습니다. PIL과 마찬가지로, 필로도 쉽게 이미지를 불러오고 조작하고, 다양한 필터와 마스크, 픽셀 단위 변형도 가능합니다.


```python
from PIL import Image, ImageFilter

kitten = Image.open("kitten.jpg")
blurryKitten = kitten.filter(ImageFilter.GaussianBlur)
blurryKitten.save("kitten_blurred.jpg")
blurryKitten.show()
```

위 코드는 kitten.jpg 이미지에 블러 효과를 추가해 기본 이미지 뷰어에서 열고, 동시에 kitten_blurred.jpg 라는 이름으로 저장합니다.  

필로는 이런 단순한 기능 외에도 많은 기능이 있습니다. 자세한 정보는 [문서](http://pillow.readthedocs.io/en/4.2.x/){:target="`_`blank"}를 참고합니다.

### 11.1.2 테서랙트

테서랙트는 OCR 라이브러리입니다. 테서랙트는 OCR과 머신 런닝으로 유명한 구글의 투자를 받고 있는데, 가장 정확한 최고의 오픈 소스 OCR 시스템으로 널리 인정받고 있습니다.  

테서랙트는 정확할 뿐 아니라 굉장히 유연합니다. 테서랙트는 폰트가 비교적 일관적이기만 하면, 숫자에 제한 없이 그 폰트를 인식하도록 훈련할 수 있으며, 유니코드 문자도 인식하도록 확장이 가능합니다.  

테서랙트는 import 문으로 불러오는 라이브러리가 아니라 파이썬으로 작성된 CLT(command line tool)입니다. 설치를 마치면 반드시 파이썬 명령행 외부에서 tesseract 명령어로 실행해야 합니다.

#### 테서랙트 설치

설치는 홈브류로 설치하면 됩니다.

```
brew install tesseract
```

테서랙트를 훈련시키는 것 같은 일부 기능은 데이터 파일(.traineddata 확장자)이 필요하며, 데이터 파일은 테서랙트 설치 위치 아래 tessdata 디렉터리에 위치해야 합니다.
> 데이터 파일을 따로 내려받지 않았다면 https://github.com/tesseract-ocr/tessdata 에서 직접 내려 받아야 합니다.

환경에 따라 테서랙트 설치 위치를 지정하는 환경 변수 `$TESSDATA_PREFIX`를 설정해야 할 수도 있습니다. 필요하다면 대부분의 리눅스와 맥 OS X에서는 아래 명령을 이용하면 됩니다.

```
$export TESSDATA_PREFIX=/usr/local/share/
```

`/usr/local/share/`는 테서랙트의 기본 설치 위치입니다.

### 11.1.3 넘파이

단순한 OCR에서는 필요하지 않지만, 테서랙트가 사용할 다른 문자나 폰트도 인식하도록 훈련하려면 넘파이(NumPy)가 필요합니다. 넘파이는 선형 대수학이나 기타 대규모 수학 애플리케이션에 사용하는 매우 강력한 라이브러리입니다. 넘파이는 이미지를 수학적인 거대한 픽셀 배열로 표현하고 조작할 수 있는데, 테서랙트에서 이런 기능을 활용할 수 있습니다. 물론 여기에서는 거기까지 사용하지 않습니다.

넘파이도 pip로 설치하면 됩니다.

```
pip install numpy
```

## 11.2 형식이 일정한 텍스트 처리

텍스트사 형식이 일정하다고 하려면 다음의 조건을 갖추어야 합니다.

- 표준 폰트 하나로 작성되어야 한다. 손으로 쓴 글씨, 필기체, 지나치게 장식적인 폰트는 제외합니다.
- 복사하거나 사진을 찍었다면 행 구분이 명료해야 하며, 복사로 인한 열화 현상이나 심하게 어두워진 부분이 없어야 합니다.
- 수평으로 잘 정렬되어 있어야 하며, 기울어진 글자가 없어야 합니다.
- 텍스트가 이미지를 벗어나거나, 이미지 모서리에 잘려서는 안 됩니다.

이런 조건 중 일부는 전처리를 통해 해결할 수 있습니다. 예를 들어 이미지를 그레이스케일로 바꾸고, 밝기와 명암을 조절하고, 필요 없는 부분을 잘라내거나 회전할 수 있습니다. 하지만 근본적인 한계는 있습니다.

![]({{site.url}}/img/post/python/crawling/c11_2_1.png)
위 이미지는 형식이 일정한 텍스트의 이상적인 예입니다.  

테서랙트를 실행해 이 이미지 파일을 읽고 결과를 텍스트 파일로 저장한 다음, 해당 텍스트 파일을 화면에 출력하는 명령입니다.

```
$ tesseract text.tif textoutput && cat textoutput.txt
```

출력 결과는 테서랙트가 실행 중임을 알리는 한 줄과 새로 만든 textoutput.txt의 내용입니다.

```
This is some text, written in Arial, that will be read by
Tesseract. Here are some symbols: !@#$%"&‘()

Tesseract Open Source OCR Engine v3.05.01 with Leptonica
```

기호 일부가 잘못 인식되긴 했지만, 결과는 거의 정확합니다. 일반적으로 텍스트 인식에 만족할 수 있을 정도입니다.  

이미지 텍스트에 블로 효과를 적용하고 JPG 압축으로 인한 열화가 생기게 하고, 배경에 그레이디언트를 추가하면 결과는 훨씬 나빠집니다.

![]({{site.url}}/img/post/python/crawling/c11_2_2.png)
> 인터넷에서 만나는 대부분의 이미지는 이런 이미지일 가능성이 높습니다.

테서랙트는 이 이미지를 이전 이미지만큼 잘 처리하지 못합니다. 주된 이유는 배경의 그레디언트 때문입니다.

```
This Is some text, wrmen In Aﬂll, ..
Tesseract Here are some symbdsz-

Tesseract Open Source OCR Engine v3.05.01 with Leptonica
```

배경의 그레이디언트가 텍스트를 구별하기 어렵게 하는 지점에 다다르자 텍스트가 잘렸습니다. 각 행의 마지막 글자도 틀렸는데, 테서랙트는 이 글자를 인식하려 했지만, 실패했습니다. JPG 열화와 블러 효과도 테서랙트가 소문자 i와 대문자 I, 숫자 1을 구분하기 어렵게 만듭니다.  

파이썬 스크립트로 이미지를 깔끔하게 만들면 도움이 됩니다. 필로 라이브러리로 임계점(threshold) 필터를 만들어 배경의 회색을 제거해서 텍스트가 잘 드러나게 하면 테서랙트가 이미지를 인식하기 쉬워집니다.

```python
from PIL import Image
import subprocess

def cleanFile(filePath, newFilePath):
    image = Image.open(filePath)

    # 회색 임계점을 설정하고 이미지를 저장합니다.
    image = image.point(lambda x: 0 if x<143 else 255)
    image.save(newFilePath)

    # 새로 만든 이미지를 테서랙트로 읽습니다.
    subprocess.call(["tesseract", newFilePath, "output"])

    # 결과 텍스트 파일을 열어 읽습니다.
    outputFile = open("output.txt", 'r')
    print(outputFile.read())
    outputFile.close()

cleanFile("text_2.tif", "text_2_clean.png")
```
자동으로 생성된 결과 이미지 `text_2_clean.png`입니다.

![]({{site.url}}/img/post/python/crawling/c11_2_1_text_2_clean.png)

문장부호 일부가 사라지거나 읽기 어렵게 되었지만, 텍스트는 최소한 사람의 눈으로 읽을 수 있는 수준입니다. 테서랙트 역시 훨씬 나은 결과를 보입니다.

```
This Is some text. written In Anal, that will be read
Tesselact Here are some symbols: !@#$%"&'0
```

마침표와 쉼표는 아주 작아서 이렇게 이미지를 이리저리 변형하다보면 사람에게나 테서랙트에게는 안보이게 됩니다. Arial를 Anal로 잘못 인식하기도 했는데, 그런 r,i를 n 한 글자로 인식했기 때문입니다.  

그래도 텍스트의 거의 반이 날아간 이전 버전보다는 개선되었습니다.  
테서랙트의 가장 큰 약점은 밝기가 일정치 않은 배경입니다. 테서랙트의 알고리즘은 텍스트를 읽기 전에 자동으로 명암을 조절하려 시도하지만, 필로 라이브러리 같은 도구로 직접 처리하는 것이 더 나은 결과를 보여줍니다.  
기울어진 이미지나 텍스트가 없는 영역이 넓은 이미지, 기타 다른 문제를 가진 이미지는 테서랙트로 읽기 전에 먼저 조정하는 것이 좋습니다.

### 11.2.1 웹사이트 이미지에서 텍스트 스크레이핑하기

웹 스크레이퍼와 테서랙트의 조합은 강력한 도구가 됩니다. 텍스트를 이미지로 만들어서 알아보기 어렵게 되는 경우도 있지만, 고의적으로 텍스트를 숨기기 위해 이미지를 쓰는 경우도 있습니다.  

아마존의 robots.txt 파일은 사이트의 상품 페이지 스크레이핑을 허용하긴 하지만, 책 미리보기를 스크랩하는 봇은 많지 않습니다. 이는 아마존이 미리보기를 사용자 행동에 반응하는 Ajax 스크립트로 불러오며 실제 몇 겹의 div 아래 깊게 숨겨져 있기 때문입니다. 사실 이런 미리보기는 이미지 파일보다는 플래시로 만든 것으로 보일 겁니다. 게다가 이미지에 접근한다 하더라도 그걸 텍스트로 읽는 건 쉽지 않습니다.  

다음 스크립트는 아마존에 있는 <이상한 나라의 앨리스> 큰 활자판으로 이동한 다음, 미리보기를 열고, 이미지 URL을 수집하고, 이미지를 내려받아 읽은 다음 그 텍스트를 출력합니다.
> 테서랙트는 텍스트를 인식할 때 활자가 큰 이미지를 더 잘 인식합니다.

```python
import time
from urllib.request import urlretrieve
import subprocess
from selenium import webdriver

# 셀레니움 드라이버를 만듭니다.
# driver = webdriver.PhantomJS()
# 가끔 펜텀JS가 이 페이지에 있는 요소를 찾아내지 못할 때가 있습니다.
# 그럴 경우 크롬드라이버를 사용하세요.
driver = webdriver.Chrome()


driver.get("https://www.amazon.com/Alice-Wonderland-Large-Lewis-Carroll/dp/145155558X")
time.sleep(2)

# 책 미리보기 버튼을 클릭합니다.
driver.find_element_by_id("sitbLogoImg").click()
imageList = set()

# 페이지 로드를 기다립니다.
time.sleep(5)

# 오른쪽 화살표를 클릭할 수 있으면 계속 클릭해서 페이지를 넘깁니다.
while "pointer" in driver.find_element_by_id("sitbReaderRightPageTurner").get_attribute("style"):
    driver.find_element_by_id("sitbReaderRightPageTurner").click()
    time.sleep(2)
    # 새로 불러온 페이지를 가져옵니다. 한 번에 여러 페이지를 불러올 때도 있지만,
    # 세트에는 중복된 요소는 들어가지는 않습니다.
    pages = driver.find_elements_by_xpath("//div[@class='pageImage']/div/img")
    for page in pages:
        image = page.get_attribute("src")
        imageList.add(image)

driver.quit()
# 수집된 이미지를 테서랙트로 처리합니다.
i = 0
for image in sorted(imageList):
    urlretrieve(image, "page" + str(i) + ".jpg")
    p = subprocess.Popen(["tesseract", "page" + str(i) + ".jpg", "page" + str(i)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    f = open("page" + str(i) + ".txt", "r", encoding="utf-8")
    print(f.read())
    i += 1
```

테서랙트는 책에 실린 긴 문장들을 거의 완벽하게 인식합니다.  
다음은 1페이지의 미리보기 결과입니다.

```
Alice was beginning to get very tired

of sitting by her sister on the bank, and of
having nothing to do. Once or twice she
had peeped into the book her sister was
reading, but it had no pictures or
conversations in it, "and what is the use of
a book," thought Alice. "without pictures
or conversations?"

So she was considering in her own mind
(as well as she could, for the day made
her feel very sleepy and stupid), whether
the pleasure of making a daisy-chain
would be worth the trouble of getting up
and picking the daisies, when suddenly a
White Rabbit with pink eyes ran close by
her.
```

하지만 책의 앞표지나 뒤표지처럼 배경에 색깔이 들어가 있으면 인식률이 떨어집니다.

```
A’lice in Wanderland

In that direction”, the cat said, waving the right paw ’round,
”llves a Hatter, and In (hat diredvon,”wavmg the other paw,
”llves a March Hare V1516 elfher you 11kg, (hey’re bath mad.”

But I don’( want to go among mad people ”, Alxce Rcmarked.
```

물론 필로 라이브러리를 써서 필요한 이미지를 수정할 수 있지만, 자동화한 설계치고는 비효율적입니다.  

다음 섹션에서는 심하게 훼손된 텍스트에 대처하는 방법을 다룹니다. 이 방법은 테서랙트를 훈련시킬 시간이 없을 때 유용합니다. 테서랙트에 텍스트 이미지를 많이 입력하고 그 원본 텍스트도 함께 입력하면 테서랙트는 나중에 같은 폰트를 훨씬 정확히 인식할 수 있습니다. 배경이 끼어들거나 위치에 문제가 있어도 가능합니다.

## 11.3 CAPTCHA 읽기와 테서랙트 훈련

CAPTCHA는 컴퓨터와 사람을 구별하기 위한 완전히 자동화한 테스트(Completely Automated Public Turing test to tell Computers and Humans Apart)의 약자입니다.

튜링 테스트는 앨런 튜링이 1950년에 발표한 논문 <Computing Machinery and Intelligence>에 처음 등장합니다. 이 논문에서 앨런은 컴퓨터 터미널을 통해 사람이 사람이나 인공지능 프로그램 모두와 소통하는 방법을 설명합니다. 일상적인 대화를 하던 사람이 대화 상대가 사람인지 AI 프로그램인지 구별하지 못했다면 AI 프로그램은 튜링 테스트를 통과한 것으로 간주하는데, 튜링은 이 테스트를 통과한 인공지능이 이유와 목적을 가지고 '생각'한다고 판단합니다.  

구글의 reCAPTCHA는 어렵기로 악명 높습니다. 현재 보안을 중요시하는 웹사이트에서 가장 널리 쓰이는 이 프로그램은 봇 뿐만 아니라 사람 조차도 4명중 한명 꼴로 사이트 접근을 막고 있습니다.  

PHP 기반 콘텐츠 관리 시스템(CMS)으로 널리 쓰이는 드루팔(Drupal)에도 CAPTCHA 모듈이 들어있습니다. 드루팔의 CAPTCHA 모둘은 다양한 난이도로 CAPTCHA 이미지를 생성할 수 있습니다.

![]({{site.url}}/img/post/python/crawling/c11_2_2.png)

이 CAPTCHA가 다른 CAPTCHA에 비해 사람이나 컴퓨터가 알기 쉬운 이유는 무엇일까요?

- 겹친 글자가 없고, 다른 글자의 영역을 침범하지도 않았습니다. 즉, 각 글자 주위에 다른 글자를 침범하지 않는 사각형을 그릴 수 있습니다.
- 배경 이미지나 줄, 기타 OCR 프로그램을 혼란시킬 방해물이 없습니다.
- 이 이미지만으로 분명히 알 수는 없지만, CAPTCHA가 사용하는 폰트에는 몇 가지 변형이 있습니다. 4, M 에는 깔끔한 산세리프 폰트를 썼고, "m.", "C,", "3"에는 필기체 스타일의 폰트를 썼습니다.
- 흰 배경과 어두운 색깔의 글자가 잘 구별됩니다.

하지만 이 CAPTCHA에는 OCR 프로그램이 읽기 어렵게 만드는 함정이 약간 섞여 있습니다.

- 글자와 숫자가 섞여 있어서 경우의 수가 늘어납니다.
- 무작위로 기울어진 글자들은 OCR 소프트웨어를 혼란시킬 수 있지만 사람이 읽는 데는 문제가 없습니다.
- 비교적 이상하게 생긴 필기체 폰트가 인식을 어렵게 합니다. Z에는 추가된 획이 있고, 소문자 m 은 문자가 너무 작아서 컴퓨터가 읽으려면 훈련이 더 필요합니다.

다음 명령으로 테서랙트가 이 이미지를 읽게 해봅시다.

```
$ tesseract captchaExample.tiff output
```

output.txt 파일을 보면 다음과 같습니다.

```
92353
```
테서랙트는 9와 3은 잘 인식하지만, CAPTCHA를 제대로 인식하려면 아직 갈 길이 멈니다.


### 11.3.1 테서랙트 훈련

## 11.2 CAPTCHA 가져오기와 답 보내기
