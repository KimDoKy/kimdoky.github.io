---
layout: post
section-type: post
title: devops - GITHUB_OUTPUT 사용 불가?
category: deploy
tags: [ 'deploy' ]
---

## Introduction

Github Actions를 사용하다 보면 이전 스텝에서 진행한 값들을 참조해야 할 때가 있습니다.
이때 `GITHUB_OUTPUT` 이라는 변수를 활용하여 해결할 수 있습니다.

```yaml
jobs:
  job1:
    runs-on: ubuntu-latest
    # Map a step output to a job output
    outputs:
      output1: ${{ steps.step1.outputs.test }}
      output2: ${{ steps.step2.outputs.test }}
    steps:
      - id: step1
        run: echo "test=hello" >> "$GITHUB_OUTPUT"
      - id: step2
        run: echo "test=world" >> "$GITHUB_OUTPUT"
  job2:
    runs-on: ubuntu-latest
    needs: job1
    steps:
      - env:
          OUTPUT1: ${{needs.job1.outputs.output1}}
          OUTPUT2: ${{needs.job1.outputs.output2}}
        run: echo "$OUTPUT1 $OUTPUT2"
```

- [Github Docs](https://docs.github.com/en/actions/using-jobs/defining-outputs-for-jobs)


하지만 github-hosted가 아닌 self-hosted라면 얘기가 복잡해집니다.
self-hosted를 사용하면 `GITHUB_OUTPUT`이라는 변수를 활용할 수 없을 수도 있습니다.
- [stackoverflow](https://stackoverflow.com/questions/74149193/github-output-directory-nonexistent-self-hosted-runner/76624766#76624766)

self-hosted의 runner의 버전을 올리면 가능할 수 있지만, 여러 이유들(해당 self-hosted에서 여러 runner가 돌고 있는 등)로 업그레이드가 어려울 수 있습니다.


여러 가지 편법을 시도해봅니다.

```bash
# way1.
## step1.
export build_info=$(.....)
## step2.
echo $build_info
## result: 실패

# way2.
## step1.
echo "export build_info=$(...)" >> ~/.bashrc
source ~/.baserc
## step2.
echo $build_info
## result: 실패
```

## Solution

태그명 같은 경우 글로벌 변수처럼 전체적인 과정에서 여러 번 사용하기 떄문에 해당 결과를 파일로 생성하고 읽어오는 방식으로 해결하였습니다.

```bash
## step1
echo `...` > build_info
## step2
echo $(cat build_info)
## resutl: 성공
```
