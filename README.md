# RHCP - Remote House Control Protocol

## SERVIDORES

É necessário que o script para execução dos servidores tenha permissão de
execução definida. Para isto:

```bash
chmod +x run.sh
```

Para executar os servidores:

```bash
./run.sh
```

## CLIENTE

Para execução do `cliente.py` há algumas possibilidades:

| Comando | Descrição | Exemplo |
| --- | --- | --- |
| `python3 cliente.py` | A requisição deverá ser inserida no terminal no formato estipulado¹. | - |
| `python3 cliente.py METODO OBJETO` | Usado para requisições do tipo GET. | `python3 cliente.py GET sala/luz` |
| `python3 cliente.py METODO OBJETO STATUS` | Usado para requisições do tipo SET. | `python3 cliente.py SET sala/luz on` |

Quaisquer outros tipos de comandos poderão implicar no não envio da requisição ao servidor. Outros métodos são permitidos para fins de teste de servidor.

¹Formato:
```
    METODO Objeto RHCP/1.0\r\n
    Campo: valor\r\n
    ...
    Campo: valor\r\n
    \r\n
```

OBS: **`Enter` SUBSTITUI `\r\n`, NÃO DIGITÁ-LOS**.

## SOBRE O PROTOCOLO

Foram estabelecidas regras de requisição e resposta.

1. Formato de Mensagem de Requisição:

```
METODO Objeto RHCP/1.0\r\n
Campo: valor\r\n
...
Campo: valor\r\n
\r\n
```

2. METODOS possíveis na Requisição: GET e SET.

3. OBJETOS possíveis na Requisição: listados no arquivo -> [status.csv](status.csv).

4. CAMPOS possíveis na Requisição: Request (apenas aceita status) e Status (apenas aceita `on`/`off`).

5. Formato de Mensagem de Resposta:

```
RHCP/1.0 Codigo Mensagem\r\n
Campo: valor\r\n
...
Campo: valor\r\n
\r\n
```
6. CODIGOS DE MENSAGEM possíveis na Resposta: 200 OK, 400 Bad Request, 404 Not Found, 405 Method Now Allowed e 500 Internal Server Error.

7. CAMPOS possíveis na Resposta: Object (apenas retorna o nome do objeto), Status (apenas retorna `on`/`off`) e Date (apenas retorna o `datetime`).

### Problemas 

Apesar de estipuladas algumas regras, há inconsistências:

1. Não foi definido quando "Date" deve ser adicionado ao cabeçalho de resposta;
2. Não foi definido o formato de "Date" ao ser retornado.

Como solução, foi definido:

1. Que o valor do Date seria sempre apresentado na Resposta;
2. Que o valor do Date estaria no formato "puro", sem formatações adicionais.
