---
layout: post
section-type: post
title: Azure Application Gateway serving with CloudFront
category: deploy
tags: [ 'deploy' ]
---

Cloudfront's origins include s3 origin and custom origin.
Of course, everything except s3 is custom origin.
The source of custom origin generally uses ec2, ALB, etc., but resources from on-premises or other cloud companies can also be linked.

However, since it is impossible to register the IP as origin, you must set the domain in advance.

### Set Origin Domain for CloudFront
Check public IP of application gateway
![]({{ site.url }}/img/post/deploy/cloudfront/appgw_ip.png)
Create a subdomain with A record in DNS Zone
![]({{ site.url }}/img/post/deploy/cloudfront/dnszone.png)

### Create CloudFront Distribution
Register with CloudFront's Origin Domain
The rest is created as default first.

![]({{ site.url }}/img/post/deploy/cloudfront/cloudfront_distribution_1.png)
![]({{ site.url }}/img/post/deploy/cloudfront/cloudfront_distribution_2.png)
![]({{ site.url }}/img/post/deploy/cloudfront/cloudfront_distribution_3.png)

Creating it creates a distribution domain for CloudFront.
(actually usable)

![]({{ site.url }}/img/post/deploy/cloudfront/cloudfront.png)

### Import Certificate to ACM
If you set Alternate Domain, you can use it as your desired domain.
A certificate is also required to set up https communication.
It can be used only after importing the certificate into ACM.

![]({{ site.url }}/img/post/deploy/cloudfront/acm_import.png)
![]({{ site.url }}/img/post/deploy/cloudfront/cert.png)
![]({{ site.url }}/img/post/deploy/cloudfront/acm_list.png)

### Set Alternate Domain
After importing the certificate into ACM, set the Alternate Domain and certificate in CloudFront Settings.

![]({{ site.url }}/img/post/deploy/cloudfront/cloudfront_alternate.png)

Register the domain to be used as an alternate domain as a cname record in Azure's DNS Zone and set the alias to Cloudfront's Distribution domain.

Even though distribution has been completed in CloudFront, distribution is actually in progress.

Distribution takes quite a long time.

After deployment is complete, you can successfully communicate by connecting to the alternate domain via https in your browser.

![]({{ site.url }}/img/post/deploy/cloudfront/browser.png)

Additionally, you must set up a certificate and settings for HTTPS in Azure Application Gateway to connect successfully.
> [Certificate on Azure Application Gateway with LetsEncrypt](https://kimdoky.github.io/deploy/2024/06/16/certificate/)
