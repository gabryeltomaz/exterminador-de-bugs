import pygame
import math

from sistemas.animacao import AnimacaoJogador


class Jogador:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

        # Movimento
        self.velocidade = 250
        self.raio = 22

        # Vida
        self.vida = 3
        self.invulnerabilidade = 0

        # Ataque
        self.tempo_ataque = 0
        self.intervalo_ataque = 0.6

        # Experiencia
        self.xp = 0
        self.nivel = 1
        self.xp_necessario = 50

        # Animacao
        self.animacao = AnimacaoJogador()

    def ganhar_xp(self, quantidade):
        self.xp += quantidade

        niveis_ganhos = 0

        while self.xp >= self.xp_necessario:
            self.xp -= self.xp_necessario

            self.nivel += 1
            self.xp_necessario += 25

            niveis_ganhos += 1

        return niveis_ganhos

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

        # Normaliza o movimento diagonal
        tamanho = math.sqrt(dx * dx + dy * dy)

        if tamanho > 0:
            dx /= tamanho
            dy /= tamanho

        # Atualiza posicao
        self.x += dx * self.velocidade * dt
        self.y += dy * self.velocidade * dt

        # Limita o jogador dentro da arena
        self.x = max(35, min(largura - 35, self.x))
        self.y = max(35, min(altura - 35, self.y))

        # Atualiza animacao
        self.animacao.atualizar(dt, dx)

        # Atualiza invulnerabilidade
        if self.invulnerabilidade > 0:
            self.invulnerabilidade -= dt

        # Atualiza intervalo de ataque
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
        self.animacao.desenhar(
            tela,
            self.x,
            self.y,
            self.invulnerabilidade
        )