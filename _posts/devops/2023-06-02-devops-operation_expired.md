---
layout: post
section-type: post
title: Terraform/Azure - Operation expired, Azure Container 배포 실패
category: devops

tags: [ 'devops', 'terraform', 'azure' ]
---

## Introduction

리소스를 생성시 `Error details: Operation expired.` 를 만나는 경우가 간혹 있습니다.

Azure로 Container App을 생성하다 약 10분의 시간이 지나면 실패 및 위의 메시지를 만나게 되었습니다.

`Error details: Operation expired.`의 원인은 클라우드의 API의 처리가 오래 걸리거나 Terraform이 API 응답을 기다리는 시간을 초과한 경우에 발생하는 것으로 알려져있습니다.

이런 경우 생성하려던 리소스는 생성이 되어, 다시 apply를 시도하면 이미 존재하는 리소스라는 에러가 발생하게 됩니다.

---
## Solution

- terraform의 상태를 업데이트

`terraform apply -refresh-only` (`terraform refresh`는 0.15.0 버전까지만 사용)

- 자원 생성 대기 시간 조정

timeouts 블록을 해당 리소스에 추가합니다.

```
resource "azurerm_container_app" "example" {
  // ...

  timeouts {
    create = "60m"
    delete = "2h"
  }
}
```
위 솔루션으로도 해결되지 않는다면 

- 해당 클라우드의 api를 최신버전으로 변경해봐야 합니다.

```
terraform {
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = "=3.58.0"  <------------
        }
    }
	...
```

하지만!!!!!! 저는 해결이 되지 않았습니다.

이럴땐...

- 차근차근 디버깅해보기..

마지막으로 성공했을 때와 실패 했을 때를 비교해보니 ingress 설정이 있었습니다.

해당 이슈는 구글링을 통해 확인 및 해결되었습니다.

ingress 설정 중에 트래픽 가중치를 할당하려고 할 때 revision hash를 포함하지 않아 revision을 찾는 데 실패하여 timeout이 되었습니다.

https://github.com/hashicorp/terraform-provider-azurerm/issues/20435

해당 이슈는 `traffic_weight`에서 `latest_revision`을 `true`로 설정해주면 해결이 됩니다.

```
  ingress {
    ...
    traffic_weight {
      latest_revision = true
	  ...
    }
  }
```

---

## Conclusion

Terraform, Azure 내공 += 1
