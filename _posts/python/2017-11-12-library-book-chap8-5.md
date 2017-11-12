---
layout: post
section-type: post
title: Python Library - chap 8. 특정 데이터 포맷 다루기 - 5. Excel 다루기
category: python
tags: [ 'python' ]
---

`openpyxl`은 Excel 파일의 읽기나 쓰기 등을 실행하는 기능을 제공합니다. Office 2007 이후의 xlsx/xlsm/xltx/xltm 포맷을 지원합니다. 셀 값 읽어오기, 셀 병합, 차트 삽입 등 Excel의 일반적인 조작을 Python 코드로 처리할 수 있습니다.

## openpyxl 설치

```
$ pip install openpyxl
```

## 엑셀 파일 읽어오기

### sample.xlsx

품목 | 재고
---|---
사과 | 2
귤 | 5
딸기 | 1
합계 | =SUM(표1[재고])

### 엑셀 파일 읽어오기와 셀 값 얻기

```python
>>> import openpyxl
>>> wb = openpyxl.load_workbook('sample.xlsx')
>>> wb.get_sheet_names()
['Sheet1', 'Sheet2']
>>> ws = wb.get_sheet_by_name('Sheet1')
>>> ws.max_column
2
>>> ws.max_row
5
>>> ws['A4'].value
'딸기'
>>> a2 = ws['A4']
>>> a2.value
'딸기'
>>> a2 = ws['A2']
>>> a2.value
'사과'

>>> a2 = ws.cell('A2')  # cell의 좌표 사용은 권장되지 않는다.
>>> a2.value

>>> a3 = ws.cell(row=3, column=1)
>>> a3.value
'귤'
>>> b5 = ws['B5']
>>> b5.value
'=SUM(B2:B4)'
```

### openpyxl.load_workbook()

형식 | openpyxl.load_workbook(filename, read_only=False, use_iterators=False, keep_vba=False, guess_type=False, data_only=False)
---|---
설명 | 엑셀 파일을 읽어온다.
인수 | filename - 읽어올 대상 엑셀 파일의 경로를 지정한다. <br> read_only - True를 지정하면 읽기 전용으로 읽어온다. 편집은 불가능하다. <br> data_only - True를 지정하면, 셀 값이 식일 때 계산 결과를 얻는다.
반환값 | Workbook 객체

앞의 예에서 load_workbook() 메서드의 data_only를 기본값 False로 실행했기 때문에 SUM 함수를 사용한 식 "=SUM(B2:B4)"를 얻었습니다. data_only를 True로 지정해 실행하면 SUM 함수의 계산 결과인 8이 값으로 얻어집니다.

### get_sheet_names()

형식 | get_sheet_names()
---|---
설명 | 읽어온 엑셀 파일 안의 시트 이름 리스트를 얻는다.
반환값 | 시트 이름 리스트

### get_sheet_by_name)_

형식 | get_sheet_by_name(name)
---|---
설명 | 엑셀 시트를 이름으로 지정하여 얻는다.
인수 | name - 시트를 지정한다.
반환값 | Workbook 객체

### cell()

형식 | cell(coordinate=None, row=None, column=None, value=None)
---|---
설명 | 셀 값을 얻는다.
인수 | coordinate - 셀을 A1,B2 등의 A1 참조 형식으로 지정한다. <br> row - 셀의 행 수를 지정한다. column과 함께 사용한다. 1행이 row=1 <br> column - 셀의 열 수를 지정한다. row와 함께 사용한다. 1열이 column=1

cell() 메서드는 셀 값을 얻을때 사용합니다. coordinate 또는 row와 column 한쌍을 지정하여 셀을 지정합니다. coordinate에 'A2'를 지정할 때와 row=2, column=1을 지정한 결과가 같습니다. row와 column을 사용할 때는 각각 맨 처음 행과 열이 ()이 아닌 1이라는 것에 주의해야 합니다.

### 셀 값을 순서대로 얻기

```python
import openpyxl
wb = openpyxl.load_workbook('sample.xlsx', data_only=True)
ws = wb.get_active_sheet()

print('A1 -> A2 -> ... B1 -> B2의 순서로 값을 얻습니다. \n--------')

for row in ws.rows:
   for cell in row:
       print(cell.value)

print('\nA1 -> B1 -> A2 -> 의 순서로 값을 얻습니다. \n---------')

for column in ws.columns:
    for cell in column:
          print(cell.value)
```

## "셀 값을 순서대로 얻기"의 실행 결과

```
A1 -> A2 -> ... B1 -> B2의 순서로 값을 얻습니다.
--------
품목
재고
사과
2
귤
5
딸기
1
합계
8

A1 -> B1 -> A2 -> 의 순서로 값을 얻습니다.
---------
품목
사과
귤
딸기
합계
재고
2
5
1
8
```

## 엑셀 파일 쓰기

```python
import openpyxl
wb = openpyxl.Workbook()

ws = wb.create_sheet(index=0, title='New Sheet')
ws['A1'] = 100

wb.save(filename='new_book.xlsx')
```

현재 디렉터리에 new_book.xlsx 가 저장됩니다.

### create_sheet()

형식 | create_sheet(index=None, title=None)
---|---
설명 | 엑셀 파일 시트를 삽입한다.
인수 | index - 시트를 삽입할 위치를 지정한다. 0을 지정하면 가장 왼쪽에 삽입된다. <br> title - 시트 이름을 지정한다.
반환값 | Worksheet 객체

### save()

형식 | save(filename)
---|---
설명 | 엑셀 파일을 저장한다.
인수 | filename - 저장하는 엑셀 파일 경로를 지정한다.
반환값 | 없음

### 치트 삽입하기

```python
import openpyxl
import random
from openpyxl.charts import Reference, Series, LineChart
from openpyxl.chart

wb = openpyxl.Workbook()
ws = wb.active

for i in range(10):
    ws.append([random.randint(1, 10)])

values = Reference(ws, min_row=1, min_col=1, max_row=10, max_col=1)
series = Series(values, title="Sample Chart")
chart = LineChart()
chart.append(series)
ws.add_chart(chart)

wb.save("sample_cahrt.xlsx")
```

위 코드를 실행하면 sample_cahrt.xlsx가 출력되며 시트 "Sheet"에 다음과 같은 꺽은 선 차트가 삽입됩니다.

![]({{site.url}}/img/post/python/library/8.5.png)

> ### Python과 Excel  
엑셀 데이터를 파이썬에서 다루는 패키지는 openpyxl 이외에도 여러 가지가 있습니다. office 2007보다 오래된 .xls 포맷을 지원하는 xlrd와  xlwt느 예전에 많이 사용했습니다. 데이터 분석용 패키지 pandas에도 엑셀 데이터를 읽어오는 기능이 탑재되어 있습니다. 엑셀 데이터 쓰기에 특화된 xlsxwriter, VBA를 대체하기 위한 강력한 기능의 xlwings 등이 있습니다.  
엑셀 조작 자동화나 효율화에 종종 VBA를 사용하는데, VBA는 용도가 한정되어 있습니다. 특히 엑셀의 처리만으로는 부족한 공정 자동화에 범용 프로그래밍 언어인 파이썬을 도입하는 것은 바람직한 시도입니다.
