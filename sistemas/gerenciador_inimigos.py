
import random

from entidades.inimigo import Inimigo
from sistemas.colisoes import colisao_circular


class GerenciadorInimigos:

    def __init__(self, largura, altura):

        self.largura = largura
        self.altura = altura

        self.inimigos = []

        # Dificuldade
        self.nivel_dificuldade = 0
        self.vida_inimigo = 5

        # Surgimento dos inimigos
        self.tempo_spawn = 0
        self.intervalo_spawn = 2.0

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

        inimigo = Inimigo(
            x,
            y,
            self.vida_inimigo
        )

        self.inimigos.append(inimigo)

    def atualizar_dificuldade(self, tempo_partida):

        # Aumenta um nivel a cada 30 segundos
        novo_nivel = int(tempo_partida // 30)

        if novo_nivel > self.nivel_dificuldade:

            aumento = novo_nivel - self.nivel_dificuldade

            self.nivel_dificuldade = novo_nivel
            self.vida_inimigo += aumento

            # Aumenta a vida dos inimigos existentes
            for inimigo in self.inimigos:
                inimigo.vida += aumento

    def atualizar_spawn(self, dt):

        self.tempo_spawn += dt

        while self.tempo_spawn >= self.intervalo_spawn:

            self.criar_inimigo()
            self.tempo_spawn -= self.intervalo_spawn

    def atualizar_movimento(self, jogador, dt):

        for inimigo in self.inimigos:

            inimigo.atualizar(
                jogador.x,
                jogador.y,
                dt
            )

    def verificar_colisoes(self, jogador):

        for inimigo in self.inimigos:

            if colisao_circular(
                jogador.x,
                jogador.y,
                jogador.raio,
                inimigo.x,
                inimigo.y,
                inimigo.raio
            ):

                jogador.receber_dano()

                if jogador.vida <= 0:
                    return

    def atualizar(self, jogador, tempo_partida, dt):

        self.atualizar_dificuldade(tempo_partida)

        self.atualizar_spawn(dt)

        self.atualizar_movimento(jogador, dt)

        self.verificar_colisoes(jogador)
