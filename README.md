# Introdução do Projeto
Uma implementação simples de um sistema cliente/servidor seguro com TLS em python, com dados baseados em Key-Value. O sistema cria uma base de dados simples em um banco de dados PostgreSQL, e permite Consulta/Inclusão/Alteração/Exclusão de dados neste sistema.

# Requisitos
Python instalado na máquina

```bash
pip install python3
```

Componentes do PostgreSQL

```bash
pip install psycopg2
```

Versão mais recente do postgreSQL (15.3) Configurada no PC, utilizando as credenciais definidas no programa server.py, no comentário # NOTA1

```bash
https://www.postgresql.org/download/windows/
```

# Criação de certificados

Criação das chaves e certificados:

1.1. Crie uma chave privada para o servidor:
```bash
openssl genpkey -algorithm RSA -out server_key.pem
```

1.2. Crie um CSR (Certificate Signing Request) para o servidor:
```bash
openssl req -new -key server_key.pem -out server_csr.pem
```
Durante este processo, você será solicitado a fornecer informações sobre o certificado. Preencha as informações conforme necessário.

1.3. Auto-assine o CSR do servidor para gerar o certificado do servidor:
```bash
openssl x509 -req -in server_csr.pem -signkey server_key.pem -out server_cert.pem
```
Agora, você terá os arquivos server_key.pem (chave privada do servidor) e server_cert.pem (certificado do servidor).

1.4. Crie uma chave privada para o cliente:
```bash
openssl genpkey -algorithm RSA -out client_key.pem
```
1.5. Crie um CSR para o cliente:
```bash
openssl req -new -key client_key.pem -out client_csr.pem
```
Preencha as informações conforme necessário.

1.6. Assine o CSR do cliente com a chave privada do servidor para gerar o certificado do cliente:
```bash
openssl x509 -req -in client_csr.pem -CA server_cert.pem -CAkey server_key.pem -CAcreateserial -out client_cert.pem
```
Agora, você terá os arquivos client_key.pem (chave privada do cliente) e client_cert.pem (certificado do cliente).

### Execução
Basta rodar os scripts para abrir uma conexão para o servidor, e outra para o cliente

```
$ python3 client.py
```
```
$ python3 server.py
```