---
layout: post
section-type: post
title: 컴퓨터 공학 - Basic Registers
category: algorithm
tags: [ 'algorithm' ]
---

# Basic Registers

## 어큐뮬레이터(Accumulator.AC.누적기)
- 연산 결과를 기억하는 레지스터
- 연산 결과를 그 다음 연산에 바로 이용할 수 있음

## 명령 레지스터(Instruction Register.IR) / 명령 디코더
- 현재 실행중인 명령의 내용을 기억
- 명령을 조합하여 한번에 연속적으로 명령을 실행함

## 스테이터스 레지스터(Program Status Word Reg.PSWR)
- CPU는 연산 결과에 따라 프로그램의 순서를 바꾸거나 입출력을 제어하는데,
판단 기준이 플래그(1bit)이다.
- 이 플래스를 8 or 16 bit로 만든 것이 '스테이터스 레지스터'이다.
- 시스템 내부 상태(오버/언더플로, 자리올림, 계산상태, 인터럽트)를 기억

## 수식 레지스터(Base, Index)
- 특정 어드레싱 모드에서 필요한 레지스터
- Base Reg : 명령에 따라 지정되는 오퍼랜드가 어떤 기준 값에 대하여 설정될 때 그 기준값을 결정
- index Reg : 현재의 프로그램 카운터에 특정한 값을 추가할 때, 오퍼랜드에 영향을 미치는 정수를 넣어두는 기능

## 데이터 레지스터(Data Reg)
- 연산에 사용될 데이터를 기억한다.

## Temp 레지스터
- 일시적으로 데이터를 기억

## 프로그램 카운터(Program Counter.PC)
- 다음에 실행할 명령의 어드레스를 기억

## 스택 포인트(Stack Point)
- 마지막으로 조작한 스택 어드레스를 기억

## 시프트 레지스터(Shift Reg)
- 저장된 값을 1 bit씩 자리이동 한다.
- 왼쪽 시프트: 2^n 곱셈 / 오른쪽 시프트: 2^n 나눗셈

## 메모리 주소 레지스터(Memory Address Reg.MAR)
- 기억장치의 데이터 주소를 기억

## 메모리 버퍼 레지스터(Memory Buffer Reg.MBR)
- 기억장치의 데이터가 CPU에서 처리되기 위해 기억
