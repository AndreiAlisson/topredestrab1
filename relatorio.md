# Relatório do trabalho prático - Tópicos em Redes
## Cliente-Servidor KVS seguro com TLS
### Andrei Alisson Ferreira Julio e João Pedro Kieras Oliveira

O trabalho foi implementado inteiramente em linguagem Python. São dois arquivos fonte: client.py e server.py .
Para executar os mesmos, basta:
```
$ python3 client.py
```
```
$ python3 server.py
```

Utilizamos um banco de dados relacional PostgreSQL, para instalar a versão mais recente utilize o link:
```bash
https://www.postgresql.org/download/windows/
```

Antecipando um pouco do que veremos adiante, a parte da criação de certificados é muito importante neste trabalho pois é com base nos certificados criados que a conexão segura é estabelecida.
Utilizamos os seguintes comandos para criar os certificados tanto para o servidor quanto para o cliente:
```
openssl req -x509 -sha256 -newkey rsa:2048 -keyout certificate-server.key -out certificate-server.crt -days 1024 -nodes
```
```
openssl req -x509 -sha256 -newkey rsa:2048 -keyout certificate-client.key -out certificate-client.crt -days 1024 -nodes
```

Explicando um pouco do que foi feito para criarmos a conexão segura com TLS:
Primeiro, criamos um contexto TLS usando o protocolo 1.2
```
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
```
Agora, sempre que criarmos uma conexão será verificado se a outra parte comunicante possui um certificado
```
context.verify_mode = ssl.CERT_REQUIRED
```
Então, carregamos o certificado da outra parte comunicante (se estivermos editando o client.py carregamos o certificado do servidor, se estivermos em server.py carregamos o certificado do cliente)
```
context.load_verify_locations(cafile='certificados/certificado_cliente_ou_servidor.crt')
```
Neste ponto carregamos nosso próprio certificado juntamente com nossa chave privada (as variáveis contém o path para os arquivos de certificado e chave privada)
```
context.load_cert_chain(certfile=cert_file, keyfile=key_file)
```
Se estivéssemos falando de programas executando no ambiente de produção de uma empresa, precisaríamos de uma terceira entidade na comunicação que faria a criação e autenticação destes certificados. Contudo, para fins didáticos e práticos, estamos utilizando certificados autoassinados para este trabalho.

Agora, falando um pouco sobre o socket, criamos a camada de segurança utilizando aquele contexto criado anteriormente:
```
secure_socket = context.wrap_socket(client_socket, server_hostname=target_ip)
```