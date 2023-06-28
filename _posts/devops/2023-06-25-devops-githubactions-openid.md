---
layout: post
section-type: post
title: devops - AccessKey를 사용하지 않고 Github Actions에 AWS 인증하기
category: deploy
tags: [ 'deploy' ]
---

## Introduction

Access Key, Secret Key를 이용한 인증 방법은 널리 사용되지만, 경우에 따라 강한 보안이 필요한 경우 Access Key, Secret Key의 사용을 제한 받는 경우들이 있습니다.
이런 경우 OpenID Connect는 좋은 방안이 될 수 있습니다.

## Solution

OpenID는 OAuth 2.0 기반으로 상호 운용 가능한 인증 프로토콜입니다. OAuth라고 하면 어떤 프로세스로 동작하는지 감이 올겁니다.  
[OpenId](https://openid.net/developers/how-connect-works/)  

OpenID를 통해 AWS의 Access Key, Secret Key를 사용하지 않고 Role 기반의 Github Actions에서 AWS 인증이 가능합니다.

#### Identity providers 생성
- Provider type: OpenID Connect
- Provider URL: token.actions.githubusercontent.com
- Click to Get thumbprint
- Audience: sts.amazonaws.com

#### Role 생성
- Trusted entity type: Web Identity
- Identity provider: token.actions.githubusercontent.com
- Audience: sts.amazonaws.com
- Add permissions
- Role Name

#### Role Trust relationshops 수정

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::....:oidc-provider/token.actions.githubusercontent.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringLike": {
                    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
                    "token.actions.githubusercontent.com:sub": "repo:<Git Repo>:<Branch>"
                }
            }
        }
    ]
}
```

#### Github actions용 yaml 파일 작성

.github/workflows 안에 yaml 파일을 작성합니다.

```yaml
name: CI/CD for AWS, Azure with Github Action
run-name: ${ github.actor } is testing
on: push

env:
  ECR_IMAGE: ${ secrets.AWS_ID }.dkr.ecr.${ secrets.AWS_REGION }.amazonaws.com/${ secrets.ECR_REPO }:${ github.sha }
  ACR_IMAGE: ${ secrets.AZURE_ARC }.azurecr.io/${ vars.APP_NAME }:latest

jobs:
  checkout:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: ${ secrets.AWS_ARN }
          role-session-name: OIDCForGithubActionCICD
          aws-region: ${ secrets.AWS_REGION }
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      - name: Build, Push Docker image
        run: |
          docker build -t $ECR_IMAGE .
          docker push $ECR_IMAGE
      - name: Deploy ECS service
        run: aws ecs update-service --region ${secrets.AWS_REGION} --cluster ${secrets.AWS_ECS_CLUSTER} --service ${secrets.AWS_ECS_SERVICE} --force-new-deployment
```

![]({{ site.url }}/img/post/deploy/cicd/github_actions.png)

---

- [github actions docs](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [ref](https://www.youtube.com/watch?v=k2Tv-EJl7V4&ab_channel=glich.stream)
