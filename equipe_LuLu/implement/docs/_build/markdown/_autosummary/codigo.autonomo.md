<a id="module-codigo.autonomo"></a>

<a id="codigo-autonomo"></a>

# codigo.autonomo

Implementação do modo autônomo.

O controle do Wall-e no modo autônomo pode ser feito usando a classe [`Auto`](#codigo.autonomo.Auto). Deve ser fornecido o

<a id="codigo.autonomo.Auto"></a>

### *class* codigo.autonomo.Auto(interface: [Interface](codigo.interface.modulos.interface.md#codigo.interface.modulos.interface.Interface), enviador: [TLSclient](codigo.interface.modulos.TLSstream.md#codigo.interface.modulos.TLSstream.TLSclient), segmentador: [Segmentador](codigo.segmentacao.modulos.interpretador.md#codigo.segmentacao.modulos.interpretador.Segmentador), controlador: [Controlador](codigo.controlador.modulos.controlador.md#codigo.controlador.modulos.controlador.Controlador), path_haar: [str](https://docs.python.org/3/library/stdtypes.html#str))

Base: [`object`](https://docs.python.org/3/library/functions.html#object)

Classe que implementa o controle do Wall-e no modo autônomo.

Segementa a imagem para obter uma mascara de objetos colidíveis. Identifica o lixo mais próximo e aplica ao controlador.
Envia as velocidades linear e angular do controlador para o Wall-e.

Ao iniciar a classe, é necessário fornecer a interface, o enviador de comandos, o
segmentador de imagens, o controlador e o path do modelo do haar cascade usado para identificar o lixo.

Para processar uma imagem (modo autônomo), use o método [`processa_imagem()`](#codigo.autonomo.Auto.processa_imagem).

<a id="codigo.autonomo.Auto.__init__"></a>

#### \_\_init_\_(interface: [Interface](codigo.interface.modulos.interface.md#codigo.interface.modulos.interface.Interface), enviador: [TLSclient](codigo.interface.modulos.TLSstream.md#codigo.interface.modulos.TLSstream.TLSclient), segmentador: [Segmentador](codigo.segmentacao.modulos.interpretador.md#codigo.segmentacao.modulos.interpretador.Segmentador), controlador: [Controlador](codigo.controlador.modulos.controlador.md#codigo.controlador.modulos.controlador.Controlador), path_haar: [str](https://docs.python.org/3/library/stdtypes.html#str))

Inicialização da classe.

Deve-se fornecer a interface gráfica, pois o resultado do processamento será apresentado na interface.
Deve-se fornecer, o enviador de comandos, para o modo autônomo poder envar comandos para o Wall-e.

Precisa do segmentador de imagens para obter a máscara de objetos colidíveis. Necessário o path do
modelo do haar cascade usado para identificar o lixo. O resultado do segmentador e do identificador de objetos
são aplicados no controlador.

* **Parâmetros:**
  * **interface** (*interface*) – A interface gráfica do suário.
  * **enviador** ([*TLSclient*](codigo.interface.modulos.TLSstream.md#codigo.interface.modulos.TLSstream.TLSclient)) – O enviador de comandos.
  * **segmentador** ([*Segmentador*](codigo.segmentacao.modulos.interpretador.md#codigo.segmentacao.modulos.interpretador.Segmentador)) – O segmentador de imagens usado para identificar regiões colidíveis.
  * **controlador** ([*Controlador*](codigo.controlador.modulos.controlador.md#codigo.controlador.modulos.controlador.Controlador)) – O controlador que determina a velocidade linear e angular no modo autônomo.
  * **path_haar** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – O path do modelo do haar cascade usado para identificar o lixo.

<a id="codigo.autonomo.Auto.enviar_dados"></a>

#### enviar_dados(dados: [bytes](https://docs.python.org/3/library/stdtypes.html#bytes))

Envia os dados para o Wall-e.

Os dados devem estar no formato de bytes.

* **Parâmetros:**
  **dados** ([*bytes*](https://docs.python.org/3/library/stdtypes.html#bytes)) – Dados a serem enviados para o Wall-e.

<a id="codigo.autonomo.Auto.processa_imagem"></a>

#### processa_imagem(imagem, BGR=False, debug=False)

Processamento da imagem (modo autônomo).

Realiza o processamento do modo autônomo na imagem recebida.

O parâmetro *imagem* deve ser uma imagem (array do numpy) no formato (linhas, colunas, canais).

* **Parâmetros:**
  * **imagem** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – A imagem a ser processada.
  * **BGR** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default False*) – Se a imagem for no formato BGR.
  * **debug** ([*bool*](https://docs.python.org/3/library/functions.html#bool)*,* *default False*) – Se a imagem de debug deve ser exibida na interface.
