---
layout: post
section-type: post
title: Python - mongoDB 다루기
category: python
tags: [ 'python' ]
---

어떤 데이터셋이든 정규화가 가능하지만, 정규화에 드는 비용은 비싸다.  
특정한 데이터 타입(텍스트,이미지,음성,불규칙한 데이터구조 등)은 그 자체가 정규화를 거부한다.  
이러한 데이터를 SQL으로 강제로 맞추기 위해 잘라내거나 늘리면 안된다.  
이런 경우 NoSQL(문서 데이터베이스)를 사용할 수 있다.

NoSQL은 객체의 비휘발성 묶음으로, 보통 속성이 있는 문서이다.

MongoDB는 비관계형 데이터베이스이다. 하나의 MongoDB 서버는 서로 연결되지 않은 다양한 데이터베이스를 지원한다. 하나의 데이터베이스는 하나 이상의 문서 컬렉션으로 구성된다. 하나의 컬렉션에 있는 모든 문서에는 고유 구분자(unique identified)가 들어있다.  

파이썬의 MongoDB 클라이언트는 파이썬 모듈인 'pymongo'으로 구현되어 있고, `MongoClient` 클래스의 인스턴스이다. 파라미터 없이 클라이언트를 생성할 수 있고, 서버의 호스트, 포트번호를 지정하거나 서버의 URI를 파라미터로 설정할 수도 있다.

```python
In [1]: import pymongo as mongo
# 기본 클라이언트를 설정
In [2]: client1 = mongo.MongoClient()
# 호스트와 포트를 지정
In [3]: client2 = mongo.MongoClient('localhost',27017)
# URL로 호스트와 포트를 지정
In [4]: client3 = mongo.MongoClient('mongodb://localhost:27017/')
# 데이터베이스를 생성 혹은 지정
In [5]: db = client1.dsdb  # db = client1["dsdb"]
# collection을 생성 혹은 지정
In [6]: people = db.people  # people = db["people"]
# 파이썬의 딕셔너리로 MongoDB 문서를 표현
# 객체를 표현하는 딕셔너리는 반드시 _id 키를 가져야 함
# 키가 없다면 서버가 자동으로 생성
In [7]: person1 = {'empname':'John Smith', 'dob':'1957-12-24'}

In [8]: person2 = {'_id':'XVT162', 'empname':'Jane Doe', 'dob':'1964-05-16'}
# 컬렉션 객체는 컬렉션에 있는 문서를 입력,조회,삭제,업데이트,교체,집계하고 인덱스를 생성하는 함수들을 제공
# insert_one(doc)과 insert_many(docs)는 1개의 문서나 문서 리스트를 컬렉션에 입력
# InsertOneResult나 InsertManyResult 객체를 반환
# 각각 inserted_id, inserted_ids 속성을 제공
In [9]: person_id1 = people.insert_one(person1).inserted_id
# _id 필드가 생성 됨
In [10]: person_id1
Out[10]: ObjectId('5c040397b520d9da78f217ef')

In [11]: person1
Out[11]:
{'empname': 'John Smith',
'dob': '1957-12-24',
'_id': ObjectId('5c040397b520d9da78f217ef')}
#  _id를 지정했기 때문에 키를 자동으로 생성하지 않음
In [12]: person_id2 = people.insert_one(person2).inserted_id

In [13]: person_id2
Out[13]: 'XVT162'

In [14]: persons = [{'empname':'Abe Lincoln', 'dob':'1809-02-12'},
   ...: {'empname':'Anon I. Muss'}]

In [15]: result = people.insert_many(persons)

In [16]: result.inserted_ids
Out[16]: [ObjectId('5c04040fb520d9da78f217f0'), ObjectId('5c04040fb520d9da78f217f1')]
# find_one(), find()는 특정 조건에 부합하는 하나 이상의 문서를 찾을 때 사용
# find_one()는 문서를 반환, find()는 커서 제너레이터를 반환
# 이는 list()나 for 루프에서 이터레이터를 사용해서 리스트를 반환할 수 있음
# 딕셔너리를 파라미터로 전달하면 파라미터로 전달된 키 값과 일치하는 값을 지닌 문서를 반환
In [17]: everyone = people.find()

In [18]: list(everyone)
Out[18]:
[{'_id': ObjectId('5c040397b520d9da78f217ef'),
 'empname': 'John Smith',
 'dob': '1957-12-24'},
{'_id': 'XVT162', 'empname': 'Jane Doe', 'dob': '1964-05-16'},
{'_id': ObjectId('5c04040fb520d9da78f217f0'),
 'empname': 'Abe Lincoln',
 'dob': '1809-02-12'},
{'_id': ObjectId('5c04040fb520d9da78f217f1'), 'empname': 'Anon I. Muss'}]

In [19]: list(people.find({'dob':'1957-12-24'}))
Out[19]:
[{'_id': ObjectId('5c040397b520d9da78f217ef'),
 'empname': 'John Smith',
 'dob': '1957-12-24'}]

In [21]: people.find_one()
Out[21]:
{'_id': ObjectId('5c040397b520d9da78f217ef'),
'empname': 'John Smith',
'dob': '1957-12-24'}

In [22]: people.find_one({'empname':'Abe Lincoln'})
Out[22]:
{'_id': ObjectId('5c04040fb520d9da78f217f0'),
'empname': 'Abe Lincoln',
'dob': '1809-02-12'}

In [23]: people.find_one({'_id':'XVT162'})
Out[23]: {'_id': 'XVT162', 'empname': 'Jane Doe', 'dob': '1964-05-16'}

In [24]: people.count()
/usr/local/var/pyenv/versions/mysql/bin/ipython:1: DeprecationWarning: count is deprecated. Use estimated_document_count or count_documents instead. Please note that $where must be replaced by $expr, $near must be replaced by $geoWithin with $center, and $nearSphere must be replaced by $geoWithin with $centerSphere
 #!/usr/local/var/pyenv/versions/3.6.0/envs/mysql/bin/python
Out[24]: 4

In [25]: people.find({'dob':'1957-12-24'}).count()
/usr/local/var/pyenv/versions/mysql/bin/ipython:1: DeprecationWarning: count is deprecated. Use Collection.count_documents instead.
 #!/usr/local/var/pyenv/versions/3.6.0/envs/mysql/bin/python
Out[25]: 1

In [26]: people.find().sort('dob')
Out[26]: <pymongo.cursor.Cursor at 0x1100a3978>

In [27]: print(people.find().sort('dob'))
<pymongo.cursor.Cursor object at 0x11008b4e0>
# delete_one(doc), delete_many(docs)는 하나의 문서 혹은 컬렉션에서 특졍 조건을 만족하는 문서를 삭제
In [28]: result = people.delete_many({'dob':'1957-12-24'})

In [29]: result.deleted_count
Out[29]: 1
```

> 출처  
- [모두의 데이터과학 with 파이썬](https://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&ejkGb=KOR&barcode=9791160502152&orderClick=JAj)  
전체 내용은 위 서적에서 발췌하였으며, 미리보기로 제공되는 선까지만 다루었습니다. :)  

- [mongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
