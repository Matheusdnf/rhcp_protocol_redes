import sys
import csv

# importando o modulo socket
import socket

# verificando os argumentos passados
if len(sys.argv) == 2:
    # definindo a porta do servidor
    # obtendo o valor da porta da linha de comando
    PORTA_SERVIDOR_RHCP = int(sys.argv[1])
    print(f"Hello, !")
else:
    print("Erro, informe a PORTA do servidor")
    exit(1)

# definindo o IP do servidor / em branco para obter automaticamente e permitir
# acesso de qualuer iP de origem
IP = ""

# criando um socket Internet (INET IPv4) sobre TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# liga o socket ao enderecamento do servidor
s.bind((IP, PORTA_SERVIDOR_RHCP))

# habilita a escuta de conexoes
s.listen(1)

print(f"Servidor RHCP na porta TCP: {PORTA_SERVIDOR_RHCP}")

while True:
    # espera por uma conexao
    (clientsocket, clientaddress) = s.accept()

    print(f"Uma conexao com o endereco {clientaddress[0]}:{clientaddress[1]} foi estabelecida")

    # obtendo a mensagem de requisicao
    msg_req = clientsocket.recv(4096).decode()
    print(f"REQUISICAO: \n {msg_req}")
    # Tipo da mensagem é string mesmo
    # mas é exibindo chave e valor? , para poder tratar o que está sendo pedido ?
    # string. como ta ai só
    # acho que e usando splitzao mesmo, mas é tao porquinho :(
    # TODO:
    
    # - processar a mensagem no formato adequado
    # Dividir a mensagem em linhas

    linhas = msg_req.split("\r\n")
    # Extrair a linha de requisição
    linha_requisicao = linhas[0]
    
    
    # Dividir a linha de requisição em partes
    partes = linha_requisicao.split(" ")
    if len(partes) != 3:
        print("Erro na linha de requisição")
        clientsocket.close()
        continue
    
    # o metodo (GET ou SET)
    metodo = partes[0]
    
    # o objeto (sala/luz, sala/ar, cozinha/luz, etc)
    objeto = partes[1]

    versao = partes[2]
    
    if versao != "RHCP/1.0":
        print("Versao RHCP invalida")
        clientsocket.close()
        continue

    # Extrair os cabeçalhos
    linha_cabecalhos = linhas[2] 

    cabecalhos = {}
    if linha_cabecalhos:
        partes_cabecalhos = linha_cabecalhos.split(": ")
        if len(partes_cabecalhos) == 2:
            chave = partes_cabecalhos[0]
            valor = partes_cabecalhos[1]
        
            # o campo (status on/off, request status, etc)    
            cabecalhos[chave] = valor
    
    # - carregar os dados do arquivo status.csv
    try:
        with open('status.csv', mode='r') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            dados = list(leitor_csv)
    except FileNotFoundError:
        print("Arquivo status.csv não encontrado.")
        clientsocket.close()
        continue
    except Exception as e:
        print(f"Erro ao ler o arquivo status.csv: {e}")
        clientsocket.close()
        continue
    
    objeto_encontrado = False
    for linha in dados:
        if linha[0] == objeto:
            objeto_encontrado = True
            if metodo == "GET":
                status_atual = linha[1]
                msg_res = f"RHCP/1.0 200 OK\r\nStatus: {status_atual}\r\n\r\n"
            
            elif metodo == "SET":
                if "Status" in cabecalhos:
                    linha[1] = cabecalhos["Status"]

                    try:
                        with open('status.csv', mode='w', newline='') as arquivo_csv:
                            escritor_csv = csv.writer(arquivo_csv)
                            escritor_csv.writerows(dados)
                        msg_res = f"RHCP/1.0 200 OK\r\nStatus atualizado para: {cabecalhos['Status']}\r\n\r\n"
                    except Exception as e:
                        print(f"Erro ao salvar o arquivo status.csv: {e}")
                        msg_res = "RHCP/1.0 500 Internal Server Error\r\n\r\n"
                else:
                    msg_res = "RHCP/1.0 400 Bad Request\r\n\r\n"
                    
            break
  
    if not objeto_encontrado:
        msg_res = "RHCP/1.0 404 Not Found\r\n\r\n"

    # enviando a mensagem de resposta ao cliente
    clientsocket.send(msg_res.encode())

    # finalizando o socket do cliente
    clientsocket.close()