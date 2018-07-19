---
layout: post
section-type: post
title: Introducing Python - chap8 - 연습문제
category: python
tags: [ 'python' ]
---

## 8.1 'This is a test of the emergency text system' 문자열을 test1 변수에 할당하라. 그리고 test1 변수를 test.txt 파일에 작성하라.

```Python
# 모범 답안
>>> test1 = "This is a test of the emergency text system"
>>> len(test1)
43

# open(), wirte(), close() 함수를 사용하여 파일을 작성
>>> outfile = open('test.txt', 'wt')
>>> outfile.write(test1)
43
>>> outfile.close()
# with 문 사용
>>> with open('test.txt', 'wt') as outfile:
...     outfile.write(test1)
43
```

## 8.2 test.txt 파일을 열어서 내용을 읽고, test2 문자열에 저장하라. test1과 test2의 값이 같은가?

```Python
>>> test2 = open('test.txt', 'rt')
>>> test1 == test2.read()
True
>>> test2.close()
```

```python
# 모범 답안
>>> with open('test.txt', 'rt') as infile:
...     test2 = infile.read()

>>> len(test2)
43
>>> test1 == test2
True
```

## 8.3 아래 텍스트를 books.csv 파일에 저장하라(필드는 콤마로 구분한다. 인용 부호 안에 콤마가 있을 때는 하나의 필드로 인식한다).

```
author,books
J R R Tolkien,The Hobbit
Lynne Truss,"Eats, Shoots & Leaves"
```

```Python
>>> text = '''author,books
J R R Tolkien,The Hobbit
Lynne Truss,"Eats, Shoots & Leaves"
'''

>>> with open('books.csv', 'wt') as outfile:
...     outfile.write(text)
```

## 8.4 csv 모듈의 DictReader 메서드를 사용하여 books.csv 파일을 읽고, books 변수에 저장하라. books 변수를 출력해보라. DictReader 메서드는 두 번째 책 제목에서 콤마와 인용 부호를 처리하는가?

```Python
# 모범 답안
>>> with open('books.csv', 'rt') as infile:
...     books = csv.DictReader(infile)
...     for book in books:
...         print(book)

OrderedDict([('author', 'J R R Tolkien'), ('books', 'The Hobbit')])
OrderedDict([('author', 'Lynne Truss'), ('books', 'Eats, Shoots & Leaves')])
```

## 8.5 아래 텍스트를 books.csv 파일로 저장하라.

```
title,author,year
The Weirdstone of Brisingamen,Alan Garner,1960
Perdido Street Station, China Mieville, 2000
Thud!,Terry Pratchett,2005
The Spellman Files,Lisa Lutz,2007
Small Gods,Terry Pratchett,1992
```

```Python
>>> text = '''
title,author,year
The Weirdstone of Brisingamen,Alan Garner,1960
Perdido Street Station, China Mieville, 2000
Thud!,Terry Pratchett,2005
The Spellman Files,Lisa Lutz,2007
Small Gods,Terry Pratchett,1992
'''

>>> with open('books.csv', 'wt') as infile:
...     infile.write(text)
```
## 8.6 sqlite3 모듈을 사용하여 books.db라는 이름의 SQLite 데이터베이스를 생성하라. 그리고 title(text), author(text), year(integer) 필드를 가진 books 테이블을 생성하라.

```Python
>>> import sqlite3
>>> db = sqlite3.connect('books.db')
>>> curs = db.cursor()
>>> curs.execute('''CREATE TABLE book (title text, author text, year int)''')
<sqlite3.Cursor at 0x10f17c730>
>>> db.commit()
```

## 8.7 books.csv를 읽고, 데이터를 book 테이블에 삽입하라.

```Python
>>> conn.hget('test', 'count')
>>> ins_str = 'insert into book values(?, ?, ?)'
>>> with open('books.csv', 'rt') as infile:
...     books = csv.DictReader(infile)
...     for book in books:
...         curs.execute(ins_str, (book[None][0], book[None][1], book[None][2]))
... #       curs.execute(ins_str, (book['title'], book['author'], book['year']))  // 작동안함
>>> db.commit()
```

## 8.8 book 테이블에서 알파벳순으로 title 열을 조회하여 결과를 출력하라.

```Python
>>> sql = 'select title from book order by title asc'
>>> for row in db.execute(sql):
...     print(row)
('Perdido Street Station',)
('Small Gods',)
('The Spellman Files',)
('The Weirdstone of Brisingamen',)
('Thud!',)
('title',)
# 튜플이 아닌 title 값만 출력
>>> for row in db.execute(sql):
...     print(row[0])
Perdido Street Station
Small Gods
The Spellman Files
The Weirdstone of Brisingamen
Thud!
title
```

## 8.9 book 테이블에서 발행일순(오름차순)으로 모든 열을 조회하여 결과를 출력하라.

```Python
>>> for row in db.execute('select * from book order by year'):
...     print(row)
('The Weirdstone of Brisingamen', 'Alan Garner', 1960)
('Small Gods', 'Terry Pratchett', 1992)
('Perdido Street Station', ' China Mieville', 2000)
('Thud!', 'Terry Pratchett', 2005)
('The Spellman Files', 'Lisa Lutz', 2007)
('title', 'author', 'year')
# 콤마와 스페이스로 구분하여 각 행의 필드를 출력
>>> for row in db.execute('select * from book order by year'):
...     print(*row, sep=', ')
The Weirdstone of Brisingamen, Alan Garner, 1960
Small Gods, Terry Pratchett, 1992
Perdido Street Station,  China Mieville, 2000
Thud!, Terry Pratchett, 2005
The Spellman Files, Lisa Lutz, 2007
title, author, year
```
## 8.10 sqlalchemy 모듈을 사용하여 연습문제 8.6에서 만든 books.db를 연결하라. 그리고 연습문제 8.8과 같이 book 테이블에서 title 열을 알파벳순으로 조회하여 결과를 출력하라.

```Python
>>> import sqlalchemy
>>> conn = sqlalchemy.create_engine('sqlite:///books.db')
>>> sql = 'select title from book order by title asc'
>>> rows = conn.execute(sql)
>>> for row in rows:
...     print(row)
('Perdido Street Station',)
('Small Gods',)
('The Spellman Files',)
('The Weirdstone of Brisingamen',)
('Thud!',)
('title',)
```

## 8.11 Redis 서버와 파이썬 redis 라이브러리(pip install redis)를 설치하라. count: 1과 name: 'Fester Bestertester' 필드(키:값)를 가진 test 해시를 생성하라.  test에 대한 모든 필드를 출력하라.

*콘솔에서 `redis-server`으로 redis 서버를 실행해야 함*

```Python
>>> import redis
>>> conn = redis.Redis()
>>> conn.delete('test')
0
>>> conn.hmset('test', {'count':1, 'name': 'Fester Bestertester'})
True
>>> conn.hgetall('test')
b'count': b'1', b'name': b'Fester Bestertester'}
```

## 8.12 test의 count 필드를 증가시키고, 출력하라.

```Python
>>> conn.hincrby('test', 'count', 3)
4
>>> conn.hget('test', 'count')
b'4'
```
