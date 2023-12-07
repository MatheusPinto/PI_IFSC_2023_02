<a id="codigo-autonomo"></a>

# codigo.autonomo

* **code:**
  [autonomo.py](../../../../codigo/autonomo.py)

<a id="module-codigo.autonomo"></a>

Implementação do modo autônomo.

O controle do Wall-e no modo autônomo pode ser feito usando a classe [`Auto`](#codigo.autonomo.Auto).
Integra todos os componentes do modo autônomo:

- Segmentador
- Controlador
- Identificador

<a id="codigo.autonomo.Auto"></a>

### *class* codigo.autonomo.Auto(interface: [Interface](codigo.interface.modulos.interface.md#codigo.interface.modulos.interface.Interface), enviador: [TLSclient](codigo.interface.modulos.TLSstream.md#codigo.interface.modulos.TLSstream.TLSclient), segmentador: [Segmentador](codigo.segmentacao.modulos.interpretador.md#codigo.segmentacao.modulos.interpretador.Segmentador), ctrl: [Controlador](codigo.controlador.modulos.controlador.md#codigo.controlador.modulos.controlador.Controlador), path_haar: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None) = None)

Base: [`object`](https://docs.python.org/3/library/functions.html#object)

Classe que implementa o controle do Wall-e no modo autônomo.

Segmenta a imagem para obter uma máscara de objetos colidíveis. Identifica o lixo mais próximo.
Aplica essas informações ao controlador. As velocidades linear e angular retornadas pelo controlador
são enviadas para o Wall-e. Assim como o sinal de identificação de lixo.

Ao iniciar a classe, é necessário fornecer a interface, o enviador de comandos, o
segmentador de imagens, o controlador e o path do modelo do haar cascade usado para identificar o lixo.

Para processar uma imagem (modo autônomo), use o método [`processa_imagem()`](#codigo.autonomo.Auto.processa_imagem).

<a id="codigo.autonomo.Auto.__init__"></a>

#### \_\_init_\_(interface: [Interface](codigo.interface.modulos.interface.md#codigo.interface.modulos.interface.Interface), enviador: [TLSclient](codigo.interface.modulos.TLSstream.md#codigo.interface.modulos.TLSstream.TLSclient), segmentador: [Segmentador](codigo.segmentacao.modulos.interpretador.md#codigo.segmentacao.modulos.interpretador.Segmentador), ctrl: [Controlador](codigo.controlador.modulos.controlador.md#codigo.controlador.modulos.controlador.Controlador), path_haar: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None) = None)

Inicialização da classe.

Deve-se fornecer a interface gráfica, pois o resultado do processamento será apresentado na interface.
Deve-se fornecer, o enviador de comandos, para o modo autônomo poder enviar comandos para o Wall-e. A
apresentação dos resultados na interface e o envio de comandos para o Wall-e já é feito pelo método
[`processa_imagem()`](#codigo.autonomo.Auto.processa_imagem). Não é necessário código externo para isso.

Precisa do segmentador de imagens para obter a máscara de objetos colidíveis. Necessário o path do
modelo do Haar Cascade usado para identificar o lixo. A instanciação do identificador de lixos é feita
automaticamente, basta fornecer o arquivo do Haar Cascade.

* **Parâmetros:**
  * **interface** ([*Interface*](codigo.interface.modulos.interface.md#codigo.interface.modulos.interface.Interface)) – A interface gráfica do suário.
  * **enviador** ([*TLSclient*](codigo.interface.modulos.TLSstream.md#codigo.interface.modulos.TLSstream.TLSclient)) – O enviador de comandos.
  * **segmentador** ([*Segmentador*](codigo.segmentacao.modulos.interpretador.md#codigo.segmentacao.modulos.interpretador.Segmentador)) – O segmentador de imagens usado para identificar regiões colidíveis.
  * **ctrl** ([*Controlador*](codigo.controlador.modulos.controlador.md#codigo.controlador.modulos.controlador.Controlador)) – O controlador que determina a velocidade linear e angular no modo autônomo.
  * **path_haar** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default None*) – O path do modelo do Haar Cascade usado para identificar o lixo.

<a id="codigo.autonomo.Auto._envia_texto"></a>

#### \_envia_texto(texto: [str](https://docs.python.org/3/library/stdtypes.html#str))

Envia um texto para o Wall-e.

O texto é convertido em bytes antes de ser enviado para o Wall-e.

* **Parâmetros:**
  **texto** ([*bytes*](https://docs.python.org/3/library/stdtypes.html#bytes)) – Texto a ser enviado para o Wall-e.

<a id="codigo.autonomo.Auto.processa_imagem"></a>

#### processa_imagem(imagem, BGR=False, debug=False)

Processamento da imagem (modo autônomo).

Realiza o processamento do modo autônomo na imagem recebida. Segmenta a imagem recebida, obtém
o objeto mais próximo, aplica ao controlador para definir a velocidade linear, angular e se deve
sinalizar lixo. Os comandos para controlar o Wall-e levando isso em conta já são enviados para o
Wall-e por meio desse método. Não é necessário código externo para tal.

O frame processado (com ou sem debug) será exibido na interface. Isso também é feito por esse método
e não é necessário código externo para tal.

O parâmetro *imagem* deve ser uma imagem (array do numpy) no formato (linhas, colunas, canais). O
OpenCV já usa esse formato por padrão. A princípio, dever do tipo RGB. Más é possível que seja do
tipo BGR, contanto que o parâmetro *BGR* seja definido como True.

* **Parâmetros:**
  * **imagem** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – A imagem a ser processada.
  * **BGR** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default False*) – Se a imagem está no formato BGR.
  * **debug** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default False*) – Se a imagem de debug deve ser exibida na interface. Caso seja false, exibe a imagem normal.
