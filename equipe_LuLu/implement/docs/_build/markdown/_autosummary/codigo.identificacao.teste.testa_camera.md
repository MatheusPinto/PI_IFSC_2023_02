<a id="codigo-identificacao-teste-testa-camera"></a>

# codigo.identificacao.teste.testa_camera

* **code:**
  [testa_camera.py](../../../../codigo/identificacao/teste/testa_camera.py)

<a id="module-codigo.identificacao.teste.testa_camera"></a>

Testa a identificação de lixo no vídeo capturado pela webcam.

O teste mostra os lixos identificados e qual é o mais próximo. As marcações são feitas de acordo com os
métodos [`identifica_lixo_mais_proximo()`](codigo.identificacao.modulos.identificador.md#codigo.identificacao.modulos.identificador.Identificador.identifica_lixo_mais_proximo)
e [`identifica_lixos()`](codigo.identificacao.modulos.identificador.md#codigo.identificacao.modulos.identificador.Identificador.identifica_lixos). Ambos da classe
[`Identificador`](codigo.identificacao.modulos.identificador.md#codigo.identificacao.modulos.identificador.Identificador).

O modelo de Haar cascade é definido pelo parâmetro ‘CASCADE’.

Resultado experado:

![image](../../../../codigo/identificacao/img/teste-deteccao-webcam.gif)

Fonte: autoria própria.
