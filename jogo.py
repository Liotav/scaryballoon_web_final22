
import pygame
import sys
import random
import time
import os

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Scary Balloon")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
TEXT_COLOR = (0, 255, 0)

font = pygame.font.SysFont("couriernew", 28, bold=True)
big_font = pygame.font.SysFont("couriernew", 40, bold=True)
small_font = pygame.font.SysFont("couriernew", 20, bold=True)

img_balao = pygame.image.load("imagens/balao.png")
img_balao = pygame.transform.scale(img_balao, (80, 120))
img_balao_start = pygame.transform.scale(img_balao, (50, 75))
img_balao_restart = pygame.transform.scale(img_balao, (90, 135))

img_susto = pygame.image.load("imagens/susto.png")
img_susto = pygame.transform.scale(img_susto, (800, 600))

logo_img = pygame.image.load("logo.png")
logo_img = pygame.transform.scale(logo_img, (140, 50))

pygame.mixer.init()
susto_som = pygame.mixer.Sound("sons/susto.mp3")

stage = 1
max_stage = 9
baloes = []
largura, altura = 80, 120
inicio_jogo = 0
susto_ativo = False
susto_inicio = None
jogo_ativo = False
venceu = False
nome_jogador = ""
digitando_nome = False
exibir_creditos = False
tela_inicio = True
tempo_final = 0
efeito_balanço = False
stage_real = 1
balao_restart_rect = None
som_tocado = False

def gerar_baloes():
    global baloes
    baloes = []
    posicoes_usadas = []
    while len(baloes) < 10:
        x = random.randint(50, 700)
        y = random.randint(50, 450)
        pos = pygame.Rect(x, y, largura, altura)
        if not any(pos.colliderect(p) for p in posicoes_usadas):
            posicoes_usadas.append(pos)
            baloes.append({'rect': pos, 'susto': False})
    sustos = random.sample(baloes, stage)
    for b in sustos:
        b['susto'] = True

def mostrar_texto(texto, y, centro=True, fonte=font, cor=TEXT_COLOR):
    img = fonte.render(texto, True, cor)
    rect = img.get_rect(center=(400, y)) if centro else (20, y)
    screen.blit(img, rect)

def salvar_recorde(nome, stage, tempo):
    with open("recordes.txt", "a") as f:
        f.write(f"{nome} – Stage {stage} – {tempo:.2f}s\n")

clock = pygame.time.Clock()
running = True
gerar_baloes()

input_box = pygame.Rect(250, 300, 300, 50)
input_color = RED

while running:
    screen.fill(BLACK)
    mouse_pos = pygame.mouse.get_pos()

    if tela_inicio:
        mostrar_texto("Welcome to SCARY BALLOON", 80, fonte=big_font)
        mostrar_texto("Rules:", 130)
        mostrar_texto("- There are 10 balloons per round", 170)
        mostrar_texto("- Click the right balloon to advance", 200)
        mostrar_texto("- If you click a scary one,", 230)
        mostrar_texto("  you're back to Stage 1!", 260)
        mostrar_texto("- Beat Stage 9 to win!", 290)
        mostrar_texto("Click the balloon to start", 350)
        balao_start_rect = screen.blit(img_balao_start, (375, 370))
        screen.blit(logo_img, (630, 545))

    elif digitando_nome:
        mostrar_texto("Enter your name to start", 180, fonte=big_font)
        pygame.draw.rect(screen, input_color, input_box, 2)
        nome_img = font.render(nome_jogador, True, WHITE)
        screen.blit(nome_img, (input_box.x + 10, input_box.y + 10))
        mostrar_texto("Press Enter to start the game", 400, fonte=small_font)
        screen.blit(logo_img, (630, 545))

    elif exibir_creditos:
        mostrar_texto("CREDITS", 100, fonte=big_font)
        mostrar_texto(f"Player: {nome_jogador}", 180)
        mostrar_texto(f"Stage reached: {stage_real}", 230)
        mostrar_texto(f"Time: {tempo_final:.2f} seconds", 280)
        mostrar_texto("Click the balloon and try again.", 400)
        balao_restart_rect = screen.blit(img_balao_restart, (355, 430))
        screen.blit(logo_img, (630, 545))

    elif susto_ativo:
        if not som_tocado:
            susto_som.play()
            som_tocado = True
        offset_x = random.randint(-10, 10)
        offset_y = random.randint(-10, 10)
        screen.blit(img_susto, (offset_x, offset_y))
        if time.time() - susto_inicio >= 1.2:
            tempo_final = time.time() - inicio_jogo
            salvar_recorde(nome_jogador, stage_real, tempo_final)
            jogo_ativo = False
            susto_ativo = False
            som_tocado = False
            exibir_creditos = True

    elif venceu:
        tempo_final = time.time() - inicio_jogo
        mostrar_texto("YOU WIN!", 150, fonte=big_font)
        mostrar_texto(f"Time: {tempo_final:.2f} seconds", 210)
        mostrar_texto("Press any key to view credits", 280)
        screen.blit(logo_img, (630, 545))

    else:
        mostrar_texto(f"Stage {stage}", 40)
        for b in baloes:
            screen.blit(img_balao, (b['rect'].x, b['rect'].y))
        screen.blit(logo_img, (630, 545))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if tela_inicio and event.type == pygame.MOUSEBUTTONDOWN:
            if balao_start_rect.collidepoint(event.pos):
                tela_inicio = False
                digitando_nome = True

        elif digitando_nome:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nome_jogador.strip() != "":
                    digitando_nome = False
                    jogo_ativo = True
                    inicio_jogo = time.time()
                    stage = 1
                    gerar_baloes()
                elif event.key == pygame.K_BACKSPACE:
                    nome_jogador = nome_jogador[:-1]
                else:
                    if len(nome_jogador) < 10:
                        nome_jogador += event.unicode

        elif jogo_ativo and not susto_ativo:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for b in baloes:
                    if b['rect'].collidepoint(event.pos):
                        if b['susto']:
                            stage_real = stage
                            susto_ativo = True
                            susto_inicio = time.time()
                        else:
                            if stage < max_stage:
                                stage += 1
                                gerar_baloes()
                            else:
                                venceu = True
                                stage_real = stage
                                tempo_final = time.time() - inicio_jogo
                                salvar_recorde(nome_jogador, stage_real, tempo_final)

        elif venceu and event.type == pygame.KEYDOWN:
            venceu = False
            exibir_creditos = True

        elif exibir_creditos and event.type == pygame.MOUSEBUTTONDOWN:
            if balao_restart_rect and balao_restart_rect.collidepoint(event.pos):
                nome_jogador = ""
                digitando_nome = False
                tela_inicio = True
                stage = 1
                venceu = False
                exibir_creditos = False
                gerar_baloes()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
