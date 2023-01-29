# Defl8-master

## Introduction

Defl8 is yet another ERC20 Token, with burning enabled in the ERC20 contract for every
Token transfer that is NOT a smart contract call ( those are "free" ). DEFL8 is a private 
project intended for experimental purposes only. 

## Description

The Defl8-webserver renders an HTML template using a flask webserver. 
The template includes web3.js code and can be used to call the mint() function off the 
Defl8 contract on any ERC20 compatible chain (default is BEP20/BSC). 

The Metamask wallet can be used together with Chromium / Chrome, other web-wallets are 
currently not supported.

## Disclaimer !
DEFL8 is a shitcoin per definition. \
It's not live and has been developed for educational purposes. \
Don't launch this cr*p!

------------------------------------Hosting Notes-------------------------------------------


sudo certbot --nginx -d defl8.me -d www.defl8.me

nohup uwsgi /var/www/defl8/config-uwsgi.ini &


systemctl restart nginx
systemctl enable nginx
systemctl disable nginx


// SSL configuration

server {
    listen 443 ssl;
    server_name defl8.me;


    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_dhparam /path/to/dhparam.pem;

    ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:!DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
    ssl_protocols TLSv1.2;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_stapling on;
    ssl_stapling_verify on;
    add_header Strict-Transport-Security max-age=15768000;
    # ...
}




 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/defl8.me/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/defl8.me/privkey.pem
   Your cert will expire on 2021-12-08. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot again
   with the "certonly" option. To non-interactively renew *all* of
   your certificates, run "certbot renew"
