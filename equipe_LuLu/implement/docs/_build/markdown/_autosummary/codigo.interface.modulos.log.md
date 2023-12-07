<a id="codigo-interface-modulos-log"></a>

# codigo.interface.modulos.log

* **code:**
  [log.py](../../../../codigo/interface/modulos/log.py)

<a id="module-codigo.interface.modulos.log"></a>

Módulo dedicado ao registro de log.

Os logs são apresentados na saída padrão stdout e salvos em um arquivo pré-configurado.
Para isso, use a classe [`LogFile`](#codigo.interface.modulos.log.LogFile).

<a id="codigo.interface.modulos.log.LogFile"></a>

### *class* codigo.interface.modulos.log.LogFile(file_path='', prefixo='')

Base: [`object`](https://docs.python.org/3/library/functions.html#object)

Apresenta mensagens de log e as registra em um arquivo de log.

As mensagens são apresentadas na saída padrão. O arquivo onde são salvas é definido pelo
método [`__init__()`](#codigo.interface.modulos.log.LogFile.__init__).

Para registra uma mensagem no log, utilize o método [`register()`](#codigo.interface.modulos.log.LogFile.register).

É possível configurar um prefixo que será colocado no começo das mensagens de log. Veja o método
[`__init__()`](#codigo.interface.modulos.log.LogFile.__init__).

### Exemplos

Registrando um log genérico:

```pycon
>>> registrador = log.LogFile("server.log", "[Server] ")
>>> registrador.register("Mensagem de log...")
```

Registrando uma mensagem de erro:

```pycon
>>>    try:
>>>        os.makedirs("diretório/")
>>>
>>>    except FileExistsError:
>>>        registrador.register("O diretório já existe!", exception=True)
```

<a id="codigo.interface.modulos.log.LogFile.__init__"></a>

#### \_\_init_\_(file_path='', prefixo='')

Configura o arquivo onde salva a mensagem, e o prefixo delas.

A mensagem será salva no arquivo fornecido pelo parâmetro *file_path*. Ele é relativo ao diretório
atual. Também é possível usar um path absoluto, como: ‘/var/log/server.log’.

É adicionado um prefixo à mensagem (tanto no arquivo salvo quanto no apresentado na saída padrão),
definido pelo parâmetro *prefixo*

* **Parâmetros:**
  * **file_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default=''*) – Arquivo onde será registrado a mensagem de log. Se estiver vazio, então não registra nada em arquivo,
    apenas mostra na saída padrão.
  * **prefixo** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default=''*) – Prefixo que será inserido antes de toda mensagem de log. Por exemplo, pode-se usar “[server] ” para
    indicar que é um log de servidor.

<a id="codigo.interface.modulos.log.LogFile.register"></a>

#### register(log_msg: [str](https://docs.python.org/3/library/stdtypes.html#str), exception=False)

Mostra a mensagem de log e registra ela no arquivo de log.

Se a mensagem de log corresponde a uma exceção sendo chamada após ela, use o parâmetro *exception=True*.
Isso mostra a mensagem original da exceção após a de log.

* **Parâmetros:**
  * **log_msg** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Mensagem de log que será apresentada, e salva no arquivo.
  * **exception** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default=False*) – Se a mensagem é referente a uma exceção. Se True, mostrará a mensagem da exceção.
