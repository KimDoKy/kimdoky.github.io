---
layout: post
section-type: post
title: devops - Latest Task Definition을 기준으로 새로운 Task Definition 등록 후 Deploy하기
category: deploy
tags: [ 'deploy' ]
---

## Introduction

aws cli를 통해 ecs service를 업데이트하면 가장 마지막에 성공한 revision을 기본 revision으로 업데이트가 진행됩니다.
task definition이 업데이트되어도 배포된 적이 없다면 업데이트된 revision으로 업데이트가 되지 않습니다.

## Solution

가장 최신의 task definition 정보를 받아와서 다시 등록하고, 해당 revision 정보를 ecs update의 param으로 넣어주면 됩니다.
aws cli로부터 받은 latest task definition을 그대로 등록한다면 양식에 맞지 않기 때문에 task definition form에 맞추어 편집하여 등록합니다.

- [AWS DOC](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RegisterTaskDefinition.html)


```python
import json
import sys

# latest task defination을 registry용으로 편집
def create_task_definition():
    ecr_name, tag = sys.argv[2], sys.argv[3]

    with open('./task-definition-origin.json', 'r') as file:
        data = json.load(file)

    data['containerDefinitions'][0]['image'] = f"{ecr_name}:{tag}"

    delete_attrs = [
        'revision',
        'registeredAt',
        'requiresAttributes',
        'registeredBy',
        'status',
        'taskDefinitionArn',
        'compatibilities',
    ]
    for i in delete_attrs:
        del data[i]

    with open('./task-definition.json', 'w') as file:
        json.dump(data, file, indent=4)

    return

# Python 스크립트를 커맨드의 인자로 넣으려면 화면으로 출력해야 한다.
def get_task_definition_arn():
    with open('./task-definition-origin.json', 'r') as file:
        data = json.load(file)

    split_str = data['taskDefinitionArn'].split(":")
    split_str[-1] = str(int(split_str[-1]) + 1)
    print(":".join(split_str))
    return

# 스크립트 파일 하나고 task 작성과 출력
if __name__ == "__main__":
    run_type = sys.argv[1]

    if run_type == "create":
        create_task_defination()
    elif run_type == "get":
        get_task_definition_arn()
```

```yaml
# Github action

     - name: Create Task Definition
         run: |
           aws ecs describe-task-definition --task-definition p3-ecs-tasks --query taskDefinition > task-definition-origin.json
           python3 task_definition.py create $ECR_IMAGE $(cat buildInfo)
 
       - name: Register Task Definition
         run: aws ecs register-task-definition --cli-input-json "$(cat < ./task-definition.json)"
 
       - name: Deploy ECS service
         run: aws ecs update-service --region ${{secrets.AWS_REGION}} --cluster ${{secrets.AWS_ECS_CLUSTER}} --service $AWS_ECS_SERVICE --force-new-deployment --task-definition $(python3 task_definition.py get)
 ```
