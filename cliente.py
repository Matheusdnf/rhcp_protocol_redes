# importando o modulo socket
import sys
import socket
import argparse

# definindo o IP do servidor
IP_SERVIDOR_RHCP = "127.0.0.1"

# definindo a porta do servidor
PORTA_SERVIDOR_RHCP = 8000

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("method", nargs="?", help="Métodos: GET, SET")
    p.add_argument("object", nargs="?", help="Objeto da requisição, ex: sala/luz")
    p.add_argument("status", nargs="?", help="Status: on/off (em requisições SET)")
    return p.parse_args()

def thow_error_and_exit(message: str):
    print(message)
    exit(1)

def read_input() -> bytes:
    print("Digite a requisição (linha vazia para enviar):")
    linhas = []
    while True:
        linha = input()
        if not linha.strip():
            break
        linhas.append(linha.strip())

    msg = ("\r\n".join(linhas) + "\r\n\r\n").encode("utf-8", errors="ignore")
    return msg

def message(meth, obj, camp=None) -> bytes:
    # Mensagem de requisição
    mensagem_requisicao = f"{meth} {obj} RHCP/1.0"
    if meth=="SET":
        cabecalho = f"Status: {camp}"
    elif meth=="GET":
        cabecalho = f"Request: status"
    else:
        cabecalho = ""

    linhas = [mensagem_requisicao] + [cabecalho] + [""]
    msg = ("\r\n".join(linhas) + "\r\n").encode("utf-8", errors="ignore")
    return msg


def load_args() -> bytes:
    args = parse_args()

    if not args.method:
        msg = read_input()
    elif args.method == "GET" and not args.object:
        thow_error_and_exit("Erro: GET requer um objeto. \nExemplo: python cliente.py GET sala/luz")
    elif args.method == "SET" and (not args.object or not args.status):
        thow_error_and_exit("Erro: SET requer um objeto e um status. \nExemplo: python cliente.py SET sala/luz on")
    elif args.method == "GET" and args.status:
        thow_error_and_exit("Erro: GET não precisa de status. \nExemplo: python cliente.py GET sala/luz")
    else:
        msg = message(args.method, args.object, args.status)
    
    return msg



# criando um socket Internet (INET IPv4) sobre TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# conectando ao servidor
s.connect((IP_SERVIDOR_RHCP, PORTA_SERVIDOR_RHCP))

# enviando a requisicao
msg_req = load_args()
print(f"REQUISICAO: \n{msg_req}")
# Formato da requisição:
# GET sala/luz RHCP/1.0
# Request: status
s.send(msg_req)

# recebendo a resposta
msg_res = s.recv(500)
# tratando a resposta
print(f"RESPOSTA: \n{msg_res}")

# fechando o socket
s.close()