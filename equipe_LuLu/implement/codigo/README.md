# Implementação do código

Nessa página está descrito a implementação do código do projeto. O código foi dividido em submódulos, cuja documentação está disponível na [documentação do código em Python](../docs/_build/markdown/index.md). Cada submódulo possui sua própria pasta de 'teste/' contendo os scripts de teste dele. O código final (do cliente e do Wall-e) está no diretório corrente. São os scripts [cliente.py](cliente.py) e [walle.py](walle.py). Eles utilizam os demais módulos para funcionar. Portanto, também é necessário enviar alguns dos módulos para o Wall-e.

Os submódulos estão listados abaixo:

- [Interface](interface)
- [movimento](movimento)
- [identificacao](identificacao)
- [Segmentação](segmentacao)
- [Controlador](controlador)

O treinamento do modelo de identificação do lixo está listado no diretório [identificador](identificador).


## Configurações

As configurações necessárias se resumem à:

- [Configurações de ambiente](ambiente.md): Se refere às configurações das credenciais e de identificação do Wall-e (IP e usuário).
- [Configuração da Raspberry](raspberry): Configurações em geral realizadas na Raspberry Pi.


## Acesso remoto via SSH e Rsync

Para acessar remotamente a Raspberry Pi, é necessário que as chaves e certificados da comunicação SSH esteja atualizada no Wall-e, como escrito na página de [configurações de ambiente](ambiente.md). Além disso, é necessário conhecer o IP dela. O processo para descobrir isso está descrito na etapa de [configuração da Raspberry Pi](raspberry/).

Há um comando que facilita o acesso via SSH:

```shell
make ssh
```

E um que facilita a sincronização do código pelo Rsync:

```shell
make rsync
```

Para tal, é necessário que tanto o computador atual quanto a Raspberry Pi possuam o Dropbear (servidor SSH) e o Rsync instalados.

**Observação:** Não há versão do Rsync para Windows, mas é possível executá-lo com o [WLS](https://learn.microsoft.com/pt-br/windows/wsl/install).

**Observação:** O acesso a Raspberry Pi por meio de SSH e do Rsync necessitam que o IP do Wall-e esteja pré-configurado no arquivo 'env/conf' para funcionar. Veja a página de [configurações de ambiente](ambiente.md) para mais informações.


## Dependências

As principais dependências do projeto são os seguintes: Numpy, OpenCV, Tensorflow, PySide6. Elas podem ser instaladas usando o comando abaixo:

```shell
pip3 install tensorflow opencv-python numpy PySide6 matplotlib
```


# Executar os códigos principais do projeto

Os códigos principais do projeto são o [walle.py](walle.py) e o [cliente.py](cliente.py). O primeiro é responsável por controlar o Wall-e e deve ser executado na Raspberry Pi, enquanto o segundo implementa a interface com o modo autônomo e deve ser executado no computador.

Primeiramente, é necessário que todas as configurações estejam feitas. Caso a Raspberry Pi já tenha sido configurada para uso anteriormente, basta atualizar as [configurações de ambiente](ambiente.md). Caso contrário, também é necessário realizar as [configurações da Raspberry Pi](raspberry). Lembre de atualizar o IP do arquivo 'env/conf' caso ele tenha sido alterado, como descrito na página das [configurações de ambiente](ambiente.md).

Assim que estiver tudo configurado, basta executar os códigos:

- [cliente.py](cliente.py): Deve ser executado no computador principal. Mostra a interface e implementa o modo autônomo.
- [walle.py](walle.py): Deve ser executado na Raspberry Pi. Acesse por meio do SSH e mova para o diretório '~/code' com o comando 'cd'. Depois, basta executar o script 'walle.py'. Os comandos necessários são o seguinte:

    ```shell
    make rsync  # para sincronizar o diretório 'env/'
    make ssh  # para acessar remotamente a Raspberry Pi
    cd code
    ./walle.py
    ```

**Observação:** Alguns códigos feitos para serem executados na Raspberry Pi utilizam o IP definido no arquivo 'env/conf'. Para executá-los fora da Raspberry Pi (para verificar o funcionamento), é possível alterar o IP desse arquivo para "127.0.0.1" (IP de loopback). Assim, ele executará normalmente em um computador qualquer. O script [walle.py](walle.py) é um desses códigos.

**Observação:** Se estiver executando os scripts [walle.py](walle.py) e [cliente.py](cliente.py) na mesma máquina (para debug) e ela usar sistema operacional Linux deve-se tomar cuidado com o botão de 'Desligar' da interface gráfica, pois pode desligar o computador.
