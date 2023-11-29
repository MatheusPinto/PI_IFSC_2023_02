<a id="module-codigo.segmentacao.teste.tempo_iteracao"></a>

<a id="codigo-segmentacao-teste-tempo-iteracao"></a>

# codigo.segmentacao.teste.tempo_iteracao

Carrega um modelo do Tensorflow Lite e faz algumas iterações com ele.

Os dados de entrada são formados por números aleatórios. O resultado da iteração não é
utilizado. O propósito desse script é apenas checar o tempo necessário para uma iteração.

Esse script utiliza a versão lite do modelo: o arquivo ‘modelo.tflite’, e apenas uma thread.

É normal que a primeira iteração seja mais lenta, por isso são realizadas mais de uma iterações e
apresentado o tempo necessário para cada.

O path do arquivo com a versão lite do modelo deve ser informado pelo parâmetro ‘MODELO_TFLITE_PATH’.
