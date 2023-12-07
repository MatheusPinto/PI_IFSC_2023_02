<a id="codigo-segmentacao-modulos-treina"></a>

# codigo.segmentacao.modulos.treina

* **code:**
  [treina.py](../../../../codigo/segmentacao/modulos/treina.py)

<a id="module-codigo.segmentacao.modulos.treina"></a>

Funções de treinamento do modelo de segmentação.

A função responsável por treinar os modelos é a função [`treina_modelo()`](#codigo.segmentacao.modulos.treina.treina_modelo).

<a id="codigo.segmentacao.modulos.treina._RestauraSeAcuraciaValidacaoForBaixa"></a>

### *class* codigo.segmentacao.modulos.treina.\_RestauraSeAcuraciaValidacaoForBaixa(acuracia_minima=0.5)

Base: `Callback`

Callback usada no treinamento para restaurá-lo se a acurácia de validação for baixa.

No final de cada época, checa se a acurácia de validação é muito baixa. Se for, restaura o
modelo para melhor versão e continua o treinamento.

<a id="codigo.segmentacao.modulos.treina._RestauraSeAcuraciaValidacaoForBaixa.__init__"></a>

#### \_\_init_\_(acuracia_minima=0.5)

Inicializa a classe de callback.

* **Parâmetros:**
  **acuracia_minima** ([*float*](https://docs.python.org/3/library/functions.html#float)*,* *default=0.5*) – A acurácia mínima aceitável para o treinamento. Se for menor do que isso, restaura os
  parâmetros do modelo.

<a id="codigo.segmentacao.modulos.treina._RestauraSeAcuraciaValidacaoForBaixa.on_epoch_end"></a>

#### on_epoch_end(epoca, logs=None)

Implementa a execução no final de cada época.

<a id="codigo.segmentacao.modulos.treina.treina_modelo"></a>

### codigo.segmentacao.modulos.treina.treina_modelo(modelo: Model, path: [str](https://docs.python.org/3/library/stdtypes.html#str) = 'modelo-segmentacao', backbone: [bool](https://docs.python.org/3/library/functions.html#bool) = False, acuracia_minima: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None) = None)

Treina um modelo do Tensorflow.

O modelo é dado pelo parâmetro *modelo*. Deve ser um modelo do Tensorflow pré-carregado. O path dos datasets
usados para treinamento são dados pelo parâmetro ‘DATASET_TREINAMENTO_PATH’ e ‘DATASET_VALIDACAO_PATH’.

O treinamento será feito usando o método ‘fit()’ do *modelo* fornecido.

Essa função foi feita para criar um registro (log) de todos os modelos treinados. Essa pasta é definida pelo parâmetro
*path*. Será criado um log na pasta definida por <path>log. Por exemplo, se *path=”modelo-segmentacao/”*, o
log será criado na pasta ‘modelo-segmentacao/log/’.

O dataset é preprocessamento antes de ser aplicado ao modelo. O pré-processamento depende se o modelo
treinado é um backbone ou o modelo de segmentação. Por isso, é necessário informar isso por meio do
parâmetro *backbone*.

O parâmetro *acuracia_minima* define a acurácia mínima aceitável para o treinamento. Os parâmetros são
restaurados para o melhor treinamento se ocorrer da acurácia de validação cair abaixo desse valor. Se
for None, não haverá uma acurácia mínima nem mesmo a restauração dos parâmetros.

A modelo com melhor acurácia é salvo no diretório definido por <path>maior-acuracia/. Por exemplo, se
*path=”modelo-segmentacao/”*, o modelo com melhor acurácia será salvo na pasta
‘modelo-segmentacao/maior-acuracia/’

* **Parâmetros:**
  * **modelo** (*tf.keras.Model*) – O modelo do Tensorflow que será treinado.
  * **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default="modelo-segmentacao"*) – O path da pasta em que os dados relacionados ao modelo serão salvos.
  * **acuracia_minima** ([*float*](https://docs.python.org/3/library/functions.html#float)*,* *default=None*) – A acurácia mínima aceitável para o treinamento. Se for menor do que isso, restaura os parâmetros do modelo.

### Notas

A acurácia não é medida durante o treinamento do backbone. Portanto, não defina uma acurácia mínima de
treinamento para ele. Pelo mesmo motivo, não será salvo o modelo do backbone com maior acurácia.
