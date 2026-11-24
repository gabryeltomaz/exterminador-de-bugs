
import pygame
import math
import os

from transformacoes import (
    matriz_translacao,
    matriz_escala,
    multiplicar_matrizes,
    transformar_ponto
)


class Inimigo:

    # Imagem compartilhada entre todos os inimigos
    imagem_base = None

    def __init__(self, x, y):

        self.x = float(x)
        self.y = float(y)

        self.velocidade = 100
        self.raio = 18

        self.tempo = 0
        self.vida = 5

        # Carrega o sprite apenas uma vez
        if Inimigo.imagem_base is None:

            caminho = os.path.join(
                os.path.dirname(__file__),
                "assets",
                "inimigo.png"
            )

            imagem = pygame.image.load(caminho).convert_alpha()

            # Mantém a proporção original da imagem
            largura, altura = imagem.get_size()

            tamanho_maximo = 44
            escala = tamanho_maximo / max(largura, altura)

            nova_largura = int(largura * escala)
            nova_altura = int(altura * escala)

            Inimigo.imagem_base = pygame.transform.scale(
                imagem,
                (nova_largura, nova_altura)
            )

    def atualizar(self, jogador_x, jogador_y, dt):

        dx = jogador_x - self.x
        dy = jogador_y - self.y

        distancia = math.sqrt(dx * dx + dy * dy)

        if distancia > 0:

            dx = dx / distancia
            dy = dy / distancia

        self.x += dx * self.velocidade * dt
        self.y += dy * self.velocidade * dt

        self.tempo += dt

    def desenhar(self, tela):

        escala = 3 

        # Matrizes de transformacao
        translacao = matriz_translacao(self.x, self.y)
        tamanho = matriz_escala(escala, escala)

        matriz = multiplicar_matrizes(translacao, tamanho)

        # Calcula o centro do sprite usando a matriz
        centro = transformar_ponto((0, 0), matriz)

        # Aplica a escala na imagem
        largura = int(Inimigo.imagem_base.get_width() * escala)
        altura = int(Inimigo.imagem_base.get_height() * escala)

        imagem = pygame.transform.scale(
            Inimigo.imagem_base,
            (largura, altura)
        )

        # Centraliza o sprite na posição do inimigo
        retangulo = imagem.get_rect(
            center=(int(centro[0]), int(centro[1]))
        )

        tela.blit(imagem, retangulo)
