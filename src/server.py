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
temp_table_column_key = 'chave'
temp_table_column_value = 'valor'
temp_table_columns = f'{temp_table_column_key} INTEGER, {temp_table_column_value} VARCHAR'

# Define o endereço IP e a porta do servidor
server_ip = 'localhost'
server_port = 3000
cert_file = 'certificados/certificate-server.crt'
key_file = 'certificados/certificate-server.key'

# Define configurações do banco de dados configurado no PostgreSQL do servidor
# NOTA1: Necessário configurar banco no PC conforme as credenciais definidas aqui
db_host = 'localhost'
db_port = 5432
db_name = 'postgres'
db_user = 'postgres'
db_password = 'andreijoao'

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

    # Deleta tabela de outras execuções
    cursor.execute(f"DROP TABLE {temp_table_name}")

    # Cria uma tabela temporária
    cursor.execute(f"CREATE TABLE {temp_table_name} ({temp_table_columns})")

    # Setta a chave primária do banco de dados
    cursor.execute(f"ALTER TABLE {temp_table_name} ADD CONSTRAINT cst_01 PRIMARY KEY ({temp_table_column_key})")

    # Adiciona dados temporários
    temp_table_values = "1, 'ANDREI'"
    cursor.execute(f"INSERT INTO {temp_table_name} VALUES ({temp_table_values})")

    temp_table_values = "2, 'JOAO'"
    cursor.execute(f"INSERT INTO {temp_table_name} VALUES ({temp_table_values})")

    return conn, cursor

# Executa uma query no banco de dados, retornando uma mensagem de acordo com o tipo da query
def execute_query (query, cursor, action):
    try:
        cursor.execute(query)

        if action == 'select':
            result = '\n'.join([', '.join(map(str, row)) for row in cursor.fetchall()])
        elif action == 'insert':
            result = 'Dados inseridos com sucesso'
        elif action == 'update':
            result = 'Dados atualizados com sucesso'
        elif action == 'delete':
            result = 'Dados excluidos com sucesso'   
    except Exception as e:
        result = str(e)

    return result

# Executa a consulta de dados e retorna todas as colunas de resposta
def handle_query(db_connection, client_response):
    cursor = db_connection.cursor()

    results = ''

    # Separa a ação (Insert/Update/Delete) e o comand
    print ('Requisicao do cliente: ' + client_response)

    # Ação do usuário
    action = client_response.split("|")[0]

    # Consulta (Chave ou valor)
    if action == '1':

        # Verifica se é consulta por chave ou por valor
        action = client_response.split("|")[1]

        # Consulta por chave
        if action == '1':
            key = client_response.split("|")[2].strip()
            print ('key: ' + key)
            results = execute_query(f"SELECT * FROM {temp_table_name} WHERE {temp_table_column_key} = {key}", cursor, 'select')

        # Consulta por valor
        elif action == '2':
            value = client_response.split("|")[2].strip()
            results = execute_query(f"SELECT * FROM {temp_table_name} WHERE {temp_table_column_value} ILIKE '%{value}%'", cursor, 'select')

    # Insert (Chave e valor)
    elif action == '2':
        key = client_response.split("|")[1].strip()
        value = client_response.split("|")[2].strip()

        results = execute_query(f"INSERT INTO {temp_table_name} VALUES  ({key}, '{value}')", cursor, 'insert')

    # Update (Chave e valor)
    elif action == '3':
        key = client_response.split("|")[1].strip()
        value = client_response.split("|")[2].strip()

        results = execute_query(f"UPDATE {temp_table_name} SET {temp_table_column_value} = '{value}' WHERE {temp_table_column_key} = {key}", cursor, 'update')

    # Delete (Chave)
    elif action == '4':
        key = client_response.split("|")[1].strip()

        results = execute_query(f"DELETE FROM {temp_table_name} WHERE {temp_table_column_key} = {key}", cursor, 'delete')

    cursor.close()
    return results

# Lida com a requisição do cliente e retorna uma mensagem
def handle_request(client_socket, db_connection):

    client_response = client_socket.recv(1024).decode('utf-8')
    print ('Mensagem recebida: ' + client_response)

    # Executa comandos no banco de dados
    db_return = handle_query(db_connection, client_response)

    # Converte resultado em string para enviar pro cliente
    msg_return = 'Retorno do banco: ' + db_return
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


## Fluxo principal ##

# Criação do banco de dados PSQL
db_connection, db_cursor = create_database();

# Criação do objeto socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincula o endereço IP e a porta ao socket
server_socket.bind((server_ip, server_port))

# Coloca o socket no modo de escuta, com limite de 5 conexões
server_socket.listen(5)

print('Servidor pronto para receber conexões...')

# Criação do contexto SSL/TLS 
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_verify_locations(cafile='certificados/certificate-client.crt')
context.load_cert_chain(certfile=cert_file, keyfile=key_file)
context.keylog_filename = './logs/keylog.log'
context.verify_mode = ssl.CERT_REQUIRED

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

    # Cria uma thread pra processar a requisição do cliente
    client_handler = threading.Thread(target=handle_request, args=(secure_connection, db_connection,))
    client_handler.start()


# Fecha as conexões com o banco de dados
db_cursor.close()
db_connection.close()