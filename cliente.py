# importando o modulo socket
import socket

# definindo o IP do servidor
IP_SERVIDOR_RHCP = "127.0.0.1"

# definindo a porta do servidor
PORTA_SERVIDOR_RHCP = 8000

def mensagem(metodo:str,objeto:str,campos:str) -> bytes:
#     METODO Objeto RHCP/1.0\r\n
#     Campo: valor\r\n
#     ...
#     Campo: valor\r\n
#     \r\n
    # Mensagem de requisição
    mensagem_requisicao = f"{metodo} {objeto} RHCP/1.0\r\n"
    cabecalhos = []
    for campo, valor in campos.items():
        cabecalhos.append(f"{campo}: {valor}")

    linhas = [mensagem_requisicao] + cabecalhos + [""]
    
    return "\r\n".join(linhas).encode()


# criando um socket Internet (INET IPv4) sobre TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# conectando ao servidor
s.connect((IP_SERVIDOR_RHCP, PORTA_SERVIDOR_RHCP))

# enviando a requisicao
msg_req = mensagem(
    metodo="GET",
    objeto="/recursos/usuarios",
    campos={
        "Host": "127.0.0.1",
        "User-Agent": "ClienteRHCP/1.0",
        "Accept": "text/plain"
    }
)
s.send(msg_req)

# recebendo a resposta
msg_res = s.recv(500)
# tratando a resposta
print(f"RESPOSTA: {msg_res}")

# fechando o socket
s.close()
