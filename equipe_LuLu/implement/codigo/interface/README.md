# Código da interface e comunicação com o Wall-e.

Os códigos disponíveis nesse diretório são referentes a interface e comunicação do cliente com o Wall-e. Eles utilizam as chaves disponíveis no diretório '../env/comunicacao' que podem ser criadas conforme as instruções de [configuração do ambiente](../ambiente.md).

A interface e a comunicação foi feita conforme especificado no [Design](../../../design/comunicacao.md). Por não conseguir executar o modelo de segmentação na Raspberry Pi, algumas funções tiveram que ser alteradas. A interface não envia mais um comando para o Wall-e ativar o modo autônomo. Em vez disso, o processamento das regiões colidíveis e a identificação de lixo é feita no cliente e o resultado apenas é enviado para o Wall-e.

As velocidades linear e angular são enviados como uma tupla de bytes do tipo: "velocidade linear, velocidade angular". Por exemplo, se deseja uma velocidade linear de 20 e uma angular de 30, ela envia "20,30"

Além disso, a tabela de comandos que serão enviados do usuário para o Wall-e foi atualizada para o seguinte:

|   Instrução    | String enviada |
|     :---:      |     :---:      |
|    Desligar    |     "halt"     |
| Sinalizar lixo |     "lixo"     |

O envio do comando de desligamento é feito pelo botão de desligar da interface. Já o envio do comando de sinalizar lixo será feito pelo [gerenciador do modo autônomo](../autonomo.py), cuja documentação está disponível em [documentação do gerenciador do modo autônomo](../../docs/_build/markdown/_autosummary/codigo.autonomo.md). O Wall-e executa a sinalização de lixo acionando seu buzzer.

Os módulos criados para implementar essa etapa estão no diretório ['modulos/'](modulos/). A documentação deles está disponível em [documentação dos módulos](../../docs/_build/markdown/_autosummary/codigo.interface.modulos.md).

Os scripts de teste estão no diretório ['teste/'](teste/). A documentação deles está disponível em [documentação dos scripts de teste](../../docs/_build/markdown/_autosummary/codigo.interface.teste.md).


## Dependências

É possível executar os códigos no próprio computador para fins de teste. Para isso, é necessário ter o Python 3 e os módulos do OpenCV (usado para captura de câmera e processamento visual), Numpy e Pyside6 (usado para implementar a interface gráfica).

Os módulos podem ser instalados com o seguinte comando:

```shell
pip3 install opencv-python numpy PySide6
```

**Observações:** é importante notar que o OpenSSL não é necessário para executar os códigos principais, apenas para gerar os certificados.
