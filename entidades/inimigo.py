
import pygame
import math
import os

from sistemas.transformacoes import (
    matriz_translacao,
    matriz_escala,
    multiplicar_matrizes,
    transformar_ponto
)


class Inimigo:

    imagem_base = None

    def __init__(self, x, y, vida=5):
        self.x = float(x)
        self.y = float(y)

        self.velocidade = 100
        self.raio = 22
        self.vida = vida

        # Carrega a imagem compartilhada
        self.carregar_imagem()

    def carregar_imagem(self):

        if Inimigo.imagem_base is not None:
            return

        caminho = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets",
            "inimigo.png"
        )

        imagem = pygame.image.load(caminho).convert_alpha()

        largura, altura = imagem.get_size()

        tamanho_maximo = 30
        escala = tamanho_maximo / max(largura, altura)

        nova_largura = int(largura * escala)
        nova_altura = int(altura * escala)

        imagem = pygame.transform.scale(
            imagem,
            (nova_largura, nova_altura)
        )

        # Aplica o tamanho final uma única vez
        escala_final = 3

        largura = int(nova_largura * escala_final)
        altura = int(nova_altura * escala_final)

        Inimigo.imagem_base = pygame.transform.scale(
            imagem,
            (largura, altura)
        )

    def atualizar(self, jogador_x, jogador_y, dt):

        dx = jogador_x - self.x
        dy = jogador_y - self.y

        distancia = math.sqrt(dx * dx + dy * dy)

        if distancia > 0:
            dx /= distancia
            dy /= distancia

        self.x += dx * self.velocidade * dt
        self.y += dy * self.velocidade * dt

    def desenhar(self, tela):

        # Matrizes de transformação
        translacao = matriz_translacao(self.x, self.y)
        escala = matriz_escala(1, 1)

        matriz = multiplicar_matrizes(
            translacao,
            escala
        )

        centro = transformar_ponto((0, 0), matriz)

        retangulo = Inimigo.imagem_base.get_rect(
            center=(int(centro[0]), int(centro[1]))
        )

        tela.blit(Inimigo.imagem_base, retangulo)
