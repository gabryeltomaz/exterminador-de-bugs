
import pygame
import os


class Tela:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        self.janela = pygame.display.set_mode(
            (largura, altura)
        )

        pygame.display.set_caption("Survivor Arena")

        # Carrega a imagem do terreno
        caminho = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "terreno.jpg"
        )

        imagem = pygame.image.load(caminho).convert()

        # Redimensiona a imagem para ocupar toda a janela
        self.fundo = pygame.transform.scale(
            imagem,
            (largura, altura)
        )

        # Cores
        self.borda = (45, 65, 75)
        self.branco = (230, 230, 230)
        self.vermelho = (220, 55, 55)

        # Fontes
        self.fonte = pygame.font.SysFont("Arial", 24)
        self.fonte_game_over = pygame.font.SysFont("Arial", 48)

    def desenhar_fundo(self):

        # Desenha a imagem do terreno
        self.janela.blit(self.fundo, (0, 0))

        # Borda da arena
        pygame.draw.rect(
            self.janela,
            self.borda,
            (10, 10, self.largura - 20, self.altura - 20),
            2
        )

    def desenhar_hud(self, jogador, inimigos):
        texto_vida = self.fonte.render(
            f"VIDA: {jogador.vida}",
            True,
            self.vermelho
        )

        self.janela.blit(texto_vida, (25, 25))

        texto_inimigos = self.fonte.render(
            f"INIMIGOS: {len(inimigos)}",
            True,
            self.branco
        )

        self.janela.blit(texto_inimigos, (25, 55))

    def desenhar_game_over(self):
        texto = self.fonte_game_over.render(
            "GAME OVER",
            True,
            self.vermelho
        )

        retangulo = texto.get_rect(
            center=(self.largura // 2, self.altura // 2)
        )

        self.janela.blit(texto, retangulo)

    def desenhar(self, jogador, inimigos, projeteis, jogo_ativo):
        self.desenhar_fundo()

        # Desenha os inimigos
        for inimigo in inimigos:
            inimigo.desenhar(self.janela)

        # Desenha os projéteis
        for projetil in projeteis:
            projetil.desenhar(self.janela)

        # Desenha o jogador
        jogador.desenhar(self.janela)

        # Desenha informações da partida
        self.desenhar_hud(jogador, inimigos)

        if not jogo_ativo:
            self.desenhar_game_over()

        pygame.display.flip()
