# importando o modulo socket
import sys
import socket

# definindo o IP do servidor
IP_SERVIDOR_RHCP = "127.0.0.1"

# definindo a porta do servidor
PORTA_SERVIDOR_RHCP = 8000

if len(sys.argv) >= 3:
    METHOD = sys.argv[1]
    OBJECT = sys.argv[2] 
else:
    print("Erro, informe: METODO E OBJETO, pelo menos")
    print("Exemplo: python3 cliente.py GET sala/luz")
    exit(1)


if len(sys.argv) == 4 and METHOD == "SET":
    CAMP = sys.argv[3] 
elif METHOD == "SET":
    print("Erro, informe o status.")
    print("Exemplo: python3 cliente.py SET sala/luz on")
    exit(1)

def mensagem() -> bytes:
#     METODO Objeto RHCP/1.0\r\n
#     Campo: valor\r\n
#     ...
#     Campo: valor\r\n
#     \r\n
    # Mensagem de requisição
    mensagem_requisicao = f"{METHOD} {OBJECT} RHCP/1.0\r\n"
    cabecalhos = []
    if METHOD=="SET":
        cabecalhos.append(f"Status: {CAMP}")
    elif METHOD=="GET":
        cabecalhos.append(f"Request: status")

    linhas = [mensagem_requisicao] + cabecalhos + [""]
    
    return "\r\n".join(linhas).encode()


# criando um socket Internet (INET IPv4) sobre TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# conectando ao servidor
s.connect((IP_SERVIDOR_RHCP, PORTA_SERVIDOR_RHCP))

# enviando a requisicao
msg_req = mensagem()
s.send(msg_req)

# recebendo a resposta
msg_res = s.recv(500)
# tratando a resposta
print(f"RESPOSTA: \n{msg_res.decode('utf-8')}")

# fechando o socket
s.close()