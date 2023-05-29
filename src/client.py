# Programa que atua como cliente no sistema de servidor/cliente
# AUTORES
# ANDREI ALISSON FERREIRA JULIO GRR20163061
# JOÃO PEDRO KIERAS OLIVEIRA GRR20190379

import socket
import ssl

# Define o endereço IP e a porta
target_ip = 'localhost'
target_port = 80
cert_file = 'certificados/cert_server.crt'
key_file = 'certificados/server.key'

# Criação do objeto socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configuração do contexto SSL/TLS
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_cert_chain(certfile=cert_file, keyfile=key_file)
context.check_hostname = False  # Desabilita verificação de hostname

# Inicia a camada de segurança SSL/TLS
secure_socket = context.wrap_socket(client_socket, server_hostname=target_ip)

# Conecta e envia uma mensagem para o servidor
secure_socket.connect((target_ip, target_port))

# Envia uma mensagem de input do usuário para o servidor
msg = input("digite uma mensagem para enviar ao servidor: ") 
secure_socket.send(msg.encode('utf-8'))

# Recebe 4096 bits de resposta
client_response = secure_socket.recv(4096)

# Imprime a resposta do servidor
print(client_response)