import numpy as np
import random
from typing import List, Tuple, Optional

class Liga4:
    def __init__(self, linhas: int = 6, colunas: int = 7):
        self.linhas = linhas
        self.colunas = colunas
        self.tabuleiro = np.full((linhas, colunas), 'B')
        self.jogador_atual = 'V'  # V para vermelho, A para azul
        
    def reset(self):
        """Reinicia o tabuleiro"""
        self.tabuleiro = np.full((self.linhas, self.colunas), 'B')
        self.jogador_atual = 'V'
        
    def jogadas_validas(self) -> List[int]:
        """Retorna lista de colunas válidas para jogada"""
        return [col for col in range(self.colunas) if self.tabuleiro[0][col] == 'B']
    
    def fazer_jogada(self, coluna: int) -> bool:
        """Realiza uma jogada na coluna especificada"""
        if coluna not in self.jogadas_validas():
            return False
            
        for linha in range(self.linhas-1, -1, -1):
            if self.tabuleiro[linha][coluna] == 'B':
                self.tabuleiro[linha][coluna] = self.jogador_atual
                self.jogador_atual = 'A' if self.jogador_atual == 'V' else 'V'
                return True
        return False
    
    def verificar_vitoria(self) -> Optional[str]:
        """Verifica se há um vencedor"""
        # Verificar horizontalmente
        for i in range(self.linhas):
            for j in range(self.colunas-3):
                if self.tabuleiro[i][j] != 'B' and \
                   self.tabuleiro[i][j] == self.tabuleiro[i][j+1] == \
                   self.tabuleiro[i][j+2] == self.tabuleiro[i][j+3]:
                    return self.tabuleiro[i][j]
        
        # Verificar verticalmente
        for i in range(self.linhas-3):
            for j in range(self.colunas):
                if self.tabuleiro[i][j] != 'B' and \
                   self.tabuleiro[i][j] == self.tabuleiro[i+1][j] == \
                   self.tabuleiro[i+2][j] == self.tabuleiro[i+3][j]:
                    return self.tabuleiro[i][j]
        
        # Verificar diagonalmente (esquerda para direita)
        for i in range(self.linhas-3):
            for j in range(self.colunas-3):
                if self.tabuleiro[i][j] != 'B' and \
                   self.tabuleiro[i][j] == self.tabuleiro[i+1][j+1] == \
                   self.tabuleiro[i+2][j+2] == self.tabuleiro[i+3][j+3]:
                    return self.tabuleiro[i][j]
        
        # Verificar diagonalmente (direita para esquerda)
        for i in range(self.linhas-3):
            for j in range(3, self.colunas):
                if self.tabuleiro[i][j] != 'B' and \
                   self.tabuleiro[i][j] == self.tabuleiro[i+1][j-1] == \
                   self.tabuleiro[i+2][j-2] == self.tabuleiro[i+3][j-3]:
                    return self.tabuleiro[i][j]
        
        return None
    
    def tabuleiro_cheio(self) -> bool:
        """Verifica se o tabuleiro está cheio"""
        return 'B' not in self.tabuleiro[0]
    
    def avaliar_estado(self) -> int:
        """Avalia o estado atual do tabuleiro para o algoritmo minimax"""
        vencedor = self.verificar_vitoria()
        if vencedor == 'V':
            return 100
        elif vencedor == 'A':
            return -100
        elif self.tabuleiro_cheio():
            return 0
            
        # Avaliação heurística
        pontuacao = 0
        # Verificar sequências de 3
        for i in range(self.linhas):
            for j in range(self.colunas-2):
                if self.tabuleiro[i][j] != 'B' and \
                   self.tabuleiro[i][j] == self.tabuleiro[i][j+1] == self.tabuleiro[i][j+2]:
                    pontuacao += 5 if self.tabuleiro[i][j] == 'V' else -5
                    
        return pontuacao
    
    def minimax(self, profundidade: int, alpha: float, beta: float, maximizando: bool) -> Tuple[int, Optional[int]]:
        """Implementação do algoritmo minimax com poda alpha-beta"""
        jogadas_validas = self.jogadas_validas()
        vencedor = self.verificar_vitoria()
        
        if profundidade == 0 or vencedor is not None or self.tabuleiro_cheio():
            if vencedor == 'V':
                return 100, None
            elif vencedor == 'A':
                return -100, None
            elif self.tabuleiro_cheio():
                return 0, None
            return self.avaliar_estado(), None
            
        if maximizando:
            valor = float('-inf')
            coluna = random.choice(jogadas_validas)
            for col in jogadas_validas:
                # Salva o estado atual
                estado_anterior = self.tabuleiro.copy()
                jogador_anterior = self.jogador_atual
                
                # Faz a jogada
                self.fazer_jogada(col)
                novo_valor = self.minimax(profundidade-1, alpha, beta, False)[0]
                
                # Restaura o estado
                self.tabuleiro = estado_anterior
                self.jogador_atual = jogador_anterior
                
                if novo_valor > valor:
                    valor = novo_valor
                    coluna = col
                alpha = max(alpha, valor)
                if alpha >= beta:
                    break
            return valor, coluna
        else:
            valor = float('inf')
            coluna = random.choice(jogadas_validas)
            for col in jogadas_validas:
                # Salva o estado atual
                estado_anterior = self.tabuleiro.copy()
                jogador_anterior = self.jogador_atual
                
                # Faz a jogada
                self.fazer_jogada(col)
                novo_valor = self.minimax(profundidade-1, alpha, beta, True)[0]
                
                # Restaura o estado
                self.tabuleiro = estado_anterior
                self.jogador_atual = jogador_anterior
                
                if novo_valor < valor:
                    valor = novo_valor
                    coluna = col
                beta = min(beta, valor)
                if alpha >= beta:
                    break
            return valor, coluna
    
    def jogada_computador(self, profundidade: int = 4) -> int:
        """Realiza a jogada do computador usando minimax"""
        _, coluna = self.minimax(profundidade, float('-inf'), float('inf'), True)
        return coluna
    
    def exibir_tabuleiro(self):
        """Exibe o tabuleiro atual"""
        print("\n  0 1 2 3 4 5 6")
        for i in range(self.linhas):
            print(f"{i} {' '.join(self.tabuleiro[i])}")
        print()

def main():
    jogo = Liga4()
    print("Bem-vindo ao Liga 4!")
    print("Você será o jogador Vermelho (V)")
    print("O computador será o jogador Azul (A)")
    
    while True:
        jogo.exibir_tabuleiro()
        
        # Jogada do humano
        while True:
            try:
                coluna = int(input("Sua vez! Escolha uma coluna (0-6): "))
                if 0 <= coluna <= 6 and jogo.fazer_jogada(coluna):
                    break
                print("Jogada inválida! Tente novamente.")
            except ValueError:
                print("Por favor, digite um número entre 0 e 6.")
        
        # Verificar vitória do humano
        if jogo.verificar_vitoria() == 'V':
            jogo.exibir_tabuleiro()
            print("Você venceu!")
            break
            
        # Jogada do computador
        print("\nVez do computador...")
        coluna = jogo.jogada_computador()
        jogo.fazer_jogada(coluna)
        
        # Verificar vitória do computador
        if jogo.verificar_vitoria() == 'A':
            jogo.exibir_tabuleiro()
            print("O computador venceu!")
            break
            
        # Verificar empate
        if jogo.tabuleiro_cheio():
            jogo.exibir_tabuleiro()
            print("Empate!")
            break

if __name__ == "__main__":
    main() 