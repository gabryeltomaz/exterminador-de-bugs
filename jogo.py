
import pygame
import random

from jogador import Jogador
from inimigo import Inimigo
from projetil import Projetil
from colisoes import colisao_circular
from tela import Tela


class Jogo:
    def __init__(self):
        pygame.init()

        self.largura = 1000
        self.altura = 650

        self.tela = Tela(self.largura, self.altura)

        self.relogio = pygame.time.Clock()

        # Criação dos objetos
        self.jogador = Jogador(
            self.largura / 2,
            self.altura / 2
        )

        self.inimigos = []
        self.projeteis = []

        # Controle de surgimento dos inimigos
        self.tempo_spawn = 0
        self.intervalo_spawn = 2.0

        self.jogo_ativo = True
        self.executando = True

    def criar_inimigo(self):
        lado = random.choice([
            "cima",
            "baixo",
            "esquerda",
            "direita"
        ])

        if lado == "cima":
            x = random.randint(30, self.largura - 30)
            y = 30

        elif lado == "baixo":
            x = random.randint(30, self.largura - 30)
            y = self.altura - 30

        elif lado == "esquerda":
            x = 30
            y = random.randint(30, self.altura - 30)

        else:
            x = self.largura - 30
            y = random.randint(30, self.altura - 30)

        self.inimigos.append(Inimigo(x, y))

    def atualizar_inimigos(self, dt):
        for inimigo in self.inimigos:
            inimigo.atualizar(
                self.jogador.x,
                self.jogador.y,
                dt
            )

            # Colisão entre jogador e inimigo
            if colisao_circular(
                self.jogador.x,
                self.jogador.y,
                self.jogador.raio,
                inimigo.x,
                inimigo.y,
                inimigo.raio
            ):
                self.jogador.receber_dano()

                if self.jogador.vida <= 0:
                    self.jogo_ativo = False

    def atualizar_projeteis(self, dt):
        removidos = []
        inimigos_derrotados = []

        for projetil in self.projeteis:
            projetil.atualizar(dt)

            if projetil.tempo_vida <= 0:
                removidos.append(projetil)
                continue

            for inimigo in self.inimigos:
                if inimigo in inimigos_derrotados:
                    continue

                if colisao_circular(
                    projetil.x,
                    projetil.y,
                    projetil.raio,
                    inimigo.x,
                    inimigo.y,
                    inimigo.raio
                ):
                    inimigo.vida -= 1
                    removidos.append(projetil)

                    if inimigo.vida <= 0:
                        inimigos_derrotados.append(inimigo)

                    break

        for projetil in removidos:
            if projetil in self.projeteis:
                self.projeteis.remove(projetil)

        for inimigo in inimigos_derrotados:
            if inimigo in self.inimigos:
                self.inimigos.remove(inimigo)

    def atacar(self):
        if not self.jogador.pode_atacar():
            return

        if len(self.inimigos) == 0:
            return

        inimigo_proximo = None
        menor_distancia = float("inf")

        for inimigo in self.inimigos:
            dx = inimigo.x - self.jogador.x
            dy = inimigo.y - self.jogador.y

            distancia = dx * dx + dy * dy

            if distancia < menor_distancia:
                menor_distancia = distancia
                inimigo_proximo = inimigo

        if inimigo_proximo is not None:
            projetil = Projetil(
                self.jogador.x,
                self.jogador.y,
                inimigo_proximo.x,
                inimigo_proximo.y
            )

            self.projeteis.append(projetil)

    def atualizar(self, dt):
        teclas = pygame.key.get_pressed()

        self.jogador.atualizar(
            dt,
            teclas,
            self.largura,
            self.altura
        )

        # Surgimento de inimigos
        self.tempo_spawn += dt

        if self.tempo_spawn >= self.intervalo_spawn:
            self.criar_inimigo()
            self.tempo_spawn = 0

        self.atualizar_inimigos(dt)

        if not self.jogo_ativo:
            return

        self.atacar()
        self.atualizar_projeteis(dt)

    def executar(self):
        while self.executando:
            dt = min(
                self.relogio.tick(60) / 1000,
                0.05
            )

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.executando = False

            if self.jogo_ativo:
                self.atualizar(dt)

            self.tela.desenhar(
                self.jogador,
                self.inimigos,
                self.projeteis,
                self.jogo_ativo
            )

        pygame.quit()
