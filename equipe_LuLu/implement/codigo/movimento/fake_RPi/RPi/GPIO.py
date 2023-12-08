#!/bin/env python3



"""Módulo de simulação para o módulo RPi.GPIO.

Permite executar os scripts que dependem do módulo RPi.GPIO fora da Raspberry Pi. Em vez de definir
os nível lógicos das GPIO, apenas mostra na saída padrão o que foi configurado.

Esse módulo não deve ser usado na Raspberry Pi. Apenas no computador de desenvolvimento. Portanto,
não deve ser enviado para a Raspberry Pi ao sincronizar o código.
"""


# Informações do módulo
RPI_INFO = {'P1_REVISION': "Script falso do módulo 'RPi.GPIO'. Substituto usado apenas para simulação."}
VERSION = "0.0.1"
_PREFIXO = "[GPIO fake]"


# Configuração das GPIO

#: Tipo de identificação dos pinos da Raspberry Pi. Se utilizado, os pinos se referem aos
#: pidos da própria placa, e não ao número da GPIO.
BOARD = "BOARD"

#: Tipo de identificação dos pinos da Raspberry Pi. Se utilizado, os pinos se referem aos
#: número da GPIO, e não aos pinos da placa.
BCM = "BCM"

#: Configuração do pino como saída
OUT = "OUT"

#: Configuração do pino como entrada
IN = "IN"

#: Nível lógico alto (3,3V). Para ser usado ao definir o estado da saída de um pino.
HIGH = 1

#: Nível lógico baixo (0V). Para ser usado ao definir o estado da saída de um pino.
LOW = 0


# Parâmetros do módulo
_NUMERACAO = None
_LISTA_CANAIS = {}
_LISTA_ESTADOS = {}
_AVISOS = True


def setmode(numeracao):
    """Define a numeração dos pinos GPIO.

    Configura o tipo de identificação dos pinos da Raspberry Pi. Se utilizado :const:`BOARD`, os pinos
    se referem aos pidos da própria placa, e não ao número da GPIO. Se utilizado :const:`BCM`, os pinos
    se referem aos número da GPIO, e não aos pinos da placa.

    Parameters
    ----------
    numeracao : :const:`BOARD` or :const:`BCM`
        O tipo de numeração dos pinos GPIO. Pode ser :const:`BOARD` ou :const:`BCM`.
    """
    global _NUMERACAO
    _NUMERACAO = numeracao

def getmode():
    """Retorna o tipo de numeração dos GPIO.

    Returns
    -------
    :const:`BOARD` or :const:`BCM`
        O tipo de numeração dos pinos GPIO. Pode ser :const:`BOARD` ou :const:`BCM`.
    """
    global _NUMERACAO
    return _NUMERACAO

def _testa_modo():
    """Checa o modo do módulo.

    Se o módo do módulo não foi definido, causa uma excessão.
    """
    if getmode() == None:
        raise Exception("O modo do módulo não foi configurado!")

def _testa_canais(canais: int|list|tuple = -1, configuracao_do_pino = None):
    """Checa o modo do módulo e  configuração do pino.

    Se o módo do módulo não foi definido, causa uma excessão.

    Checa se os *canais* foram configurados de acordo com *configuracao_do_pino*. Caso não seja, resulta em uma excessão.
    A *configuracao_do_pino* se refere aos modos :const:`IN` e :const:`OUT`.

    Se fornecido um número inteiro em *canais*, checa apenas esse canal. Mas se for fornecido uma lista ou tupla, checa
    todos os canais dela.

    Parameters
    ----------
    canais : int or list or tuple, default -1
        Os canais a serem checados.

    configuracao_do_pino : :const:`IN` ou :const:`OUT`
        A configuração correta dos canais (para checagem). Pode ser :const:`IN` ou :const:`OUT`.
    """
    _testa_modo()

    global _LISTA_CANAIS
    global _INICIAL_CANAIS

    # Checagem da configuração do canal
    if canais != -1:
        # A checagem dos canais funciona com listas
        if type(canais) == int:
            canais = [canais]

        # A configuração dos canais e seus estados serão salvos como listas
        for canal in canais:
            canal = str(canal)

            # Checa se o canal foi configurado
            if canal in _LISTA_CANAIS:

                # Checagem da configuração do pino.
                if configuracao_do_pino != None:
                    # Checa se o canal foi configurado de acordo com o definido por *configuracao_do_pino*
                    if _LISTA_CANAIS[canal] != configuracao_do_pino:
                        raise Exception(
                                "O canal " + canal + " está configurado como " + _LISTA_CANAIS[canal] +
                                " e não como " + configuracao_do_pino
                                )

            # O canal ainda não foi configurado
            else:
                raise Exception("O canal " + canal + " não foi configurado")

# Avisos de erro
def setwarnings(avisos: bool):
    """Ativa ou desativas os avisos.

    Essa função não implica em nada no módulo de simulação. Está disponível apenas para conveniência.

    Parameters
    ----------
    avisos : bool
        Se True, ativa os avisos. Se False, desativa os avisos.
    """
    _testa_modo()

    global _AVISOS
    _AVISOS = avisos

def setup(canais: int|list|tuple, config):
    """Define um canal ou uma lista de canais como entrada ou saída.

    Se fornecido um número inteiro em *canais*, o canal desse número será definido com entrada
    ou saída, dependendo do parâmetro *config*.

    Caso *canais* seja uma lista ou tupla, o canal de cada elemento da lista ou tupla será definido
    com entrada ou saída, dependendo do parâmetro *config*.

    Parameters
    ----------
    canais : int or list or tuple
        O canal a ser configurado. Deve ser um número inteiro.

    config : :const:`OUT` or :const:`IN`
        A configuração do canal. Pode ser 'OUT' ou 'IN'.
    """
    _testa_modo()

    global _LISTA_CANAIS
    global _INICIAL_CANAIS

    # A definição de canis funciona com listas
    if type(canais) == int:
        canais = [canais]

    # A configuração dos canais e seus estados serão salvos como listas
    for canal in canais:
        canal = str(canal)
        _LISTA_CANAIS[canal] = config
        _LISTA_ESTADOS[canal] = 0

def output(canais: int|list|tuple, estado):
    """Define a saída de um canal.

    O canal deve estar onfigurado como 'GPIO.OUTPUT' usando a função :func:`setup`.

    Parameters
    ----------
    canais : int or list or tuple
        O canal cuja saída será definida. Deve ser um número inteiro.

    estado : :const:`LOW` or :const:`HIGH`
        O estado do canal. Pode ser :const:`LOW` ou :const:`HIGH`.
    """
    _testa_canais(canais, OUT)

    global _LISTA_CANAIS
    global _LISTA_ESTADOS

    # A definição de canis funciona com listas
    if type(canais) == int:
        canais = [canais]

    # A configuração dos canais e seus estados serão salvos como listas
    for canal in canais:
        canal = str(canal)
        _LISTA_ESTADOS[canal] = estado
        print(_PREFIXO, "Configurando canal", canal, "como", estado)

# PWM
class PWM():
    """Simulação de um PWM.

    Apenas apresenta os valores de frequẽncia e duty cycle definidos na saída padrão quando eles são ajustados.
    """

    def __init__(self, canal:int, freq: float):
        """Inicialização.

        Parameters
        ----------
        canal : int
            O canal a ser configurado. Deve ser um número inteiro.

        freq : float
            A frequência do PWM.
        """
        _testa_canais(canal, OUT)

        global _LISTA_CANAIS
        global _LISTA_ESTADOS

        self._canal = canal
        self._frequecia = freq
        self._dc = 0
        self._iniciado = False

        print(_PREFIXO, "Criando PWM no canal", self._canal, "e definindo frequência para", freq, "Hz")

    def start(self, duty_cycle: float):
        """Incia o PWM.

        Parameters
        ----------
        duty_cycle : float
            O duty cycle do PWM.
        """
        self._iniciado = True
        self._dc = duty_cycle
        print(_PREFIXO, "Iniciando PWM no canal", self._canal, "com duty cycle de", duty_cycle, "%")

    def ChangeFrequency(self, freq: float):
        """Altera a frequência do PWM.

        Parameters
        ----------
        freq : float
            A nova frequência do PWM.
        """
        if not self._iniciado:
            raise Exception("PWM do canal " + str(self._canal) + " não iniciado")

        self._frequecia = freq
        print(_PREFIXO, "Mudando frequência do PWM", self._canal, "para", freq, "Hz")

    def ChangeDutyCycle(self, duty_cycle: float):
        """Altera o duty cycle do PWM.

        Parameters
        ----------
        duty_cycle : float
            O novo duty cycle do PWM.
        """
        if not self._iniciado:
            raise Exception("PWM do canal " + str(self._canal) + " não iniciado")

        self._dc = duty_cycle
        print(_PREFIXO, "Mudando duty cycle do PWM", self._canal, "para", duty_cycle, "%")

    def stop(self):
        """Para o PWM."""
        self._iniciado = False
        print(_PREFIXO, "Parando PWM no canal", self._canal)

# Finalização dos canais
def cleanup(canais: tuple = None):
    """Desliga os canais.

    Parameters
    ----------
    canais : tuple, optional
        Os canais a serem desligados. Se None, desliga todos os canais.
    """
    _testa_modo()

    global _LISTA_CANAIS
    global _LISTA_ESTADOS

    if canais == None:
        print("Desligando todos os canais")
        _LISTA_CANAIS = {}
        _LISTA_ESTADOS = {}
        return None

    else:
        print("Desligando canais:", canais)
    
        # O desligamento de canis funciona com listas
        if type(canais) == int:
            canais = [canais]

        # Desliga os canais especificados
        for canal in canais:
            canal = str(canal)
            _LISTA_CANAIS[canal] = None
            _LISTA_ESTADOS[canal] = None
