# Programa que atua como servidor TCP para o sistema servidor/cliente
# AUTORES
# ANDREI ALISSON FERREIRA JULIO GRR20163061
# JOÃO PEDRO KIERAS OLIVEIRA GRR20190379

import socket
import ssl
import psycopg2
import threading

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Dados temporários do banco de dados
temp_db_name = 'temp_database'
temp_table_name = 'temp_table'
temp_table_columns = 'nome VARCHAR, id INTEGER'

# Define o endereço IP e a porta do servidor
server_ip = 'localhost'
server_port = 80
cert_file = 'certificados/server_cert.pem'
key_file = 'certificados/server_key.pem'

# Define configurações do banco de dados configurado no PostgreSQL do servidor
# NOTA: Necessário configurar banco no PC, baixando o PostgreSQL
db_host = 'localhost'
db_port = 5432
db_name = 'postgres'
db_user = 'postgres'
db_password = 'andrei'

# Conexão com o banco de dados
def connect_database():
    return psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )

# Cria um banco de dados inicial para o cliente consultar
def create_database():
    
    # Conecta com o servidor PostgreSQL
    conn = connect_database();

    # Define o nível de isolamento como AUTOCOMMIT
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # Cria um cursor para executar consultas
    cursor = conn.cursor()

    # Cria um banco de dados temporário
    cursor.execute(f"SELECT 'CREATE DATABASE {temp_db_name} TEMPLATE template0' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{temp_db_name}')")

    # Cria uma tabela temporária
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {temp_table_name} ({temp_table_columns})")

    # Reseta os dados da tabela caso já exista
    cursor.execute(f"DELETE FROM {temp_table_name}")

    # Adiciona dados temporários
    temp_table_values = "'ANDREI', 1"
    cursor.execute(f"INSERT INTO {temp_table_name} VALUES ({temp_table_values})")

    temp_table_values = "'JOAO', 2"
    cursor.execute(f"INSERT INTO {temp_table_name} VALUES ({temp_table_values})")

    return conn, cursor

# Executa a consulta de dados e retorna todas as colunas de resposta
def handle_query(db_connection):
    cursor = db_connection.cursor()
    cursor.execute(f'SELECT * FROM {temp_table_name}')
    results = cursor.fetchall()
    cursor.close()
    return results

# Lida com a requisição do cliente e retorna uma mensagem
def handle_request(client_socket, db_connection):

    client_response = client_socket.recv(1024).decode('utf-8')
    print ('Mensagem recebida: ' + client_response)

    # Executa consultas no banco de dados
    db_return = handle_query(db_connection)

    # Converte resultado em string para enviar pro cliente
    msg_return = 'Consulta realizada: ' + '\n'.join([', '.join(map(str, row)) for row in db_return])
    print (msg_return)

    # Retorna resultado da consulta para o cliente
    client_socket.send(msg_return.encode('utf-8'))
    client_socket.close()

# Função que verifica a necessidade de encerrar o servidor pelo input (ou interrupção) via prompt
def handle_server(server_socket):
    print ("Digite 'exit' para encerrar o servidor ativo")
    while True:
        try:
            msg_input = input("")
            if msg_input == 'exit':
                server_socket.close()
                break
        except:
            print ('Encerrando execucao por interrupcao do usuario')
            server_socket.close()
            break


########## main ##########

db_connection, db_cursor = create_database();

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

# Cria uma thread para poder interromper a execução do servidor
server_status = threading.Thread(target=handle_server, args=(server_socket,))
server_status.start()

# Loop para recepcionar requisições do cliente continuinamente
while True:

    # Fica em modo escuta até o servidor ser interrompido pelo terminal (via handle_server())
    try:
        client_socket, client_addr = server_socket.accept()
    except:
        break

    print ('[*] Conexao aceita!')

    # Inicia camada de segurança SSL/TLS
    secure_connection = context.wrap_socket(client_socket, server_side=True)

    # Cria uma thread pra processar a requisicao do cliente
    client_handler = threading.Thread(target=handle_request, args=(secure_connection, db_connection,))
    client_handler.start()


# Fecha as conexões com o banco de dados
db_cursor.close()
db_connection.close()