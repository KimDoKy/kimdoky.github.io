---
layout: post
section-type: post
title: Python Library - chap 8. 특정 데이터 포맷 다루기 - 6. 이미지 다루기
category: python
tags: [ 'python' ]
---

`Pillow`는 이미지 데이터(JPEG, PNG 등)를 다루는 기능을 제공합니다. Pillow를 이용하면 이미지 축소, 확대, 색조 변경 등 다양한 이미지 편집이 가능합니다.  

PIL(Python Imaging Library)라는 패키지는 2009년 기준으로 개발이 중단되었습니다. 뜻이 있는 개발자들이 PIL을 Fork하여 Pillow라는 패키지 이름으로 배포하였고, 현재도 활발히 개발되고 있습니다.

## Pillow 설치

```
$ pip install pillow
```

Pillow를 import할 때는 "import PIL"이라고 합니다. Pillow는 PIL의 Fork 프로젝트이므로, 소스 코드의 호환성 유지를 위해 이 이름이 채택되었습니다.  

또한 Pillow는 libjpeg나 zlib 등의 라이브러리에 따라 다릅니다. 필요한 라이브러리가 설치되어 있지 않으면, 예를 들어 JPEG 이미지를 다룰 때 "OSError: encoder jpeg not available"이라는 오류가 발생할 수 있습니다. 라이브러리 인식 상태는 pip 설치 맨 마지막에 표시됩니다.

## 이미지 크기 변경 및 회전

#### 편집 전 이미지

![]({{site.url}}/img/post/python/library/8.6_1.png)

### 이미지 크기 변경 및 회전

```python
from PIL import Image

# 이미지 불러오기
img = Image.open('sample1.png')

# 200px X 200px로 크기 변경
resized_img = img.resize((200,200))

# 시계방향으로 90도 회전
rotated_img = resized_img.rotate(90)


rotated_img.save('processed_sample1.jpg', quality=100)
```

#### 편집 후 이미지

![]({{site.url}}/img/post/python/library/8.6_2.jpg)

### 다양한 이미지 형식으로 저장하기

```python
rotated_img.save('processed_sample1.png', format='PNG', compress_level=1)

# 인수 format을 생략하면 파일 이름 확장자로 자동 판별한다.
rotated_img.save('processed_sample1.png', compress_level=1)
rotated_img.save('processed_sample1.gif')
rotated_img.save('processed_sample1.bmp')
```

### Image.open()

형식 | Image.open(file_path, mode='r')
---|---
설명 | 이미지 파이을 연다.
인수 | file_path - 이미지 파일 경로를 지정한다. <br> mode - 모드를 지정하면 인수지만, 'r' 이외는 사용할 수 없다.
반환값 | 이미지 객체

Image 모듈에는 신규 이미지를 생성하는 new()도 있지만, 실제로는 기존 이미지를 여는 open() 메서드를 사용하는 경우가 많습니다.

### Image.resize()

형식 | Image.resize(size, resample=0)
---|---
설명 | 이미지 크기를 변경한다.
인수 | size - 변경 후 크기(픽셀)를 (width, height) 튜플로 지정한다. <br> resample - 리샘플링 필터를 지정한다.
반환값 | 이미지 객체

resample에 지정할 수 있는 리샘플링 필터로는 PIL.Image.NEAREST(최근접법), PIL.Image.BILINEAR(바이리니어법), PIL.Image.BICUBIC(바이큐빅법), PIL.Image.LANCZOS(란초스법)가 있습니다. 일반적으로 란초스 또는 바이큐빅 리샘플링이 완성도가 좋은 것으로 알려져 있습니다. 처리 속도가 요구될 때는 비용 대시 효과가 좋은 바이리니어법도 좋습니다.

### Image.retate()

형식 | Image.rotate(angle, resample=0, expand=0)
---|---
설명 | 이미지를 회전한다.
인수 | angle - 시계방향으로 회전할 각도를 지정한다.
반환값 | 이미지 객체

resample의 사용법은 resize() 메서드와 같습니다.

### Image.save()

형식 | Image.save(file_path, format=None, \**params)
---|---
설명 | 이미지를 저장한다.
인수 | file_path - 이미지를 저장할 파일 경로를 지정한다. <br> format - 저장할 이미지 포맷을 지정한다. 생략하면 file_path 확장자로부터 자동으로 판별한다. <br> \**params - 이미지 포맷별로 다른 옵션을 지정하는 인수

format에는 JPEG, JPEG200, PNG, BMP 등을 지정할 수 있습니다. 이미지 포맷에 따라 \**params로 지정할 수 있는 옵션이 결정됩니다. JPEG의 경우 quality 값을 100보다 작게 하면 이미지 품질이 떨어지는 대신 압축률이 높아져 이미지의 크기를 줄일 수 있습니다. 프로그레시브 JPEG를 생성하는 옵션 progressive도 있습니다. PNG의 경우, 압축 레벨을 0~9 사이로 지정하는 compress_level과 투명도를 지정하는 transparency 등이 있습니다. 이미지 포맷별로 많은 옵션이 있습니다.

## 텍스트 넣기
이미지에 텍스트를 넣습니다.

```python
from PIL import Image, ImageDraw, ImageFont

img = Image.open('processed_sample1.jpg')
draw = ImageDraw.Draw(img)

# 폰트 종류와 크기를 지정
font = ImageFont.truetype('~/Library/Fonts/Anonymice Powerline Bold Italic.ttf', 22)

# 텍스트 넣기
draw.text((63, 7), 'Python!', font=font, fill='#000')

img.save('drew_text.png', format='PNG')
```

### 텍스트를 넣은 이미지

![]({{site.url}}/img/post/python/library/8.6_3.png)

"Python!"이 삽입되었습니다.

### ImageFont.truetype()

형식 | ImageFont.truetype(font=None, size=10, index=0, encoding='', filename=None)
---|---
설명 | TrueType 형식의 폰트를 읽어와 폰트 객체를 생성한다.
인수 | font - 폰트 파일을 지정한다. <br> size - 폰트 크기를 지정한다. <br> index - 지정한 폰트 파일에 여러 개의 폰트가 포함된 경우, ttc 번호를 지정한다. <br> filename - 사용하지 않음
반환값 | 폰트 객체

truetype() 메서드는 TrueType 형식 폰트르 읽어와 폰트 객체를 생성합니다. 인수 index에는 ttc 번호를 지정합니다. 예를 들어, msgothic.ttc에는 "MS 고딕"과 그 professional 폰트 "MS P 고딕"이 포함되어 있으며 ttc 번호는 각각 0, 1입니다.  

ImageFont 모듈에는 비트맵 형식의 폰트를 읽어오는 load() 메서드도 있었습니다. 한국어 텍스트를 삽입할 때는 한국어가 포함된 폰트를 지정해야 합니다.

### ImageDraw.Draw.text()

형식 | ImageDraw.Draw.text(xy, text, fill=None, font=None, anchor=None)
---|---
설명 | 이미지에 텍스트를 삽입한다.
인수 | xy - 텍스트를 삽입할 좌표(x,y)를 튜플로 지정한다. <br> text - 이미지에 삽입할 텍스트 <br> fill - 텍스트의 색상을 지정한다. <br> font - 폰트 객체를 지정한다.

텍스트 생상 지정 방법 예는 다음과 같습니다.

- RGB 16진수를 문자열로 지정 - fill='#FF0000'
- RGB 10진수를 튜플로 지정 - fill=(255, 0, 0)
- 색상 이름을 지정 - fill='red'
