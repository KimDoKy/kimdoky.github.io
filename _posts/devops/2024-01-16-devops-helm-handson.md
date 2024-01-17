---
layout: post
section-type: post
title: Helm Hands On
category: devops
tags: [ 'k8s', 'helm' ]
---

## Install Helm CLI
```bash
# for Mac
$ brew install helm

# other linux
$ curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
$ chmod 700 get_helm.sh     (== chmod +x get_helm.sh)
$ ./get_helm.sh

$ helm version
```
## Install Helm Chart
```bash
# add repo
$ helm repo add bitnami https://charts.bitnami.com/bitnami
"bitnami" has been added to your repositories
$ helm repo list
NAME    URL
bitnami https://charts.bitnami.com/bitnami

## remove repo
$ helm repo remove [repo-name]

# search repo
$ helm search repo bitnami
...

# helm install [name] [chart] [flags]
$ helm install my-release bitnami/wordpress
NAME: my-release
LAST DEPLOYED: Tue Jan 16 22:11:03 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: wordpress
CHART VERSION: 19.1.0
APP VERSION: 6.4.2

** Please be patient while the chart is being deployed **
...

# helm 조회
$ helm ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART             APP VERSION
my-release      default         1               2024-01-16 22:11:03.908208464 +0900 KST deployed        wordpress-19.1.0  6.4.2

$ kubectl get po
NAME                                     READY   STATUS    RESTARTS   AGE
my-release-mariadb-0                     0/1     Pending   0          8m35s
my-release-wordpress-bd87c998b-p7lz9     0/1     Pending   0          8m36s

$ kubectl get cm
NAME                 DATA   AGE
kube-root-ca.crt     1      22d
my-release-mariadb   1      9m46s

$ kubectl get svc
NAME                   TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
kubernetes             ClusterIP      10.96.0.1       <none>        443/TCP                      22d
my-release-mariadb     ClusterIP      10.104.108.96   <none>        3306/TCP                     10m
my-release-wordpress   LoadBalancer   10.104.88.7     <pending>     80:31380/TCP,443:31234/TCP   10m

$ kubectl get pvc
NAME                        STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
data-my-release-mariadb-0   Pending                                                     10m
my-release-wordpress        Pending                                                     10m

$ kubectl get secret
NAME                               TYPE                 DATA   AGE
my-release-mariadb                 Opaque               2      11m
my-release-wordpress               Opaque               1      11m
sh.helm.release.v1.my-release.v1   helm.sh/release.v1   1      11m

## minikube로 실행시 tunnel을 통해 external ip를 생성할 수 있다.
$ minikube tunnel
$ kubectl get svc
```
## Upgrade Helm Chart
```bash
# helm upgrade [release] [chart] [flags]
# ex) helm upgrade -f myvalues.yaml -f override.yaml redis ./redis
# ex) helm upgrade --set foo=bar --set foo=newbar redis ./redis
$ cat myvalues.yaml
replicaCount: 3

$ helm ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART             APP VERSION
my-release      default         1               2024-01-16 22:11:03.908208464 +0900 KST deployed        wordpress-19.1.0  6.4.2

$ helm upgrade my-release bitnami/wordpress -f myvalues.yaml
Release "my-release" has been upgraded. Happy Helming!
NAME: my-release
LAST DEPLOYED: Tue Jan 16 22:39:49 2024
NAMESPACE: default
STATUS: deployed
REVISION: 2
TEST SUITE: None
NOTES:
CHART NAME: wordpress
CHART VERSION: 19.1.0
APP VERSION: 6.4.2

** Please be patient while the chart is being deployed **
...

$ kubectl get po
NAME                                     READY   STATUS    RESTARTS   AGE
my-release-mariadb-0                     0/1     Pending   0          29m
my-release-wordpress-bd87c998b-6hmbf     0/1     Pending   0          22s
my-release-wordpress-bd87c998b-mj9gc     0/1     Pending   0          22s
my-release-wordpress-bd87c998b-p7lz9     0/1     Pending   0          29m

$ helm ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART             APP VERSION
my-release      default         2               2024-01-16 22:39:49.207040692 +0900 KST deployed        wordpress-19.1.0  6.4.2

$ kubectl get deploy
NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
my-release-wordpress     0/3     3            0           31m

## revision을 secret으로 따로 관리한다.
## rollback시 이를 사용하여 복구한다.
$ kubectl get secret
NAME                               TYPE                 DATA   AGE
my-release-mariadb                 Opaque               2      32m
my-release-wordpress               Opaque               1      32m
sh.helm.release.v1.my-release.v1   helm.sh/release.v1   1      32m
sh.helm.release.v1.my-release.v2   helm.sh/release.v1   1      3m37s

# release가 가지고 있는 값 조회
# helm get [command]
## command: all, hooks, manifest, notes, values
$ helm get values my-release
USER-SUPPLIED VALUES:    # user가 추가한 값. 기본과 다르다는 것을 알 수 있음
replicaCount: 3

## revision을 명시하여 바뀐 점을 알 수 있다.
$ helm get values my-release --revision 1
USER-SUPPLIED VALUES:
null

# revision의 다른 점을 조회하는 diff 플러그인이 있다.
## diff 플러그인 설치
$ helm plugin install https://github.com/databus23/helm-diff
# helm diff [command]
## command: release, revision, rollback, upgrade, version
$ helm diff revision my-release 1 2
default, my-release-wordpress, Deployment (apps) has changed:
...
    strategy:
      type: RollingUpdate
-   replicas: 1
+   replicas: 3
    template:
...
```
## RollBack Helm Chart
```bash
$ helm ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART             APP VERSION
my-release      default         2               2024-01-16 22:39:49.207040692 +0900 KST deployed        wordpress-19.1.0  6.4.2

$ cat myvalues.yaml
replicaCount: 3

# helm history
$ helm history my-release
REVISION        UPDATED                         STATUS          CHART                   APP VERSION     DESCRIPTION
1               Tue Jan 16 22:11:03 2024        superseded      wordpress-19.1.0        6.4.2           Install complete
2               Tue Jan 16 22:39:49 2024        deployed        wordpress-19.1.0        6.4.2           Upgrade complete

# helm rollback <release> [revision]
## --dry-run : 실제로 수행하지 않고 수행되었을 때의 결과만 알려준다.
$ helm rollback my-release 1 --dry-run
Rollback was a success! Happy Helming!
$ helm rollback my-release 1
Rollback was a success! Happy Helming!
$ helm history my-release
REVISION        UPDATED                         STATUS          CHART                   APP VERSION     DESCRIPTION
1               Tue Jan 16 22:11:03 2024        superseded      wordpress-19.1.0        6.4.2           Install complete
2               Tue Jan 16 22:39:49 2024        superseded      wordpress-19.1.0        6.4.2           Upgrade complete
3               Wed Jan 17 08:12:24 2024        deployed        wordpress-19.1.0        6.4.2           Rollback to 1
## revision 1과 같은 상태인 것을 알 수 있다.
$ helm get values my-release --revision 3
USER-SUPPLIED VALUES:
null
$ kubectl get deploy
NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
my-release-wordpress     0/1     1            0           10h
nfs-client-provisioner   1/1     1            1           17d
$ kubectl get po
NAME                                     READY   STATUS    RESTARTS   AGE
my-release-mariadb-0                     0/1     Pending   0          10h
my-release-wordpress-bd87c998b-p7lz9     0/1     Pending   0          10h
```
## Delete Helm Chart
```bash
# helm uninstall
## alias: uninstall, del, delete, un
## --key-history : 자원을 모두 지우지만, 지우는 것도 revision으로 관리하여 복구할 수 있다.(secret 유지)
$  helm delete my-release --keep-history
release "my-release" uninstalled
# 관련 자원들이 모두 삭제되었다.
$ helm ls
NAME    NAMESPACE       REVISION        UPDATED STATUS  CHART   APP VERSION
$ kubectl get po
No resources found in default namespace.
$ kubectl get svc
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   22d
$ kubectl get cm
NAME               DATA   AGE
kube-root-ca.crt   1      22d

# history를 조회하면 revision이 secret을 통해 관리되고 있다.
$  helm history my-release
REVISION        UPDATED                         STATUS          CHART                   APP VERSION     DESCRIPTION
1               Tue Jan 16 22:11:03 2024        superseded      wordpress-19.1.0        6.4.2           Install complete
2               Tue Jan 16 22:39:49 2024        superseded      wordpress-19.1.0        6.4.2           Upgrade complete
3               Wed Jan 17 08:12:24 2024        superseded      wordpress-19.1.0        6.4.2           Rollback to 1
4               Wed Jan 17 08:19:16 2024        uninstalled     wordpress-19.1.0        6.4.2           Uninstallation complete
$ kubectl get secret
NAME                               TYPE                 DATA   AGE
sh.helm.release.v1.my-release.v1   helm.sh/release.v1   1      10h
sh.helm.release.v1.my-release.v2   helm.sh/release.v1   1      9h
sh.helm.release.v1.my-release.v3   helm.sh/release.v1   1      14m
sh.helm.release.v1.my-release.v4   helm.sh/release.v1   1      7m23s

## 다시 rollback
$ helm history my-release
REVISION        UPDATED                         STATUS          CHART                   APP VERSION     DESCRIPTION
1               Tue Jan 16 22:11:03 2024        superseded      wordpress-19.1.0        6.4.2           Install complete
2               Tue Jan 16 22:39:49 2024        superseded      wordpress-19.1.0        6.4.2           Upgrade complete
3               Wed Jan 17 08:12:24 2024        superseded      wordpress-19.1.0        6.4.2           Rollback to 1
4               Wed Jan 17 08:19:16 2024        uninstalled     wordpress-19.1.0        6.4.2           Uninstallation complete
5               Wed Jan 17 08:29:18 2024        deployed        wordpress-19.1.0        6.4.2           Rollback to 4
$ kubectl get po
NAME                                     READY   STATUS    RESTARTS   AGE
my-release-mariadb-0                     0/1     Pending   0          23s
my-release-wordpress-bd87c998b-5lbqz     0/1     Pending   0          23s
my-release-wordpress-bd87c998b-fmsbq     0/1     Pending   0          23s
my-release-wordpress-bd87c998b-gj26p     0/1     Pending   0          23s

## namespace를 지우면 해당 secret 및 revision도 삭제된다.
# 완전 삭제
## 복구 불가
$ helm ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
my-release      default         5               2024-01-17 08:29:18.617890062 +0900 KST deployed        wordpress-19.1.0        6.4.2
$ helm delete my-release
release "my-release" uninstalled
$ helm ls
NAME    NAMESPACE       REVISION        UPDATED STATUS  CHART   APP VERSION
$ helm history my-release
Error: release: not found
$ kubectl get secret
No resources found in default namespace.
```
