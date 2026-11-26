
import pygame
import os

from interface.hud import HUD


class Tela:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        self.janela = pygame.display.set_mode(
            (largura, altura)
        )

        pygame.display.set_caption("Survivor Arena")

        # Carrega o cenário
        caminho = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets",
            "fundoprincipal.png"
        )

        imagem = pygame.image.load(caminho).convert()

        self.fundo = pygame.transform.scale(
            imagem,
            (largura, altura)
        )

        # Borda da arena
        self.borda = (45, 65, 75)

        # Interface
        self.hud = HUD(largura, altura)

    def desenhar_fundo(self):

        self.janela.blit(self.fundo, (0, 0))

        pygame.draw.rect(
            self.janela,
            self.borda,
            (10, 10, self.largura - 20, self.altura - 20),
            2
        )

    def desenhar(
        self,
        jogador,
        inimigos,
        projeteis,
        armas,
        jogo_ativo,
        tempo,
        nivel_dificuldade
    ):

        self.desenhar_fundo()

        # Desenha inimigos
        for inimigo in inimigos:
            inimigo.desenhar(self.janela)

        # Desenha armas
        for arma in armas:
            arma.desenhar(self.janela)

        # Desenha projeteis
        for projetil in projeteis:
            projetil.desenhar(self.janela)

        # Desenha jogador
        jogador.desenhar(self.janela)

        # Desenha interface
        self.hud.desenhar(
            self.janela,
            jogador,
            inimigos,
            tempo,
            nivel_dificuldade
        )

        # Game Over
        if not jogo_ativo:
            self.hud.desenhar_game_over(self.janela)

        pygame.display.flip()
