<a id="codigo-segmentacao-treina-modelo"></a>

# codigo.segmentacao.treina_modelo

* **code:**
  [treina_modelo.py](../../../../codigo/segmentacao/treina_modelo.py)

<a id="module-codigo.segmentacao.treina_modelo"></a>

Continua o treinamento do modelo.

O modelo deve ter sido criado previamento pelo script ‘cria_modelo.py’.

É necessário informar o diretório onde o modelo está pelo parâmetro ‘MODELO_PATH’.

É possível configurar a acurácia mínima do treinamento pelo parâmetro ‘ACURACIA_MINIMA’. Se a acurácia de
validação cair para um valor abaixo desse durante o treinamento, os parãmnetros serão restaurados para o
do modelo de melhor acurácia.

Para saber como funciona o treinamento, veja a função `treina_modelo()` do
módulo `modulos.treina`.
