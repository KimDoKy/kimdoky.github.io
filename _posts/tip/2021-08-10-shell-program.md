---
layout: post
section-type: post
title: Linux - Shell Programming Syntax
category: tip
tags: [ 'tip' ]
---

## run shell script

- `sh script.sh`
- `source script.sh`
- `. script.sh`
- `chmod 755 script.sh` 후 `./script.sh`
 - 스크립트 안에서 다른 스크립트를 실행하기 위해 필요

## comment

- 앞에 `#`를 붙임

```bash
#!/bin/sh
# 주석입니당
```

## variable

- `var=value`
 - `${name}`: name 변수 사용
 - `${name:=value}`: name 변수가 null이면 value를 할당. 주로 변수 기본값 지정시 사용
 - `${name:+value}`: name 변수가 null이 아니면 value를 사용(저장 x)
 - `${name:-value}`: name 변수가 null이면 value를 사용 (저장 x)
 - `${name:?value}`: name 변수가 null이면 error 를 발생시키고 value를 반환
 - `${#name}`: name의 문자열 길이
 - `${name:offset}`: offset 만큼 삭제후 반환
 - `${name:offset:length}`: offset 만큰 삭제후, length 만큼의 뒤 값을 반환

- argument
 - `$0`: 실행된 셸 스크립트명
 - `$1`, `$2`: 스크립트에 넘겨진 1, 2번째 인자
 - `$#`: 인자 개수
 - `$$`: 셸 스크립트의 PID
 - `$*`: 인자 전체 중 IFS 변수의 첫번째 문자로 구분
 - `$@`: 위와 동일(IFS 환경 변수 사용 안함)
 - `$?`: 실행뒤 반환 값. 0 = True / 1 = False
 - `$-`: 현재 Shell이 호출될 때 사용한 옵션들

### variable command

- set: 셸 변수 출력
- env: 환경 변수를 출력
- export: 전역 변수
- unset: 변수 제거

## echo - escape

- `-e` 옵션으로 excape 특수문자 사용 가능
 - `\f`: Formfeed. 앞 문자열만큼 열을 밀어서 이동
 - `\n`: New line
 - `\r`: Carriage Return. 앞 문자열의 앞에서부터 뒷 문자열만큼 대체하여 반환
 - `\t`: Tap

## condition

### if

```bash
if [condition]
then
    <commands>
fi
```

```bash
if [ccondition]
then
    <commands>
else
    <commands>
fi
```

```bash
if [condition]
then
    <commands>
enif [condition]
then
    <commands>
else
    <commands>
fi
```

### case

```bash
case [string]
in
    1) <commands>;;
    2) <commands>;;
    ...
esac
```

### select

- Korn Shell과 Bash에만 존재

```bash
select <var> in <value1>, <value2>, ...
    do
        <commands>
    done
```

선택된 값을 변수로 지정하고, 실행한다.

## iteration

### for

```bash
for <var> in <value1>, <value2>
    do
        <commands>
    done
```

### while

```bash
while [condition]
    do
        <commands>
    done
```

### until

```bash
until [condition]
    do
        <commands>
    done
```

## function

```bash
<function_name>()
{
    <commands>
}
```

```bash
function <function_name>
{
    <commands>
}
```

## pattern

- `${var#pattern}`: var에서 pattern과 일치하는 최소 부분을 제거하고 반환
- `${var##pattern}`: var에서 pattern과 일치하는 최대 부분을 제거하고 반환
- `${var%pattern}`: var의 뒤에서부터 pattern과 일치하는 최소 부분을 제거하고 반환
- `${var%%pattern}`:  var의 뒤에서부터 pattern과 일치하는 최대 부분을 제거하고 반환
