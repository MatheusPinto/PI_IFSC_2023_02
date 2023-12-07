# Configurações de ambiente

Configurações de ambiente se referem, no contexto desse projeto, às chaves e certificados, além da definição do IP e usuário para se conectar ao Wall-e. Recebem esse nome por que os arquivos relacionados ficam numa pasta com o nome de 'env/' (enviroment). Será explicado como foi configurado o ambiente para esse projeto, e como é possível reproduzir essas configurações caso o leitor deseje.

As configurações de ambiente devem estar no diretório 'env/'. É nele onde são salvas as chaves privadas e certificados usados na comunicação entre o cliente e o Wall-e. Esses arquivos não são fornecidos por questão de segurança, mas podem ser criados.

São compostos pelas chaves e certificados usadas na comunicação SSH e sincronização de arquivos com o Rsync (pasta 'env/ssh/'). Além das chaves e certificados usados pela comunicação da interface com o Wall-e (pasta 'env/comunicacao/'). Além disso, possui um arquivo de configuração onde estão definidos o IP do Wall-e e o nome do usuário usado para se conectar por meio do SSH: o 'env/conf'.

Existe uma pasta de exemplo desse diretório: ['env.exemplo/'](env.exemplo/). Se deseja executar o projeto sem criar novas chaves, basta renomear esse diretório para 'env/'. Por questão de segurança, é melhor criar novas chaves e certificados, como será descrito posteriormente.

Por questões de segurança, não deve ser fornecido o diretório 'env/' a ninguém. Nem mesmo versionado com o Git. São as chaves e certificados que garantem a segurança e autenticidade da comunicação.


## Atualizar as chaves usadas na comunicação com o Wall-e

Para gerar/atualizar as chaves e certificados usados na comunicação com o Wall-e, deve-se ter instalado o OpenSSL e o Python 3.

O comando que atualiza as chaves é o seguinte:

```shell
make atualiza-certificados
```

No caso de não estar usando um sistema com suporte ao [GNU Make](https://www.gnu.org/software/make/), pode-se atualizar as chaves executando o script [atualiza_certificados.py](atualiza_certificados.py)

As chaves serão geradas no diretório 'env/comunicacao/'.

**Observações:** Atualizar os certificados sobrescreve os certificados anteriores. Os certificados duram apenas 365 dias. Após isso, deixam de valer e devem ser atualizados.


## Atualizar as chaves usadas no SSH e Rsync

Para gerar/atualizar as chaves e certificados usados na comunicação com o Wall-e, deve-se ter instalado o OpenSSL. Além disso, deve-se estar em um sistema operacional Linux.

O comando que atualiza as chaves é o seguinte:

```shell
make atualiza-ssh
```


## Configuração da Raspberry Pi

A configuração da Raspberry Pi está descrita na página de [configuração da Raspberry Pi](raspberry/).

Atualizar as chaves e certificados no computador torna necessário atualizá-las no Wall-e. Elas podem ser atualizadas copiando o diretório 'env/' do computador para o '~/code/env/' da Raspberry Pi por meio de um pendrive. Se apenas os certificados usados na comunicação entre usuário e Wall-e foi afetado, pode-se atualizá-las no Wall-e por meio do Rsync.
