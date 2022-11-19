import socket
import threading
import yahooquery as yq
from yahooquery import Ticker


class Servidor():
    """
    Classe Servidor - API Socket
    """

    def __init__(self, host, port):
        """
        Construtor da classe servidor
        """
        self._host = host
        self._port = port

    def start(self):
        """
        Método que inicializa a execução do servidor
        """
        # criando um serviço com API SOCKET
        # CRIOU UM ATRIBUTO PRIVADO " 2 X _"
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # PRIMEIRO ARGUMETO - familia de endereços que vai receber aquele serviço (documentação da classe socket tem os demais)
        # AF_INET -> qualquer cliente que tenha algum ipv4 valido poderá se conectar ao serviço (defnido pelo comando socket)

        # SEGUNDO ARGUMENTO - qual o protocolo da camada de transporte que quer usar (SOCK_STREAM (TCP) OU SOCK_DGRAM (UDP))

        endpoint = (self._host, self._port)  # será utilizado para o bind

        try:  # Usado em aplicação distribuidas, algo pode dar errado: cabos, portas já sendo usadas, etc...
            # TRY -> Cria um bloco de código que é sucetível ao lançamento de exceções, tudo dentro dele é passivo de dar erro
            self.__tcp.bind(endpoint)
            # passa (0) ou () desativa , passar (1) ativa a backlog
            self.__tcp.listen(1)
            print("Servidor iniciado em ", self._host, ": ", self._port)
            while True:
                # método bloqueante, a aplicação fica parada até que seja sincronizado
                con, client = self.__tcp.accept()
                # con -> conexão com o cliente (objeto que permite ter acesso ao local do cliente)
                # client -> endpoint do cliente (host e porta do cliente)
                # passa os dados do cliente ao qual quer fornecer o serviço
                self._service(con, client)
        except Exception as e:  # Except -> para onde o código/execução será levado caso haja problema dentro do try
            # é acionado caso o try ocorra algum erro
            print("Erro ao inicializar o servidor", e.args)

    def _service(self, con, client):
        """
        Método que implementa o serviço de calculadora
        :param con: objeto socket utilizado para enviar e receber dados
        :param client: é o endereço do cliente
        """
        print("Atendendo cliente ", client)
        while True:
            try:
                # recv -> recive receber, metodo bloqueante que estpera receber os dados
                msg = con.recv(1024)
                # 1024 -> bytes -> é o tamanho maximo que pode ser recebido do cliente
                # decodifica os bytes utilizando a tabela ASCII e transforma em uma string
                msg_s = str(msg.decode('ascii'))

                code = msg_s.split(",")

                if code[1] == 'TRADEABLE':
                    resp = Ticker(msg_s).quotes[code[0]]['tradeable']
                if code[1] == 'REGION':
                    resp = Ticker(msg_s).quotes[code[0]]['region']
                if code[1] == 'PRICEHINT':
                    resp = Ticker(msg_s).quotes[code[0]]['priceHint']
                if code[1] == 'REGULARMARKETDAYRANGE':
                    resp = Ticker(
                        msg_s).quotes[code[0]]['regularMarketDayRange']

                # converte para string -> bytes (codifica)
                con.send(bytes(str(resp), 'ascii'))
                print(client, " -> requisição atendida")
            except OSError as e:
                print("Erro de conexão ", client, ": ", e.args)
                return
            except Exception as e:
                print("Erro nos dados recebidos pelo cliente ",
                      client, ": ", e.args)
                con.send(bytes("Erro", 'ascii'))
        # fica até perder a conexão
