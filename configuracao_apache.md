
**Como exemplo de configuração, ver ssl_apache.conf no raiz deste projeto**

**Referências:**

[https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-apache-in-ubuntu-16-04]

[https://stuff-things.net/2015/09/28/configuring-apache-for-ssl-client-certificate-authentication/]

[https://certificados.serpro.gov.br/acserprorfb/certificate-chain]

### Configuração básica de SSL

1 - Instalar openssl no apache (mod_ssl), se ainda não instalado.

2 - Habilitar ssl na configuração do Apache (no nosso caso, /etc/httpd/conf.d/ssl.conf)

```
SSLEngine on
SSLCertificateFile      /etc/ssl/certs/apache-selfsigned.crt
SSLCertificateKeyFile /etc/ssl/private/apache-selfsigned.key
```

3 - Gerar as chaves para o Servidor se não existirem

```
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt
```

4 - Reiniciar o servidor 
```
$sudo httpd -t
$sudo systemctl restart httpd.service
```

### Configuração de autenticação do Certificado de cliente e-CPF/ICP Brasl 

1. Instalar openssl no apache (mod_ssl), se ainda não instalado.

2. Montar e enviar a Cadeia de Certificação:

    * Entrar no site https://certificados.serpro.gov.br/acserprorfb/certificate-chain e baixar todas as cadeias

    * Salvar todas as cadeias .crt em apenas um arquivo.crt, de forma concatenada.

    * Enviar este arquivo ao servidor. No nosso caso, foi salvo em /etc/ssl/certs/

3. Habilitar no Apache as seguintes linhas (no nosso caso, em /etc/httpd/conf.d/ssl.conf):

```
SSLCACertificate /etc/ssl/certs/AC_RFB.crt
SSLVerifyClient require
SSLVerifyDepth 10
```

4 - Reiniciar o servidor 
```
$sudo httpd -t
$sudo systemctl restart httpd.service
```

*Obs:* Quando houver uma nova versão da cadeia de certificação (o que ocorre aproximadamente a cada 3 anos),
 as novas caedias devem ser inseridas ao AC_RFB.crt, reiniciando o servidor.
 
 
### Configuração dos caminhos de ProxyPass das aplicações

1 - Configurar os endpoints responsáveis pela autenticação (no nosso caso, em /etc/httpd/conf.d/ssl.conf).

```
# initialize the special headers to a blank value to avoid http header forgeries
RequestHeader set SSL_CLIENT_S_DN    ""
RequestHeader set SSL_CLIENT_I_DN    ""
RequestHeader set SSL_SERVER_S_DN_OU ""
RequestHeader set SSL_CLIENT_VERIFY  ""

<Location /ajnaapi/api/login_certificado>
 SSLVerifyClient require
 # add all the SSL_* you need in the internal web application
 RequestHeader set SSL_CLIENT_S_DN "%{SSL_CLIENT_S_DN}s"
 RequestHeader set SSL_CLIENT_I_DN "%{SSL_CLIENT_I_DN}s"
 RequestHeader set SSL_SERVER_S_DN_OU "%{SSL_SERVER_S_DN_OU}s"
 RequestHeader set SSL_CLIENT_VERIFY "%{SSL_CLIENT_VERIFY}s"

 ProxyPass http://127.0.0.1:5004/ajnaapi/api/login_certificado
 ProxyPassReverse http://127.0.0.1:5004/ajnaapi/api//login_certificado
</Location>
<Location /virasana/login_certificado>
 SSLVerifyClient require
 # add all the SSL_* you need in the internal web application
 RequestHeader set SSL_CLIENT_S_DN "%{SSL_CLIENT_S_DN}s"
 RequestHeader set SSL_CLIENT_I_DN "%{SSL_CLIENT_I_DN}s"
 RequestHeader set SSL_SERVER_S_DN_OU "%{SSL_SERVER_S_DN_OU}s"
 RequestHeader set SSL_CLIENT_VERIFY "%{SSL_CLIENT_VERIFY}s"

 ProxyPass http://127.0.0.1:5001/virasana/login_certificado
 ProxyPassReverse http://127.0.0.1:5001/virasana/login_certificado
</Location>
```

2 - Configurar ProxyPass para as aplicações.

```
 <Location /ajnaapi>
     ProxyPass http://127.0.0.1:5004/ajnaapi
     ProxyPassReverse http://127.0.0.1:5004/ajnaapi
 </Location>
 <Location /docs>
     ProxyPass http://127.0.0.1:5004/ajnaapi/docs
     ProxyPassReverse http://127.0.0.1:5004/ajnaapi/docs
 </Location>
 <Location /virasana>
     ProxyPass http://127.0.0.1:5001/virasana
     ProxyPassReverse http://127.0.0.1:5001/virasana
 </Location>

```


3 - Configurar Redirect na porta 80 (no nosso caso em /etc/httpd/conf.d/sites.conf)

```
 <VirtualHost *:80>
    (...)
	Redirect / https://server_domain_or_IP

```

 
