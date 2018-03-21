---
layout: post
section-type: post
title: Google Map Custom Image Marker
category: front
tags: [ 'front' ]
---

사진을 업로드하면 사진에서 GPS 정보를 추출하는 작업이 필요한 프로젝트를 진행하다가

그 GPS 정보를 구글맵으로 바로 보여주는 작업이 해보고 싶어서... 해봤습니다.

프론트단에서 해야할 작업이지만, Django Template으로 작업해 봤습니다.

우선 GPS 정보를 먼저 추출합니다.

```python
import piexif
from PIL import Image


def get_gps(photo):
    image = Image.open(photo)
    exif_dict = piexif.load(image.info['exif'])
    try:
        gps = exif_dict['GPS']
        latitude = (gps[2][0][0]) + (gps[2][1][0] / 60 + (gps[2][2][0]) / 360000)
        longitude = (gps[4][0][0]) + (gps[4][1][0] / 60 + (gps[4][2][0]) / 360000)
        return round(latitude, 4), round(longitude, 4)
    except KeyError:
        latitude = None
        longitude = None
        return latitude, longitude
```
> [BestShes](https://github.com/BestShes) 님이 작업해 주었습니다.


위의 코드를 통해 GPS 정보를 추출 후 Template에 적용합니다.

아래 코드의 주 요점은 다음과 같습니다.

- 구글맵 삽입하기
- 한 페이지에 여러 구글맵 삽입하기 : 한 페이지에 여러 구글맵을 여러개 넣기 위해 `map` 뒤에 id를 추가하여 각기 다른 이름으로 정의해주었습니다.
- 마커를 원하는 사진으로 교체하기 : `google.maps.MarkerImage`을 이용하면 됩니다. 여기서는 `IconImage` 라는 변수로 이미지를 정의합니다. 다른 방법들을 시도하여봤지만, 이 함수가 만족할 만한 결과를 보여주었습니다.(원하는 이미지, 원하는 사이즈, 등)

```html
<body>
<script async defer src="https://maps.googleapis.com/maps/api/js?key=API_KEY&callback=initMap">
</script>
<style>
{% for num in testmodel_list %}
    {% if num.lng == "1" %}
    {% else %}
    <!-- 구글맵을 여러개 삽입하기 위해 for문을 이용해서 각 instance의 id를 변수명에 추가하여 각기 다른 이름의 변수를 정의함 -->
    #map{{ num.id }} {
        height: 300px;
        width: 100%;
    }
    {% endif %}
{% endfor %}
</style>
<script>
    function initMap() {
        {% for gps in testmodel_list %}
        {% if gps.lng == "1" %}
        {% else %}
        <!-- Custom Image Marker -->
        var IconImage = new google.maps.MarkerImage(
                "{{ gps.photo.url }}",
                null,
                null,
                null,
                new google.maps.Size(100, 100));
        <!-- GPS 정보 -->
        var GPS{{ gps.id }} = {lat: {{ gps.lat }}, lng: {{ gps.lng }} };
        <!-- Google Map Setting -->
        var map{{ gps.id }} = new google.maps.Map(document.getElementById('map{{ gps.id }}'), {
            zoom: 18,
            center: GPS{{ gps.id }}
        });
        <!-- Marker Setting-->
        var marker{{ gps.id }} = new google.maps.Marker({   
            position: GPS{{ gps.id }},
            map: map{{ gps.id }},
            icon: IconImage,
        });
        {% endif %}
        {% endfor %}
    }
    </script>

{% for test in testmodel_list %}
    Create_at : {{ test.create_at }}<br>
    <!-- GPS 정보가 들어 있는지 여부를 확인하고 출력 / migrate 당시 GPS가 없는 이미지는 1을 기본값으로 처리함 -->
    {% if test.lng == "1" %}
        GPS : no gps<br>
    {% else %}
        GPS : {{ test.lng }}, {{ test.lat }}<br>
        <div id="map{{ test.id }}"></div>
    {% endif %}
    <!-- 마커에 표시된 사진이 원하는 이미지인지 확인하기 위해 이미지를 출력 -->
    {% if test.photo %}
        <img src='{{ test.photo.url }}' height='150' width='150'>
    {% endif %}
   <hr>
{% endfor %}
</body>
```

반드시 `<body>` 태그 안에 넣어주어야 합니다.
