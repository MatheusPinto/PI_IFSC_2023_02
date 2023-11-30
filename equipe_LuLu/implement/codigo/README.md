# Implementação do código

Nessa página está descrito a implementação do código do projeto. O código foi dividido em submódulos, cuja documentação está disponível na [documentação dos módulos](../docs/_build/markdown/index.md). Cada submódulo possui sua própria pasta de 'teste/' contendo os scripts de teste dele. O código final (do cliente e do Wall-e) está no diretório corrente. São os scripts [cliente.py](cliente.py) e [walle.py](walle.py). Eles utilizam os demais módulos para funcionar. Portanto, também é necessário enviar alguns dos módulos para o Wall-e.

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
- [Configuração da raspberry](raspberry): Configurações em geral realizadas na Raspberry Pi.


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

Para tal, é necessário que tanto o computador atual quanto a Raspberry Pi possuam o Dropbear (servidor SSH) e o Rsunc instalados.

OBS.: Não há versão do Rsync para windows, mas é possível executá-lo com o [WLS](https://learn.microsoft.com/pt-br/windows/wsl/install).


# Dica para executar os códigos da Raspberry Pi.

Alguns códigos feitos para serem executados na Raspberry Pi utilizam o IP definido no arquivo 'env/conf'. Para executá-los fora da Raspberry Pi (para verificar o funcionamento), é possível alterar o IP desse arquivo para "127.0.0.1" (IP de loopback). Assim, ele executará normalmente em um computador qualquer. O script [walle.py](walle.py) é um desses códigos.
