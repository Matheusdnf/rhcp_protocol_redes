import sys
import csv
from datetime import datetime
import socket

def close_socket_with_message(sock, message):
    sock.send(message.encode())
    sock.close()

def make_response(code=200, msg=None, objeto=None, status=None):
    linhas = [f"RHCP/1.0 {code} {msg if msg else 'OK'}"]
    if objeto: linhas.append(f"Object: {objeto}")
    if status: linhas.append(f"Status: {status}")
    linhas.append("Date: " + str(datetime.now()))
    linhas.append("")
    return "\r\n".join(linhas) + "\r\n"


def parse_request(msg: str):
    lines = msg.split("\r\n")
    line_req = lines[0]
    parts = line_req.split(" ")
    if len(parts) != 3:
        return None, None, None, None
    method = parts[0]
    obj = parts[1]
    version = parts[2]
    headers = {}
    for line in lines[1:]:
        if not line.strip():
            break
        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()
    return method, obj, version, headers


def handle_request(method, obj, headers, data):
    if obj not in data:
        return make_response(404, "Not Found")
    
    if method == "GET":
        if "Request" not in headers or headers["Request"] != "status":
            return make_response(400, "Bad Request")
        status = data[obj]
        return make_response(200, "OK", objeto=obj, status=status)
    else:
        if "Status" not in headers:
            return make_response(400, "Bad Request")
        new_status = headers["Status"]
        if new_status not in ["on", "off"]:
            return make_response(400, "Bad Request")
        data[obj] = new_status
        
        # salvando os dados atualizados no arquivo
        try:
            with open('status.csv', mode='w', newline='') as arquivo_csv:
                csv_writer = csv.writer(arquivo_csv)
                for key, value in data.items():
                    csv_writer.writerow([key, value])
        except Exception as e:
            print(f"Erro ao escrever no arquivo status.csv: {e}")
            return make_response(500, "Internal Server Error")
        return make_response(200, "OK", objeto=obj, status=new_status)
    
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

    msg_req = clientsocket.recv(4096).decode()
    
    print(f"REQUISICAO: \n{msg_req}")

    method, obj, version, headers = parse_request(msg_req)
        
    if method is None or version != "RHCP/1.0":
        close_socket_with_message(clientsocket, make_response(400, "Bad Request"))
        continue
    
    if method not in ["GET", "SET"]:
        close_socket_with_message(clientsocket, make_response(405, "Method Not Allowed"))
        continue

    # Carregar os dados do arquivo status.csv
    try:
        with open('status.csv', mode='r') as arquivo_csv:
            csv_reader = csv.reader(arquivo_csv)
            data = list(csv_reader)
        datadict = {row[0]: row[1] for row in data}

    except Exception as e:
        print(f"Erro ao ler o arquivo status.csv: {e}")
        close_socket_with_message(clientsocket, make_response(500, "Internal Server Error"))
        continue
    
    msg_res = handle_request(method, obj, headers, datadict)

    # enviando a mensagem de resposta ao cliente
    clientsocket.send(msg_res.encode())

    # finalizando o socket do cliente
    clientsocket.close()