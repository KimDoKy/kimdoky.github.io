---
layout: post
section-type: post
title: Windows에서 SSH으로 AWS 접속하기
category: deploy
tags: [ 'deploy' ]
---

AWS를 접속할때는 기본적으로 `*.pem` 파일을 키로 사용하여 접속한다.  

리눅스나 mac os에서는 ssh로 접속하면 되지만, 윈도우에서는 ssh로 접속하기 위해 PuTTY라는 프로그램을 사용하여 접속해야 한다.

하지만 PuTTY에서 pem 파일을 사용하여 접속하려 하면, ppk 파일을 요구한다. 이때 사용하는 것이 PuTTYgen이다.

![]({{ site.url }}/img/post/aws/putty1.jpg)
![]({{ site.url }}/img/post/aws/putty2.jpg)

`load` 버튼을 눌러 AWS에서 받은 키 파일을 선택한다. 파일 종류를 모두로 바꾸어 주어야 선택이 가능하다.

![]({{ site.url }}/img/post/aws/putty3.jpg)

`save private key` 버튼을 눌러 ppk 파일로 생성한다.

![]({{ site.url }}/img/post/aws/putty4.jpg)

이렇게 생성한 ppk 파일을 PuTTY의 [SSH]-[AUTH]-[Authenticaion parameters]에 불러온 후 접속한다.

![]({{ site.url }}/img/post/aws/putty5.jpg)

기본적으로 유저이름은 `ec2-user`이다. 접속후 유저이름을 입력하면 정상적으로 접속한다.

![]({{ site.url }}/img/post/aws/putty6.jpg)

웹서버를 실행하고, EC2 화면의 하단의 퍼블릭 IP를 접속하면 정상 동작을 확인할 수 있다.

![]({{ site.url }}/img/post/aws/putty7.png)

![]({{ site.url }}/img/post/aws/putty8.png)

> 아파치 서버로 테스트하였습니다.

## Apache 기본 셋팅

#### Linux Webserver Apache
sudo yum update
sudo yum install httpd
sudo service httpd start
sudo service httpd status
sudo service --status-all | grep httpd

#### Tomcat 5.x
- jdk
 - download jdk 64bit linux
 - install jdk 64bi
  - sudo yum install jdk....
 - path...
- tomcat zip
 - download tomcat
  - tar xvfz [filename]  : 압축 해제
 - start tomcat
 - simple.war
- beanstalk
