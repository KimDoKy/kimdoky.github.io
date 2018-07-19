---
layout: post
section-type: post
title: 삽질기 - 쇼핑몰 파일 통합하기
category: diary
tags: [ 'diary' ]
---

## 계기

현재 근무하는 회사에서는 여러 오픈마켓(쿠팡, 티몬, 위메프 등)에서 주문을 받고 있다.

현재 MD 자리가 비여 있어서, 매일 주문 마감 업무가 더해졌다.

문제는, 현재 회사에서 진행하는 오픈마켓의 갯수도 많고, 주문 파일(엑셀)안에 주문에 필요하지 않은 정보도 많아서 보기 힘들 뿐더러, 각 쇼핑몰마다 엑셀 양식이 모두 달라서 주문 취합에 너무 많은 시간이 소비 되었다.

그리하여, 언제 뽑힐 지 모를 MD 업무를 위해, 자동 주문 파일 취합 프로그램을 만들기로 하였다.

## 개발... 문제점

문제점은 역시 많은 파일과 각 파일들이 양식이 모두 다르다는 것이다. 즉, 자동화 작업을 해도 각 파일 별로 커스텀을 해야 하기 때문에 노가다성이 짙다. 방법이 없다.

## 각 쇼핑몰 파일 파싱하기
각 쇼핑몰에서 주문 파일을 다운 받는다. 파일들은 모두 엑셀 파일이다. 엑셀 파일 파이썬 라이브러리인 `openpyxl` 모듈을 사용하기로 했다. 하지만 파싱하면서 문제점이 발생하였다. `openpyxl` 모듈은 xls, csv 파일은 파싱하지 못한다. csv 파일이야 그렇다 쳐도 xls 파일까지... 사실 이 문제를 만나기 전까지 이런 확장자기 존재하는지도 몰랐다.

이 프로그램을 빨리 개발하여 바로 사용해야 하기 때문에, 각 쇼핑몰 파일을 .xlsx 파일로 수동 변환하기로 하였다. 확장자 문제는 부채가 되었다. (해당 부채는 미래의 내가 해결하겠지 뭐)

## 동적 변수 자동 생성하기
많은 파일들을 자동으로 모두 열어야 하기 때문에 각 쇼핑몰별로 다른 이름의 변수이름이 필요하였다. 하지만 어떻게 자동으로 변수이름이 각각 다르게 생성하지? 이 부분이 가장 삽질을 한 부분이다.  

우선 주문 파일들을 하나의 디렉토리에 모아둔다. 그리고 각 파일들을 쇼핑몰 구분을 위해 파일명을 각 쇼핑몰명으로 바꾼다. 그러고 파일들을 읽어와서 파일명으로 변수명을 설정한다.

```Python
import os
# 작업할 디렉터리를 지정
file_path = 'C:/Users/doky/Desktop/test/order'
# 해당 디렉터리로 작업 위치 변경
os.chdir(file_path)
# 폴더 내의 파일 리스트를 file_list 변수에 저장
file_list = os.listdir()
# 디렉터리 내의 .xlsx 파일만 따로 리스트 저장
order_file_list = [order for order in file_list if order[-5:] == '.xlsx' or order[-4:] == '.xls']
```

확장자에 대한 부채가 계속 거슬리지만, 미래의 나에게 떠넘긴다.

이렇게 받아온 파일 리스트로 동적으로 엑셀 wb(워크북),ws(워크시트)를 선언한다.

```Python
for file_name in order_file_list:
    if file_name[-5:] == '.xlsx':
        path = file_name[:-5]
    # xls 파일도 추가 파싱 예정
    elif file_name[-4:] == '.xls':
        path = file_name[:-4]
    wb_str = "wb_%s = openpyxl.load_workbook('%s')" % (path, file_name)
    ws_str = "ws_%s = wb_%s.active" % (path, path)
    order_str = "order_list = ws_%s" % path
    close_str = "wb_%s.close()" % path
    print('--------------', path, '------------')
    # execute
    exec(wb_str)
    exec(ws_str)
    exec(order_str)

#     print("파일 로딩 성공 테스트")
#     for r in order_list.rows:
#         print(r[3].value)
```

위 코드는 더 다듬어야 하는데 뭐.. 일단.
파일명을 쇼핑몰별 고유 변수명으로 잡고, wb와 ws를 선언할 문자열을 만든다. 그리고 `exec()`함수로 실행한다. 여기서 주의해야 할 점은 `exec()` 함수는 다른 함수에서 작성하면 동작하지 않는다. 각 기능별로 함수를 분리하려고 `exec()` 함수를 분리했다가 삽질의 늪에 빠졌다.. 구글링에서도 답을 못찾았....ㅠ 아무튼, 이렇게 동적으로 N개의 각 다른 이름의 wb, ws을 생성한다.  

마지막 코드는 잘 선언되었는지 확인하기 위해 내용을 출력하게 하였다.

## 파싱하기

```Python
def coupang(order_ws):
    print('-------쿠팡 파일 분석중---------')
    file_order = {}
    row_index =  0
    for r in order_ws.rows:
        if r[0].value == None: continue
        elif r[0].value == '번호': continue
        cate = change_category(r[10].value)
        file_order['category'+str(row_index)] = cate
        file_order['path'+str(row_index)] = '쿠팡'
        file_order['product'+str(row_index)] = r[10].value
        file_order['option'+str(row_index)] = r[12].value
        file_order['count'+str(row_index)] = r[22].value
        file_order['price'+str(row_index)] = r[18].value
        file_order['delivery'+str(row_index)] = r[20].value
        file_order['orderer'+str(row_index)] = r[24].value
        file_order['payee'+str(row_index)] = r[27].value
        file_order['call'+str(row_index)] = r[28].value
        file_order['address'+str(row_index)] = r[30].value
        file_order['postal_code'+str(row_index)] = r[29].value
        file_order['message'+str(row_index)] = r[31].value
        row_index += 1
    return file_order, row_index
```

file_order는 사전형 주문 정보다. row_index는 주문의 갯수이다.  

주문 정보들은 file_order 라는 이름으로 dict로 저장하였다. 주문에는 오차가 있으면 안되기 때문에 키와 값이 있는 사전형으로 선택하였다. if 문으로 제외할 라인을 구분한다. 여러 파일들의 정보를 저장해야 하기 때문에 처음라인(품목,수량..등 정보의 설명? 정의)은 제외하였다. 그리고 빈 값은 주문의 끝을 알려준다.

각 주문 상품은 각기 다른 주문 라인으로 접수를 해야 하기 때문에 구분을 해주어야 한다. 하지만 쇼핑몰 파일은 그렇게 친절하지 않다. 그래서 상품명에서 유니크한 단어를 찾아서 주문 라인을 구별한다.

```Python
def change_category(product):
    if product.find('녹용') != -1:
        cate = '품목1'
    elif product.find('잉어곰') != -1 or product.find('다슬기') != -1:
        cate = '품목2'
...
    elif (product.find('마늘') != -1 or product.find('산수유') != -1
          or product.find('야관문') != -1 or product.find('민들레') != -1 or product.find('오가피') != -1):
        cate = '품목17'
    else:
        cate = product
    return cate
```

## 주무 파일(엑셀)로 생성하기
이렇게 만들어진 주문 정보를 엑셀 파일로 저장한다.

```Python
# 주문파일 함수로 결과물 파일 생성
# row_index : 주문 갯수
# index : 결과 파일 작업 위치
# order_file : 각 쇼핑몰 함수를 통해 나온 주문 정리 데이터
# order_ws : 결과물 파일.

def create_file(order_file, order_ws, row_index):
    global index

    print('~~~~~파일 생성중입니다~~~~~~')

    file_index = 0
    for num in range(row_index):
        print('파일 기록중입니다.')
        order_ws['B'+str(index)] = order_file['category'+str(file_index)]
        order_ws['C'+str(index)] = order_file['product'+str(file_index)]
        order_ws['D'+str(index)] = order_file['option'+str(file_index)]
        order_ws['E'+str(index)] = order_file['count'+str(file_index)]
        order_ws['F'+str(index)] = order_file['price'+str(file_index)]
        order_ws['G'+str(index)] = order_file['delivery'+str(file_index)]
        print(order_file['orderer'+str(file_index)])
        order_ws['H'+str(index)] = order_file['orderer'+str(file_index)]
        order_ws['I'+str(index)] = order_file['payee'+str(file_index)]
        order_ws['J'+str(index)] = order_file['call'+str(file_index)]
        order_ws['K'+str(index)] = order_file['address'+str(file_index)]
        order_ws['L'+str(index)] = order_file['postal_code'+str(file_index)]
        order_ws['M'+str(index)] = order_file['message'+str(file_index)]
        index += 1
        file_index += 1

create_file(order_file, order_ws, row_index)
```

create_file 함수에 필요한 인자는 방금 만든 주문 정보파일(order_file), 결과물이 될 ws, 주문 갯수(row_index)이다. 주문 갯수는 for의 주기 횟수를 정한다. index는 전역 별수로 지정하였다. 그 이유는 파일이 하나가 아니라 여러 개라서 내용을 덮어쓰지 않고 이어쓰기를 하기 위해서이다.

## 이제부터 노가다

이제 각 쇼핑몰 별로 파싱 코드를 짜야한다. 각 파일이 모두 달라서 n개만큼 작업을 해야한다.

```Python
if path == '쇼핑몰':
    order_file, row_index = shop(order_list)
elif path == '티몬':
    order_file, row_index = tmon(order_list)
elif path == '스토어팜':
    order_file, row_index = farm(order_list)
elif path == '십일번가':
    order_file, row_index = eleven(order_list)
elif path == '쿠팡':
    order_file, row_index = coupang(order_list)
elif path == '인터파크':
    order_file, row_index = interpark(order_list)
elif path == '네이버페이':
    order_file, row_index = naverpay(order_list)
elif path == '지마켓' or path == '옥션':
    order_file, row_index = gmarket(order_list)
elif path == '위메프':
    order_file, row_index = wemape(order_list)
elif path == '김약사':
    order_file, row_index = kim(order_list)
elif path == '와우김약사':
    order_file, row_index = wow_kim(order_list)
elif path == '임박몰':
    order_file, row_index = imbak(order_list)
else:
    order_file, row_index = {}, 0
```

노가다로 만든 파싱 함수들을 연결한다.

## 저장하기

주문은 매일매일 들어가기 때문에 결과물 파일은 날짜로 정했다.

```Python
# 금일 날짜로 파일 이름 만들기
from datetime import datetime
result_file_name = datetime.today().strftime("%Y_%m_%d.xlsx")
# 엑셀 파일 저장
order_wb.save(filename=result_file_name)
```

## 확인하기

```Python
# 생성된 파일 존재 여부 확인하기
import os
print(result_file_name)
os.path.exists(result_file_name)
```

## 잊지말자.

각각의 워크북 파일을 꼭 닫아주자. 갯수가 많은 만큼 닫는것 깜빡하면 프로세스 재앙이 올 것이다...

```Python
# 각 쇼핑몰 파일 닫기
close_str = "wb_%s.close()" % path
exec(close_str)
# 결과물 파일 닫기
order_wb.close()
```

## 이제 파일을 나누자
노가다성이 짙어서 코드의 길이가 상당히 길다. 그래서 가독성이 나쁘다.  
기능별로 구분이 되기에 기능별로 파일을 나눈다.(주문정보 파싱, 메인, 파싱 생성)

나눈 파일들은 깃에 잘 올라가 있다.
[otherprogram](https://github.com/KimDoKy/otherprogram/tree/master/shopping_order)

임포트만 잘하면 되지...

## 개선점

openpyxl 모듈은 xlsx 파일만 읽을 수 있다. 그래서 다른 확장자의 파일을 xlsx 파일로 자동 convert 작업 코드를 만들려고 했다. convert 과정에서 어차피 파싱 작업이 필요해서, 그냥 csv와 xls파일도 같이 파싱하기로 했다.

## 빨리 직원이 뽑혔으면...

애초에 해당 업무 직원이 있으면 이런 뻘 짓을... ㅠ
