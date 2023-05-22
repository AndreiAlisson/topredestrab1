# Programa que atua como cliente no sistema de servidor/cliente
# AUTORES
# ANDREI ALISSON FERREIRA JULIO GRR20163061
# JOÃO PEDRO KIERAS

import socket

# Define o endereço IP e a porta
target_ip = 'localhost'
target_port = 80

# Criação do objeto socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta e envia uma mensagem para o servidor
client_socket.connect((target_ip, target_port))

# Envia uma mensagem de input do usuário para o servidor
msg = input("digite uma mensagem para enviar ao servidor: ") 
client_socket.send(msg.encode('utf-8'))

# Recebe 4096 bits de resposta
client_response = client_socket.recv(4096)

# Imprime a resposta do servidor
print(client_response)