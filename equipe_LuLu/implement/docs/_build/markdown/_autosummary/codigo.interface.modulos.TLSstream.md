<a id="module-codigo.interface.modulos.TLSstream"></a>

<a id="codigo-interface-modulos-tlsstream"></a>

# codigo.interface.modulos.TLSstream

Módulo para gerenciar streams de dados via TCP com suporte a TLS.

A comunicação é P2P com suporte ao protocolo TLS (caso desejado), baseada no modelo cliente-servidor.

Para iniciar um servidor, use a classe [`TLSserver`](#codigo.interface.modulos.TLSstream.TLSserver). Para iniciar um cliente que se conecta com um servidor,
use a classe [`TLSclient`](#codigo.interface.modulos.TLSstream.TLSclient). Os parâmetros necessários para instanciar essas classes são o PATH dos arquivos da
chave privada própria, do certificado próprio, do certificado do PEER (quem está do outro lado da conexão), e
do arquivo de log. Se os arquivos de chaves e certificados forem omitidos, não será usado TLS na comunicação.

Não é possível um objeto ([`TLSserver`](#codigo.interface.modulos.TLSstream.TLSserver) ou [`TLSclient`](#codigo.interface.modulos.TLSstream.TLSclient)) enviar e receber dados simultaneamente. Isso é
uma limitação da implementação. Caso deseje enviar dados e receber simultaneamente, crie dois objetos para isso.
Um que envia dados, e outro que recebe dados.

O envio e recebimento de dados é feito exigindo a confirmação pelo outro lado da comunicação. Ou seja, se um frame
(conjunto de dados enviado) for enviado, o lado recebedor envia uma confirmação para o lado que enviou.

Não use a classe \_TLSstreamBase. Ela serve apenas de base para as demais classes.

<a id="codigo.interface.modulos.TLSstream.TLSclient"></a>

### *class* codigo.interface.modulos.TLSstream.TLSclient(my_key='', my_crt='', peer_crt='', log_file_path='')

Base: [`_TLSstreamBase`](#codigo.interface.modulos.TLSstream._TLSstreamBase)

Cliente que se comunica com um servidor. Utiliza TLS.

Essa classe é a implementação da [`_TLSstreamBase`](#codigo.interface.modulos.TLSstream._TLSstreamBase) para atuar como cliente da comunicação.
O cliente é quem solicita o início da comunicação com o servidor.

Os métodos para iniciar a conexão, receber e enviar dados são herdados da [`_TLSstreamBase`](#codigo.interface.modulos.TLSstream._TLSstreamBase).

* **Parâmetros:**
  * **my_key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default=''*) – Arquivo da chave privada própria.
  * **my_crt** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default=''*) – Arquivo do certificado próprio.
  * **peer_crt** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default=''*) – Arquivo do certificado de quem está no outro lado da conexão.
  * **log_file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default=''*) – Arquivo de log.

<a id="codigo.interface.modulos.TLSstream.TLSclient.log_prefix"></a>

#### log_prefix

Prefixo colocado nas mensagens de log do objeto.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str), default=”[Client ]”

<a id="codigo.interface.modulos.TLSstream.TLSclient._PROTOCOL_TLS"></a>

#### \_PROTOCOL_TLS

Configuração do protocolo TLS usado na comunicação.

* **Type:**
  \_SSLMethod, default=ssl.PROTOCOL_TLS_CLIENT

### Exemplos

Para criar um cliente, use:

```pycon
>>> cliente = TLSstream.TLSclient(
>>>     "minha-chave.key",
>>>     "meu-certificado.crt",
>>>     "certificado-peer.crt",
>>>     "arquivo-log.log"
>>>     )
```

Para estabelecer uma conexão, use:

```pycon
>>> cliente.connect("192.168.0.1", 3000)  # Se conectando ao IP 192.168.0.1 e porta 3000
```

Enviando dados ao servidor:

```pycon
>>> cliente.send(b"12345")
```

É possível configurá-lo para receber dados da seguinte forma:

```pycon
>>> def callback_recebimento(self):
>>>     print(self.dados)  # mostra os dados recebidos
>>>
>>> cliente.recv_set(callback_recebimento)
```

### Notas

Após a conexão ser configurada para recebimento, não é possível mais enviar dados por ela.
Se deseja receber e enviar dados, use duas conexões. Uma para envio e outra para recebimento.

<a id="codigo.interface.modulos.TLSstream.TLSclient._connect_async"></a>

#### *async* \_connect_async()

Implementação da conexão assíncrona do ‘asyncio’.

Inicia a comunicação. Checa a possibilidade de erros. Se estiver no modo de envio,
chama o método [`_send()`](#codigo.interface.modulos.TLSstream._TLSstreamBase._send). Caso esteja no modo de recebimento, chama o método
[`_recv()`](#codigo.interface.modulos.TLSstream._TLSstreamBase._recv). Ambos são herdados da classe [`_TLSstreamBase`](#codigo.interface.modulos.TLSstream._TLSstreamBase).

<a id="codigo.interface.modulos.TLSstream.TLSserver"></a>

### *class* codigo.interface.modulos.TLSstream.TLSserver(my_key='', my_crt='', peer_crt='', log_file_path='')

Base: [`_TLSstreamBase`](#codigo.interface.modulos.TLSstream._TLSstreamBase)

Servidor que se comunica com o cliente. Utiliza TLS.

Essa classe é a implementação da [`_TLSstreamBase`](#codigo.interface.modulos.TLSstream._TLSstreamBase) para atuar como servidor da comunicação.
O servidor é quem aguarda a solicitação de comunicação do cliente.

Os métodos para iniciar a conexão, receber e enviar dados são herdados da [`_TLSstreamBase`](#codigo.interface.modulos.TLSstream._TLSstreamBase).

O cliente e o servidor são operados da mesma forma. A diferença é que servidor espera pelo
cliente iniciar a comunicação com ele. Os métodos [`send()`](#codigo.interface.modulos.TLSstream._TLSstreamBase.send) e
`set_recv()` são válidas para essa classe e funcionam da mesma forma.

* **Parâmetros:**
  * **my_key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default=''*) – Arquivo da chave privada própria.
  * **my_crt** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default=''*) – Arquivo do certificado próprio.
  * **peer_crt** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default=''*) – Arquivo do certificado de quem está no outro lado da conexão.
  * **log_file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default=''*) – Arquivo de log.

<a id="codigo.interface.modulos.TLSstream.TLSserver.log_prefix"></a>

#### log_prefix

Prefixo colocado nas mensagens de log do objeto.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str), default=”[Client ]”

<a id="codigo.interface.modulos.TLSstream.TLSserver._PROTOCOL_TLS"></a>

#### \_PROTOCOL_TLS

Configuração do protocolo TLS usado na comunicação.

* **Type:**
  \_SSLMethod, default=ssl.PROTOCOL_TLS_CLIENT

### Exemplos

Para criar um servidor, use:

```pycon
>>> servidor = TLSstream.TLSserver(
>>>     "minha-chave.key",
>>>     "meu-certificado.key",
>>>     "certificado-peer.key",
>>>     "arquivo-log.log"
>>>     )
```

Para aguardar uma conexão em uma porta, use:

```pycon
>>> servidor.connect("192.168.0.1", 3000)  # Aguarda uma conexão na porta 3000
```

Enviando dados ao cliente:

```pycon
>>> servidor.send(b"12345")
```

É possível configurá-lo para receber dados da seguinte forma:

```pycon
>>> def callback_recebimento(self):
>>>     print(self.dados)  # mostra os dados recebidos
```

```pycon
>>> servidor.recv_set(callback_recebimento)
```

### Notas

Após a conexão ser configurada para recebimento, não é possível mais enviar dados por ela.
Se deseja receber e enviar dados, use duas conexões. Uma para envio e outra para recebimento.

Para configurar o servidor, não use o endereço de loopback “127.168.0.1”. Ele é um endereço
interno ao sistema e apenas pode ser usado para estabelecer conexões internas (para teste, por exemplo).
Use o endereço IP da própria máquina. Lembre que o cliente se conectará usando esse mesmo IP.

<a id="codigo.interface.modulos.TLSstream.TLSserver._connect_async"></a>

#### *async* \_connect_async()

Implementação da conexão assíncrona do ‘asyncio’.

Inicia a comunicação. Checa a possibilidade de erros. Se não ocorreu nenhum erro,
espera a conexão do cliente. A conexão com o cliente é feita por meio do método [`_server_callback()`](#codigo.interface.modulos.TLSstream.TLSserver._server_callback).

<a id="codigo.interface.modulos.TLSstream.TLSserver._server_callback"></a>

#### *async* \_server_callback(reader, writer)

Método de Callback chamado ao estabelecer a comunicação.

Inicia a comunicação. Checa a possibilidade de erros. Se estiver no modo de envio,
chama o método [`_send()`](#codigo.interface.modulos.TLSstream._TLSstreamBase._send). Caso esteja no modo de recebimento, chama o método
[`_recv()`](#codigo.interface.modulos.TLSstream._TLSstreamBase._recv). Ambos são herdados da classe [`_TLSstreamBase`](#codigo.interface.modulos.TLSstream._TLSstreamBase).

* **Parâmetros:**
  * **reader** – Recebedor de streams da biblioteca Streams.
  * **writer** – Enviador de streams da biblioteca Streams.

<a id="codigo.interface.modulos.TLSstream.TLSserver.close"></a>

#### close()

Finaliza o servidor.

<a id="codigo.interface.modulos.TLSstream._TLSstreamBase"></a>

### *class* codigo.interface.modulos.TLSstream.\_TLSstreamBase(my_key='', my_crt='', peer_crt='', log_file_path='')

Base: [`object`](https://docs.python.org/3/library/functions.html#object)

Base para a implementação do stream de dados com criptografia TLS.

Não funciona por conta própria. Essa classe não deve ser usada pelo cliente final.
Eles devem usar a [`TLSclient`](#codigo.interface.modulos.TLSstream.TLSclient) e [`TLSserver`](#codigo.interface.modulos.TLSstream.TLSserver) ao invés disso.

Após iniciar o objeto, é necessário estabelecer a conexão. Para isso, use o método [`connect()`](#codigo.interface.modulos.TLSstream._TLSstreamBase.connect).
Ao estabelecer a conexão, estará inicialmente em modo de envio de dados. Ou seja, apenas pode enviar
dados, não pode receber. Use o método [`send()`](#codigo.interface.modulos.TLSstream._TLSstreamBase.send) para enviar os dados.

Para receber dados, use o método [`recv_set()`](#codigo.interface.modulos.TLSstream._TLSstreamBase.recv_set). Ele configura a conexão para modo de recebimento.
Após isso, a conexão não pode mais enviar dados (não use mais o método [`send()`](#codigo.interface.modulos.TLSstream._TLSstreamBase.send)), mas consegue
receber dados do outro ponto da conexão. Após o recebimento de um conjunto de dados, ele será salvo
no atributo *dados* do objeto, e a função de callback será chamada.

Para finalizar o cliente ou servidor use o método [`close()`](#codigo.interface.modulos.TLSstream._TLSstreamBase.close). O objeto se torna inutilizável após isso.

<a id="codigo.interface.modulos.TLSstream._TLSstreamBase.log_prefix"></a>

#### log_prefix

Prefixo colocado nas mensagens de log do objeto.

* **Type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str), default=”[exemplo ]”

<a id="codigo.interface.modulos.TLSstream._TLSstreamBase._PROTOCOL_TLS"></a>

#### \_PROTOCOL_TLS

Configuração do protocolo TLS usado na comunicação.

* **Type:**
  \_SSLMethod, default=ssl.PROTOCOL_TLS_CLIENT

<a id="codigo.interface.modulos.TLSstream._TLSstreamBase.__init__"></a>

#### \_\_init_\_(my_key='', my_crt='', peer_crt='', log_file_path='')

Configura o stream de dados com TLS.

Configura as credenciais (chave privada e certificados), e arquivo de log da comunicação.

Se os parâmetros *my_key*, *my_crt* e *peer_crt* forem omitidos, a conexão
ocorrerá sem verificação de credenciais (sem criptografia).

Todos os arquivos de credenciais devem estar no formato PEM.
Para mais informações, veja: [https://docs.python.org/3/library/ssl.html#certificates](https://docs.python.org/3/library/ssl.html#certificates)

Se o parâmetro *log_file_path* estiver vazio, o log não será registrado. Apenas será
apresentado na saída padrão;

Esse método não inicia a conxão automáticamente, use o método [`connect()`](#codigo.interface.modulos.TLSstream._TLSstreamBase.connect) para isso.

* **Parâmetros:**
  * **my_key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default=''*) – Arquivo da chave privada própria.
  * **my_crt** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default=''*) – Arquivo do certificado próprio.
  * **peer_crt** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default=''*) – Arquivo do certificado de quem está no outro lado da conexão.
  * **log_file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default=''*) – Arquivo de log.

<a id="codigo.interface.modulos.TLSstream._TLSstreamBase._connect_async"></a>

#### *async* \_connect_async()

Implementação da stream P2P.

A implementação depende se é um cliente ou servidor. Por isso, está vazia nessa classe. As
classes [`TLSclient`](#codigo.interface.modulos.TLSstream.TLSclient) e [`TLSserver`](#codigo.interface.modulos.TLSstream.TLSserver) sobrescreverão esse método.

<a id="codigo.interface.modulos.TLSstream._TLSstreamBase._connect_thread"></a>

#### \_connect_thread()

Thread onde será executado a conexão.

Inicia a conexão de forma assíncrona com a biblioteca ‘asyncio’.

<a id="codigo.interface.modulos.TLSstream._TLSstreamBase._recv"></a>

#### *async* \_recv(reader, writer)

Método executado ao receber uma mensagem do outro lado da comunicação.

Recebe os dados enviados pelo outro lado da conexão, salva no atributo *self.dados* e chama a método de
callback `_recv_callback()`. Esse método é configurado pelo método [`recv_set()`](#codigo.interface.modulos.TLSstream._TLSstreamBase.recv_set).

É chamado apenas quando o objeto estiver configurado para recebimento.

Os parâmetros *reader* e *writer* são os mesmos obtidos ao estabelecer uma comunicação usando biblioteca ‘asyncio’.

* **Parâmetros:**
  * **reader** – Recebedor de streams da biblioteca Streams.
  * **writer** – Enviador de streams da biblioteca Streams.

<a id="codigo.interface.modulos.TLSstream._TLSstreamBase._reset_connection_config"></a>

#### \_reset_connection_config()

Redefine as configurações de conexão.

Também pode ser chamado ao iniciar uma conexão para definir as configurações padrões.

<a id="codigo.interface.modulos.TLSstream._TLSstreamBase._send"></a>

#### *async* \_send(reader, writer)

Envia os dados salvos no atributo *self.dados* para o outro lado da conexão.

Esse método é chamado apenas quando o objeto estiver configurado para envio.

Os parâmetros *reader* e *writer* são os mesmos obtidos ao estabelecer uma comunicação usando biblioteca ‘asyncio’.

* **Parâmetros:**
  * **reader** – Recebedor de streams da biblioteca Streams.
  * **writer** – Enviador de streams da biblioteca Streams.

<a id="codigo.interface.modulos.TLSstream._TLSstreamBase.close"></a>

#### close()

Finaliza a conexão.

O objeto se torna inutilizável após isso.

<a id="codigo.interface.modulos.TLSstream._TLSstreamBase.connect"></a>

#### connect(HOST, PORT)

Inicia o stream P2P. Conecta ao *HOST* pela porta *PORT*.

Ela será feita no servidor *HOST* pela porta *PORT*. No caso de ser um servidor, ficará escutando
na porta *PORT* do servidor *HOST*. No caso de ser um cliente, tentará se conectar ao servidor.

Por padrão, a conexão estará configurada para modo de envio. Use o método [`recv_set()`](#codigo.interface.modulos.TLSstream._TLSstreamBase.recv_set)
para configurar para modo de recebimento. Após mudar para recebimento, não será possível mais
enviar mensagens por essa conexão.

* **Parâmetros:**
  * **HOST** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Endereço do servidor usado na conexão.
  * **PORT** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Porta usada para estabelecer a conexão.

<a id="codigo.interface.modulos.TLSstream._TLSstreamBase.recv_set"></a>

#### recv_set(callback)

Define para receber os dados assincronamente.

Ao receber os dados, eles serão salvos no atributo *self.dados* e a função de
callback será chamada. Ela tem a seguinte definição: callback(self). *self* é o
objeto que recebeu os dados.

Deve ser chamada antes de iniciar a conexão com o método [`connect()`](#codigo.interface.modulos.TLSstream._TLSstreamBase.connect). Após ser
chamada, não será mais possível enviar mensagens, apenas receber.

* **Parâmetros:**
  **callback** (*callable*) – Função que será executada ao receber os dados.

<a id="codigo.interface.modulos.TLSstream._TLSstreamBase.send"></a>

#### send(dados: [bytes](https://docs.python.org/3/library/stdtypes.html#bytes), wait=True)

Envia um conjunto de dados pela conexão.

Esse método apenas pode ser chamado quando o objeto estiver configurado para envio.
Os dados devem estar no formato de bytes.

* **Parâmetros:**
  * **dados** ([*bytes*](https://docs.python.org/3/library/stdtypes.html#bytes)) – Dados a serem enviados para o outro lado da comunicação.
  * **wait** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default=True*) – Se o valor for True, espera o conjunto de dados anterior ser completamente enviado até de
    enviar o próximo. Se for False, cancela o envio caso um pacote já esteja sendo enviado.
