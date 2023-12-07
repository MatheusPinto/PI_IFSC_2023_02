<a id="codigo-segmentacao-modulos-padronizacao"></a>

# codigo.segmentacao.modulos.padronizacao

* **code:**
  [padronizacao.py](../../../../codigo/segmentacao/modulos/padronizacao.py)

<a id="module-codigo.segmentacao.modulos.padronizacao"></a>

Módulo para padronização de imagens.

Não foi colocado junto ao módulo [`preprocessamento`](codigo.segmentacao.modulos.preprocessamento.md#module-codigo.segmentacao.modulos.preprocessamento) porque o módulo atual será
importado pelo segmentador. Separar ele do de preprocessamento evitar carregar todo o Tensorflow durante a
execução do segmentador.

Para padronizar as imagens, use a função [`padroniza_imagem()`](#codigo.segmentacao.modulos.padronizacao.padroniza_imagem)

<a id="codigo.segmentacao.modulos.padronizacao.padroniza_imagem"></a>

### codigo.segmentacao.modulos.padronizacao.padroniza_imagem(imagem)

Padroniza a imagem.

Padroniza a imagem para a entrada do modelo de segmentação. Essa função deve ser usada no tensor da imagem
usada para o treinamento e no tensor da imagem usada no segmentador.

* **Parâmetros:**
  **imagem** (*tf.Tensor*) – A imagem a ser padronizada.
* **Retorna:**
  A imagem padronizada.
* **Tipo de retorno:**
  tf.Tensor

### Notas

Não utilize essa função na máscara de segmentação. Apenas na imagem original.
