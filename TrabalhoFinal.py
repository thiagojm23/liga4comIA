import random


class TrabalhoFinal:
    def __init__(self):
        self.reiniciar = True
        while self.reiniciar:
            tabuleiro = [[" " for _ in range(7)] for _ in range(6)]
            self.criar_tabuleiro(tabuleiro)
            jogador1 = True
            vitoria = False
            corJogador = self.escolha()
            while not vitoria:
                self.exibir_tabuleiro(tabuleiro)
                if jogador1:
                    coluna = int(input("Jogador, faça sua jogada (coluna de 1 a 7): "))
                    while (
                        coluna < 1
                        or coluna > 7
                        or not self.coluna_valida(tabuleiro, coluna - 1)
                    ):
                        coluna = int(
                            input(
                                "Coluna inválida. Digite apenas entre 1 e 7 ou verifique se a coluna está cheia: "
                            )
                        )
                    self.realizar_jogada(tabuleiro, coluna, corJogador)
                else:
                    print("Computador está fazendo sua jogada...")
                    coluna = self.obter_jogada_computador(tabuleiro, corJogador)
                    self.realizar_jogada_pc(
                        tabuleiro, coluna, "V" if corJogador == "A" else "A"
                    )

                vitoria = self.verificar_vitoria(tabuleiro)

                if vitoria:
                    self.exibir_tabuleiro(tabuleiro)
                    if jogador1:
                        print("Você venceu!")
                    else:
                        print("O computador venceu!")
                elif self.tabuleiro_completo(tabuleiro):
                    self.exibir_tabuleiro(tabuleiro)
                    print("Empate!")
                    break

                jogador1 = not jogador1

            self.reiniciar = self.reiniciar_jogo()

    def escolha(self):
        print("Escolha entre a cor vermelho (V) ou azul (A)")
        while True:
            escolha = input().strip().upper()
            if escolha in ("V", "A"):
                return escolha
            print("Escolha inválida, digite novamente")

    def reiniciar_jogo(self):
        resposta = input("Deseja jogar novamente? Digite sim ou nao: ").strip().lower()
        while resposta not in ("sim", "nao"):
            resposta = input("Resposta inválida, digite novamente: ").strip().lower()
        return resposta == "sim"

    def criar_tabuleiro(self, tabuleiro):
        for i in range(len(tabuleiro)):
            for j in range(len(tabuleiro[i])):
                tabuleiro[i][j] = " "

    def exibir_tabuleiro(self, tabuleiro):
        print("    1   2   3   4   5   6   7")
        for i in range(len(tabuleiro)):
            print(f"{i+1} |", end="")
            for j in range(len(tabuleiro[i])):
                print(f" {tabuleiro[i][j]} |", end="")
            print()
        print("-----------------------------")

    def realizar_jogada(self, tabuleiro, coluna, cor):
        coluna -= 1
        for i in range(len(tabuleiro) - 1, -1, -1):
            if self.coluna_valida(tabuleiro, coluna) and tabuleiro[i][coluna] == " ":
                tabuleiro[i][coluna] = cor
                break

    def avaliar_estado(self, tabuleiro, cor_computador, maximizandoEhJogadorAtual):
        """Avalia o estado atual do tabuleiro"""
        pontuacao = 0

        # Verificar vitória
        if self.verificar_vitoria(tabuleiro):
            return 10000 if not maximizandoEhJogadorAtual else -10000

        # Verificar empate
        if self.tabuleiro_completo(tabuleiro):
            return 0

        # Avaliar sequências de 3
        for i in range(6):
            for j in range(4):
                # Horizontal
                if (
                    tabuleiro[i][j] != " "
                    and tabuleiro[i][j] == tabuleiro[i][j + 1] == tabuleiro[i][j + 2]
                ):
                    pontuacao += 15 if tabuleiro[i][j] == cor_computador else -20

        for i in range(3):
            for j in range(7):
                # Vertical
                if (
                    tabuleiro[i][j] != " "
                    and tabuleiro[i][j] == tabuleiro[i + 1][j] == tabuleiro[i + 2][j]
                ):
                    pontuacao += 15 if tabuleiro[i][j] == cor_computador else -20

        # Avaliar posições centrais
        colunaCentral = 3
        for j in range(6):
            if tabuleiro[j][colunaCentral] == cor_computador:
                pontuacao += 25
            elif tabuleiro[j][colunaCentral] != " ":
                pontuacao -= 25

        return pontuacao

    def minimaxPoda(
        self, tabuleiro, profundidade, alpha, beta, maximizando, cor_computador
    ):
        """Implementação do algoritmo minimax com poda alpha-beta"""
        jogadas_validas = [
            col for col in range(7) if self.coluna_valida(tabuleiro, col)
        ]

        if (
            profundidade == 0
            or self.verificar_vitoria(tabuleiro)
            or self.tabuleiro_completo(tabuleiro)
        ):
            return None, self.avaliar_estado(tabuleiro, cor_computador, maximizando)

        if maximizando:
            valor = float("-inf")
            coluna = random.choice(jogadas_validas)

            for col in jogadas_validas:
                # Criar cópia do tabuleiro
                tabuleiro_temp = [linha[:] for linha in tabuleiro]
                # Fazer jogada
                for i in range(5, -1, -1):
                    if tabuleiro_temp[i][col] == " ":
                        tabuleiro_temp[i][col] = cor_computador
                        break

                novo_valor = self.minimaxPoda(
                    tabuleiro_temp, profundidade - 1, alpha, beta, False, cor_computador
                )[1]

                if novo_valor > valor:
                    valor = novo_valor
                    coluna = col
                alpha = max(alpha, valor)
                if alpha >= beta:
                    break
            return coluna, valor

        else:
            valor = float("inf")
            coluna = random.choice(jogadas_validas)

            for col in jogadas_validas:
                # Criar cópia do tabuleiro
                tabuleiro_temp = [linha[:] for linha in tabuleiro]
                # Fazer jogada
                for i in range(5, -1, -1):
                    if tabuleiro_temp[i][col] == " ":
                        tabuleiro_temp[i][col] = "V" if cor_computador == "A" else "A"
                        break

                novo_valor = self.minimaxPoda(
                    tabuleiro_temp, profundidade - 1, alpha, beta, True, cor_computador
                )[1]

                if novo_valor < valor:
                    valor = novo_valor
                    coluna = col
                beta = min(beta, valor)
                if alpha >= beta:
                    break
            return coluna, valor

    def obter_jogada_computador(self, tabuleiro, corJogador):
        """Obtém a melhor jogada para o computador usando minimax"""
        cor_computador = "V" if corJogador == "A" else "A"  # Cor do computador
        coluna, _ = self.minimaxPoda(
            tabuleiro, 7, float("-inf"), float("inf"), True, cor_computador
        )
        return coluna

    def realizar_jogada_pc(self, tabuleiro, coluna, cor):
        """Realiza a jogada do computador"""
        for i in range(len(tabuleiro) - 1, -1, -1):
            if self.coluna_valida(tabuleiro, coluna) and tabuleiro[i][coluna] == " ":
                tabuleiro[i][coluna] = cor
                break

    def verificar_vitoria(self, tabuleiro):
        # Horizontal
        for i in range(6):
            for j in range(4):
                p = tabuleiro[i][j]
                if (
                    p != " "
                    and p
                    == tabuleiro[i][j + 1]
                    == tabuleiro[i][j + 2]
                    == tabuleiro[i][j + 3]
                ):
                    return True
        # Vertical
        for i in range(3):
            for j in range(7):
                p = tabuleiro[i][j]
                if (
                    p != " "
                    and p
                    == tabuleiro[i + 1][j]
                    == tabuleiro[i + 2][j]
                    == tabuleiro[i + 3][j]
                ):
                    return True
        # Diagonal (esquerda para cima)
        for i in range(3, 6):
            for j in range(4):
                p = tabuleiro[i][j]
                if (
                    p != " "
                    and p
                    == tabuleiro[i - 1][j + 1]
                    == tabuleiro[i - 2][j + 2]
                    == tabuleiro[i - 3][j + 3]
                ):
                    return True
        # Diagonal (direita para cima)
        for i in range(3, 6):
            for j in range(3, 7):
                p = tabuleiro[i][j]
                if (
                    p != " "
                    and p
                    == tabuleiro[i - 1][j - 1]
                    == tabuleiro[i - 2][j - 2]
                    == tabuleiro[i - 3][j - 3]
                ):
                    return True
        return False

    def tabuleiro_completo(self, tabuleiro):
        for linha in tabuleiro:
            if " " in linha:
                return False
        return True

    def coluna_valida(self, tabuleiro, coluna):
        return tabuleiro[0][coluna] == " "


if __name__ == "__main__":
    TrabalhoFinal()
