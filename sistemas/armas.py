
import pygame
import math

from sistemas.colisoes import colisao_circular


class EsferasOrbitais:
    def __init__(self):
        self.quantidade = 2

        self.raio_orbita = 65
        self.raio_esfera = 10

        self.angulo = 0
        self.velocidade_rotacao = 2.5

        self.dano = 5
        self.intervalo_dano = 0.5

        self.tempos_dano = {}

        self.posicoes = []

    def atualizar(self, jogador, inimigos, dt):

        # Atualiza o angulo das esferas
        self.angulo += self.velocidade_rotacao * dt

        # Atualiza o tempo de espera para causar dano
        for inimigo in list(self.tempos_dano.keys()):

            self.tempos_dano[inimigo] -= dt

            if inimigo not in inimigos:
                del self.tempos_dano[inimigo]

        self.posicoes = []

        # Calcula a posicao de cada esfera
        for i in range(self.quantidade):

            angulo_esfera = (
                self.angulo +
                (2 * math.pi * i / self.quantidade)
            )

            x = jogador.x + math.cos(angulo_esfera) * self.raio_orbita
            y = jogador.y + math.sin(angulo_esfera) * self.raio_orbita

            self.posicoes.append((x, y))

        inimigos_derrotados = []

        # Verifica colisao das esferas com os inimigos
        for x, y in self.posicoes:

            for inimigo in inimigos:

                if inimigo in inimigos_derrotados:
                    continue

                if colisao_circular(
                    x,
                    y,
                    self.raio_esfera,
                    inimigo.x,
                    inimigo.y,
                    inimigo.raio
                ):

                    tempo_restante = self.tempos_dano.get(inimigo, 0)

                    if tempo_restante <= 0:

                        inimigo.vida -= self.dano

                        self.tempos_dano[inimigo] = self.intervalo_dano

                        if inimigo.vida <= 0:
                            inimigos_derrotados.append(inimigo)

        return inimigos_derrotados

    def desenhar(self, tela):

        # Desenha as esferas
        for x, y in self.posicoes:

            centro = (int(x), int(y))


            # Corpo da esfera
            pygame.draw.circle(
                tela,
                (50, 210, 255),
                centro,
                self.raio_esfera
            )


