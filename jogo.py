
import pygame

from entidades.jogador import Jogador
from sistemas.gerenciador_inimigos import GerenciadorInimigos
from sistemas.gerenciador_combate import GerenciadorCombate
from interface.tela import Tela


class Jogo:

    def __init__(self):

        pygame.init()

        self.largura = 1000
        self.altura = 650

        self.tela = Tela(
            self.largura,
            self.altura
        )

        self.relogio = pygame.time.Clock()

        # Jogador
        self.jogador = Jogador(
            self.largura / 2,
            self.altura / 2
        )

        # Gerenciador de inimigos
        self.gerenciador_inimigos = GerenciadorInimigos(
            self.largura,
            self.altura
        )

        # Gerenciador de combate
        self.gerenciador_combate = GerenciadorCombate(
            self.jogador,
            self.gerenciador_inimigos.inimigos
        )

        # Tempo da partida
        self.tempo_partida = 0

        # Estado do jogo
        self.jogo_ativo = True
        self.executando = True

    def atualizar(self, dt):

        # Atualiza o tempo da partida
        self.tempo_partida += dt

        # Atualiza jogador
        teclas = pygame.key.get_pressed()

        self.jogador.atualizar(
            dt,
            teclas,
            self.largura,
            self.altura
        )

        # Atualiza inimigos
        self.gerenciador_inimigos.atualizar(
            self.jogador,
            self.tempo_partida,
            dt
        )

        # Verifica se o jogador morreu
        if self.jogador.vida <= 0:
            self.jogo_ativo = False
            return

        # Atualiza combate
        self.gerenciador_combate.atualizar(dt)

    def executar(self):

        while self.executando:

            dt = min(
                self.relogio.tick(60) / 1000,
                0.05
            )

            # Eventos
            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    self.executando = False

            # Atualiza partida
            if self.jogo_ativo:
                self.atualizar(dt)

            # Desenha partida
            self.tela.desenhar(
                self.jogador,
                self.gerenciador_inimigos.inimigos,
                self.gerenciador_combate.projeteis,
                self.gerenciador_combate.armas,
                self.jogo_ativo,
                self.tempo_partida,
                self.gerenciador_inimigos.nivel_dificuldade
            )

        pygame.quit()
