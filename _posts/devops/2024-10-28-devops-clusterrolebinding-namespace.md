---
layout: post
section-type: post
title: --namespace argument of clusterrolebinding
category: devops
tags: [ 'k8s', 'namespace', 'clusterrole', 'clusterrolebinding', 'rolebinding' ]
---

clusterrolebinding is scoped to the entire cluster regardless of namespace.  
However, in the [k8s documentation](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/kubectl_create_clusterrolebinding/), there is a `--namespae` argument in cluterrolebinding.

So I tested it.

```bash
controlplane ~ ➜  k create ns test-1
namespace/test-1 created

controlplane ~ ➜  k create ns test-2
namespace/test-2 created

controlplane ~ ➜  k get ns
NAME              STATUS   AGE
default           Active   32m
kube-node-lease   Active   32m
kube-public       Active   32m
kube-system       Active   32m
test-1            Active   15m
test-2            Active   15m

controlplane ~ ➜  k create sa tester -n test-1
serviceaccount/tester created

controlplane ~ ➜  k create clusterrole test-role --resource=pods --verb=get,list,create,delete -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  creationTimestamp: "2024-10-29T00:24:38Z"
  name: test-role
  resourceVersion: "1911"
  uid: eeef6968-2112-47d9-9812-a745682e7afb
rules:
- apiGroups:
  - ""
  resources:
  - pods
  verbs:
  - get
  - list
  - create
  - delete

controlplane ~ ➜  k create clusterrolebinding test-diff-ns-rolebinding --clusterrole=test-role --serviceaccount=test-1:tester -n test-2 -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  creationTimestamp: "2024-10-29T00:24:43Z"
  name: test-diff-ns-rolebinding
  resourceVersion: "1922"
  uid: 1bc66e49-937c-42be-99b3-8f09b560cd40
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: test-role
subjects:
- kind: ServiceAccount
  name: tester
  namespace: test-1

controlplane ~ ➜  k auth can-i create pods --as system:serviceaccount:test-1:tester
yes

controlplane ~ ➜  k auth can-i create pods --as system:serviceaccount:test-1:tester -n test-1
yes

controlplane ~ ➜  k auth can-i create pods --as system:serviceaccount:test-1:tester -n test-2
yes

controlplane ~ ➜  k delete clusterrolebinding test-diff-ns-rolebinding
clusterrolebinding.rbac.authorization.k8s.io "test-diff-ns-rolebinding" deleted

controlplane ~ ➜  k auth can-i create pods --as system:serviceaccount:test-1:tester
no

controlplane ~ ✖ k auth can-i create pods --as system:serviceaccount:test-1:tester -n test-1
no

controlplane ~ ✖ k auth can-i create pods --as system:serviceaccount:test-1:tester -n test-2
no

controlplane ~ ✖ k create rolebinding test-diff-ns-rolebinding --clusterrole=test-role --serviceaccount=test-1:tester -n test-2 -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  creationTimestamp: "2024-10-29T00:26:49Z"
  name: test-diff-ns-rolebinding
  namespace: test-2
  resourceVersion: "2098"
  uid: 26c6943a-ba5d-4a7c-9773-1b403a68fd6b
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: test-role
subjects:
- kind: ServiceAccount
  name: tester
  namespace: test-1

controlplane ~ ➜  k auth can-i create pods --as system:serviceaccount:test-1:tester
no

controlplane ~ ✖ k auth can-i create pods --as system:serviceaccount:test-1:tester -n test-1
no

controlplane ~ ✖ k auth can-i create pods --as system:serviceaccount:test-1:tester -n test-2
yes

```

`--namespace` exists, but when creating clusterrolebinding, the contents of the `--namespace` argument are not applied to yaml, and the actions for the set namespace are not applied.

I don't know the role of the `--namespcae` argument in the official documentation.

