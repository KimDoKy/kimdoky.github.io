---
layout: post
section-type: post
title: IaC - Terraform
category: deploy
tags: [ 'deploy' ]
---

## Terraform 이론과 사용법

### 코드형 인프라란?

- 인프라의 구축, 관리, 프로비저닝을 코드로 관리하는 방법론
- 프로비저닝, 시스템 변경, 구성 등 반복되는 과정을 코드를 통해 자동화하여 일관성있게 구성/변경
- 인프라 형상을 정의한 source code가 있다면 언제든지 동일한 인프라를 전개할 수 있다.
- 인프라 형상을 코드화하였기 때문에 git으로 버전관리가 가능하다.

### Idempotent Code
- 코드로 관리하기 때문에 항상 같은 전개를 할 수 있다.
	- 코드로 관리하기 때문에, 테라폼 환경을 벗어난 리소스에 대한 핸들링은 피해야 한다.

### Terraform 사용법

- `terraform init`
	- 지정한 backend에 상태 저장을 위한 `.tfstate` 파일을 생성
	- init 작읍을 완료하면, local에는 `.tfstate`에 정의된 내용을 담은 `.terraform` 파일이 생성됨
	- 기존에 다른 개발자가 이미 `.tfstate`에 인프라를 정의했다면, 다른 개발자는 init을 통해 local에서 sync를 맞출 수 있다.

- `terraform plan`
	- Public Cloud에 적용하기 전에 Terrarom Code의 문법을 확인하는 명령어
	- `+`: 새로 생성
	- `-`: 삭제
	- `~`: 교체/변경

- `terraform apply`
	- 문법 검사 결과를 배포하는 명령어

- `terraform destroy`
	- 이미 배포된 IaC Infra를 제거하는 명령어

## AWS VPC

```
variable "변수명" {
	type = string or list or map
	description = "설명"
	default = [
	    value
	]
]
```

### AWS Provider

Provider를 사용하여 어떤 Infra 자원을 사용할 것인지 선택할 수 있다.

```
provider "aws" {
	region = var.region변수
	access_key = var.access_key변수
	secret_key = var.secret_key변수
}

terraform {
	required_provider {
		aws = {
			source = "hashicorp/aws"
			version = "버전명"
		}
	}
}
```

### VPC

```
resource "aws_vpc" "변수명" {
	cidr_block = "CIDR"
	tags = {
		Name = "VPC 이름"
	}
}

ex)
resource "aws_vpc" "kr-front-vpc" {
	cidr_block = "10.101.0.0/16"
	enable_dns_support = true
	enable_dns_hostnames = true
	tags = {
		Name = "Zen Front VPC(10.101.0.0/16)"
	}
}
```

### Subnet

```
resource "aws_subnet" "서브넷 변수명" {
	cidr_block = "서버넷 CIDR 범위"
	vpc_id = aws_vpc.서브넷 변수명.id
	availability_zone = "가용성존"
	tags = {
		Name = "서브넷 Name"
	}
}
```

### Internet Gateway

```
resource "aws_internet_gateway" "InternetGateway변수명" {
	vpc_id = aws_vpc.VPC변수명.id
	tags = {
		Name = "InternetGateway명"
	}
}
```

### Route Table

```
resource "aws_route_table" "RouteTable변수명" {
	vpc_id = aws_vpc.VPC변수명.id
	route {
		cidr_block = "CIDR값"
		gateway_id = aws_internet_gateway.InternetGateway변수명.id
	}
	tags = {
		Name = "RouteTable명"
	}
}

resource "aws_route_table_association" "RT변수" {
	subnet_id = aws_subnet.서브넷변수명.id
	route_table_id = aws.route_table.RT명.id
}
```

### NAT Gateway

```
resource "aws_eip" "EIP 변수명" {
	vpc = true
	tags = {
		Name = "EIP명"
	}
}

resource "aws_nat_gateway" "NAT gateway변수" {
	allocation_id = aws_eip.EIP변수명.id
	subnet_id = aws_subnet.Sunet변수명.id
	depends_on = ["aws_internet_gateway.InternetGateway변수명"]
	tags = {
		Name = "NAT Gateway명"
	}
}
```

### Security Group

```
resource "aws_security_group" "SG변수" {
	vpc_id = aws_vpc.VPC변수명.id
	name = "SG이름"
	description = "SG 요약"
	ingress {
		description = "주석"
		from_port = 포트 번호 범위
		to_port = 포트 번호 범위
		protocol = "프로토콜 타입"
		cidr_blocks = ["CIDR"]
	}
	engress {
		from_port = 포트 번호 범위
		to_port = 포트 번호 범위
		protocol = "프로토콜 타입"
		cidr_blocks = ["CIDR"]
	}
	tags = {
		Name = "SG Tag"
	}
}
```

### NACL

```
resource "aws_network_acl" "NACL변수" {
	vpc_id = aws_vpc.VPC변수명.id
	ingress {
		protocol = "-1"
		rule_no = 100
		action = "allow"
		cidr_block = "0.0.0.0/0"
		from_port = 0
		to_port = 0
	}
	engress {
		protocol = "-1"
		rule_no = 100
		action = "allow"
		cidr_block = "0.0.0.0/0"
		from_port = 0
		to_port = 0
	}
	tags = {
		Name = "NACL Tag"
	}
}

resource "aws_network_acl_association" "NACL명" {
	network_acl_id = aws_network_acl.NACL변수명.id
	subnet_id = aws_subnet.서브넷변수명.id
}
```

### VPC Peering

```
resource "aws_vpc_peering_connection" "VP변수" {
	vpc_id = aws_vpc.VPC변수명.id
	peer_vpc_id = aws_vpc.Peering할 VPC변수명.id
	auto_accept = true
	tags = {
		Name = "Peering 명"
	}
}
```

### EC2

```
resource "aws_instance" "인스턴스 변수" {
	ami = "원하는 AMI"
	instance_type = var.인스턴스 타입 변수
	key_name = var.PEM KEY 변수
	subnet_id = aws_subnet.전개할 subnet.id
	vpc_security_group_ids = aws_security_group.SG변수명.id
	root_block_device {
		volume_size = "EBS 용량"
		volume_type = "EBS 타입"
		delete_on_termination = true   # EC2 종료시 EBS 볼륨 삭제
	}
	tags = {
		Name = "EC2 인스턴스명"
	}
}
```

### ALB

```
resource "aws_alb" "ALB변수" {
	name = "ALB명"
	idle_timeout = value   # web server timeout
	load_balancer_type = "LB type"
	security_group = [aws_security_group.SG변수명.id]
	subnets = [aws_subnet.Subnet변수명.id]
	enable_deletion_protection = true   # 삭제보호 활성화/비활성화
	tags = {
		Name = "ALB 명"
	}
}

resource "aws_lb_listener" "리스터 변수" {
	load_balancer_arn = aws_alb.ALBGroup변수.arn
	port = 리스터 포트
	protocol = "리스너 프로토콜 type"
	default_action {
		type = "forward"
		target_group_arn = aws_lb_target_group.ALB TargetGroup 변수.arn
	}
}

resource "aws_lb_target_group" "ALB TargetGroup변수" {
	name = "ALB Target Group명"
	port = 포트번호
	protocol = "프로토콜 type"
	vpc_id = aws_vpc.VPC변수.id
	tags = {
		Name = "ALB TargetGroup명"
	}
}

resource "aws_lb_target_group_attachment" "TG연결변수" {
	target_group_arn = aws_lb_target_group.ALBGroup변수.arn
	target_id = aws_instance.인스턴스 변수.id
}
```

### S3

```
# 생성
resource "aws_s3_bucket" "버킷변수" {
	bucket = "버킷명"
	lifecycle {
		prevent_destroy = false
	}
}

# Access 제한
resource "aws_s3_bucket_public_access_block" "Public Access 제한변수" {
	bucket = "aws_s3_bucket.버킷변수.id
	block_public_acls = true
	block_public_policy = true
	ignore_public_acls = true
	restrict_public_buckets = true
}

# public Access 제한
resource "aws_s3_access_point" "Access Point 변수" {
	name = "Access Point 이름"
	bucket = "버킷명"
	# 특정 VPC에서만 연결 설정
	vpc_configuration {
		vpc_id = aws_vpc.VPC변수.id
	}
}
```

### EFS

```
# 리소스 생성
resource "aws_efs_file_system" "EFS 변수" {
	availability_zone_name = 가용성존 이름
	creation_token = "토큰이름"
	encrypted = true    # 암호화 활성화 여부
	# kms_key_id = "암호화 키파일"
	performance_mode = 성능모드 선택(기본 Bust Mode)
	throughput_mode = throughput 모드 선택("provisioued")
	# provisioned_throughput_in_mibps =
	tags = {
		Name = "EFS 이름"
	}
}

# 리소스 연결
resource "aws_efs_mount_target" "마운트 타겟 변수" {
	file_system_id = aws_efs_file_system.EFS변수.id
	subnet_id = var.서브넷ID변수
	security_group = [
		aws_security_group.SG변수.id
	]
}
```

### RDS

```
resource "aws_db_subnet_group" "SG변수명" {
	name = "SubnetGroup 명"
	subnet_ids = [aws_subnet.DB SG변수.id]
	tags = {
		Name = "DB SubnetGroup 명"
	}
}
```

### Aurora Mysql Serverless

```
resource "aws_rds_cluster_instance" "DB인스턴스변수" {
	count = 총 생성할 인스턴스 수
	identifier = "인스턴스명"
	engine = DB 엔진
	engine_version = DB 엔진 버전
	cluster_identifier = aws_rds_cluster.RDS클러스터변수.cluster_identifier
	instance_class = "DB 인스턴스 타입"
	db_subnet_group_name = aws_db_subnet_group.DB서브넷그룹변수.id
	db_parameter_group_name = aws_db_parameter_group.DB파라미터변수.id
	publicly_accessible = false
}
```

```
resource "aws_rds_cluster" "Mysql Server Cluster변수" {
	cluster_identifier = "클러스터 식별자 정의"
	engine = "DB 엔진명"
	engine_mode = "serverless"   # 중요
	engine_version = "DB 엔진 버전"
	availability_zone = ["가용성존"]
	database_name = "DB 이름 정의"
	master_username = DB 마스터 계정
	master_password = DB 마스터 패스워드
	port = "포트"
	db_subnet_group_name = aws_db_subnet_group.DB서브넷그룹변수.id
	vpc_security_group_ids = [aws_security_group.DB보안그룹변수.id]
	db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.DB클러스터 파라미터그룹.id
	backup_retention_period = 백업기간
	preferred_backup_window = "백업시간"
	storage_encryted = true # 스토리지 활성화 여부
	final_snapshot_identifier = "DB 스냅샷 이름"
	skip_final_snapshot = false
	lifecycle {
		create_before_destroy = true
	}
}
```

### Document DB

```
# AWS Cloud Tail 감시로그 활성화
parameter {
	name = "audit_logs"
	value = "enabled"
}

# 변경 스트림 로그 유지, 사용기간
parameter {
	name = "change_stream_log_retention_duration"
	value = "3600"
}

# 느린 작업 프로파일링
parameter {
	name = "profiler"
	value = "enabled"
}

# 샘플링 작업속도
parameter {
	name = "profile_sampling_rate"
	value = "0.1"
}

parameter {
	name = "profiler_threshold_ms"
	value = "120"
}
```

### MemoryDB for Redis

```
# 샤드, 리플리카 갯수
num_shards = 2
num_replicas_per_shard = 2
# 전송중 암호화
tls_enabled = true
```

---
- [terraform docs](https://registry.terraform.io/providers/aaronfeng/aws/latest/docs)
- thanks to 신선호
