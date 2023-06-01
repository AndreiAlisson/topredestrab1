# Programa que atua como cliente no sistema de servidor/cliente
# AUTORES
# ANDREI ALISSON FERREIRA JULIO GRR20163061
# JOÃO PEDRO KIERAS OLIVEIRA GRR20190379

import socket
import ssl

# Define o endereço IP e a porta
target_ip = 'localhost'
target_port = 80
cert_file = 'certificados/certificate-client.crt'
key_file = 'certificados/certificate-client.key'

# Criação do objeto socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configuração do contexto SSL/TLS
#context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_verify_locations(cafile='certificados/certificate-server.crt')
context.load_cert_chain(certfile=cert_file, keyfile=key_file)

#context.check_hostname = False  # Desabilita verificação de hostname
context.verify_mode = ssl.CERT_REQUIRED

# Inicia a camada de segurança SSL/TLS
secure_socket = context.wrap_socket(client_socket, server_hostname=target_ip)

# Conecta e envia uma mensagem para o servidor
secure_socket.connect((target_ip, target_port))

# Envia uma mensagem de input do usuário para o servidor
while True:
    msg_input = input("Digite uma acao: 0-Select, 1-Insert, 2-Update, 3-Delete, 4-Exit\n")
    if msg_input not in ['0', '1', '2', '3', '4']:
        print ('Entrada incorreta')
        continue

    if msg_input == '0':
        print ('Digite os dados (Chave) a serem consultados no banco de dados')
    elif msg_input == '1':
        print ('Digite os dados (Chave, Valor) a serem inseridos no banco de dados')
    elif msg_input == '2':
        print ('Digite os dados (Chave, Valor antigo, Valor novo)a serem atualizados no banco de dados')
    elif msg_input == '3':
        print ('Digite os dados (Chave, Valor) a serem excluidos do banco de dados')
    elif msg_input == '4':
        print ('Encerrando cliente.')
        break
    print ('chegou')
    cmd_input = input ("")

    cmd_input = msg_input + '|' + cmd_input
    secure_socket.send(cmd_input.encode('utf-8'))

    # Recebe 4096 bits de resposta
    client_response = secure_socket.recv(4096)

    # Imprime a resposta do servidor
    print(client_response)