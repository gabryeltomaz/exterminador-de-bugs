
import math


def matriz_translacao(tx, ty):

    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]


def matriz_escala(sx, sy):

    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ]


def matriz_rotacao(angulo):

    c = math.cos(angulo)
    s = math.sin(angulo)

    return [
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ]


def multiplicar_matrizes(a, b):

    resultado = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    for i in range(3):
        for j in range(3):

            for k in range(3):
                resultado[i][j] += a[i][k] * b[k][j]

    return resultado


def transformar_ponto(ponto, matriz):

    x, y = ponto

    novo_x = matriz[0][0] * x + matriz[0][1] * y + matriz[0][2]
    novo_y = matriz[1][0] * x + matriz[1][1] * y + matriz[1][2]

    return (novo_x, novo_y)
