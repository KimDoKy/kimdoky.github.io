---
layout: post
section-type: post
title: crawling - P1.스크레이퍼 제작 _ cahp 5. 데이터 저장
category: python
tags: [ 'python' ]
---

터미널로 출력하는 것도 흥미롭지만, 웹 스크레이퍼를 유용하게 활용하려면 스크랩한 정보를 저장할 수 있어야 합니다.  

이번 챕터에서는 3 가지 데이터 관리 방법을 다룹니다.

1. 스크랩한 데이터를 웹사이트에 사용하거나, 직접 API를 만들 생각인가요?
- 데이터베이스가 필요합니다.

2. 인터넷에서 문서를 수집해 하드디스크에 저장할 쉽고 빠른 방법을 찾고 있습니까?
- 파일 스트림이 해결책입니다.

3. 주기적 알림을 받거나, 하루에 한 번 데이터를 집계하려 하나요?
- 스스로에게 이메일을 보내세요.

꼭 웹 스크레이핑이 아니더라도, 최신 애플리케이션에는 대량의 데이터를 저장하고 조작하는 능력이 반드시 필요합니다.

## 5.1 미디어 파일

미디어 파일을 저장하는 방법은 크게 두 가지입니다. 하나는 참조를 저장하는 것이고, 다른 하나는 파일 자체를 내려받는 것입니다. 파일 참조 저장을 간단합니다. 파일이 위치한 URL을 저장하기만 하면 됩니다. 이 방법에는 여러 장점이 있습니다.

- 스크레이퍼가 파일을 내려받을 필요가 없으므로 훨씬 빨리 동작하고, 대역폭도 적게 요구합니다.
- URL만 저장하므로 컴퓨터의 공간도 확보할 수 있습니다.
- URL만 저장하고 파일을 내려받지 않는 코드는 만들기 쉽습니다.
- 큰 파일을 내려받지 않으므로 호스트 서버의 부하도 적습니다.

물론 단점도 있습니다.

- 이들 URL을 당신의 웹사이트나 애플리케이션에 포함시키는 것을 **핫링크** 라 부르는데, 말썽이 생길 소지가 많습니다.
- 애플리케이션에 사용할 미디어 파일을 다른 사람의 서버에 맡기고 싶지 않을 수 있습니다.
- 외부에 있는 파일은 바뀔 수 있습니다. 공개된 블로그 같은 곳에 핫링크 이미지를 쓰면 난처한 일이 생길 수 있습니다. 파일을 더 연구할 목적으로 나중에 저장하려고 했는데, 막상 그 나중이 되니 파일이 사라졌거나 완전히 다른 것으로 바뀌었을 수도 있습니다.
- 실제 웹 브라우저는 페이지의 HTML만 요청하지 않고, 거기 포함된 파일도 내려받습니다. 스크레이퍼에서 파일을 내려받으면 실제 사람이 사이트를 보는 것처럼 보일 수 있고, 이것이 장점이 될 때가 있습니다.

파일을 저장할지 아니면 URL만 저장할지 결정해야 한다면, 그 파일을 한두 번 이상 실제로 보거나 읽을지, 아니면 데이터베이스를 유지하면서 수집하기만 할지 생각해봐야 합니다. 답이 후자라면 그냥 URL만 저장해도 충분합니다.  

만약 전자의 경우라면, 파이썬 3.x에서는 `urllib.request.urlretrieve`을 사용해 원격 URL의 파일을 내려받을 수 있습니다.

```python
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com")
bsObj = BeautifulSoup(html, "html.parser")
imageLocation = bsObj.find("a", {"id": "logo"}).find("img")["src"]
urlretrieve(imageLocation, "logo.jpg")
```

이 코드는 http://pythonscraping.com 에서 로고를 내려받아, 스크랩트를 실행한 디렉터리에 logo.jpg라는 이름으로 저장합니다.  
이 코드는 내려받을 파일이 하나뿐이고, 파일 이름과 확장자를 어떻게 정할지 알고 있다면 잘 동작합니다. 하지만 대부분의 스크레이퍼는 파일 하나만 내려받고 끝나지 않습니다. 다음 코드에서와 같이 http://pythonscraping.com 홈페이지에서 src 속성이 있는 태그에 연결된 내부 파일을 모두 내려받습니다.

```python
import os
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

downloadDirectory = "downloaded"
baseUrl = "http://pythonscraping.com"

def getAbsoluteURL(baseUrl, source):
    if source.startswith("http://www."):
        url = "http://" + source[11:]
    elif source.startswith("http://"):
        url = source
    elif source.startswith("www."):
        url = source[4:]
        url = "http://"+source
    else:
        url = baseUrl + "/" + source
    if baseUrl not in url:
        return None
    return url

def getDownloadPath(baseUrl, absoluteUrl, downloadDirectory):
    path = absoluteUrl.replace("www.", "")
    path = path.replace(baseUrl, "")
    path = downloadDirectory + path
    directory = os.path.dirname(path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    return path

html = urlopen("http://www.pythonscraping.com")
bsObj = BeautifulSoup(html, "html.parser")
downloadList = bsObj.find_all(src=True)

for download in downloadList:
    fileUrl = getAbsoluteURL(baseUrl, download["src"])
    if fileUrl is not None:
        print(fileUrl)

urlretrieve(fileUrl, getDownloadPath(baseUrl, fileUrl, downloadDirectory))
```
> ### 실행 전에 주의합니다.  
인터넷에서 불확실한 파일을 내려받는 건 위험합니다. 이 스크립트는 만나는 모든 것을 컴퓨터의 하드 디스크에 내려받습니다. 여기에는 스크립트, `.exe`파일, 기타 잠재적 멀웨어가 포함됩니다.  
이 프로그램을 관리자 권한으로 실행한다면 골칫거리를 자초하게 됩니다. 웹사이트에서 발견한 파일이 그 자신을 `../../../../usr/bin/python`으로 이동하는 파일이라면? 다음에 명령줄에서 파이썬 스크립트를 실행하는 순간, 컴퓨터에 멀웨어를 초청하게 되는겁니다.  
이 프로그램은 오직 예시 목적으로 만들어졌습니다. 더 광범위하게 파일 이름을 체크하는 코드 없이 무작위로 배포해서는 안되며, 권한이 제한된 계정에서만 실행해야 합니다. 항상 그렇지만, 파일을 백업하고 예민한 정보는 하드디스크에 저장하지 않으며 상식을 따르면 안전할 수 있습니다.

다음은 실행 결과입니다.

```
http://pythonscraping.com/misc/jquery.js?v=1.4.4
http://pythonscraping.com/misc/jquery.once.js?v=1.2
http://pythonscraping.com/misc/drupal.js?os2esm
http://pythonscraping.com/sites/all/themes/skeletontheme/js/jquery.mobilemenu.js?os2esm
http://pythonscraping.com/sites/all/modules/google_analytics/googleanalytics.js?os2esm
http://pythonscraping.com/sites/default/files/lrg_0.jpg
http://pythonscraping.com/img/lrg%20(1).jpg
```

이 스크립트는 람다 함수를 써서 첫 페이지의 src 속성이 있는 태그를 모두 선택한 후, URL을 손질하고 절대 경로로 바꿔 내려받을 준비를 합니다.(외부링크는 내려받지 않습니다.) 그리고 각 파일을 컴퓨터의 downloaded 폴더 안에 경로를 유지하며 내려받습니다.  

파이썬 os 모듈은 각 파일이 저장될 디렉터리가 있는지 확인하고 없으면 만들기 위해 사용했습니다. os 모듈은 파이썬과 운영체제 사이의 인터페이스 구실을 합니다. 파일 경로를 조작하고, 디렉터리를 만들고, 실행 중인 프로세스와 환경 변수에 관한 정보를 얻고, 그 외에도 여러가지 유용한 일을 할 수 있습니다.

## 5.2 데이터를 CSV로 저장

**CSV(comma-separated values)** 는 스프레드시트 데이터를 저장할 때 가장 널리 쓰이는 파일 형식입니다. 이 파일은 매우 단순하므로 마이크로소프트 엑셀을 비롯해 여러 애플리케이션에서 지원합니다. 다음은 유효한 CSV 파일 예제입니다.

```
fruit,cost
apple,1,00
banana,0.30
pear,1.25
```

파이썬과 마찬가지로 CSV에서도 공백이 중요합니다. 각 행은 줄바꿈 문자로 구분하고, 각 열은 (이름대로) 쉼표로 구분합니다. 탭이나 기타 문자로 행을 구분하는 CSV 파일도 있지만, 이런 형식은 널리 쓰이지 않고 지원하는 프로그램도 많지 않습니다.  
웹에서 CSV 파일을 내려받아, 파싱하거나 수정하지 않고 그대로 저장만 할 것이라면 다른 파일과 마찬가지로 내려받아 CSV 파일로 저장하면 됩니다.  

파이썬 csv 라이브러리를 사용하면 CSV 파일을 쉽게 수정하거나 만들 수 있습니다.

```python
import csv

csvFile = open("./files/test.csv", 'wt')
try:
    writer = csv.writer(csvFile)
    writer.writerow(('number', 'number plus 2', 'number times 2'))
    for i in range(10):
        writer.writerow((i, i+2, i*2))
finally:
    csvFile.close()
```
먼저 염두에 두고 조심할 것이 있습니다. 파이썬을 파일을 만들 때 에러를 거의 일으키지 않습니다. `./files/test.csv`가 존재하지 않으면 파이썬이 파일을 자동으로 만듭니다.(디렉터리를 자동으로 만듭니다.) 파일이 이미 존재하면 파이썬은 test.csv 를 경고 없이 새 데이터로 덮어씁니다.

코드를 실행하면 다음과 같은 CSV 파일이 생깁니다.

```csv
number,number plus 2,number times 2
0,2,0
1,3,2
2,4,4
...
```
웹 스크레이핑에서 자주 하는 일 중 하나는 HTML 테이블을 가져와서 CSV 파일을 만드는 겁니다. 위키백과의 텍스트 에디터 비교(https://en.wikipedia.org/wiki/Comparison_of_text_editors) 항목에는 매우 복잡한 HTML 테이블이 있습니다. 이 테이블에는 색깔도 들어있고, 링크와 정렬 기능, 기타 HTML 코드들이 있는데 CSV 파일로 만들기 전에 이것들을 제거해야 합니다. `BeautifulSoup`와 `get_text()` 함수를 써서 20줄도 안되는 코드로 그 일을 할 수 있습니다.

```python
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://en.wikipedia.org/wiki/Comparison_of_text_editors")
bsObj = BeautifulSoup(html, "html.parser")
# 비교 테이블은 현재 태이블은 현재 페이지의 첫 번째 테이블입니다.
table = bsObj.find_all("table", {"class":"wikitable"})[0]
rows = table.find_all("tr")

csvFile = open("./files/editors.csv", 'wt')
writer = csv.writer(csvFile)
try:
    for row in rows:
        csvRow = []
        for cell in row.find_all(['td', 'th']):
            csvRow.append(cell.get_text())
            writer.writerow(csvRow)
finally:
    csvFile.close()
```
> ### 실무에 쓰기 전에, 잠깐  
HTML 테이블을 CSV 파일로 바꿔야 하는 일이 자주 있다면 이 스크립트를 스크레이퍼에 통합하는 것이 좋습니다. 하지만 딱 한 번만 바꾼다면 더 좋은 방법이 있습니다. 복사해서 붙여 넣기만 하면 됩니다. HTML 테이블의 콘텐츠를 선택해서 복사하고 엑셀에 붙여 넣으면 스크립트를 실행하지 않아도 CSV 파일을 얻을 수 있습니다.

코드를 실행하면 잘 정리된 CSV 파일 `./files/editors.csv`가 만들어 집니다.

## 5.3 MySQL

MySQL(공식 발음은 마이에스큐엘이지만 마이시퀄이라고 읽는 사람이 많습니다.)은 현재 가장 널리 쓰이는 오픈 소스 관계형 데이터베이스 관리 시스템입니다. MySQL은 두 경쟁자인 마이크로소프트 SQL 서버, 오라클 DBMS와 서로 발전해왔는데, 강력한 경쟁자를 두고 있는 오픈 소스 프로젝트치고는 흔치 않은 일입니다.  

물론 MySQL의 인기에는 그만한 이유가 있습니다. 대부분의 애플리케이션은 MySQL로 충분합니다. MySQL은 매우 확장성이 높고 견고하며 다양한 기능을 갖춘 DBMS입니다. 유투브(http://bit.ly/1LWVmc8), 트위터(http://bit.ly/1KHDKns), 페이스북(http://bit.ly/1RFMqvw) 등 여러 주요 웹사이트에서 MySQL을 사용하고 있습니다.  

MySQL은 어디서든 쓰이고 무료이고 사용하기 쉽기까지 해서 웹 스크레이핑 프로젝트에서 데이터베이스로 쓰기 안성맞춤입니다.

### 5.3.1 MySQL 설치

MySQL의 핵심은 데이터베이스에 저장된 정보를 모두 담고 있는 데이터 파일 세트입니다.
MySQL 소프트웨어는 명령줄 인터페이스를 통해 데이터를 간편하게 조작하는 방법을 제공합니다. 예를 들어 다음 명령어는 데이터 파일을 검색해서 이름이 Ryan인 모든 사용자 목록을 반환합니다.

```sql
SELECT * FROM users WHERE firstname = "Ryan"
```

리눅스에서의 설치는 간단합니다.

```
$ sudo apt-get install mysql-server
```
설치 과정을 보고 있다가 메모리 요구사항을 확인하고, 루트 사용자 비밀번호를 요청할 때 입력하기만 하면 됩니다.  

맥 OS X는 패키지 관리자 홈브류(http://brew.sh)으로 설치할 수 있습니다.

```
$ brew install mysql
```

> ### MAC에서 MySQL 삭제
```
sudo rm /usr/local/mysql
sudo rm -rf /usr/local/mysql*
sudo rm -rf /Library/StartupItems/MySQLCOM
sudo rm -rf /Library/PreferencePanes/My*
rm -rf ~/Library/PreferencePanes/My*
sudo rm -rf /Library/Receipts/mysql*
sudo rm -rf /Library/Receipts/MySQL*
sudo rm -rf /var/db/receipts/com.mysql.*
sudo vi /etc/hostconfig
```

홈브류는 훌륭한 오픈 소스 프로젝트이며 파이썬 패키지와 매우 잘 어울립니다.  

맥 OS X에 MySQL을 설치했으면 다음 명령으로 서버를 시작할 수 있습니다.

```
$ mysql.server start
$ mysql -u root
```

>
... ERROR! The server quit without updating PID file (/usr/local/var/mysql/DoKyungui-MacBook-Pro.local.pid)  에러가 발생한다면  
>
해결책 $ ps aux | grep mysql
이미 실행중인 mysql 의 pid를 확인하여 사살 $ kill (mysql_pid)
mysql 재실행 $ mysql.server restart

> #### MySQL root passwd 분실시 재설정 방법
```
$ mysql -u root
mysql> USE mysql;
mysql> UPDATE user SET authentication_string=PASSWORD("NEWPASSWORD") WHERE User='root';
mysql> FLUSH PRIVILEGES;
mysql> quit
```

### 5.3.2 기본 명령어

MySQL 서버가 시작되면 여러 가지 방법으로 데이터베이스를 조작할 수 있습니다. MySQL 명령어를 직접 사용하지 않고, 최소한으로 줄여주는 인터페이스 소프트웨어가 많이 있습니다. phpMyAdmin과 MySQL 워크벤치 같은 도구를 쓰면 더 쉽고 빠르게 데이터를 보고, 정렬하고, 삽입할 수 있습니다. 하지만 명령어 사용 방법은 알고 있어야 합니다.  

변수 이름을 제외하면, MySQL은 대소문자를 구분하지 않습니다. 예를 들어 SELECT는 sELEcT 는 같습니다. MySQL 문을 쓸 때 키워드를 모두 대문자로 쓰는 표기법이 널리 쓰입니다. 반대로 테이블과 데이터베이스 이름에는 소문자로 쓰는 개발자들이 많습니다.  

MySQL에 처음 로그인하면 데이터를 추가할 데이터베이스가 없으니 만들어야 합니다.

```SQL
> CREATE DATABASE scraping;
```

MySQL 서버 인스턴스 하나에 데이터베이스가 여러 개 있을 수 있으므로, 먼저 어떤 데이터베이스를 조작하려 하는지 명시해야 합니다.

```SQL
> USE scraping;
```
여기서부터(최소한 MySQL 연결을 끊거나 다른 데이터베이스로 전환하기 전까지) 입력하는 모든 명령어는 방금 만든 scraping 데이터베이스를 대상으로 실행됩니다.  

스크랩한 웹 페이지를 저장할 테이블을 만듭니다.
```SQL
> CREATE TABLE pages;
```
여기서 에러가 발생합니다.
```
ERROR 1113 (42000): A table must have at least 1 column
```
데이터베이스는 테이블이 없어도 전재할 수 있지만, 테이블은 열 없이 존재할 수 없습니다. MySQL에서 열을 정의하려면 `CREATE TABLE <tablename>`문 다음에 괄호를 쓰고 그 안에 쉼표로 구분된 목록을 씁니다.

```
> CREATE TABLE pages (id BIGINT(7) NOT NULL AUTO_INCREMENT, title VARCHAR(200), content VARCHAR(10000), created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(id));
```
각 열의 정의는 세 부분으로 나뉩니다.

- 이름(id, title, created 등)
- 변수 타입(BIGINT(7), VARCHAR, TIMESTAMP)
- 옵션으로, 추가 속성(NOT NULL, AUTO_INCREMENT)

열 목록 마지막에는 반드시 테이블의 키를 정의해야 합니다. MySQL은 키를 사용해서 테이블 콘텐츠를 빨리 검색할 수 있도록 준비합니다. 키를 활용해서 데이터베이스를 더 빠르게 이용할 수 있지만, 지금은 테이블의 id 열을 키로 사용하는 일반적인 방법을 사용합니다.  

쿼리를 실행하고 나면 언제든 DESCRIBE 명령으로 테이블 구조를 확인할 수 있습니다.

```
mysql> DESCRIBE pages;
+---------+----------------+------+-----+-------------------+----------------+
| Field   | Type           | Null | Key | Default           | Extra          |
+---------+----------------+------+-----+-------------------+----------------+
| id      | bigint(7)      | NO   | PRI | NULL              | auto_increment |
| title   | varchar(200)   | YES  |     | NULL              |                |
| content | varchar(10000) | YES  |     | NULL              |                |
| created | timestamp      | NO   |     | CURRENT_TIMESTAMP |                |
+---------+----------------+------+-----+-------------------+----------------+
4 rows in set (0.01 sec)
```

물론 여전히 빈 테이블입니다. 다음 명령으로 pages 테이블에 테스트 데이터를 삽입해봅니다.

```
> INSERT INTO pages (title, content) VALUES ("Test page title", "This is some test page content. It can be up to 10,000 characters long.");
```
테이블에는 열이 네 개(id, title, content, created)가 있지만, title과 content 두 열만 지정해도 데이터를 삽입할 수 있습니다. id 열은 자동 증가(`AUTO_INCREMENT`) 열이므로 새 행을 삽입할 때마다 MySQL에서 자동으로 1씩 늘리며, 일반적으로 더 신경 쓸 필요 없습니다. 또한 timestamp 열에는 기본값으로 현재 시간이 들어갑니다.

물론 이들 기본값을 오버라이드 할 수도 있습니다.

```
> INSERT INTO pages (id, title, content, created) VALUES (3, "Test page title", "This is some test page content. It can be up to 10,000 characters long", "2014-09-21 10:25:32");
```

id 열에 이미 데이터베이스에 존재하지 않는 정수를 입력하기만 하면 이 문은 잘 동작합니다. 하지만 일반적으로 좋은 방법이 아닙니다. 반드시 그래야만 하는 이유가 있지 않다면, id와 timestamp 열은 MySQL이 처리하는게 가장 좋습니다.

이제 테이블에 데이터가 좀 생겼으니 이 데이터를 다양한 방법으로 선택할 수 있습니다. 다음은 몇 가지 SELECT 문 예제입니다.

```
> SELECT * FROM pages WHERE id = 2;
```
이 문은 'pages에서 id가 2인 것을 모두 선택하라'는 의미입니다. 에스터리스크(`*`)는 와일드카드이며 where 절을 충족하는 (id가 2인) 행을 모두 반환합니다. 따라서 이 명령은 테이블의 두 번째 행을 반환하거나, id가 2인 행이 없으면 아무것도 반환하지 않습니다. 다음 쿼리는 title 필드에 test가 들어 있는 모든 행을 반환합니다.(% 기호는 MySQL 문자열의 와일드카드입니다.)

```
> SELECT * FROM pages WHERE title LIKE "%test%";
```
테이블에 열이 여러 개 있고 그중 일부만 보려면 어떻게 해야 할까요? 와일드카드를 쓰지 않고 열 이름을 명시적으로 쓰면 됩니다.

```
> SELECT id, title FROM pages WHERE content LIKE "%page content%";
```
이 쿼리는 content에 page content가 들어 있는 열에서 id와 title만 반환합니다.

DELETE 문도 SELECT 문과 비슷한 문법을 사용합니다.

```
> DELETE FROM pages WHERE id = 1;
```
두 문의 문법이 비슷하므로, DELETE 문을 쓰기 전에 SELECT 문을 먼저 써서(여기서는 `SELECT * FROM pages WHERE id = 1`) 삭제하려는 데이터만 반환되는지 확인한 다음, `SELECT *`를 `DELETE`로 바꿔서 다시 명령하는 게 좋습니다. 특히, 쉽게 복구할 수 없는 중요한 테이블이라면 반드시 이렇게 해야 합니다. 많은 프로그래머들이 DELETE 문을 잘못 코딩하거나 심지어 바쁠때 그걸 알아차리지도 못해서 고객의 데이터를 잃어버린 악몽 같은 경험을 갖고 있습니다.  

마찬가지로 UPDATE 문을 쓸 때도 주의해야 합니다.

```
> UPDATE pages SET title="A new title", content="some new content" WHERE id=2;
```
여기서는 단순한 MySQL 문만 사용해서 기본적인 선택과 삽입, 업데이트만 합니다.

### 5.3.3 파이썬과의 통합

파이썬은 MySQL 지원을 내장하고 있지 않습니다. [`PyMySQL`](http://www.pymysql.org/){:target="`_`blank"}라는 라이브러리를 이용해서 MySQL을 사용할 수 있습니다.

pip를 이용해서 설치합니다.

```
pip install PyMySQL
```

설치하고 나면 자동으로 PyMySQL 패키지에 접근할 수 있습니다. 그리고 로컬에서 MySQL 서버가 실행되는 동안에는 다음 스크립트가 성공적으로 실행되어야 합니다.(루트 비밀번호 부분을 설정한 비밀번호로 바꾸세요.)

```python
import pymysql
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='None', db='mysql')

cur = conn.cursor()
cur.execute("USE scraping")
cur.execute("SELECT * FROM pages WHERE id=1")
print(cur.fetchone())
cur.close()
conn.close()
```

이 예는 새로운 객체 타입이 두 개 있습니다. 하나는 연결 객체(conn)이고, 다른 하나는 커서 객체(cur)입니다.

연결/커서 모델은 데이터베이스 프로그래밍에 널리 쓰이는 개념입니다. 연결 객체는 물론 데이터베이스 연결에 관여하지만, 그 외에도 데이터베이스에 정보를 보내고, 롤백(쿼리를 취소하고 데이터베이스를 이전 상태로 되돌리는 것)을 처리하고 새 커서 객체를 만드는 역할도 합니다.  

연결 하나에 커서 여러 개가 있을 수 있습니다. 커서는 어떤 데이터베이스를 사용 중인지 같은 **상태** 정보를 추적합니다. 데이터베이스가 여럿 있고 이들 전체에 정보를 저장해야 한다면 커서도 여러개 필요합니다. 커서는 또 마지막에 실행한 쿼리 결과도 가지고 있습니다. `cur.fetchone()`과 같이 커서에서 함수를 호출하여 이 정보에 접근할 수 있습니다.  

커서와 연결 사용을 마치면 이들을 닫아야 합니다. 이들을 닫는 걸 게을리 하면 **연결 누수(connection leaks)** 현상이 발생할 수 있습니다.(더는 사용하지 않는 연결인데도 소프트웨어 입장에서는 닫아도 된다는 확신이 없어서 닫히지 않은 연결이 쌓이는 현상) 연결 누수가 심해지면 데이터베이스가 다운될 수 있으니 항상 연결을 닫도록 합니다.  

지금 가장 먼저 하려는 것은 스크레이핑 결과를 데이터베이스에 저장하는 것입니다.

웹 스크레이핑을 하면서 유니코드 텍스트를 다루는 일이 좀 어려울 수 있습니댜. MySQL은 기본적으로 유니코드를 처리하지 않습니다. 다행히 이 기능을 켤 수는 있습니다(크기가 조금 커지는 부작용이 있습니다.). 위키백과를 돌아다니다 보면 여러 가지 문자를 만날테니, 이제 데이터베이스에 유니코드에 대비하라고 알려줄 때입니다.

```
> ALTER DATABASE scraping CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
> ALTER TABLE pages CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
> ALTER TABLE pages CHANGE title title VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
> ALTER TABLE pages CHANGE content content VARCHAR(10000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
> #### `ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: NO)` 에러가 발생한다면??  
```
> mysql -u root -p databasename
```

위 4 행은 데이터베이스와 테이블, 두 열의 기본 문자셋을 utf8mb4(일단 유니코드이긴 하지만 지원이 형평없기로 악명 높습니다)에서 `utf8mb4_unicode_ci`으로 바꿉니다.  

움라우트나 한자를 title과 content 필드에 삽입해도 에러가 없다면 위 명령은 제대로 실행된 겁니다.  

이제 데이터베이스는 위키백과에서 쏟아낼 다양한 것들을 받을 준비가 됐으니 다음 코드를 실행해도 됩니다.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import pymysql
import re

conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd=None, db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE scraping")

random.seed(datetime.datetime.now())

def store(title, content):
    cur.execute("INSERT INTO pages (title, content) VALUES (\"%s\", \"%s\")", (title,content))
    cur.connection.commit()

def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    title = bsObj.find("h1").get_text()
    content = bsObj.find("div", {"id":"mw-content-text"}).find("p").get_text()
    store(title, content)
    return bsObj.find("div", {"id":"bodyContent"}).find_all("a", href=re.compile("^(/wiki/)((?!:).)*$"))

links = getLinks("/wiki/Kevin_Bacon")
try:
    while len(links) > 0:
        newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
        print(newArticle)
        links = getLinks(newArticle)
finally:
    cur.close()
    conn.close()
```
> import re를 추가하고 find("span")를 삭제하였습니다.

연결 문자열에 "charset='utf8'"이 추가되었습니다. 이 부분은 연결에서 데이터베이스에 정보를 보낼 때 모두 UTF-8로 보내야 한다는 뜻입니다.  

store 함수가 추가되었습니다. 이 함수는 문자열 변수 title과 content를 받고, 이 변수를 INSERT 문에 추가합니다. 커서는 INSERT 문을 실행하고, 자신의 연결을 통해 데이터베이스에 보냅니다. 이 함수는 커서와 연결이 어떻게 구분되는지 잘 보여줍니다. 커서는 데이터베이스와 자신의 컨텍스트에 관한 정보를 갖고 있지만, 정보를 데이터베이스에 보내고 삽입하려면 연결을 통해야 합니다.  
마디막으로, 코드 마지막 부분에서 finally 문을 프로그램의 메인 루프에 추가했습니다. finally 문은 프로그램이 어떻게든 방해를 받거나, 실행 중 예외가 발생하더라도(물론, 웹은 항상 예외가 발생합니다) 프로그램을 종료하기 전에 반드시 커서와 연결을 닫기 위해 사용했습니다. 데이터베이스 연결을 열어둔 채 스크래이핑을 할 때는 항상 `try...finally` 문을 쓰는게 좋습니다.  
PyMySQL는 그리 크지 않은 패키지이지만, 유용한 함수가 너무 많기 때문에 [파이썬 문서](http://bit.ly/1KHzoga){:target="`_`blank"}를 참고하세요.

### 5.3.4 데이터베이스 테크닉과 모범 사례

데이터베이스를 빨리 배워두면 대부분의 애플리케이션을 감당할 수 있고 또 충분히 빨리 동작하게 하는 요령이 있습니다.  

먼저, 극히 일부인 예외를 제외하면, 테이블에는 항상 id 열을 추가합니다. MySQL의 테이블에는 반드시 정렬 기준이 되는 프라이머리 키가 최소한 하나 있어야 하는데, 무엇을 키로 정할지 프로그램에서 판단하기는 어렵습니다. 인위적으로 만든 id 열이 프라이머리 키로 쓰기에 더 좋은지, 아니면 username 같은 고유한 열이 더 좋은지는 데이터 과학자와 소프트웨어 엔지니어들이 몇 년째 토론하고 있는 문제입니다. 어떤 방법을 택할지는 복잡한 문제이지만, 기업에서 사용할 시스템이 아닌 이상 항상 자동 증가하는 id 열을 프라이머리 키로 써야 합니다.  

둘째, 인덱스 관리를 잘 해야합니다. 사전은 알파벳 순으로 나열한 단어 목록입니다. 단어 순서가 정해져 있으니, 철자만 알고 있다면 단어를 빠르게 찾을 수 있습니다. 그런데 어떤 사전이 단어의 철자가 아니라 그 정의의 철자 순으로 만들져있다고 가정해봅니다. 이런 사전은 단어의 정의를 듣고 어떤 단어인지 맞히는 게임을 하지 않는 한 쓸모가 없을 것입니다. 하지만 데이터베이스 검색의 세계에는 이런 일이 발생합니다. 예를 들어 데이터베이스에 쿼리 대상으로 자주 사용하는 필드가 있다고 가정합니다.

![]({{site.url}}/img/post/python/crawling/p1c5_1.png)

id 열이 아마 있겠지만, definition 열의 검색을 빠르게 하기 위해 테이블에 키를 추가하고 싶을 겁니다. 하지만 인덱스를 추가하면 그만큼 공간을 더 차지하고, 새 행을 삽입할 때마다 처리 시간이 조금씩 더 소요됩니다. MySQL이 이 열의 처음 몇 글자만 인덱스로 만들게 하면 그 문제는 완화됩니다. 다음 명령은 definition 필드의 처음 16글자에 인덱스를 만듭니다.

```
> CREATE INDEX definition ON dictionary (id, definition(16));
```
이 인덱스는 단어의 정의 전체를 써서 검색할 때 훨씬 빨리 답을 찾고, 공간도 적게 소모하며 이후 테이블에 행을 삽입할 때 걸리는 시간도 별로 늘어나지 않습니다.  

쿼리 시간 vs 데이터베이스 크기 문제는 데이터베이스 공학에서 기본적인 균형 작업의 하나인데, 이와 관련해서 자주 저지르는 실수가 있습니다. 특히 웹 스크레이핑을 통해 자연어 텍스트를 아주 많이 저장할 때 자주 일어나는데, 중복된 데이터를 아무 많이 저장하는 문제입니다. 예를 들어 여러 웹사이트에서 공통적으로 나타나는 구절이 있는지, 있다면 몇 회나 되는지 알아보고 싶다고 합시다. 이런 구절은 이미 만들어진 목록을 쓸 수도 있고, 일종의 텍스트 분석 알고리즘에서 자동으로 생성할 수도 있습니다. 아마 데이터를 다음과 같은 형식으로 저장하고 싶을 겁니다.

![]({{site.url}}/img/post/python/crawling/p1c5_2.png)

이렇게 하면 사이트에서 구절을 찾을 때마다 그 구절과 URL로 데이터베이스에 한 행을 추가합니다. 하지만 데이터를 테이블 세 개로 분리하면 데이터 크기를 어마어마하게 줄일 수 있습니다.

![]({{site.url}}/img/post/python/crawling/p1c5_3.png)

테이블 정의가 더 커지긴 했지만, 열 대부분은 정수만 저장하는 id 필드입니다. 이런 필드는 공간을 적게 차지합니다. 또한 각 URL과 구절의 전체 텍스트는 정확히 한 번씩만 저장됩니다.  

그런 용도의 패키지를 따로 설치하거나 로그를 꼼꼼하게 관리하지 않으면 데이터가 언제 추가됐고, 언제 업데이트됐고, 언제 제거됐는지 알 수 없습니다. 데이터에 쓸 수 있는 공간, 변경 빈도, 그리고 변경이 언제 일어났는지 알아야 할 필요성 등을 고려해보고, 'created', 'updated', 'deleted' 같은 타임스탬프를 만드는 것도 한 방법입니다.


### 5.3.5 여섯 다리와 MySQL

## 5.4 이메일
