---
layout: post
section-type: post
title: Install Jupyter Notebook and shortcuts
category: tip
tags: [ 'tip' ]
---

[Jupyter 공식 페이지](http://jupyter.readthedocs.io/en/latest/install.html){:target="\_blank"}


## Jupyter Notebook ??

Python을 돌릴 수 있는 IDE(?) tool입니다. markdown으로 문서 작업도 가능하고, python 코드를 입력 및 실행도 가능합니다. 작성한 파일은 jupyter 파일(ipynb)으로 저장되는데 git에 올리면 편집한 화면 그대로 보여주기 때문에 프리젠테이션 등에서 유용하게 사용할 수 있는 tool입니다.

## Jupyter Notebook Install

```
pip install jupyter
```

Anaconda를 설치하면 기본적으로 같이 설치됩니다.  
Anaconda에는 jupyter notebook 이외에도 데이터 사이언스에서 사용하는 많은 라이브러리가 있습니다만.  
가볍게 입문(?)용을 pip로 설치합니다.

## Run Jupyter Notebook

```
jupyter notebook
```
## Display

![]({{site.url}}/img/post/tip/jupyter/1.png)

실행하면 브라우저를 통해 대쉬보드를 볼 수 있습니다.  
[new] 를 눌러보면 Python3, text file, folder, terminal 을 볼 수 있습니다. 모두 실행이 가능합니다.  
그냥 내 컴퓨터 안에 새로운 노트북이 있다는 느낌입니다. 그래서 jupyter notebook 인가 봅니다. 편리하네요.  
인터페이스도 간단해서 굳이 튜토리얼이나 강좌같은걸 볼 필요가 있을까 싶네요.

### Shortcuts

Command Mode (press Esc to enable)| || Edit Mode (press Enter to enable)| |
---|---|---|---|---
Enter | enter edit mode	|| Tab | code completion or indent
Shift-Enter | run cell, select below	||	Shift-Tab | tooltip
Ctrl-Enter  | run cell || Ctrl-] | indent
Alt-Enter   | run cell, insert below || Ctrl-[ | dedent
Y |	to code	|| Ctrl-A | select all
M |	to markdown	|| Ctrl-Z | undo
R | to raw	|| Ctrl-Shift-Z | redo
1 | to heading 1	||	Ctrl-Y 	| redo
2	| to heading 2	||	Ctrl-Home |	 go to cell star
3	| to heading 3	||	Ctrl-Up 	| go to cell start
4 | to heading 4	||	Ctrl-End 	| go to cell end
5	| to heading 5	||	Ctrl-Down 	| go to cell end
6 | to heading 6	||	Ctrl-Left 	| go one word left
Up |	select cell above || Ctrl-Right |	 go one word right
K | select cell above	|| Ctrl-Backspace | delete word before
Down | select cell below ||	Ctrl-Delete  | delete word after
J | select cell below	|| Esc | command mode
A | insert cell above	||	Ctrl-M | command mode
B | insert cell below	|| Shift-Enter | run cell, select below
X | cut selected cell	|| Ctrl-Enter |	 run cell
C | copy selected cell || Alt-Enter |	run cell, insert below
Shift-V | paste cell above || Ctrl-Shift-Subtract | split cell
V | paste cell below	|| Ctrl-Shift-- | split cell
Z | undo last cell deletion	|| Ctrl-S |Save and Checkpoint
D,D |	delete selected cell || Up | move cursor up or previous cell
Shift-M |merge cell below	||	Down| move cursor down or next cell
S | Save and Checkpoint	|| Shift | ignore
Ctrl-S |	 Save and Checkpoint			
L |	 toggle line numbers				
O | toggle output				
Shift-O |	 toggle output scrolling
Esc |	 close pager				
Q |	 close pager				
H | show keyboard shortcut help			
I,I |	 interrupt kernel				
0,0 |	 restart kernel				
Space |	 scroll down				
Shift-Space |	 scroll up				
Shift |	 ignore			

사용하다보면 손에 익겠죠 뭐...ㅎ

## 하지만 jekyll과 궁합은 안좋습니다. 포스팅에 사용하려 했는데, 삽입하는 방법은 있지만 그 과정들 진행하면서까지 사용하기엔 너무 비효율적입니다. 나중에 스터디할때 더 활용해 봐야겠습니다.
