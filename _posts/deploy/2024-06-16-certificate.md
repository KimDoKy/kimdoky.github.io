---
layout: post
section-type: post
title: Certificate on Azure Application Gateway with LetsEncrypt
category: deploy
tags: [ 'deploy' ]
---

AWS can easily apply HTTPS through ACM, but Azure does not have a system like ACM.
So, I issued a certificate through LetsEncrypt and applied it to Application Gateway.

The domain was purchased cheaply for testing.

## Certificate issuance
```bash
certbot certonly --manual --preferred-challenges dns -d czarcie.store -d '*.czarcie.store'

set DNS txt record...

Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/czarcie.store/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/czarcie.store/privkey.pem
This certificate expires on 2024-09-15.
These files will be updated when the certificate renews.
```

pem file created in /etc/letsencrypt/live/czarcie.store

```bash
.
├── README
├── cert.pem -> ../../archive/czarcie.store/cert1.pem
├── chain.pem -> ../../archive/czarcie.store/chain1.pem
├── fullchain.pem -> ../../archive/czarcie.store/fullchain1.pem
└── privkey.pem -> ../../archive/czarcie.store/privkey1.pem
```

## Create a combined pem file
```bash
cat /etc/letsencrypt/live/czarcie.store/fullchain.pem /etc/letsencrypt/live/czarcie.store/privkey.pem > cert_chain.pem

.
└── cert_chain.pem
```

### Create PFX file
```bash
openssl pkcs12 -export -out certificate.pfx -in cert_chain.pem -passout pass:password

.
├── cert_chain.pem
└── certificate.pfx
```

### Register a certificate in the listner TLS certificates
![]({{ site.url }}/img/post/deploy/certificate/listener_cert.png)

### Set Listener
![]({{ site.url }}/img/post/deploy/certificate/listener.png)

### Set Application Gateway
- rules (routing rule)
- backend settings
- probe

### Set DNS Zone
Register the IP of the application gateway as an A record in DNS Zone.

### check
![]({{ site.url }}/img/post/deploy/certificate/browser.png)

