# Relatório do trabalho prático - Tópicos em Redes
## Cliente-Servidor KVS seguro com TLS
### Andrei Alisson Ferreira Julio e João Pedro Kieras Oliveira

### Funcionamento do TLS
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

Agora, falando um pouco sobre o socket, criamos a camada de segurança utilizando aquele contexto criado anteriormente e passamos como parâmetro nosso próprio socket e o IP destino:
```
secure_socket = context.wrap_socket(nosso_socket, server_hostname=target_ip)
```

E então, fazemos a conexão e enviamos uma mensagem utilizando como parâmetros o IP e porta do destino:
```
secure_socket.connect((target_ip, target_port))
secure_socket.send(...)
```

### Tentativa de ataque

Para simular uma tentativa de ataque ao sistema podemos utilizar como base o próprio programa client.py alterando o certificado e a chave privada. Um atacante, por mais que soubesse o endereço IP do servidor e as portas utilizadas, muito dificilmente teria acesso aos certificados usados na comunicação pois essa parte é feito por uma organização terceira. Ao tentar utilizar um certificado e chave privada diferente do que o servidor aceita e conhece, obtemos o seguinte erro (por parte do servidor) ao tentar executar o programa:

```bash
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate (_ssl.c:1131)
```

O que comprova que a comunicação é, de fato, segura e garante autenticidade.