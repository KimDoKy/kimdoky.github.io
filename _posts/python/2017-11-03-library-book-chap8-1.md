---
layout: post
section-type: post
title: Python Library - chap 8. 특정 데이터 포맷 다루기 - 1. CSV 파일 다루기
category: python
tags: [ 'python' ]
---

>
소프트웨어 개발에서는 CSV, TSV 파일 등의 특정 포맷을 따르는 데이터를 다루는 경우가 있습니다. 이번 챕터에서는 CSV외에도 YAML이나 JSON 등 일반적으로 널리 사용하는 포맷을 Python으로 다룹니다. 또한 Excel 파일이나 JPEG, PNG 등의 이미지 데이터를 다루는 패키지도 다룹니다.

---

# CSV 파일 다루기

`csv` 모듈은 CSV나 TSV 포맷의 파일을 다루는 기능을 제공합니다. csv 모듈을 이용하면 파일을 쉽게 읽고 쓸 수 있습니다.

## CSV 파일의 읽기와 쓰기

실습할 샘플 파일입니다.

### sample.csv

```csv
"id","경기도","인구(명)","면적(km2)"
"1","서울시","13000000","2103.97"
"2","인천","900000","2416.05"
"3","일산","6200000","5081.93"
"4","수원","7200000","3767.92"
```

sample.csv를 불러와 내용을 print합니다.

### CSV 파일 읽어오기

```python
import csv

with open('sample.csv', mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

`reader()` 함수는 반복 가능한(iterable) reader 객체를 반환합니다. for 문으로 한 행씩 처리합니다.

### "CSV 파일 읽어오기" 실행 결과

```
['id', '경기도', '인구(명)', '면적(km2)']
['1', '서울시', '13000000', '2103.97']
['2', '인천', '900000', '2416.05']
['3', '일산', '6200000', '5081.93']
['4', '수원', '7200000', '3767.92']
```

CSV 파일의 한 행이 하나의 리스트형으로, 각 데이터가 리스트 요소로 취급됩니다.

### csv.reader() 함수

형식 | csv.reader(csvfile, dialect='excel', \**fmtparams)
---|---
설명 | CSV 파일 각 행의 데이터를 반복 처리하는 reader 객체를 반환한다.
인수 | csvfile - 반복자 프로토코를 지원하는 객체를 지정한다. <br> dialect - 서식화 매개변수의 집합 이름
반환값 | reader 객체

csvfile는 파일 객체를 지정할 수 있습니다.  

dialect는 자주 사용하는 서식화 매개변수의 집합을 지정할 수 있습니다. 서식화 매개변수란, 구분 문자나 종단 기호를 가리킵니다. dialect는 excel(Excel로 출력되는 CSV 파일), excel-tab(TSV 파일), unix(종단 기호를 '\n'으로 하는 파일) 중에서 선택합니다.  

서식화 매개변수는 dialect를 지정하는 것 외에 개별적으로 지정할 수도 있습니다. 특히 자주 쓰는 것은 `delimiter`와 `quotechar`입니다. `delimiter`는 구분 문자를 지정합니다. 기본 값은 쉽표(`.`)입니다. 쉼표 대신 탭이나 파이프를 지정하면 쉼표 이외의 다른 구분 문자를 사용하는 포맷을 지원할 수 있습니다. `quotechar`는 인용 부호를 지정합니다. 기본값은 큰 따옴표(`"`)입니다.

### 구분 문자와 인용 부호 지정

```
# TSV  파일 읽어오기
reader1 = csv.reader('sample.tsv', delimiter='\t')

# 인용 부호를 "#"으로 지정하여 읽어오기
reader2 = csv.reader('sample.tsv', delimiter='\t', quotechar='#')
```

### 파일 읽기와 가공, 출력
CSV 파일을 읽어와서 간단히 가공하여 TSV 파일로 출력합니다.

```python
import csv

with open('sample.csv', mode='r', encoding='utf-8') as read_file:
    reader = csv.reader(read_file)
    next(reader)

    with open('result.tsv', mode='w', encoding='utf-8') as write_file:
        writer = csv.writer(write_file, delimiter='\t')
        writer.writerow(['경기도','인구 밀도(명/km2)'])

        for row in reader:
            population_density = float(row[2]) / float(row[3])
            writer.writerow([row[1], int(population_density)])
```

result.tsv가 출력됩니다.

### result.tsv

```tsv
경기도	인구 밀도(명/km2)
서울시	6178
인천	372
일산	1220
수원	1910
```

### csv.writer() 함수

형식 | csv.writer(file, dialect='excel', \**fmtparams)
---|---
설명 | CSV 파일의 데이터를 구분 문자로 구분된 문자열을 변환하여 출력하기 위한 writer 객체를 반환한다.
인수 | file - 쓰기 대상 파일 객체 <br> dialect - 서식화 매개변수의 집합 이름
반환값 | writer 객체

### csv.writer.writerow() 함수

형식 | csv.writer.writerow(row)
---|---
설명 | 데이터를 서식화하여 writer 파일 객체에 쓴다.
인수 | row - 문자열 또는 수치 시퀀스

CSV 파일(또는 지정한 delimiter에 의한 구분 파일)을 출력하면 csv.writer.writerow() 메서드를 사용합니다. 샘플 코드에 나와 있듯이, for문 안에서 요소의 수치나 문자열을 가공하여 출력할 수 있습니다.

## CSV 파일 헤더를 이용한 편리한 읽어오기

csv.reader()를 이용하여 파일을 읽어오면 각 행의 데이터는 리스트 객체로 취급됩니다. 파일 열(column) 수가 많으면 리스트 요소 수도 커지기 때문에, 코드 상에서 어떤 열을 다루고 있는지 판별하기 어려워집니다. 취급한 열만을 알기 쉽게 이름을 붙인 변수로 저장하는 방법도 있지만, 열 수가 많으면 힘든건 마찬가지입니다.  

`DictReader()`는 헤더 행을 dict의 키로, 각 행의 값을 dict의 값으로 취급할 수 있는 편리한 클래스입니다.

### DictReader()를 이용한 읽어오기

```python
import csv

with open('sample.csv', mode='r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        print(row)
```

### DictReader()의 출력 결과

```
{'인구(명)': '13000000', '면적(km2)': '2103.97', '경기도': '서울시', 'id': '1'}
{'인구(명)': '900000', '면적(km2)': '2416.05', '경기도': '인천', 'id': '2'}
{'인구(명)': '6200000', '면적(km2)': '5081.93', '경기도': '일산', 'id': '3'}
{'인구(명)': '7200000', '면적(km2)': '3767.92', '경기도': '수원', 'id': '4'}
```

읽어온 파일의 각 행이 dict 형으로 출력됩니다.  

DictReader()를 사용해 `population_density`를 생성하는 코드를 변경해봅니다.

### DictReader()를 사용할 때의 열 선택

```python
# 원래 코드
# population_density = float(row[2]) / float(row[3])

# DictReader()를 사용할 때
population_density = float(row['인구(명)']) / float(row['면적(km2)'])
```

이렇게 하면 헤더 행 문자열을 이용할 수 있어 처리 내용이 더 명확해집니다.  

### csv.DictReader() 클래스

형식 | class csv.DictReader(csvfile, fieldnames=None, restkey=None, restval=None, dialect='excel', \*args, \**kwargs)
---|---
설명 | 데이터를 dict 형식으로 읽어온다.
인수 | csvfile - 반복자 프로토콜을 지원하는 객체를 지정한다. <br> fieldnames - dict의 키를 헤더 행으로부터 얻는 것이 아니라, 시퀀스로 지정한다. <br> restkey - fieldnames로 지정한 키의 숫자와 실제 읽어온 열 수가 일치하지 않을 때 dict의 키를 보간하기 위한 문자열을 지정한다. <br> restval - restkey와 만찬가지로 열 수가 일치하지 않을 때 dict의 값을 보간하기 위한 문자열을 지정한다. <br> dialect - 서식화 매개변수의 집합 이름
반환값 | reader 객체(키 포함)

> 보간? 보간이 뭔가?  
어떤 알고있는 두 데이터의 사잇값을 추정하고자 하는 것
