---
layout: post
section-type: post
title: Python Library - chap 12. 암호 관련 - 1. 다양한 암호화 다루기
category: python
tags: [ 'python' ]
---

애플리케이션이 정보를 적절히 통신하고 저장하기 위해서는 암호화 기술이 필수입니다. 이번 챕터는 암호화, 복호화와 관련된 기능을 제공하는 PyCrypto와 원격 서버의 보안 통신에 이용하는 paramiko에 대해 다룹니다.

# 다양한 암호화 다루기
`PyCrypto`는 암호화와 관련된 도구를 제공합니다.  

PyCrypto는 AES와 DES, RSA등 다양한 암호 알고리즘을 지원합니다. 암호화/복호화와 SSH 통신 공개키, 비밀키를 생성하는 목적으로 이용됩니다. 또한 MD5와 SHA-512 등의 해시 알고리즘도 갖추고 있어 부호화와 암호화를 폭넓게 지원할 수 있는 기본적인 패키지입니다.

## PyCrypto 설치

```
$ pip install pycrypto
```

### 해시값 생성하기
PyCrypto에서는 MD5나 SHA-512 알고리즘을 이용하여 해시값을 생성할 수 있습니다.

#### 지원 알고리즘

- MD5
- RIPEMD-160
- SHA-1
- SHA-256
- SHA-512

자주 쓰이는 MD5와 SHA-512의 알고리즘 해시값을 생성해봅니다.

```Python
>>> from Crypto.Hash import MD5, SHA512
>>> hash_md5 = MD5.new()  # MD5를 이용한다.
>>> hash_md5.update(b'hamegg')  # 문자열을 바이트 문자열로 전달해야 한다.
>>> hash_md5.hexdigest()
'38f778abb3f6c5e050baaffdf74dac4e'

>>> hash_sha512 = SHA512.new()  # SHA-512를 이용한다.
>>> hash_sha512.update(b'ham')
>>> hash_sha512.hexdigest()
'b3ba728159b78a601c7dd0b08906ae7e45d2d4c8def566639200538401eab4a38aa59c60d45478d90c2d823e56f2a727059ab1a2feab7935a804e75c86da4e19'

>>> hash_md5 = MD5.new(b'hamegg')  # 인스턴스를 생성할 때 데이터도 전달할 수 있다.
>>> hash_md5.hexdigest()
'38f778abb3f6c5e050baaffdf74dac4e'
>>> hash_md5 = MD5.new(b'ham')
>>> hash_md5.hexdigest()
'79af0c177db2ee64b7301af6e1d53634'

>>> hash_md5.update(b'egg')  # update 함수는 추가로 작성한다.
>>> hash_md5.hexdigest()  # b'ham'과 b'egg'가 연결되어 b'hamegg'가 되었다.
'38f778abb3f6c5e050baaffdf74dac4e'
```

어떤 알고리즘이든 통일된 API로 이용할 수 있습니다.

## RSA 암호화 알고리즘 이용하기
암호화 방식에는 크게 공통키 암호와 공개키 암호가 있습니다. 공통키 암호 방식 알고리즘으로는 DES, 2DES, AES가 있고, 공개키 암호 방식 알고리즘은 RSA가 많이 알려졌습니다.

### RSA를 사용한 비밀키와 공개키 생성

```Python
from Crypto.PublicKey import RSA
rsa = RSA.generate(2048)
private_pem = rsa.exportKey(format='PEM', passphrase='password')
with open('private.pem', 'wb') as f:
    f.write(private_pem)
public_pem = rsa.publickey().exportKey()
with open('public.pem', 'wb') as f:
   f.write(public_pem)
```
위 코드를 실행하면 다음 파일이 출력됩니다.

### private.pem
```pem
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-EDE3-CBC,E90B8FC480EC6817

C1KCqPtCIV/2Td+kUIvVkTBdbgyYsaUAmR9o+GLe8gFPjc6v6JVkBvOTdlfC4Y8u
XjRpsXTFH0tVhFD4cWcU/WBjc1kP+ecaNIqCWhVSjbe8tmO/sXqE4sVzYeWrBQaq

...

rJNorbg5xmSzQAhQiBCA3OQ6aswRAcB5QJZGcXIHv9KBLnyUvRF9tfD7R/7mKImv
dKdx/42++mhBNl6rKw2calV/JKHjNDEfH4XxHce5JP3h0eqEF4OBB19kCfV7R+sI
-----END RSA PRIVATE KEY-----%
```

### public.pem
```pem
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy0Swa/9bKt91SEMJADN8
J2l4vDY+zxdCi80zsSxpNbIzOCoR3JNXE9YTJXDYGynjie4vRaOoiYMQSDAIVfYb
...
qs75ksMkLqwCa8QIwrxKZUSYyZqVd/kWHQ35E/v8fEK4WwTzBvBIs+hu4Nb5xNK2
lQIDAQAB
-----END PUBLIC KEY-----%
```

### RSA.generate()

형식 | RSA.generate(bits, randfunc=None, progress_func=None, e=65537)
---|---
설명 | RSA 키를 무작위로 생성한다.
인수 | bits - 비트 강도
반환값 | RSA key 객체(\_RSAobj)

### \_RSAobj.exportKey()

형식 | \_RSAobj.exportKey(format='PEM', passphrase=None, pkcs=1)
---|---
설명 | RSA 키를 작성한다.
인수 | format - 키의 포맷 <br> passphrase - 비밀키의 pass phrase.format을 PEM으로 지정한 경우에만 유효
반환값 | 비밀키 또는 공개키 바이트 문자열

### 비밀키와 공개키를 사용한 데이터 암호화/복호화

```Python
from Crypto.PublicKey import RSA
from Crypto import Random

# 생성한 공개키와 비밀키를 읽어온다.
public_key_file = open('public.pem', 'r')
private_key_file = open('private.pem', 'r')

public_key = RSA.importKey(public_key_file.read())
private_key = RSA.importKey(private_key_file.read(), passphrase='password')

plain_text = 'ham'
print('원래 문자열:', plain_text)

# 암호화 실행
random_func = Random.new().read
encrypted = public_key.encrypt(plain_text.encode('utf-8'), random_func)
print('암호화된 문자열:', encrypted)

# 복호화 실행
decrypted = private_key.decrypt(encrypted)
print('복호화된 문자열:', decrypted.decode('utf-8'))

public_key_file.close()
private_key_file.close()
```

### '비밀키와 공개키를 사용한 데이터 암호화와 복호화'의 실행 결과

```
원래 문자열: ham
암호화된 문자열: (b"[w\xcf'\x1e\x9e-\xed9?'\x1aP\x058L\xc6J\x89)\xf2\x8f\xdev\xfc\x03\xd9\\\x02\x1d\x84V\x9a\x1eC\x80\xcc\x9b\x81\x83+}\xaev\xd8+\xc9\xef\xe6\xa6\xf3n=\x84*C\x902<\x03\xfd\xab\xbe\xa3\x8e\xb8\xbd\xa2\xe0RO\t\xd5o\x1d\x80\xfd\xaes<\x8c\xe6\x01\x168\xe0`\xa0\xf9\x91K\x04\xf4\xedcI^\xb3\x95+\xf0\xf8?#`!\tE\xbe\xed?\xb8\xd3\x8ej\x1c\xd1Fr\xfei\x9dg\x88\xa5\x04\x1c\x8a\xe7\x0c\xf9\tQC<$\x1f\xd7\xa26,\xd2i\xf7'TRq\x14\xb3\xb4\xd0\x91\xae9o\\\x18\xa7\x95\x93b\xbdh_\x9e\x9f\x7f}\xbc7\x87?r\xdb\xb3\xe3\xec\xb4P\x0c\xfb\x7f\xd9\xef\x91t2-\x98\x1d\xf3U~\xf8\x88\xfb\x93\xbe\xa1\xc3\xde\xb2o?\xbel15=\x9b\xd5\x8dv\xb2|\xc0\xf1\x15pD\x84l\xdbb\xff\x0eH\x96\x9c\xc7\x82\x08C\xf6\xda\xfb\xc36sv\x91\xe1d\x03\x81\xc0E\x1b\x1f\x91\x15\xc7\x96O\xb4",)
복호화된 문자열: ham
```

문자열 ham이 한 번 암호화되고 나서 다시 복호화된 것을 확인했습니다.

### RSA.importKey()

형식 | RSA.importKey(externKey, passphrase=None)
---|---
설명 | 암호화된 RSA 키를 읽어온다.
인수 | externKey -  공개키 또는 비밀키를 지정한다. <br> passphrase - 비밀키일 때, pass phrase를 지정할 수 있다.
반환값 | RSA key 객체(\_RSAobj)

### \_RSAobj.encrypt()

형식 | \_RSAobj.encrypt(plaintext, K)
---|---
설명 | RSA 방식으로 데이터를 암호화한다.
인수 | plaintext - 암호화 대상 문자열 <br> K - 난수를 생성하는 함수를 지정한다.
반환값 | 암호화된 바이트 문자열

### \_RSAobj.decrypt()

형식 | \_RSAobj.decrypt(ciphertext)
---|---
설명 | RSA 방식으로 데이터를 복호화한다.
인수 | ciphertext - 복호화 대상인 암호화된 바이트열을 지정한다.
반환값 | 복호화된 바이트 문자열

> #### 표준 라이브러리 hashlib  
해시값 생성은 hashlib으로도 가능합니다.
```
>>> import hashlib
>>> hash_md5 = hashlib.md5(b'hamegg')
>>> hash_md5.hexdigest()
'38f778abb3f6c5e050baaffdf74dac4e'
```
이처럼 해시값 생성에 hashlib를 사용해도 좋습니다.
