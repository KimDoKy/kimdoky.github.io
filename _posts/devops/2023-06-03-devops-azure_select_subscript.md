---
layout: post
section-type: post
title: Azure - Subscriptions 선택하기
category: devops
tags: [ 'devops', 'cli', 'azure' ]
---

## Introduction

Azure는 [Active Directory](https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-whatis)라는 개념이 있습니다.  

AWS의 경우 계정별로 프로필을 선택하지만, Azure는 계정이 아닌 구독을 관리해주어야 합니다.

---
## Solution

```zsh
# 구독 조회
$ az account list --output table
Name                       CloudName    SubscriptionId                        TenantId                              State    IsDefault
------------------------  -----------  ------------------------------------  ------------------------------------  -------  -----------
Azure Subscription for G  AzureCloud   *********-****-****-****-***********  ******-****-****-****-***********     Enabled  True
Azure Pass - Sponsorship  AzureCloud   *********-****-****-****-***********  ******-****-****-****-***********     Enabled  False

# 구독 셋팅
$ az account set --subscription "Azure Pass - Sponsorship"

# 구독 확인
$ az account list --output table
Name                       CloudName    SubscriptionId                        TenantId                              State    IsDefault
------------------------  -----------  ------------------------------------  ------------------------------------  -------  -----------
Azure Subscription for G  AzureCloud   *********-****-****-****-***********  ******-****-****-****-***********     Enabled  False
Azure Pass - Sponsorship  AzureCloud   *********-****-****-****-***********  ******-****-****-****-***********     Enabled  True
```

---

## Conclusion

AWS와 Azure는 클라우드라는 영역에서 비슷해보이지만 근본적인 부분부터 많은 차이가 있습니다.  

AWS가 클라우드 영역에서 업계 1위라고는 하지만 Multi Cloud가 점점 중요해지면서 여러 클라우드를 알아 둘 필요가 있습니다.  

Azure도 더 많이 사용해보고 이해를 해 둘 필요가 있습니다.
