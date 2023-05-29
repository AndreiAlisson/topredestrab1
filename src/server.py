# Programa que atua como servidor TCP para o sistema servidor/cliente
# AUTORES
# ANDREI ALISSON FERREIRA JULIO GRR20163061
# JOÃO PEDRO KIERAS OLIVEIRA GRR20190379

import socket
import ssl
import psycopg2
import threading

# Executa a consulta de dados e retorna todas as colunas de resposta
def handle_query(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('SELECT * FROM table_name')
    results = cursor.fetchall()
    cursor.close()
    return results

# Conexão com o banco de dados
def connect_database():
    return psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )


# Lida com a requisição do cliente e retorna uma mensagem
def handle_request(client_socket):

    client_response = client_socket.recv(1024).decode('utf-8')
    print ('Mensagem recebida: ' + client_response)
    msg_return = 'Mensagem recebida com sucesso: ' + client_response

    ##### TODO #####
    # Conecta com o banco de dados
    """db_connection = connect_database"""

    # Executa consultas no banco de dados
    """db_return = handle_query(db_connection)"""

    # Fecha a conexão com o banco de dados
    """db_connection.close()"""

    # Retorna resultado da consulta para o cliente
    client_socket.send(msg_return.encode('utf-8'))
    client_socket.close()


########## main ##########

# Define o endereço IP e a porta do servidor
server_ip = 'localhost'
server_port = 80
cert_file = 'certificados/cert_server.crt'
key_file = 'certificados/server.key'

# Define configurações do banco de dados
db_host = 'localhost'
db_port = 5432
db_name = 'database_name'
db_user = 'username'
db_password = 'password'

# Criação do objeto socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincula o endereço IP e a porta ao socket
server_socket.bind((server_ip, server_port))

# Coloca o socket no modo de escuta, com limite de 5 conexões
server_socket.listen(5)

print('Servidor pronto para receber conexões...')

# Criação do contexto SSL/TLS 
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=cert_file, keyfile=key_file)

# Loop para recepcionar requisições do cliente continuinamente
while True:
    # Aceita uma nova conexão
    client_socket, client_addr = server_socket.accept()
    print ('[*] Conexao aceita!')

    # Inicia camada de segurança SSL/TLS
    secure_connection = context.wrap_socket(client_socket, server_side=True)

    client_handler = threading.Thread(target=handle_request, args=(secure_connection,))
    client_handler.start()