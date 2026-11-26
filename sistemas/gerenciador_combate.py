
from entidades.projetil import Projetil
from sistemas.armas import EsferasOrbitais
from sistemas.colisoes import colisao_circular


class GerenciadorCombate:

    def __init__(self, jogador, inimigos):

        self.jogador = jogador
        self.inimigos = inimigos

        self.projeteis = []
        self.armas = []

    def atacar(self):

        # Nao tenta atacar se nao existem inimigos
        if len(self.inimigos) == 0:
            return

        if not self.jogador.pode_atacar():
            return

        inimigo_proximo = None
        menor_distancia = float("inf")

        # Procura o inimigo mais proximo
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

    def remover_inimigos_derrotados(self, inimigos_derrotados):

        for inimigo in inimigos_derrotados:

            if inimigo in self.inimigos:

                self.inimigos.remove(inimigo)

                niveis_ganhos = self.jogador.ganhar_xp(10)

                if niveis_ganhos > 0:

                    print(
                        f"Subiu para o nivel {self.jogador.nivel}!"
                    )

                    self.verificar_desbloqueios()

    def verificar_desbloqueios(self):

        # Desbloqueia as esferas orbitais no nivel 2
        if self.jogador.nivel >= 2:

            possui_esferas = False

            for arma in self.armas:

                if isinstance(arma, EsferasOrbitais):
                    possui_esferas = True
                    break

            if not possui_esferas:

                self.armas.append(EsferasOrbitais())

                print("Nova arma desbloqueada: Esferas Orbitais!")

    def atualizar_projeteis(self, dt):

        projeteis_ativos = []
        inimigos_derrotados = []

        for projetil in self.projeteis:

            projetil.atualizar(dt)

            # Remove projeteis que acabaram seu tempo de vida
            if not projetil.esta_vivo():
                continue

            acertou = False

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
                    acertou = True

                    if inimigo.vida <= 0:
                        inimigos_derrotados.append(inimigo)

                    break

            # Mantem apenas projeteis que nao acertaram
            if not acertou:
                projeteis_ativos.append(projetil)

        self.projeteis = projeteis_ativos

        self.remover_inimigos_derrotados(
            inimigos_derrotados
        )

    def atualizar_armas(self, dt):

        inimigos_derrotados = []

        for arma in self.armas:

            derrotados = arma.atualizar(
                self.jogador,
                self.inimigos,
                dt
            )

            inimigos_derrotados.extend(derrotados)

        self.remover_inimigos_derrotados(
            inimigos_derrotados
        )

    def atualizar(self, dt):

        # Ataque automatico
        self.atacar()

        # Atualiza projeteis
        self.atualizar_projeteis(dt)

        # Atualiza armas adicionais
        self.atualizar_armas(dt)
