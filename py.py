from enum import Enum
from typing import TypedDict
from random import choice

# pagos[row][col]
pagosPosibles = [
    [(1, 1), (-2, 3)],
    [(3, -3), (-1, -1)],
]


class EstrategiasPosibles(Enum):
    """define nombres de estrategias"""
    TitForTat = "TitForTat"
    Angel = "Angel"
    Grudge = "Grudge"
    Random = "Random"
    Custom = "Custom"


class Move(Enum):
    """movimientos posibles"""
    COOPERAR = 0
    TRAICION = 1


def correrJuego(
    estrategiaJugador1: EstrategiasPosibles,
    estrategiaJugador2: EstrategiasPosibles,
) -> list[tuple]:
    """simula juego dado una estrategia"""
    # funciones de estrategia de jugadores
    sP1 = strToFunction(estrategiaJugador1)
    sP2 = strToFunction(estrategiaJugador2)
    # movimiento jugador (player) 1 y 2 anterior
    mP1 = None
    mP2 = None
    # traicionada
    P1Traicionado = False
    P2Traicionado = False
    # pagos
    pagos: list[tuple] = []
    # correr juego 100 veces
    for _ in range(0, 100):
        paramsP1: Params = {
            "movimientoOponenteAnterior": mP2,
            "traicionado": P1Traicionado,
        }
        paramsP2: Params = {
            "movimientoOponenteAnterior": mP1,
            "traicionado": P2Traicionado,
        }
        # actualizar movimientos
        mP1 = sP1(paramsP1)
        mP2 = sP2(paramsP2)
        # actualizar traicionado
        P1Traicionado = P1Traicionado or (mP2 == Move.TRAICION)
        P2Traicionado = P2Traicionado or (mP1 == Move.TRAICION)
        # jugador 1 en fila, jugador 2 en columna, retorna resultados
        pagos.append(pagosPosibles[mP1.value][mP2.value])
    return pagos


def strToFunction(string: EstrategiasPosibles) -> callable:
    """retorna funcion de estrategia dado un nombre de funcion"""
    funciones: dict(EstrategiasPosibles, callable) = {
        EstrategiasPosibles.TitForTat: titForTat,
        EstrategiasPosibles.Angel: angel,
        EstrategiasPosibles.Grudge: grudge,
        EstrategiasPosibles.Random: random,
        EstrategiasPosibles.Custom: custom,
    }
    return funciones[string]


class Params(TypedDict):
    """parametros de funciones de estrategias"""
    movimientoOponenteAnterior: Move
    traicionado: bool


# estrategias
def titForTat(params: Params) -> Move:
    """se copia del movimiento anterior del otro jugador
    en el primer turno coopera por defecto"""
    movimientoOponenteAnterior = params["movimientoOponenteAnterior"]
    # en primer turno, cooperar por defecto
    if (movimientoOponenteAnterior is None):
        movimientoOponenteAnterior = Move.COOPERAR
    return movimientoOponenteAnterior


def angel(_: Params) -> Move:
    """siempre coopera"""
    return Move.COOPERAR


def grudge(params: Params) -> Move:
    """siempre coopera, pero si lo traicionan una vez traiciona por el resto del juego"""
    if params["traicionado"] is True:
        return Move.TRAICION
    return Move.COOPERAR


def random(_: Params) -> Move:
    """escoger entre cooperar y traicion al azar"""
    return choice([Move.COOPERAR, Move.TRAICION])


def custom(_: Params) -> Move:
    """siempre traiciona"""
    return Move.TRAICION


# casos
class Casos:
    """todos los casos requeridos"""

    @staticmethod
    def printResults(resultados: list[tuple]):
        """imprime resultados a consola"""
        utilidadTotalP1 = 0
        utilidadTotalP2 = 0
        for i in resultados:
            utilidadTotalP1 += i[0]
            utilidadTotalP2 += i[1]
        print(f"utilidad total jugador 1: {utilidadTotalP1}")
        print(f"utilidad total jugador 2: {utilidadTotalP2}")
        print("")

    @staticmethod
    def caso1():
        """caso 1: Random y Angel"""
        resultados = correrJuego(
            EstrategiasPosibles.Random,
            EstrategiasPosibles.Angel,
        )
        print("----------------CASO 1----------------")
        print("   100 iteraciones, Random y Angel   ")
        print("--------------------------------------")
        Casos.printResults(resultados)

    @staticmethod
    def caso2():
        """caso 2: Grudge y Tit for Tat"""
        resultados = correrJuego(
            EstrategiasPosibles.Grudge,
            EstrategiasPosibles.TitForTat,
        )
        print("----------------CASO 2----------------")
        print("100 iteraciones, Grudge y Tit for Tat")
        print("--------------------------------------")
        Casos.printResults(resultados)

    @staticmethod
    def caso3():
        """caso 3: Custom y Tit for Tat"""
        resultados = correrJuego(
            EstrategiasPosibles.Custom,
            EstrategiasPosibles.TitForTat,
        )
        print("----------------CASO 3----------------")
        print("100 iteraciones, Custom y Tit for Tat")
        print("--------------------------------------")
        Casos.printResults(resultados)


Casos.caso1()
Casos.caso2()
Casos.caso3()
