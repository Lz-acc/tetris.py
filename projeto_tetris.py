import pygame
import random
import sys

pygame.init()

LARGURA, ALTURA = 500, 600
TAMANHO_BLOCO = 30
COLUNAS = 10
LINHAS = 20
MARGEM_ESQUERDA = 200

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Tetris OG")

FONTE = pygame.font.Font("PressStart2P.ttf", 16)
FONTE_GRANDE = pygame.font.Font("PressStart2P.ttf", 28)
FONTE_TITULO = pygame.font.Font("PressStart2P.ttf", 28)

CORES = [
    (0, 255, 255), (255, 255, 0), (128, 0, 128),
    (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0)
]

FORMAS = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]]
]

class Peca:
    def __init__(self, x, y, forma):
        self.x = x
        self.y = y
        self.forma = forma
        self.cor = CORES[FORMAS.index(forma)]

    def rotacionar(self):
        self.forma = [list(row) for row in zip(*self.forma[::-1])]

def criar_grade(tetos):
    return [[tetos.get((x, y), (0, 0, 0)) for x in range(COLUNAS)] for y in range(LINHAS)]

def pos_valida(peca, grade):
    for y, linha in enumerate(peca.forma):
        for x, bloco in enumerate(linha):
            if bloco:
                nx, ny = peca.x + x, peca.y + y
                if nx < 0 or nx >= COLUNAS or ny >= LINHAS or grade[ny][nx] != (0, 0, 0):
                    return False
    return True

def fixar_peca(peca, tetos):
    for y, linha in enumerate(peca.forma):
        for x, bloco in enumerate(linha):
            if bloco:
                tetos[(peca.x + x, peca.y + y)] = peca.cor

def limpar_linhas(tetos):
    linhas = []
    for y in range(LINHAS):
        if all((x, y) in tetos for x in range(COLUNAS)):
            linhas.append(y)
    for y in linhas:
        for x in range(COLUNAS):
            if (x, y) in tetos:
                del tetos[(x, y)]
        for x, y2 in sorted(tetos.copy(), key=lambda a: -a[1]):
            if y2 < y:
                tetos[(x, y2 + 1)] = tetos.pop((x, y2))
    return len(linhas) * 100

def desenhar_grid(grade):
    for y in range(LINHAS):
        for x in range(COLUNAS):
            pygame.draw.rect(TELA, grade[y][x], (MARGEM_ESQUERDA + x*TAMANHO_BLOCO, y*TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO))
            pygame.draw.rect(TELA, (40, 40, 40), (MARGEM_ESQUERDA + x*TAMANHO_BLOCO, y*TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO), 1)

def desenhar_lateral(pontos, proxima):
    pygame.draw.rect(TELA, (20, 20, 20), (0, 0, MARGEM_ESQUERDA, ALTURA))
    titulo = FONTE_TITULO.render("TETRIS", True, (255, 100, 100))
    TELA.blit(titulo, (20, 20))
    score = FONTE.render(f"Score: {pontos}", True, (255, 255, 255))
    TELA.blit(score, (20, 80))

    # Botão Pause
    pygame.draw.rect(TELA, (100, 100, 255), (20, 140, 120, 40))
    pause_text = FONTE.render("Pause", True, (0, 0, 0))
    pause_x = 20 + (120 - pause_text.get_width()) // 2
    pause_y = 140 + (40 - pause_text.get_height()) // 2
    TELA.blit(pause_text, (pause_x, pause_y))

    # Botão Fechar
    pygame.draw.rect(TELA, (255, 100, 100), (20, 200, 120, 40))
    fechar_text = FONTE.render("Fechar", True, (0, 0, 0))
    fechar_x = 20 + (120 - fechar_text.get_width()) // 2
    fechar_y = 200 + (40 - fechar_text.get_height()) // 2
    TELA.blit(fechar_text, (fechar_x, fechar_y))

    if proxima:
        TELA.blit(FONTE.render("Próxima:", True, (255, 255, 255)), (20, 280))
        for y, linha in enumerate(proxima.forma):
            for x, bloco in enumerate(linha):
                if bloco:
                    pygame.draw.rect(TELA, proxima.cor, (20 + x*TAMANHO_BLOCO, 320 + y*TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO))

def tela_final(texto, mostrar_creditos=False):
    TELA.fill((0, 0, 0))
    msg = FONTE_GRANDE.render(texto, True, (255, 0, 0))
    retry = FONTE.render("Clique para jogar novamente", True, (255, 255, 255))
    creditos = FONTE.render("Créditos", True, (100, 200, 255))
    TELA.blit(msg, (LARGURA//2 - msg.get_width()//2, ALTURA//2 - 80))
    TELA.blit(retry, (LARGURA//2 - retry.get_width()//2, ALTURA//2))
    TELA.blit(creditos, (LARGURA//2 - creditos.get_width()//2, ALTURA//2 + 40))
    pygame.display.update()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                x, y = e.pos
                if ALTURA//2 + 40 <= y <= ALTURA//2 + 60:
                    mostrar_creditos = True
                else:
                    return mostrar_creditos
        if mostrar_creditos:
            TELA.fill((0, 0, 0))
            nomes = ["Lorenzo Accasto", "Eduardo Augusto", "Luan Pereira", "Pedro Lucas"]
            for i, nome in enumerate(nomes):
                TELA.blit(FONTE.render(nome, True, (255, 255, 255)), (LARGURA//2 - 100, 150 + i*30))
            voltar = FONTE.render("Clique para voltar", True, (255, 255, 255))
            TELA.blit(voltar, (LARGURA//2 - voltar.get_width()//2, 300))
            pygame.display.update()
            for evento in pygame.event.get():
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    return False

def mostrar_pausa():
    s = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    s.fill((0, 0, 0, 180))  # Preto com transparência
    TELA.blit(s, (0, 0))
    texto = FONTE_GRANDE.render("PAUSED", True, (255, 255, 255))
    TELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2 - texto.get_height() // 2))
    pygame.display.update()

def jogo():
    relogio = pygame.time.Clock()
    tetos = {}
    peca = Peca(COLUNAS // 2 - 2, 0, random.choice(FORMAS))
    proxima = Peca(0, 0, random.choice(FORMAS))
    pontos = 0
    tempo_queda = 0
    delay_lado = 0
    velocidade_base = 500
    queda_manual = False
    pausado = False

    while True:
        grade = criar_grade(tetos)
        tempo_queda += relogio.get_rawtime()
        relogio.tick()

        velocidade = max(velocidade_base - pontos // 5, 100)
        mouse = pygame.mouse.get_pressed()
        pos_mouse = pygame.mouse.get_pos()
        delay_lado += 1

        if not pausado and tempo_queda > (50 if queda_manual else velocidade):
            peca.y += 1
            if not pos_valida(peca, grade):
                peca.y -= 1
                fixar_peca(peca, tetos)
                pontos += limpar_linhas(tetos)
                if pontos >= 9999:
                    if tela_final("YOU WIN!"):
                        tela_final("Créditos")
                    return jogo()
                peca = proxima
                proxima = Peca(COLUNAS // 2 - 2, 0, random.choice(FORMAS))
                if not pos_valida(peca, grade):
                    if tela_final("GAME OVER"):
                        tela_final("Créditos")
                    return jogo()
            tempo_queda = 0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    peca.rotacionar()
                    if not pos_valida(peca, grade):
                        for _ in range(3): peca.rotacionar()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if 20 <= pos_mouse[0] <= 140 and 140 <= pos_mouse[1] <= 180:
                    pausado = not pausado
                elif 20 <= pos_mouse[0] <= 140 and 200 <= pos_mouse[1] <= 240:
                    pygame.quit()
                    sys.exit()

        if not pausado:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and delay_lado > 80:
                peca.x -= 1
                if not pos_valida(peca, grade): peca.x += 1
                delay_lado = 0
            elif keys[pygame.K_RIGHT] and delay_lado > 80:
                peca.x += 1
                if not pos_valida(peca, grade): peca.x -= 1
                delay_lado = 0
            queda_manual = keys[pygame.K_DOWN] or keys[pygame.K_SPACE]

        TELA.fill((0, 0, 0))
        desenhar_grid(grade)
        desenhar_lateral(pontos, proxima)
        for y, linha in enumerate(peca.forma):
            for x, bloco in enumerate(linha):
                if bloco:
                    pygame.draw.rect(TELA, peca.cor, (MARGEM_ESQUERDA + (peca.x + x)*TAMANHO_BLOCO, (peca.y + y)*TAMANHO_BLOCO, TAMANHO_BLOCO, TAMANHO_BLOCO))
        if pausado:
            mostrar_pausa()
        else:
            pygame.display.update()

jogo()