# Liga 4 - Implementação com Busca Competitiva

Este projeto implementa o jogo Liga 4 (Connect Four) usando algoritmos de busca competitiva em Python.

## Descrição do Jogo

O Liga 4 é um jogo de tabuleiro para dois jogadores onde o objetivo é alinhar quatro peças da mesma cor em uma linha horizontal, vertical ou diagonal. O tabuleiro possui 6 linhas e 7 colunas, e as peças são inseridas de cima para baixo, ocupando o espaço mais baixo disponível na coluna escolhida.

### Estado Inicial

- Tabuleiro vazio de 6x7
- Jogador atual (Vermelho ou Azul)
- Todas as posições marcadas como 'B' (branco/vazio)

### Estado Objetivo

- Um jogador consegue alinhar 4 peças da mesma cor em qualquer direção
- O tabuleiro fica completamente preenchido (empate)

### Função Sucessor

- Para cada coluna válida (não completamente preenchida), é possível fazer uma jogada
- Uma jogada válida coloca uma peça na posição mais baixa disponível da coluna escolhida

### Custo de Caminho

- Cada jogada tem custo unitário
- O jogo termina quando um jogador vence ou ocorre empate

## Algoritmo Escolhido

Foi implementado o algoritmo Minimax com podoa Alpha-Beta para a tomada de decisão do computador. Este algoritmo foi escolhido porque:

1. O jogo é determinístico - cada jogada tem um resultado previsível
2. É um jogo de soma zero - o ganho de um jogador é a perda do outro
3. Possui um número finito de estados possíveis
4. Permite avaliar estados intermediários através de uma função heurística

### Características da Implementação

- Profundidade de busca configurável (padrão: 4)
- Função heurística que avalia:
  - Sequências de 3 peças
  - Posições centrais do tabuleiro
  - Possibilidade de vitória imediata
- Poda Alpha-Beta para otimização da busca

## Como Executar

1. Certifique-se de ter Python 3.x instalado
2. Instale as dependências:
   ```
   pip install numpy
   ```
3. Execute o jogo:
   ```
   python liga4.py
   ```

## Como Jogar

1. O jogador humano é representado pela cor Vermelha (V)
2. O computador é representado pela cor Azul (A)
3. Em cada turno, escolha uma coluna (0-6) para fazer sua jogada
4. O primeiro a alinhar 4 peças da mesma cor vence
5. Se o tabuleiro ficar cheio sem um vencedor, o jogo termina em empate
