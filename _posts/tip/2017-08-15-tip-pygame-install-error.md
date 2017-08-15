---
layout: post
section-type: post
title: tip - pygame install error
category: tip
tags: [ 'tip' ]
---

오늘 가족과 함께 시간을 보내느라 공부할 시간이 조금밖에 나지 않았습니다.

그래서 지금 진행하고 있는 공부할 부분은 오늘 진행하기엔 시간이 부족할 것 같아서

pyGame을 간단히 실행보려고 했습니다.

가상환경을 따로 설정해두고 pygame을 설치합니다.

```
pip install pygame
```

하지만!! ERROR가 발생하였습니다.

```
...
src/scrap.c:27:10: fatal error: 'SDL.h' file not found
#include "SDL.h"
         ^
1 error generated.
error: command 'clang' failed with exit status 1

----------------------------------------
Command "/usr/local/var/pyenv/versions/3.5.2/envs/game/bin/python -u -c "import setuptools, tokenize;__file__='/private/var/folders/63/cd4_xzc12lg7vjqb1hqltffr0000gn/T/pip-build-bavgp3j0/pygame/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /var/folders/63/cd4_xzc12lg7vjqb1hqltffr0000gn/T/pip-70z7iyq7-record/install-record.txt --single-version-externally-managed --compile --install-headers /usr/local/var/pyenv/versions/3.5.2/envs/game/include/site/python3.5/pygame" failed with error code 1 in /private/var/folders/63/cd4_xzc12lg7vjqb1hqltffr0000gn/T/pip-build-bavgp3j0/pygame/
```

...

뭐지... 역시 안될땐 구글신과 스택오버플로죠!

[스택오버플로 답변](https://stackoverflow.com/questions/17869101/unable-to-install-pygame-using-pip){:target="`_`blank"}

많은 답변들이 달렸는데 저의 경우는 마지막의 케이스였습니다.  

현재 사용중엔 OS는 macOS Sierra 였고, macOS 마다 간혹 있는 오류들 중 하나인 것 같습니다.

먼저 Brew를 통해 Mercurial을 설치합니다.
```
brew install mercurial
```
그런 다음 pyGame 종속성을 설치합니다.
```
brew install sdl sdl_image sdl_mixer sdl_ttf smpeg portmidi
```
그리고 pip3로 pyGame을 설치합니다.
```
pip3 install pygame
```

이것으로 설치 끝!!

정상 작동을 위한 샘플 코드를 실행합니다.

```python
import pygame, sys
pygame.init() #load pygame modules
size = width, height = 320, 240 #size of window
speed = [2, 2] #speed and direction
screen = pygame.display.set_mode(size) #make window
s=pygame.Surface((100,50)) #create surface 100px by 50px
s.fill((33,66,99)) #color the surface blue
r=s.get_rect() #get the rectangle bounds for the surface
clock=pygame.time.Clock() #make a clock
while 1: #infinite loop
        clock.tick(30) #limit framerate to 30 FPS
        for event in pygame.event.get(): #if something clicked
                if event.type == pygame.QUIT: #if EXIT clicked
                        sys.exit() #close cleanly
        r=r.move(speed) #move the box by the "speed" coordinates
        #if we hit a  wall, change direction
        if r.left < 0 or r.right > width: speed[0] = -speed[0]
        if r.top < 0 or r.bottom > height: speed[1] = -speed[1]
        screen.fill((0,0,0)) #make redraw background black
        screen.blit(s,r) #render the surface into the rectangle
        pygame.display.flip() #update the screen
```

[swharden.com](http://www.swharden.com/){:target="`_`blank"} 이 곳에 좋은 샘플 코드들이 많이 있으므로, 한 번쯤 들려서 이것 저것 구경해 봐도 좋습니다.
