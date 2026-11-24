
import pygame
import math

from transformacoes import (
    matriz_translacao,
    transformar_ponto
)


class Jogador:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

        self.velocidade = 250
        self.raio = 22

        self.vida = 3
        self.invulnerabilidade = 0

        self.tempo_ataque = 0
        self.intervalo_ataque = 0.6

    def atualizar(self, dt, teclas, largura, altura):
        dx = 0
        dy = 0

        # Movimento WASD
        if teclas[pygame.K_w]:
            dy -= 1
        if teclas[pygame.K_s]:
            dy += 1
        if teclas[pygame.K_a]:
            dx -= 1
        if teclas[pygame.K_d]:
            dx += 1

        # Normaliza a direção para evitar movimento diagonal mais rápido
        tamanho = math.sqrt(dx * dx + dy * dy)

        if tamanho > 0:
            dx /= tamanho
            dy /= tamanho

        self.x += dx * self.velocidade * dt
        self.y += dy * self.velocidade * dt

        # Impede que o jogador saia da arena
        self.x = max(35, min(largura - 35, self.x))
        self.y = max(35, min(altura - 35, self.y))

        # Atualiza a invulnerabilidade
        if self.invulnerabilidade > 0:
            self.invulnerabilidade -= dt

        # Controla o intervalo entre ataques
        self.tempo_ataque += dt

    def pode_atacar(self):
        if self.tempo_ataque >= self.intervalo_ataque:
            self.tempo_ataque = 0
            return True

        return False

    def receber_dano(self):
        if self.invulnerabilidade <= 0:
            self.vida -= 1
            self.invulnerabilidade = 1.0

    def desenhar(self, tela):
        matriz = matriz_translacao(self.x, self.y)

        ROXO = (120, 70, 200)
        ROXO_ESCURO = (75, 40, 120)
        PELE = (230, 190, 150)
        BRANCO = (230, 230, 230)
        CIANO = (50, 220, 220)

        def para_tela(ponto):
            return (int(ponto[0]), int(ponto[1]))

        # Corpo do mago
        corpo = [
            (-17, 8),
            (17, 8),
            (23, 42),
            (-23, 42)
        ]

        corpo_transformado = [
            para_tela(transformar_ponto(ponto, matriz))
            for ponto in corpo
        ]

        pygame.draw.polygon(tela, ROXO, corpo_transformado)

        # Cabeça
        cabeca = para_tela(
            transformar_ponto((0, -5), matriz)
        )

        pygame.draw.circle(tela, PELE, cabeca, 11)

        # Chapéu
        chapeu = [
            (-14, -13),
            (14, -13),
            (0, -35)
        ]

        chapeu_transformado = [
            para_tela(transformar_ponto(ponto, matriz))
            for ponto in chapeu
        ]

        pygame.draw.polygon(tela, ROXO_ESCURO, chapeu_transformado)

        # Cajado
        inicio = para_tela(
            transformar_ponto((22, 5), matriz)
        )

        fim = para_tela(
            transformar_ponto((30, 45), matriz)
        )

        pygame.draw.line(tela, BRANCO, inicio, fim, 4)

        # Pedra mágica
        pedra = para_tela(
            transformar_ponto((22, 0), matriz)
        )

        pygame.draw.circle(tela, CIANO, pedra, 6)
