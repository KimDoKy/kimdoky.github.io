---
layout: post
section-type: post
title: Python Library - chap 12. 암호 관련 - 2. SSH 프로토콜 다루기
category: python
tags: [ 'python' ]
---

`paramiko`는 SSH 모듈 기능을 제공합니다. 다양한 기능을 가진 패키지이지만, 주로 다음 목적으로 이용합니다.

- SSH 접속과 명령어 실행
- SFTP 접속을 통한 파일 전송

인증은 ID와 패스워드 인증 이외에 키 교환 방식도 지원합니다. 구성 관리 도구인 Ansible이나 Fabric이 이러한 paramiko를 이용하고 있습니다.  

또한 paramiko에서는 FTP 접속은 불가능합니다. FTP 접속이 필요하다면 표준 라이브러리 ftplib을 이용하세요.

## paramiko 설치

```
$ pip install paramiko
```

### SSH 명령어 실행하기
paramiko를 사용하면 원격 서버에 SSH 로그인해서 명령어를 실행할 수 있습니다. 리눅스 서버에 접속하여 명령어 ls -l/tmp를 실행하는 코드입니다.

```Python
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect('hamegg.com', 22, 'your_user', key_filename='/home/your_user/.ssh/id_rsa')

stdin, stdout, stderr = ssh.exec_command('ls -l /home')

for line in stdout:
    print(line, end="")

ssh.close()
```

### "SSH 명령어 실행하기"의 결과 예

```
drwx------ 3 your_user your_user 4096 11 25 01:43 your_user
drwx------ 3 test      test      4096 11 25 01:43 test
```

### paramiko.client.SSHClient.connect()

형식 | paramiko.client.SSHClient.connect(hostname, port=22, username=None, password=None, pkey=None, key_filename=None, timeout=None, allow_agent=True, look_for_keys=True, compress=False, sock=None, gss_auth=False, gss_key=False, gss_deleg_creds=True, gss_host=None, banner_timeout=None)
---|---
설명 | SSH 서버에 대한 접속 및 인증을 실행한다.
인수 | hostname - 접속할 서버 호스트를 지정한다. <br> port - 접속할 포트 번호를 지정한다. <br> username - 접속할 로그인 사용자를 지정한다. <br> password - 패스워드를 지정한다. <br> key_filename = 비밀키 경로를 지정한다.

### paramiko.client.SSHClient.exec_command()

형식 | paramiko.client.SSHClient.exec_command(command, bufsize=-1, timeout=None, get_pty=False)
---|---
설명 | SSH 서버상에서 명령어를 실행한다.
인수 | command - 실행할 명령어를 지정한다.
반환값 | 표준 입력, 표준 출력, 표준 오류 출력

### paramiko.client.SSHClient.set_missing_host_key_policy()

형식 | paramiko.client.SSHClient.set_missing_host_key_policy(policy)
---|---
설명 | 모르는 서버 호스트에 접속할 경우 policy를 설정한다.
인수 | policy - policy

## SFTP 파일 전송하기

### SFTP 올리기/내려받기

```Python
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect('hamegg.com', 22, 'your_user', key_filename='/home/your_user/.ssh/id_rsa')
sftp = client.open_sftp()

# 올리기
sftp.put('local_file', 'remote_file')

# 권한을 0755로 지정
sftp.chmod('remote_file', '0o0755')

# 내려받기
sftp.get('remote_file', 'local_file')

sftp.close()
ssh.close()
```

### paramiko.sftp_client.SFTPClient.put()

형식 | paramiko.sftp_client.sftp_client.put(localpath, remotepath, callback=None, confirm=True)
---|---
설명 | 로컬 호스트로부터 SFTP 서버에 파일을 복사한다.
인수 | localpath - 올릴 파일의 원래 경로 <br> remotepath - 파일을 올릴 위치의 경로
반환값 | SFTPAttributes

remotepath에는 파일 이름까지 포함한 경로를 지정해야 합니다.

### paramiko.sftp_client.SFTPClient.get()

형식 | paramiko.sftp_client.SFTPClient.get(remotepath, localpath, callback=None)
---|---
설명 | SFTP 서버로부터 로컬 호스트로 파일을 복사한다.
인수 | remotepath - 내려받을 파일의 원래 경로 <br> localpath - 파일을 내려받을 위치의 경로

### paramiko.sftp_client.SFTPClient.chmod()

형식 | paramiko.sftp_client.SFTPClient.chmod(path, mode)
---|---
설명 | 파일 권항르 변경한다.
인수 | path - 권한을 변경할 대상의 파일 경로 <br> mode - 권한

mode 에는 권한을 수치로 지정합니다. mode를 다룰 때는 주의를 해야 합니다. 예를 들어, 리눅스 명령어 "chmod 644"와 같은 동작을 기대하고 "mode=644"라고 지정하면, 실제로는 "--w----r-T"(chmod 1204)라는 권한이 설정됩니다. mode는 받은 값을 10진수 644라고 인식하여 8진수인 1204로 변환하기 때문입니다. 권한 644를 설정하려면 8진수 644를 10진수로 변환한 값인 "mode=420"이라고 지정하거나, 맨 앞에 0o(zero, o)를 붙여 0o0644와 같이 8진수로 지정해야 합니다.

> #### subprocess가 아닌 paramiko를 사용합시다.
Python 코드로 SFTP/SCP 파일을 전송할 떄, subprocess로 리눅스의 SFTP/SCP 명령어를 사용하는 경우를 종종 보게 됩니다.
> #### subprocess로 SCP 명령어를 사용하는 예
> ```Python
import subprocess
subprocess.Popen(["scp", local_file, destination_host]).wait()
```
>
앞선 코드로도 파일을 전송할 수 있지만, paramiko를 쓰는 편이 오류 처리가 쉽습니다.


> #### paramiko와 known_hosts
known_hosts는 접속할 서버 호스트의 진위 여부를 확인하기 위하여 서버 호스트 이름과 호스트 공개키 한 쌍을 기록해두는 파일을 가리킵니다. 보통은 사용자의 홈 디렉터리 아래 "~/.ssh/known_hosts"에 저장되어 있습니다.  
앞의 예에서 `set_missing_host_key_policy()` 메서드는 connect() 메서드로 접속할 대상의 서버 호스트 정보가 known_hosts에 없을 경우의 policy를 지정합니다. 자동으로 접속 완료 대상에 추가하는 paramiko.AutoAddPolicy()와 추가하지 않는 paramiko.RejectPolicy()를 지정할 수 있습니다.  
known_hosts에 등록되어 있지 않은 서버 호스트에 접속할 때는 set_missing_host_key_policy()를 생략하거나 RejectPolicy()를 지정하면, 예외 "SSHException: Sever 'url' not found in known_hosts"가 발생합니다.  
AutoAddPolicy()를 지정하는 것만으로는 실제로 known_hosts 파일에 내용이 입력되지 않습니다. SSHClient 클래스의 인스턴스 변수 \_host_keys에 대입될 뿐입니다. known_hosts에 내용을 입력하고 싶을 때에는 load_host_keys()와 save_host_keys()를 이용합니다.  
> #### known_hosts의 읽기와 쓰기
>```Python
import paramiko
KNOWN_HOSTS = '/home/your_user/.ssh/known_hosts'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.load_host_keys(KNOWN_HOSTS_FILE)
ssh.connect('url')
ssh.save_host_keys(KNOWN_HOSTS_FILE)
ssh.close()
```
>
실제로 load_host_keys() 메서드로 읽어온 파일의 경로는 임의의 것이라도 상관없습니다. load_host_keys() 메서드는 신규 파일을 생성하지 않기 때문에 파일을 미리 배치해두어야 합니다.  
load_system_host_keys() 메서느도 known_hosts 를 읽어오는 메서드지만, 파일 경로를 생략하면 자동으로 ~/.ssh/known_hosts를 읽어오고, 읽어온 파일에 대해 save_host_keys() 메서드로 내용을 입력할 수는 없다는 차이점이 있습니다.  
load_host_keys() 또는 load_system_host_keys() 메서드로 읽어온 known_hosts 파일에 호스트 정보가 기재되어 있지 않고, 또한 policy에 paramiko.AutoAddPolicy()가 지정되어 있지 않으면, 예외 "paramiko.ssh_exception.SSHException: Server 'url' not found in known_hosts" 가 발생합니다.  
이러한 known_hosts 취급에 대해 잘 알아두고 적절한 policy로 운용해야합니다.
