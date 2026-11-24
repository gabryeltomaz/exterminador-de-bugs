
import pygame
import math

from transformacoes import (
    matriz_translacao,
    matriz_rotacao,
    multiplicar_matrizes,
    transformar_ponto
)


class Projetil:

    def __init__(self, x, y, alvo_x, alvo_y):

        self.x = float(x)
        self.y = float(y)

        dx = alvo_x - x
        dy = alvo_y - y

        distancia = math.sqrt(dx * dx + dy * dy)

        if distancia > 0:

            dx /= distancia
            dy /= distancia

        self.dx = dx
        self.dy = dy

        self.velocidade = 450
        self.raio = 7

        # Angulo de rotacao
        self.angulo = math.atan2(dy, dx)

        self.tempo_vida = 2.0

    def atualizar(self, dt):

        self.x += self.dx * self.velocidade * dt
        self.y += self.dy * self.velocidade * dt

        self.tempo_vida -= dt

    def desenhar(self, tela):

        # Matrizes de transformacao
        rotacao = matriz_rotacao(self.angulo)

        translacao = matriz_translacao(self.x, self.y)

        matriz = multiplicar_matrizes(translacao, rotacao)

        # Formato local do projetil
        vertices = [
            (12, 0),
            (-7, -5),
            (-4, 0),
            (-7, 5)
        ]

        pontos = []

        for ponto in vertices:

            novo_ponto = transformar_ponto(ponto, matriz)

            pontos.append((
                int(novo_ponto[0]),
                int(novo_ponto[1])
            ))

        # Corpo do projetil
        pygame.draw.polygon(
            tela,
            (50, 220, 220),
            pontos
        )

        # Brilho
        pygame.draw.circle(
            tela,
            (180, 255, 255),
            (int(self.x), int(self.y)),
            3
        )
