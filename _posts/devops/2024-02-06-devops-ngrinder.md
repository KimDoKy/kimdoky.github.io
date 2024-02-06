---
layout: post
section-type: post
title: nGrinder on K8S (for HPA)
category: devops
tags: [ 'k8s', 'ngrinder' ]
---

> [nGrinder Git](https://github.com/naver/ngrinder/wiki/Architecture)

## Architecture

![]({{ site.url }}/img/post/deploy/ngrinder/architecture.png)

## Run nGrinder

```yaml
# ngrinder controller
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: ngrinder-controller
  name: ngrinder-controller
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ngrinder-controller
  template:
    metadata:
      labels:
        app: ngrinder-controller
    spec:
      containers:
      - name: ngrinder
        image: ngrinder/controller:3.5.4
        ports:
        # Controller's web port
        - containerPort: 80
        # Health-chceck && Keepalive
        - containerPort: 16001
        # Agents's ports
        - containerPort: 12000
        - containerPort: 12001
        - containerPort: 12002
        - containerPort: 12003
        - containerPort: 12004
        - containerPort: 12005
        - containerPort: 12006
        - containerPort: 12007
        - containerPort: 12008
        - containerPort: 12009
---
apiVersion: v1
kind: Service
metadata:
  name: ngrinder-controller-svc
spec:
  type: LoadBalancer
  selector:
    app: ngrinder-controller
  ports:
 # each of port has own purpose. See above
  - name: port80
    port: 80
    targetPort: 80
  - name: port16001
    port: 16001
    targetPort: 16001
  - name: port12000
    port: 12000
    targetPort: 12000
  - name: port12001
    port: 12001
    targetPort: 12001
  - name: port12002
    port: 12002
    targetPort: 12002
  - name: port12003
    port: 12003
    targetPort: 12003
  - name: port12004
    port: 12004
    targetPort: 12004
  - name: port12005
    port: 12005
    targetPort: 12005
  - name: port12006
    port: 12006
    targetPort: 12006
  - name: port12007
    port: 12007
    targetPort: 12007
  - name: port12008
    port: 12008
    targetPort: 12008
  - name: port12009
    port: 12009
    targetPort: 12009
```

```yaml
# agent contoller
apiVersion: apps/v1
kind: DaemonSet
metadata:
  labels:
    app: ngrinder-agent
  name: ngrinder-agent
spec:
  selector:
    matchLabels:
      app: ngrinder-agent
  template:
    metadata:
      labels:
        app: ngrinder-agent
    spec:
      containers:
      - name: ngrinder-agent
        image: ngrinder/agent:3.5.4
        # LB ip or domain name or any reachable address to connect the nGrinder controller
        # args: [ngrinder.test.com:80] or [nnn.nnn.nnn.nnn:80]
        args: [34.66.75.175:80]
```

```basn
$ kubectl create ns ngrinder
namespace/ngrinder created
 
$ kubectl apply -f ngrinder-controller.yaml
deployment.apps/ngrinder-controller created
service/ngrinder-controller-svc created
 
$ kubectl get svc -n ngrinder
NAME                      TYPE           CLUSTER-IP    EXTERNAL-IP   PORT(S)                                                                                                                                                                                        AGE
ngrinder-controller-svc   LoadBalancer   10.80.4.214   34.66.75.175   80:31934/TCP,16001:32188/TCP,12000:32737/TCP,12001:32305/TCP,12002:30752/TCP,12003:30412/TCP,12004:32402/TCP,12005:30610/TCP,12006:32752/TCP,12007:32584/TCP,12008:31989/TCP,12009:30674/TCP   40m
```

## Connect nGrinder

![]({{ site.url }}/img/post/deploy/ngrinder/connect.png)

## init auth info
- id / pw : admin

## check Agent
admin(right top) - Agent Management

![]({{ site.url }}/img/post/deploy/ngrinder/check-agent.png)

## Deploy Target Server
nginx applyed hpa for ngrinder test
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: sample-nginx
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 1 # start Pod count
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 100m
          limits:
            cpu: 200m
 
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-hpa
  namespace: sample-nginx
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx-deployment
  minReplicas: 1
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
 
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-loadbalancer
  namespace: sample-nginx
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
  selector:
    app: nginx
apiVersion: v1
kind: Namespace
metadata:
  name: sample-nginx
```

```bash
$ kubectl create ns sample-nginx
$ kubectl apply -f sample-hpa-nginx.yaml
NAME                 TYPE           CLUSTER-IP    EXTERNAL-IP     PORT(S)        AGE
nginx-loadbalancer   LoadBalancer   10.80.5.190   34.171.28.156   80:32068/TCP   39s
```
### Set and Run Test

![]({{ site.url }}/img/post/deploy/ngrinder/save-test-1.png)
![]({{ site.url }}/img/post/deploy/ngrinder/save-test-2.png)
Performance Test - Create Test
![]({{ site.url }}/img/post/deploy/ngrinder/save-test-3.png)
![]({{ site.url }}/img/post/deploy/ngrinder/save-test-4.png)

### Save and Start
![]({{ site.url }}/img/post/deploy/ngrinder/start-test-1.png)
after 5min...
![]({{ site.url }}/img/post/deploy/ngrinder/start-test-2.png)
![]({{ site.url }}/img/post/deploy/ngrinder/start-test-3.png)
- TPS : Transaction per Success. (Higher the better)
- Mean Test Time : Average response time
