---
layout: post
section-type: post
title: GithubActions/AWS - Github Actions에서 MFA 설정된 계정으로 AWS 접근하기
category: devops
tags: [ 'devops', 'aws', 'github', 'actions' ]
---

## Introduction

github actions은 Github에서 직접 CI/CD 작업을 자동화할 수 있는 도구입니다.

github actions으로 통해 테스트, 빌드, 배포 등의 작업을 자동화 할 수 있습니다.

유즈케이스에 따라 다르겠지만 복잡한 Jenkins 설정에 비해 많은 부분이 간소화되었습니다.


AWS와 같은 클라우드 계정은 보안을 위해 MFA 설정을 하게 됩니다.

MFA(Multi-Factor Authentication)은 두 가지 이상의 인증을 결합한 보안절차로, 물리적 장치 등으로 추가적인 인증을 진행합니다.

하지만 MFA는 매 요청마다 일회용 코드를 입력해야 하기 때문에 github actions과 같은 자동화에는 적용하기 어렵습니다.

---
## solution

AWS IAM의 Role을 이용하면 MFA를 유지하면서 자동화를 할 수 있습니다.

IAM Role은 보안 자격 증명을 가진 엔티티로, IAM Role을 통해 권한을 일시적으로 위임받는 방식으로 해결할 수 있습니다.

MFA가 활성화된 사용자가 Role을 승인하면  github actions은 Role을 통해 AWS에 접근할 수 있습니다.

- IAM Role 생성

github actions에서 AWS 리소스에 접근하는데 필요한 권한을 설정합니다.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::account-id:user/user-name"},
      "Action": "sts:AssumeRole",
      "Condition": {"Bool": {"aws:MultiFactorAuthPresent": "true"}}
    }
  ]
}
```

- Trust Policy 설정

MFA가 활성화된 사용자가 cli를 통해 승인해야 합니다.

```bash
aws sts assume-role --role-arn "arn:aws:iam::123456789012:role/YourRole" --role-session-name "GitHubActionsSession" --serial-number "arn:aws:iam::123456789012:mfa/user" --token-code 123456
```

승인하면 `AccessKeyId`, `SecretAccessKey`, `SessionToken` 값을 얻을 수 있습니다.

- Github Actions 설정
위 과정을 통해 얻게된  `AccessKeyId`, `SecretAccessKey`, `SessionToken` 을 Github의 Secret에 등록후 참조해서 사용하면 됩니다.

---
## Conclusion

MFA를 사용하지 않는 배포 전용 계정을 생성하기도 하지만, 위 방법을 통해 MFA를 유지하여 보안을 유지할 수 있습니다.
