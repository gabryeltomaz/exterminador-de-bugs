
import pygame


class HUD:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        # Cores
        self.branco = (230, 230, 230)
        self.vermelho = (220, 55, 55)
        self.amarelo = (255, 200, 60)
        self.azul_xp = (50, 180, 255)
        self.fundo_barra = (30, 30, 40)

        # Fontes
        self.fonte = pygame.font.SysFont("Arial", 24)
        self.fonte_pequena = pygame.font.SysFont("Arial", 18)
        self.fonte_game_over = pygame.font.SysFont("Arial", 48)

    def desenhar_texto(self, superficie, texto, fonte, cor, x, y):
        imagem = fonte.render(texto, True, cor)
        superficie.blit(imagem, (x, y))

    def desenhar(self, tela, jogador, inimigos, tempo, nivel_dificuldade):

        # Tempo da partida
        minutos = int(tempo // 60)
        segundos = int(tempo % 60)

        tempo_formatado = f"{minutos:02d}:{segundos:02d}"

        self.desenhar_texto(
            tela, f"TEMPO: {tempo_formatado}",
            self.fonte, self.branco, 25, 25
        )

        # Vida
        self.desenhar_texto(
            tela, f"VIDA: {jogador.vida}",
            self.fonte, self.vermelho, 25, 55
        )

        # Quantidade de inimigos
        self.desenhar_texto(
            tela, f"INIMIGOS: {len(inimigos)}",
            self.fonte, self.branco, 25, 85
        )

        # Dificuldade
        self.desenhar_texto(
            tela, f"DIFICULDADE: NIVEL {nivel_dificuldade + 1}",
            self.fonte, self.amarelo, 25, 115
        )

        # Nivel do jogador
        self.desenhar_texto(
            tela, f"NIVEL DO JOGADOR: {jogador.nivel}",
            self.fonte, self.azul_xp, 25, 150
        )

        # Experiencia
        self.desenhar_texto(
            tela,
            f"XP: {jogador.xp} / {jogador.xp_necessario}",
            self.fonte_pequena,
            self.branco,
            25,
            180
        )

        self.desenhar_barra_xp(tela, jogador)

    def desenhar_barra_xp(self, tela, jogador):

        largura_barra = 220
        altura_barra = 14

        porcentagem = jogador.xp / jogador.xp_necessario

        largura_preenchida = int(
            largura_barra * porcentagem
        )

        # Fundo da barra
        pygame.draw.rect(
            tela,
            self.fundo_barra,
            (25, 205, largura_barra, altura_barra)
        )

        # Preenchimento
        pygame.draw.rect(
            tela,
            self.azul_xp,
            (25, 205, largura_preenchida, altura_barra)
        )

        # Borda
        pygame.draw.rect(
            tela,
            self.branco,
            (25, 205, largura_barra, altura_barra),
            1
        )

    def desenhar_game_over(self, tela):

        texto = self.fonte_game_over.render(
            "GAME OVER",
            True,
            self.vermelho
        )

        retangulo = texto.get_rect(
            center=(self.largura // 2, self.altura // 2)
        )

        tela.blit(texto, retangulo)
