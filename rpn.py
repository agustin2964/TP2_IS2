"""
Módulo que implementa una calculadora RPN (Reverse Polish Notation).
Permite evaluar expresiones, aplicar funciones y manejar errores.
"""

import math


class RPNError(Exception):
    """Excepción para errores en la evaluación RPN."""


def _err(msg):
    """Lanza una excepción de tipo RPNError."""
    raise RPNError(f"Error: {msg}")


def _pop(pila, n=1):
    """
    Extrae uno o dos elementos de la pila.

    Args:
        pila (list): pila de operandos
        n (int): cantidad de elementos a extraer

    Returns:
        float o tuple: elemento(s) extraído(s)

    Raises:
        RPNError: si no hay suficientes elementos
    """
    if len(pila) < n:
        _err("pila insuficiente")

    if n == 1:
        return pila.pop()

    b = pila.pop()
    a = pila.pop()
    return b, a


# -------------------------
# FUNCIONES AUXILIARES
# -------------------------


def _add(a, b):
    return a + b


def _sub(a, b):
    return a - b


def _mul(a, b):
    return a * b


def _div(a, b):
    if b == 0:
        _err("división por cero")
    return a / b


def _sqrt(x):
    if x < 0:
        _err("sqrt negativo")
    return math.sqrt(x)


def _log(x):
    if x <= 0:
        _err("log inválido")
    return math.log10(x)


def _ln(x):
    if x <= 0:
        _err("ln inválido")
    return math.log(x)


def _inv(x):
    if x == 0:
        _err("división por cero")
    return 1 / x


def _pow10(x):
    return 10 ** x


def _chs(x):
    return -x


# -------------------------
# TABLAS DE OPERACIONES
# -------------------------

BINARIAS = {
    "+": _add,
    "-": _sub,
    "*": _mul,
    "/": _div,
}

UNARIAS = {
    "sqrt": _sqrt,
    "log": _log,
    "ln": _ln,
    "ex": math.exp,
    "10x": _pow10,
    "1/x": _inv,
    "chs": _chs,
}

CONSTANTES = {
    "p": math.pi,
    "e": math.e,
    "j": (1 + math.sqrt(5)) / 2,
}


# -------------------------
# PROCESAMIENTO DE TOKENS
# -------------------------


def _procesar_token(token, pila):
    """Procesa un token individual modificando la pila."""

    # Intento de parseo numérico
    try:
        pila.append(float(token))
        return
    except ValueError:
        pass

    if token in CONSTANTES:
        pila.append(CONSTANTES[token])

    elif token in BINARIAS:
        b, a = _pop(pila, 2)
        pila.append(BINARIAS[token](a, b))

    elif token in UNARIAS:
        pila.append(UNARIAS[token](_pop(pila)))

    elif token == 'dup':
        v = _pop(pila)
        pila.extend([v, v])

    elif token == 'swap':
        b, a = _pop(pila, 2)
        pila.extend([b, a])

    elif token == 'drop':
        _pop(pila)

    elif token == 'clear':
        pila.clear()

    elif token == 'yx':
        x, y = _pop(pila, 2)
        pila.append(y ** x)

    else:
        _err(f"token inválido '{token}'")


# -------------------------
# FUNCION PRINCIPAL
# -------------------------


def evaluar_rpn(expresion: str) -> float:
    """
    Evalúa una expresión en notación polaca inversa (RPN).

    Admite:
    - Números reales
    - Operadores binarios: +, -, *, /
    - Funciones: sqrt, log, ln, ex, 10x, yx, 1/x, chs
    - Constantes: p (pi), e, j (phi)
    - Comandos de pila: dup, swap, drop, clear

    Raises:
        RPNError: si la expresión es inválida o ocurre un error matemático.
    """
    if not expresion.strip():
        _err("expresión vacía")

    pila = []

    for token in expresion.split():
        _procesar_token(token, pila)

    if len(pila) != 1:
        _err("expresión inválida")

    return pila[0]
