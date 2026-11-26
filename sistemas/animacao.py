import pygame
import os


class AnimacaoJogador:
    def __init__(self):
        self.direcao = "east"

        self.frame_atual = 0
        self.tempo_animacao = 0
        self.intervalo_animacao = 0.10

        self.sprites = {
            "east": [],
            "west": []
        }

        self.carregar_sprites()

    def carregar_sprites(self):
        caminho_assets = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets"
        )

        for direcao in ["east", "west"]:
            caminho_pasta = os.path.join(
                caminho_assets,
                direcao
            )

            for i in range(6):
                nome_arquivo = f"frame_{i:03d}.png"

                caminho_imagem = os.path.join(
                    caminho_pasta,
                    nome_arquivo
                )

                imagem = pygame.image.load(
                    caminho_imagem
                ).convert_alpha()

                largura = int(imagem.get_width() * 2)
                altura = int(imagem.get_height() * 2)

                imagem = pygame.transform.scale(
                    imagem,
                    (largura, altura)
                )

                self.sprites[direcao].append(imagem)

    def atualizar(self, dt, dx):
        # Atualiza a direcao do personagem
        if dx > 0:
            self.direcao = "east"

        elif dx < 0:
            self.direcao = "west"

        # Atualiza os frames da animacao
        if dx != 0:
            self.tempo_animacao += dt

            if self.tempo_animacao >= self.intervalo_animacao:
                self.frame_atual += 1

                self.frame_atual %= len(
                    self.sprites[self.direcao]
                )

                self.tempo_animacao = 0

        else:
            self.frame_atual = 0
            self.tempo_animacao = 0

    def desenhar(self, tela, x, y, invulnerabilidade):
        imagem = self.sprites[self.direcao][self.frame_atual]

        retangulo = imagem.get_rect(
            center=(int(x), int(y))
        )

        # Efeito visual de dano
        if invulnerabilidade > 0:
            tempo_decorrido = 1.0 - invulnerabilidade
            intervalo = 1.0 / 6

            piscar = int(tempo_decorrido / intervalo) % 2 == 0

            if piscar:
                imagem = imagem.copy()

                camada_vermelha = pygame.Surface(
                    imagem.get_size(),
                    pygame.SRCALPHA
                )

                camada_vermelha.fill((255, 0, 0, 120))

                imagem.blit(
                    camada_vermelha,
                    (0, 0),
                    special_flags=pygame.BLEND_RGBA_ADD
                )

        tela.blit(imagem, retangulo)