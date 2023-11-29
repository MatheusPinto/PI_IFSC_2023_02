<a id="module-codigo.interface.teste.video_interface_client"></a>

<a id="codigo-interface-teste-video-interface-client"></a>

# codigo.interface.teste.video_interface_client

Script de teste da interface - cliente.

Recebe os frames do servidor e mostra na interface gráfica. Além disso, mostra os dados
do frame na saída padrão.

Deve ser executado junto ao script ‘video_interface_server.py’, que envia os
frames capturados pela câmera.

<a id="codigo.interface.teste.video_interface_client.video_callback"></a>

### codigo.interface.teste.video_interface_client.video_callback(interface, RGB: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray), BGR: [ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray))

Recebe uma imagem e mostra os dados.

O parâmetro *imagem* deve ser uma imagem (array do numpy) no formato (linhas, colunas, canais).

* **Parâmetros:**
  * **RGB** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – Imagem cujos dados serão apresentados.
  * **BGR** ([*numpy.ndarray*](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)) – Versão em BGR da imagem anterior
