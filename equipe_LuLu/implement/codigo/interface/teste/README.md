# Scripts de teste

A documentação dos scripts deste diretório está disponível em [documentação dos scripts de teste](../../../docs/_build/markdown/_autosummary/codigo.interface.teste.md).

Alguns scripts são organizados em pares. Ou seja, é necessário que dois scripts sejam executados simultaneamente:

- Execute os scripts [stream_client.py](stream_client.py) e [stream_server.py](stream_server.py) simultaneamente. O script [stream_client.py](stream_client.py) deve enviar um conjunto de dados para o [stream_server.py](stream_server.py), que receberá esses dados e apresentará na saída padrão.

- Execute os scripts [video_client.py](video_client.py) e [video_server.py](video_server.py) simultaneamente. O script [video_server.py](video_server.py) deve capturar a câmera de webcam e enviar para o [video_client.py](video_client.py), que receberá a captura e mostrará na interface gráfica padrão do OpenCV.

- Execute os scripts [video_interface_client.py](video_interface_client.py) e [video_interface_server.py](video_interface_server.py) simultaneamente. O script [video_interface_server.py](video_interface_server.py) deve capturar a câmera de webcam e enviar para o [video_interface_client.py](video_interface_client.py), que receberá a captura e apresentará na interface. Além disso, a interface enviará os comandos para o servidor, que apresentará na sua saída padrão.
