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

# Lida com os inputs do usuario para obter os detalhes da requisicao
def handle_input():

    # Recebe a ação a ser realizada
    msg_input = input("Digite uma acao: 1-Select, 2-Insert, 3-Update, 4-Delete, 5-Exit: ")
    if msg_input not in ['1', '2', '3', '4', '5']:
        print ('Entrada Invalida, tente novamente')
        return 'continue'

    # Consulta (Chave ou valor)
    if msg_input == '1':
        msg_input += '|' + input('Digite o campo utilizado para consulta: 1-Chave, 2-Valor: ')
        if msg_input not in ['1|1', '1|2']:
            print ('Entrada invalida, tente novamente')
            return 'continue'
        
        # Consulta por chave
        if msg_input == '1|1':
            msg_tmp = input ('Digite a Chave a ser consultada no banco de dados: ')

            # Verifica se a chave digitada é um valor inteiro
            if not (msg_tmp.isdigit()):
                print ('Dado digitado deve ser inteiro, tente novamente')
                return 'continue'
            
            msg_input += '|' + msg_tmp
            
        # Consulta por valor
        elif msg_input == '1|2':
            msg_tmp = input ('Digite o valor a ser consultado no banco de dados: ')

            if msg_tmp == '':
                print ('Dado nao pode ser vazio, tente novamente')
                return 'continue'
            
            msg_input += '|' + msg_tmp

        cmd_input = msg_input
    
    # Insert (Chave e Valor)
    elif msg_input == '2':
        msg_tmp = input ('Digite a Chave a ser inserida no banco de dados: ')

        # Verifica se a chave digitada é um valor inteiro
        if not (msg_tmp.isdigit()):
            print ('Dado digitado deve ser inteiro, tente novamente')
            return 'continue'
        
        msg_input += '|' + msg_tmp
        
        msg_tmp = input ('Digite o valor a ser inserido no banco de dados: ')

        if msg_tmp == '':
            print ('Dado nao pode ser vazio, tente novamente')
            return 'continue'
        
        msg_input += '|' + msg_tmp

        cmd_input = msg_input
        
    # Update (Chave e valor)
    elif msg_input == '3':
        msg_tmp = input ('Digita a chave do dado a ser atualizado: ')

         # Verifica se a chave digitada é um valor inteiro
        if not (msg_tmp.isdigit()):
            print ('Dado digitado deve ser inteiro, tente novamente')
            return 'continue'
        
        msg_input += '|' + msg_tmp

        msg_tmp = input ('Digite o novo valor a ser atualizado no banco de dados: ')

        if msg_tmp == '':
            print ('Dado nao pode ser vazio, tente novamente')
            return 'continue'
        
        msg_input += '|' + msg_tmp

        cmd_input = msg_input

    # Delete (Chave)
    elif msg_input == '4':
        msg_tmp = input ('Digite a Chave a ser excluida do banco de dados: ')

        # Verifica se a chave digitada é um valor inteiro
        if not (msg_tmp.isdigit()):
            print ('Dado digitado deve ser inteiro, tente novamente')
            return 'continue'
        
        msg_input += '|' + msg_tmp

        cmd_input = msg_input

    # Encerra o programa
    elif msg_input == '5':
        print ('Encerrando cliente.')
        return 'exit'


    # Caso algo dê errado
    if cmd_input == '':
        print ('Entrada invalida')
        return 'continue'

    print ('comando a ser enviado: ' + cmd_input)

    return cmd_input


# Envia uma mensagem de input do usuário para o servidor
while True:

    # Lida com os inputs do usuario para saber como proceder
    cmd_input = handle_input()

    if cmd_input == 'continue':
        continue

    if cmd_input == 'exit':
        break

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

    secure_socket.send(cmd_input.encode('utf-8'))

    # Recebe 4096 bits de resposta
    client_response = secure_socket.recv(1024)

    # Imprime a resposta do servidor
    print(client_response)

    secure_socket.close()
    client_socket.close()