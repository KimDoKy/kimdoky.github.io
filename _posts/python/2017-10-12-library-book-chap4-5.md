---
layout: post
section-type: post
title: Python Library - chap 4. 자료형과 알고리즘 - 4.5 약한 참조를 통한 객체 관리
category: python
tags: [ 'python' ]
---
객체의 약한 참조 기능을 제공하는 weakref에 대해 다룹니다.  

Python은 애플리케이션이 사용하는 객체의 참조 상황을 감시하고 있으며, 필요 없어진 객체를 자동으로 해제합니다. 변수나 리스트 요소로서 참조된 객체는 필요한 객체이지만, 전혀 참조를 하지 않게 되면 객체는 필요 없어진 것으로 판단되어 가비지 컬렉터에 의해 삭제됩니다.  

반면 외부에서 참조 중인 경우라도 참조된 객체를 필요 없는 것으로 판단하여 해제할 수 있는 참조 방식도 존재합니다 이와 같은 참조는 "약한 참조(Weak reference)"라고 합니다. 약한 참조에 의한 참조가 존재하더라도 일반 참조가 없는 객체는 가비지 컬렉터가 삭제합니다.

## 약한 참조로 파일 내용 캐시 생성하기
같은 파일에서 불러온 내용을 각각 별도의 메모리에 저장하지 않고 공유하는 방법을 생각해봅니다. 약한 참조를 사용하지 않을 때는 다음과 같이 작성합니다.

### 파일 내용 공유하기

```python
>>> _files = {}
>>> def share_file(filename):
...     if filename not in _file:
...         ret = _files[filename] = open(filename)
...     else:
...         ret = _files[filename]
...     return ret
```

share_file()은 지정한 파일 내용이 \_files에 등록된 것이면 그 내용을 반환하고, 등록되지 않았으면 파일을 열어 \_files에 등록하고 나서 그 내용을 반환합나다.  

이러한 share_file()에서는 한 번 dict에 등록한 내용은 삭제되지 않습니다. 따라서 많은 파일을 불러오는 애플리케이션을 사용하면 필요 없는 데이터로 메모리를 소모하게 됩니다.  

다음 예는 같은 처리에 약한 참조를 사용한 것입니다.

### 약한 참조를 사용하여 파일 내용 공유하기

```python
>>> import weakref
>>> _files = weakref.WeakValueDictionary()
>>> def share_file(filename):
...     if filename not in _files:
...         ret = _files[filename] = open(filename)
...     else:
...         ret = _files[filename]
...     return ret
```

share_file()의 처리 내용은 변함 없지만, 파일을 저장하는 dict으로 weakref.WeakValueDictionary를 사용하고 있습니다.  

weakref.WeakValueDictionary는 일반 dict와 마찬가지로 키와 값 한 쌍으로 저장하는 매핑 객체이지만, 값을 참조가 아닌 약한 참조로 저장합니다. weakref.WeakValueDictionary에 등록된 요소의 값이 일반 참조를 모두 잃어버리게 되면 가비지 컬렉터에 의해 회수되며, weakref.WeakValueDictionary는 해당하는 키와 값 항목을 삭제합니다.  

이 예에서 읽어온 파일은 약한 참조를 사용한 dict에 등록되어 있습니다. 따라서 파일이 다른 처리에 사용되는 동안은 dict의 요소가 계속 저장된 채로 유지되며, 이때에 다시 한번 같은 파일 이름이 호출되더라고 새로운 파일을 불러오지 않고 캐시한 내용을 반환합니다.  

모든 처리에서 이 파일이 쓸모없어지면 그때 \_files로부터 요소가 삭제되며 불필요한 메모리도 자동으로 삭제됩니다.

### WeakValueDictionary 클래스

형식 | class weakref.WeakValueDictionary([dict])
---|---
인수 | dict - dict를 지정하면 그 키와 값을 초깃값으로 등록한다.
반환값 | WeakValueDictionary 객체

weakref.WeakValueDictionary는 dict 값이 아닌 키를 약한 참조로 유지합니다. 키의 객체가 삭제되면 자동으로 해당 키와 값 항목이 삭제됩니다.

### WeakKeyDictionary 클래스

형식 | class weakref.WeakKeyDictionary([dict])
---|---
인수 | dict - dict를 지정하면 그 키와 값을 초깃값으로 등록한다.
반환값 | WeakKeyDictionary 객체
