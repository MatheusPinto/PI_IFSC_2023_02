<a id="codigo-walle"></a>

# codigo.walle

* **code:**
  [walle.py](../../../../codigo/walle.py)

<a id="module-codigo.walle"></a>

Script principal do Wall-e.

Realiza o streaming de vídeo. Captura a imagem de uma câmera, converte para JPG e envia
para o usuário de forma criptografada.

Recebe a direção do cliente e aplica no movimento do Wall-e. Além de executar os
comandos recebidos do Wall-e: desligar e sinalizar que encontrou lixo.

Gerencia os motores DC e servo motores. Se não receber nenhuma instrução do usuário depois de um
determinado tempo, para os motores por segurança.
