---
layout: post
section-type: post
title: Google API - reverse geocoding
category: tip
tags: [ 'tip' ]
---

위도와 경도(lat, lng)를 가지고 Google Map Api를 이용하면 역으로 주소를 불러 올 수 있습니다.  

```python
import requests

def get_address(country, lat, lng, api_key):
    url = "https://maps.googleapis.com/maps/api/geocode/json?language=%s&latlng=%f,%f&key=%s" % (country, lat, lng, api_key)   
    r = requests.get(url).json()
    """
    new_full_adr : 신주소
    old_full_adr : 구주소
    """
    new_full_adr = r['results'][1]['formatted_address']
    old_full_adr = r['results'][0]['formatted_address']
    city = r['results'][1]['address_components'][-3]['long_name']
    local = r['results'][1]['address_components'][-2]['long_name']
    country = r['results'][1]['address_components'][-1]['long_name']
    return new_full_adr, old_full_adr, country, city, local
```

한국의 경우 신주소와 구주소로 나누어져 있어서 따로 변수에 저장하였습니다.

결과값을 앞에서부터 가져오면 IndexError가 발생하기 때문에 뒤에서부터 불러와야 에러를 피할 수 있습니다.

파라미터에  `language` 인자에 국가 코드를 넣어주면 해당 국가 언어로 주소를 반환해 줍니다.
