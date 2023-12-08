# Código do controlador

Os códigos disponíveis nesse diretório são referentes ao controlador do Wall-e no modo autônomo.

O controlado usado não foi um com MLP, como especificado na documentação do [design do modo autônomo](../../../design/autonomo.md). O MLP deveria ser treinado o que dificultaria sua execução. Além disso, como se trata de um algorítimo de machine learning, existe uma possibilidade maior de não funcionar como esperado e causar algum acidente. O novo controlador possui chances menores de causar isso, além de ser mais simples de implementar.

Esse controlador apenas não foi a primeira escolha devido à ausência, na época, de um algorítimo de suavização para o caminho gerado pelo A-estrela. Assim que encontrado, tornou-se a melhor opção.

O controlador utilizado recebe a máscara do algorítimo de segmentação e a posição do objeto que deve seguir (lixo), e retorna a velocidade linear e angular que o Wall-e deve seguir, e se deve ativar a sinalização. Essa é sua principal função. O controlador usa o algorítimo A-estrela para definir o melhor caminho até o objeto. Ele checa se não há nada colidível em sua frente e, caso tenha, ordena o Wall-e a desviar ajustando sua velocidade linear e angular. Por exemplo, se existir uma parede e ele não conseguir ir em frente, zera a velocidade linear e coloca a velocidade angular no máximo (gira em torno do seu eixo).

Se identificar um lixo, o controlador para o Wall-e (zera as velocidades linear e angular) e retorna um indicador de sinalização. Esse indicador de sinalização deve ser enviado para o Wall-e para que ele ative a sinalização de lixo. Caso não esteja sinalizando lixo, a decisão da direção que o Wall-e deve seguir é feita conforme o seguinte diagrama de atividades:

![Diagrama controlador](img/controlador.svg)

Fonte: autoria própria.

Os módulos criados para implementar essa etapa estão no diretório ['modulos/'](modulos/). A documentação deles está disponível em [documentação dos módulos](../../docs/_build/markdown/_autosummary/codigo.controlador.modulos.md).

Os scripts de teste estão no diretório ['teste/'](teste/). A documentação deles está disponível em [documentação dos scripts de teste](../../docs/_build/markdown/_autosummary/codigo.controlador.teste.md).


## Aplicação do controlador PID

Inicialmente, o resultado do controlador possuía variações muito abruptas de direção, como ilustrado abaixo.

![Teste sem PID](img/teste-sem-PID.gif)

Fonte: autoria própria.

Para resolver isso, foram utilizados dois controladores PID para as velocidades resultantes do algorítimo controlador. Um para a velocidade linear e um para a angular. A ideia base dessa implementação é que o PID ajusta o valor atual das velocidades de forma mais sutil até alcançar a velocidade resultante do algorítimo controlador (definida como o setpoint do PID). Os controladores são independentes entre si. Ou seja, o PID da velocidade linear não afeta o da angular e vice-versa. A seguir, o teste com PID:

![Teste com PID](img/teste-com-PID.gif)

Fonte: autoria própria.


## Dependências

Para executar o código, é necessário ter o Python 3 e os módulos do OpenCV (usado para processamento visual) e Numpy.

Eles podem ser instalados com o seguinte comando:

```sh
pip3 install opencv-python numpy
```

Além disso, é necessário instalar o módulo simple-pid, usado para implementar um controlador PID na velocidade linear e angular que será fornecida ao Wall-e:

```shell
pip3 install simple-pid
```
