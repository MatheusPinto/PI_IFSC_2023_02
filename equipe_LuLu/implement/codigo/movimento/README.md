# Código da movimentação

Os códigos disponíveis nesse diretório são referentes à movimentação do Wall-e.

A definição dos duty cycle dos motores funciona conforme o especificado no [design da movimentação](../../../design/movimentacao.md). É possível definir suas velocidades linear e angular do Wall-e em valores relativos (-100 a 100), como especificado na documentação do módulo [movimentacao.py](../../docs/_build/markdown/_autosummary/codigo.movimento.modulos.movimentacao.md).

Os módulos criados para implementar esse projeto estão no diretório ['modulos/'](modulos/). A documentação deles está disponível em [documentação dos módulos](../../docs/_build/markdown/_autosummary/codigo.movimento.modulos.md).

Os scripts de teste estão no diretório ['teste/'](teste/). A documentação deles está disponível em [documentação dos scripts de teste](../../docs/_build/markdown/_autosummary/codigo.movimento.teste.md).

Também há alguns scripts de teste usados durante a etapa de validação do funcionamento dos motores DC e de passo. Eles estão no diretório [teste_validacao](teste_validacao). A documentação deles está disponível em [documentação dos scripts de teste](../../docs/_build/markdown/_autosummary/codigo.movimento.teste_validacao.md).



## Dependências

É possível rodar os códigos no próprio computador para fins de teste. Para isso, é necessário ter o Python 3. No caso de estar em uma Raspberry Pi, deve-se possuir o módulo 'RPi.GPIO'. Como esse módulo foi instalado na Raspberry Pi está descrito na página de [configuração da Raspberry Pi](../raspberry).


No caso de estar executando os scripts desse módulo fora da Raspberry Pi (apenas para simulação), há uma versão de simulação do módulo disponível no diretório [fake-RPi](fake-RPi).

OBS.: Ao enviar esse código para a Raspberry Pi, o diretório [fake_RPi](fake_RPi) não pode estar incluído. Por isso, o Rsync foi configurado para ignorá-lo.
