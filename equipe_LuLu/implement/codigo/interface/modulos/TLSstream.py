#!/bin/env python3


"""Módulo para gerenciar streams de dados via TCP com suporte a TLS.

A comunicação é P2P com suporte ao protocolo TLS (caso desejado), baseada no modelo cliente-servidor.

Para iniciar um servidor, use a classe :class:`TLSserver`. Para iniciar um cliente que se conecta com um servidor,
use a classe :class:`TLSclient`. Os parâmetros necessários para instanciar essas classes são o PATH dos arquivos da
chave privada própria, do certificado próprio, do certificado do PEER (quem está do outro lado da conexão), e
do arquivo de log. Se os arquivos de chaves e certificados forem omitidos, não será usado TLS na comunicação.

Não é possível um objeto (:class:`TLSserver` ou :class:`TLSclient`) enviar e receber dados simultaneamente. Isso é
uma limitação da implementação. Caso deseje enviar dados e receber simultaneamente, crie dois objetos para isso.
Um que envia dados, e outro que recebe dados.

O envio e recebimento de dados é feito exigindo a confirmação pelo outro lado da comunicação. Ou seja, se um frame
(conjunto de dados enviado) for enviado, o lado recebedor envia uma confirmação para o lado que enviou.

Não use a classe `_TLSstreamBase`. Ela serve apenas de base para as demais classes.
"""


from .log import LogFile
import threading
import asyncio
import ssl
import time


class _TLSstreamBase():
    """Base para a implementação do stream de dados com criptografia TLS.
    
    Não funciona por conta própria. Essa classe não deve ser usada pelo cliente final.
    Eles devem usar a :class:`TLSclient` e :class:`TLSserver` ao invés disso.

    Após iniciar o objeto, é necessário estabelecer a conexão. Para isso, use o método :meth:`connect()`.
    Ao estabelecer a conexão, estará inicialmente em modo de envio de dados. Ou seja, apenas pode enviar
    dados, não pode receber. Use o método :meth:`send()` para enviar os dados.

    Para receber dados, use o método :meth:`recv_set()`. Ele configura a conexão para modo de recebimento.
    Após isso, a conexão não pode mais enviar dados (não use mais o método :meth:`send()`), mas consegue
    receber dados do outro ponto da conexão. Após o recebimento de um conjunto de dados, ele será salvo
    no atributo *dados* do objeto, e a função de callback será chamada.

    Para finalizar o cliente ou servidor use o método :meth:`close()`. O objeto se torna inutilizável após isso.

    Attributes
    ----------
    log_prefix : str, default="[exemplo ]"
        Prefixo colocado nas mensagens de log do objeto.

    _PROTOCOL_TLS : _SSLMethod, default=ssl.PROTOCOL_TLS_CLIENT
        Configuração do protocolo TLS usado na comunicação.
    """

    log_prefix = "[exemplo] "
    _PROTOCOL_TLS = ssl.PROTOCOL_TLS_CLIENT

    def __init__(self, my_key='', my_crt='', peer_crt='', log_file_path=''):
        """Configura o stream de dados com TLS.

        Configura as credenciais (chave privada e certificados), e arquivo de log da comunicação.

        Se os parâmetros *my_key*, *my_crt* e *peer_crt* forem omitidos, a conexão
        ocorrerá sem verificação de credenciais (sem criptografia).

        Todos os arquivos de credenciais devem estar no formato PEM.
        Para mais informações, veja: https://docs.python.org/3/library/ssl.html#certificates

        Se o parâmetro *log_file_path* estiver vazio, o log não será registrado. Apenas será
        apresentado na saída padrão;

        Esse método não inicia a conxão automáticamente, use o método :meth:`connect` para isso.

        Parameters
        ----------
        my_key: str, default=''
            Arquivo da chave privada própria.

        my_crt: str, default=''
            Arquivo do certificado próprio.

        peer_crt: str, default=''
            Arquivo do certificado de quem está no outro lado da conexão.

        log_file_path: str, default=''
            Arquivo de log.
        """
        # Atributos
        self.dados = ''
        self.HOST = ''
        self.PORT = ''
        self._esta_recebendo = False
        self._pode_usar_dados = True
        self._pode_enviar_receber_dados = False
        self._recv_callback = None
        self.esta_conectado = False

        # Credenciais
        self._contexto = None
        if my_key!='' or my_crt!='' or peer_crt!='':
            self._contexto = ssl.SSLContext(self._PROTOCOL_TLS)
            self._contexto.check_hostname = False
            self._contexto.verify_mode = ssl.CERT_REQUIRED
            self._contexto.load_cert_chain(my_crt, my_key)
            self._contexto.load_verify_locations(peer_crt)

        # Arquivo de log
        self._log = LogFile(log_file_path, self.log_prefix)

    async def _send(self, reader, writer):
        """Envia os dados salvos no atributo *self.dados* para o outro lado da conexão.

        Esse método é chamado apenas quando o objeto estiver configurado para envio.

        Os parâmetros *reader* e *writer* são os mesmos obtidos ao estabelecer uma comunicação usando biblioteca 'asyncio'.

        Parameters
        ----------
        reader:
            Recebedor de streams da biblioteca Streams.

        writer:
            Enviador de streams da biblioteca Streams.
        """
        # Pode realizar operações de envio de dados
        self._pode_usar_dados = True

        # Realiza o recebimento e envio até a conexão encerrar
        while self._continuar_conexao:
            # Aguarda até o próximo frame poder ser enviado
            while not self._pode_enviar_receber_dados:
                pass

            self._pode_enviar_receber_dados = False

            # Envia o cabeçalho do frame
            cabecalho = (str(len(self.dados)) + '!').encode()
            writer.write(cabecalho)
            await writer.drain()

            # Envia o frame
            writer.write(self.dados)
            await writer.drain()

            # Espera a confirmação do cliente
            confirmacao = await reader.readuntil(b'!')

            # Erro na confirmação
            if confirmacao != b'OK!':
                self._log.register("Erro na confirmação de recebimento do frame! Finalizando conexão...")
                break

            # Pode escrever nos dados (próximo envio)
            self._pode_usar_dados = True

        # Finaliza a conexão
        writer.close()
        await writer.wait_closed()

    async def _recv(self, reader, writer):
        """Método executado ao receber uma mensagem do outro lado da comunicação.

        Recebe os dados enviados pelo outro lado da conexão, salva no atributo *self.dados* e chama a método de
        callback :meth:`_recv_callback()`. Esse método é configurado pelo método :meth:`recv_set()`.

        É chamado apenas quando o objeto estiver configurado para recebimento.

        Os parâmetros *reader* e *writer* são os mesmos obtidos ao estabelecer uma comunicação usando biblioteca 'asyncio'.

        Parameters
        ----------
        reader:
            Recebedor de streams da biblioteca Streams.

        writer:
            Enviador de streams da biblioteca Streams.
        """
        while self._continuar_conexao:
            # Lê os dados
            self.dados = await reader.readuntil(b'!')

            if isinstance(self.dados, bytes):
                tamanho = int(self.dados.decode()[0:-1])

            else:
                break

            self.dados = await reader.read(tamanho)

            # Conexão finalizada pelo enviador
            if not self.dados:
                self._log.register("Conexão finalizada. Esperando próxima conexão...")
                break

            # Envia a confirmação de recebimento
            writer.write(b'OK!')
            await writer.drain()

            self._recv_callback(self)

        # Finaliza a conexão
        writer.close()
        await writer.wait_closed()

    def _reset_connection_config(self):
        """Redefine as configurações de conexão.

        Também pode ser chamado ao iniciar uma conexão para definir as configurações padrões.
        """
        self.esta_conectado = False
        self._pode_usar_dados = False
        self.dados = ''

        # No caso de o recebimento ser assíncrono, deve considerar que sempre pode receber dados
        if self._recv_callback == None:
            self._pode_enviar_receber_dados = False  # Síncrono

        else:
            self._pode_enviar_receber_dados = True   # Assíncrono

    async def _connect_async(self):
        """Implementação da stream P2P.

        A implementação depende se é um cliente ou servidor. Por isso, está vazia nessa classe. As
        classes :class:`TLSclient` e :class:`TLSserver` sobrescreverão esse método.
        """
        pass

    def _connect_thread(self):
        """Thread onde será executado a conexão.

        Inicia a conexão de forma assíncrona com a biblioteca 'asyncio'.
        """
        asyncio.run(self._connect_async())

    def connect(self, HOST, PORT):
        """Inicia o stream P2P. Conecta ao *HOST* pela porta *PORT*.

        Ela será feita no servidor *HOST* pela porta *PORT*. No caso de ser um servidor, ficará escutando
        na porta *PORT* do servidor *HOST*. No caso de ser um cliente, tentará se conectar ao servidor.

        Por padrão, a conexão estará configurada para modo de envio. Use o método :meth:`recv_set()`
        para configurar para modo de recebimento. Após mudar para recebimento, não será possível mais
        enviar mensagens por essa conexão.

        Parameters
        ----------
        HOST : str
            Endereço do servidor usado na conexão.

        PORT : int
            Porta usada para estabelecer a conexão.
        """
        # Salva as informações de conexão
        self.HOST = HOST
        self.PORT = PORT

        # Inicia a conexão em uma thread diferente da principal
        self._thread = threading.Thread(target=self._connect_thread)
        self._continuar_conexao = True
        self._thread.start()

    def send(self, dados: bytes, wait=True):
        """Envia um conjunto de dados pela conexão.

        Esse método apenas pode ser chamado quando o objeto estiver configurado para envio.
        Os dados devem estar no formato de bytes.

        Parameters
        ----------
        dados: bytes
            Dados a serem enviados para o outro lado da comunicação.

        wait: bool, default=True
            Se o valor for True, espera o conjunto de dados anterior ser completamente enviado até de
            enviar o próximo. Se for False, cancela o envio caso um pacote já esteja sendo enviado.
        """
        # Cancela o envio se não pode enviar
        if not wait and not self._pode_usar_dados:
            return 1

        # Espera até poder enviar os dados
        while not self._pode_usar_dados:
            pass

        # Envia os dados
        self._pode_usar_dados = False

        self.dados = dados

        self._pode_enviar_receber_dados =  True

        # Espera até os dados serem enviados
        while wait and not self._pode_usar_dados:
            pass

        return 0

    def recv_set(self, callback):
        """Define para receber os dados assincronamente.

        Ao receber os dados, eles serão salvos no atributo *self.dados* e a função de
        callback será chamada. Ela tem a seguinte definição: callback(self). *self* é o
        objeto que recebeu os dados.

        Deve ser chamada antes de iniciar a conexão com o método :meth:`connect()`. Após ser
        chamada, não será mais possível enviar mensagens, apenas receber.

        Parameters
        ----------
        callback: callable
            Função que será executada ao receber os dados.
        """
        self._esta_recebendo = True
        self._recv_callback = callback

    def close(self):
        """Finaliza a conexão.

        O objeto se torna inutilizável após isso.
        """
        self._continuar_conexao = False

        # Se não foi feito uma conexão, então o atributo *self._thread* não foi instanciado.
        # Por isso, checa se ela existe e se está ativa antes de se juntar thread.
        if '_thread' in locals():
            if self._thread.is_alive():
                self._thread.join()


class TLSclient(_TLSstreamBase):
    """Cliente que se comunica com um servidor. Utiliza TLS.

    Essa classe é a implementação da :class:`_TLSstreamBase` para atuar como cliente da comunicação.
    O cliente é quem solicita o início da comunicação com o servidor.

    Os métodos para iniciar a conexão, receber e enviar dados são herdados da :class:`_TLSstreamBase`.

    Parameters
    ----------
    my_key: str, default=''
        Arquivo da chave privada própria.

    my_crt: str, default=''
        Arquivo do certificado próprio.

    peer_crt: str, default=''
        Arquivo do certificado de quem está no outro lado da conexão.

    log_file_path: str, default=''
        Arquivo de log.

    Attributes
    ----------
    log_prefix : str, default="[Client ]"
        Prefixo colocado nas mensagens de log do objeto.

    _PROTOCOL_TLS : _SSLMethod, default=ssl.PROTOCOL_TLS_CLIENT
        Configuração do protocolo TLS usado na comunicação.

    Examples
    --------
    Para criar um cliente, use:

    >>> cliente = TLSstream.TLSclient(
    >>>     "minha-chave.key",
    >>>     "meu-certificado.crt",
    >>>     "certificado-peer.crt",
    >>>     "arquivo-log.log"
    >>>     )

    Para estabelecer uma conexão, use:

    >>> cliente.connect("192.168.0.1", 3000)  # Se conectando ao IP 192.168.0.1 e porta 3000

    Enviando dados ao servidor:

    >>> cliente.send(b"12345")
    
    É possível configurá-lo para receber dados da seguinte forma:

    >>> def callback_recebimento(self):
    >>>     print(self.dados)  # mostra os dados recebidos
    >>> 
    >>> cliente.recv_set(callback_recebimento)

    Notes
    -----
    Após a conexão ser configurada para recebimento, não é possível mais enviar dados por ela.
    Se deseja receber e enviar dados, use duas conexões. Uma para envio e outra para recebimento.
    """

    log_prefix = "[Client] "                 # Prefixo do arquivo de log
    _PROTOCOL_TLS = ssl.PROTOCOL_TLS_CLIENT  # Será um cliente

    async def _connect_async(self):
        """
        Implementação da conexão assíncrona do 'asyncio'.

        Inicia a comunicação. Checa a possibilidade de erros. Se estiver no modo de envio,
        chama o método :meth:`~_TLSstreamBase._send()`. Caso esteja no modo de recebimento, chama o método
        :meth:`~_TLSstreamBase._recv()`. Ambos são herdados da classe :class:`_TLSstreamBase`.
        """
        while self._continuar_conexao:
            # Configuração inicial das conexões
            self._reset_connection_config()

            try:
                reader, writer = await asyncio.open_connection(self.HOST, self.PORT, ssl=self._contexto)

            # Se a conexão não funcionou por algum motivo
            except ssl.SSLError:
                self._log.register("Erro relacionado ao TLS! Tentando novamente...", True)
                time.sleep(1)
                continue

            except ssl.SSLCertVerificationError:
                self._log.register("Falha na validação do certificado! Tentando novamente...", True)
                time.sleep(1)
                continue

            except ConnectionRefusedError:
                self._log.register("Conexão recusada! Tentando novamente...", True)
                time.sleep(1)
                continue

            except ConnectionResetError:
                self._log.register("Conexão interrompida! Esperando próxima conexão...", True)
                time.sleep(1)
                continue

            # Conexão estabelecida com sucesso
            else:
                self._log.register("Conectado ao host " + self.HOST + ":" + str(self.PORT))

                try:
                    # Inicia o tipo de conexão correspondente
                    if self._esta_recebendo:
                        await self._recv(reader, writer)

                    else:
                        await self._send(reader, writer)

                # Em caso de encerramento forçado, limpa os dados e reinicia a conexão
                except ConnectionResetError:
                    self._log.register("Conexão interrompida! Finalizando conexão...", True)

                except BrokenPipeError:
                    self._log.register("Leitura/escrrita da Stream interrompida! Finalizando conexão...", True)

                except ssl.SSLError:
                    self._log.register("Erro relacionado ao TLS (após a conexão)! Finalizando conexão...", True)

                except asyncio.exceptions.IncompleteReadError:
                    self._log.register("Conexão incompleta! Finalizando conexão...", True)


class TLSserver(_TLSstreamBase):
    """Servidor que se comunica com o cliente. Utiliza TLS.

    Essa classe é a implementação da :class:`_TLSstreamBase` para atuar como servidor da comunicação.
    O servidor é quem aguarda a solicitação de comunicação do cliente.

    Os métodos para iniciar a conexão, receber e enviar dados são herdados da :class:`_TLSstreamBase`.

    O cliente e o servidor são operados da mesma forma. A diferença é que servidor espera pelo
    cliente iniciar a comunicação com ele. Os métodos :meth:`~_TLSstreamBase.send` e
    :meth:`~_TLSstreamBase.set_recv` são válidas para essa classe e funcionam da mesma forma.

    Parameters
    ----------
    my_key: str, default=''
        Arquivo da chave privada própria.

    my_crt: str, default=''
        Arquivo do certificado próprio.

    peer_crt: str, default=''
        Arquivo do certificado de quem está no outro lado da conexão.

    log_file_path: str, default=''
        Arquivo de log.

    Attributes
    ----------
    log_prefix : str, default="[Client ]"
        Prefixo colocado nas mensagens de log do objeto.

    _PROTOCOL_TLS : _SSLMethod, default=ssl.PROTOCOL_TLS_CLIENT
        Configuração do protocolo TLS usado na comunicação.

    Examples
    --------
    Para criar um servidor, use:

    >>> servidor = TLSstream.TLSserver(
    >>>     "minha-chave.key",
    >>>     "meu-certificado.key",
    >>>     "certificado-peer.key",
    >>>     "arquivo-log.log"
    >>>     )

    Para aguardar uma conexão em uma porta, use:

    >>> servidor.connect("192.168.0.1", 3000)  # Aguarda uma conexão na porta 3000

    Enviando dados ao cliente:

    >>> servidor.send(b"12345")
    
    É possível configurá-lo para receber dados da seguinte forma:

    >>> def callback_recebimento(self):
    >>>     print(self.dados)  # mostra os dados recebidos

    >>> servidor.recv_set(callback_recebimento)

    Notes
    -----
    Após a conexão ser configurada para recebimento, não é possível mais enviar dados por ela.
    Se deseja receber e enviar dados, use duas conexões. Uma para envio e outra para recebimento.

    Para configurar o servidor, não use o endereço de loopback "127.168.0.1". Ele é um endereço
    interno ao sistema e apenas pode ser usado para estabelecer conexões internas (para teste, por exemplo).
    Use o endereço IP da própria máquina. Lembre que o cliente se conectará usando esse mesmo IP.
    """

    log_prefix = "[Server] "                 # Prefixo do arquivo de log
    _PROTOCOL_TLS = ssl.PROTOCOL_TLS_SERVER  # Será servidor

    async def _server_callback(self, reader, writer):
        """Método de Callback chamado ao estabelecer a comunicação.

        Inicia a comunicação. Checa a possibilidade de erros. Se estiver no modo de envio,
        chama o método :meth:`~_TLSstreamBase._send()`. Caso esteja no modo de recebimento, chama o método
        :meth:`~_TLSstreamBase._recv()`. Ambos são herdados da classe :class:`_TLSstreamBase`.

        Parameters
        ----------
        reader:
            Recebedor de streams da biblioteca Streams.

        writer:
            Enviador de streams da biblioteca Streams.
        """
        # Configuração inicial das conexões
        self._reset_connection_config()
        self.esta_conectado = True

        # Realiza o recebimento e envio até a conexão encerrar
        try:
            self._log.register("Nova conexão estabelecida...")

            # Inicia o tipo de conexão correspondente
            if self._esta_recebendo:
                await self._recv(reader, writer)

            else:
                await self._send(reader, writer)

        # Em caso de encerramento ou erro, limpa os dados e reinicia a conexão
        except ConnectionResetError:
            self._log.register("Conexão interrompida! Finalizando conexão...", True)

        except BrokenPipeError:
            self._log.register("Leitura/escrrita da Stream interrompida! Finalizando conexão...", True)

        except ssl.SSLError:
            self._log.register("Erro relacionado ao TLS (após a conexão)! Finalizando conexão...", True)

        except asyncio.exceptions.IncompleteReadError:
            self._log.register("Conexão incompleta! Finalizando conexão...", True)

        self.esta_conectado = False

    async def _connect_async(self):
        """
        Implementação da conexão assíncrona do 'asyncio'.

        Inicia a comunicação. Checa a possibilidade de erros. Se não ocorreu nenhum erro,
        espera a conexão do cliente. A conexão com o cliente é feita por meio do método :meth:`_server_callback()`.
        """
        try:
            self._server = await asyncio.start_server(self._server_callback, self.HOST, self.PORT, ssl=self._contexto)

        except:
            self._log.register("Ocorreu um erro ao tentar iniciar o servidor! Finalizando...")
            TLSstreamer.close(self)

        else:
            async with self._server:
                await self._server.serve_forever()

    def close(self):
        """Finaliza o servidor."""
        time.sleep(1)
        self._server.close()
        _TLSstreamBase.close(self)
