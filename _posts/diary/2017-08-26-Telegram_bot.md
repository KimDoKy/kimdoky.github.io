---
layout: post
section-type: post
title: Telegram Bot 만들기
category: diary
tags: [ 'diary' ]
---

파이썬 크롤링 스터디를 마치고, 다음 스터디로 넘어가기전에 가볍고(?) 빠르게 결과를 볼 수 있는 것을 진행하려고 합니다.  

[준범님의 블로그](https://beomi.github.io/2017/04/20/HowToMakeWebCrawler-Notice-with-Telegram/){:target="`_`blank"}를 둘러보는중 텔레그램 봇을 활용하는 내용을 발견하였고, 링크를 따라가보니 빠른 시간에 결과를 볼 수 있을꺼 같고, 현재 재직하고 있는 회사에서는 텔레그램을 메신져로 이용하고 있기 때문에 회사에서 사용할 수 있는 무언가를 만들때 활용할 수 있을꺼라 생각되어 시작하게 되었습니다.

모든 내용은 [python으로 telegram bot 활용하기](https://blog.psangwoo.com/coding/2016/12/08/python-telegram-bot-1.html){:target="`_`blank"}의 내용을 따라 진행하는 것이기 때문에 위 링크에서 기본 사용법을 익혀보는 것을 추천합니다.
> 자잘한 에러들에 대해서는 언급이 안되어 있어서 저와 같은 에러를 겪게 된다면 제 글을 읽어보시면 됩니다.

telegram bot을 만들기에 앞서 알아두어야 할 용어들입니다.

#### 용어 설명
- 계정 :  하나의 주체입니다. 사용자 혹은 bot 등이 해당됩니다.  
- 채널 : 채팅방, 그룹채팅방 등입니다. 채널을 공개하여 여러 사람이 들어올 수 있으며(ex:지진희알림), 관리자를 지정하고 이들만 채팅이 가능하도록 하는 등 알림용도로 사용이 가능합니다.
- BotFather : bot을 생성, 관리할 수 있는 계정입니다.(bot 형태입니다.)  
BotFather과 대화로 bot을 생성하고 여러 기능을 설정할 수 있습니다.

#### 준비물
telegram 어플을 설치한 휴대폰이 필요합니다. (telegram PC 버젼으로 하는걸 추천합니다. 토큰 복붙 하기가 편리하니까요.)

## 시작하기

대화 상대에서 BotFather을 검색하여 추가합니다.  

그리고 `/start` 라는 메세지를 보내면, 여러 설명 및 할 수 있는 일들을 알려줍니다.

![]({{site.url}}/img/post/diary/telegram/botfather.png)

봇을 만듭니다.

```
/newbot
```

그러면 `Alright, a new bot. How are we going to call it? Please choose a name for your bot.`라면서 이름을 지어달라고 합니다. 원하는 이름은 메시지로 보내면 됩니다.

저는 나중에 회사에서 쓰임새 있는 것으로 바꿀 예정이라 현재 진행하는 프로젝트 명으로 하였습니다. 원하는 이름을 메시지로 보내면 `Good. Now let's choose a username for your bot. It must end in 'bot'. Like this, for example: TetrisBot or tetris_bot.`라면 bot으로 끝나는 username을 정해달라고 합니다.
username은 봇을 검색할 때 사용하게 됩니다.(username 지정시 처음은 영문으로 시작해야 합니다.)

![]({{site.url}}/img/post/diary/telegram/botfather_2.png)

4season이 봇의 이름, `@`로 시작하는 부분이 username입니다.

전체 과정입니다. (봇의 처음 설명이 너무 길어서 `/start`는 캡쳐에서 제외하였습니다.)

![]({{site.url}}/img/post/diary/telegram/botfather_3.png)

마지막에 token이 xxxx:yyyyyy 형태로 발행됩니다. 이 토큰이 있으면 해당 계정(봇)의 권한을 거의 모두 사용할 수 있습니다. 그렇기 때문에 관리를 잘 해야 합니다.  

Python 코딩에 앞서 자신의 텔레그램에서 방금 생성한 봇과 채팅을 시작합니다. 그래야 테스트를 눈으로 확인 할 수 있으니까요.

### Python 작업

#### Bot으로 온 메시지 확인하기

python에서 telegram api를 사용하기 위해 python-telegram-bot이라는 모듈을 사용하면 됩니다. 설치는 pip로 하면 됩니다.

```
$ pip install python-telegram-bot
```
설치가 완료되었다면 토큰을 이용하여 봇을 사용해봅시다.

```python
import telegram # 텔레그램 모듈을 임포트합니다.

my_token = '여기에 토큰을 입력하세요' # 토큰을 변수에 저장합니다.

bot = telegram.Bot(token = my_token) # bot을 선언합니다.

updates = bot.getUpdates() # 업데이트 내역을 받아옵니다.

for u in updates:
    print(u.message) # 업데이트 내역 중 메시지를 출력합니다.
```
> 임포트 하는 과정에서 계속 에러가 발생했습니다.
구글 신에서 검색을 해본 결과 [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)에서 해답을 찾았습니다.  
telegram-bot을 설치하기전에 urllib3 하위 모듈을 초기화해야 에러가 해결됩니다.

> `AttributeError: module 'token' has no attribute '__all__'`에러가 난다면?  
git clone 으로 telegram-bot을 설치하고 설치한 디렉터리에서 파일을 실행합니다.

응답입니다.

```
{'message_id': 5, 'text': '엇 되네? ㅋㅋㅋ', 'delete_chat_photo': False, 'date': 1503732264, 'from': {'last_name': '-', 'id': -, 'language_code': 'ko-KR', 'first_name': '-'}, 'group_chat_created': False, 'new_chat_member': None, 'new_chat_photo': [], 'photo': [], 'supergroup_chat_created': False, 'chat': {'id': -, 'last_name': '-', 'type': 'private', 'first_name': '-'}, 'channel_chat_created': False, 'entities': [], 'new_chat_members': []}
```
> 저는 이러 저러한 에러를 겪어서.. 메시지가 저따구네요...ㅋㅋㅋ

`u.message`에서 text(내용), 누구에게서 왔는지, 발신자의 id(username과 동일하게 사용됩니다.) 등을 확인할 수 있습니다. 만약 수신된 내용만 보려면 `u.message.text`를 사용하면 됩니다.

#### Bot으로 메시지 보내기

메시지를 보내기 위해서는 보낼 상대의 username-api에서 말하는 `chat_id`를 알아야 합니다.  
bot을 테스트 할 때 메시지를 보내두었고 위의 예제가 잘 실행되었다면 `u.message.chat.id`로 메시지를 보낸 사람의 `chat_id`를 확인할 수 있습니다.

chat 그룹 안의 id부분이 `chat_id`입니다.

```python
chat_id = bot.getUpdates()[-1].message.chat.id
bot.sendMessage(chat_id = chat_id, text="저는 봇입니다.")
```

그러면 bot이 메시지를 보낸 것을 확인 할 수 있습니다.

![]({{site.url}}/img/post/diary/telegram/botfather_4.png)
