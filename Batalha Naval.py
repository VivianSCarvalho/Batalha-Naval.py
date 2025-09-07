from tkinter import *
from PIL import Image, ImageTk
import random

TAMANHO_TABULEIRO = 5
NUM_NAVIOS = 3
BOMBAS = 2
ACERTOS = 0

#Função para criar o tabuleiro vazio
def criar_tabuleiro():
    return [['~' for _ in range(TAMANHO_TABULEIRO)] for _ in range(TAMANHO_TABULEIRO)]

#Função para colocar navios no tabuleiro
def colocar_navios(tabuleiro):
    navios_colocados = 0
    while navios_colocados < NUM_NAVIOS:
        linha = random.randint(0, TAMANHO_TABULEIRO - 1)
        coluna = random.randint(0, TAMANHO_TABULEIRO - 1)
        if tabuleiro[linha][coluna] != 'X':
            tabuleiro[linha][coluna] = 'X'
            navios_colocados += 1

#Funções de ação para os botões
def acao_botao():
    global ACERTOS
    linha = entry_linha.get()
    coluna = entry_coluna.get()

    if not linha.isdigit() or not coluna.isdigit():
        resultado_label.config(text="Coordenadas inválidas. Use números inteiros!")
        return

    linha, coluna = int(linha), int(coluna)

    if 0 <= linha < TAMANHO_TABULEIRO and 0 <= coluna < TAMANHO_TABULEIRO:
        if tabuleiro_jogador[linha][coluna] != '~':
            resultado_label.config(text="Você já atacou ai paceiro.")
            return

        if tabuleiro_oponente[linha][coluna] == 'X':
            tabuleiro_jogador[linha][coluna] = 'X'
            resultado_label.config(text="Você acertou! Estouro demais!")
            ACERTOS += 1
        else:
            tabuleiro_jogador[linha][coluna] = 'O'
            resultado_label.config(text="Você errou kkkkkkkkk, é agua!")

        mostrar_tabuleiro()

        if ACERTOS == NUM_NAVIOS:
            mostrar_parabens()
    else:
        resultado_label.config(text="Coordenadas fora do tabuleiro. Tente novamente!")

def usar_bomba_linha():
    global BOMBAS, ACERTOS

    if BOMBAS <= 0:
        resultado_label.config(text="vish, acabou as bombas vei, calma lá Bin Laden!")
        return

    linha = entry_linha.get()

    if not linha.isdigit():
        resultado_label.config(text="Linha inválida. Use números inteiros!")
        return

    linha = int(linha)
    if not (0 <= linha < TAMANHO_TABULEIRO):
        resultado_label.config(text="Linha fora do tabuleiro. Tente novamente!")
        return

    BOMBAS -= 1
    bomba_label.config(text=f"Bombas restantes: {BOMBAS}")

    for coluna in range(TAMANHO_TABULEIRO):
        if tabuleiro_jogador[linha][coluna] == '~':  # Evitar atacar a mesma célula
            if tabuleiro_oponente[linha][coluna] == 'X':
                tabuleiro_jogador[linha][coluna] = 'X'
                ACERTOS += 1
            else:
                tabuleiro_jogador[linha][coluna] = 'O'

    mostrar_tabuleiro()

    if ACERTOS == NUM_NAVIOS:
        mostrar_parabens()
    else:
        resultado_label.config(text=f"Bomba na linha {linha} usada com sucesso!")


def usar_bomba_coluna():
    global BOMBAS, ACERTOS

    if BOMBAS <= 0:
        resultado_label.config(text="vish, acabou as bombas vei, calma lá Bin Laden!")
        return

    coluna = entry_coluna.get()

    if not coluna.isdigit():
        resultado_label.config(text="Coluna inválida. Use números!")
        return

    coluna = int(coluna)
    if not (0 <= coluna < TAMANHO_TABULEIRO):
        resultado_label.config(text="Coluna fora do tabuleiro. Tente novamente!")
        return

    BOMBAS -= 1
    bomba_label.config(text=f"Bombas restantes: {BOMBAS}")

    for linha in range(TAMANHO_TABULEIRO):
        if tabuleiro_jogador[linha][coluna] == '~':  # Evitar atacar a mesma célula
            if tabuleiro_oponente[linha][coluna] == 'X':
                tabuleiro_jogador[linha][coluna] = 'X'
                ACERTOS += 1
            else:
                tabuleiro_jogador[linha][coluna] = 'O'

    mostrar_tabuleiro()

    if ACERTOS == NUM_NAVIOS:
        mostrar_parabens()
    else:
        resultado_label.config(text=f"Bomba na coluna {coluna} usada com sucesso!")


def mostrar_tabuleiro():
    for i in range(TAMANHO_TABULEIRO):
        for j in range(TAMANHO_TABULEIRO):
            grid_labels[i][j].config(text=tabuleiro_jogador[i][j])

def mostrar_parabens():
    parabens_janela = Toplevel()
    parabens_janela.title("PARABÉNS!!!")
    parabens_janela.configure(bg="black")

    msg_label = Label(parabens_janela, text="PARABÉNS VEI!!!! VOCÊ AFUNDOU OS CARAS!!!", 
                      font=("Verdana", 18, "bold"), fg="white", bg="black")
    msg_label.pack(pady=20)
    
    #Canvas para confetes
    canvas = Canvas(parabens_janela, width=400, height=300, bg="black", highlightthickness=0)
    canvas.pack()
    
    #Animação de confetes
    def criar_confete():
        x = random.randint(0, 400)
        tamanho = random.randint(5, 15)
        cor = random.choice(["#8B0000", "#FFD700", "#4169E1", "#DC143C", "#FF4500", "white"])
        confete = canvas.create_oval(x, 0, x + tamanho, tamanho, fill=cor, outline=cor)
        
        def mover_confete():
            canvas.move(confete, 0, 5)
            if canvas.coords(confete)[1] < 300:  #Verifica se está dentro da tela
                parabens_janela.after(50, mover_confete)
            else:
                canvas.delete(confete)
        
        mover_confete()
    
    def animar_confetes():
        for _ in range(10):
            criar_confete()
        parabens_janela.after(100, animar_confetes)  # Continuar gerando confetes

    animar_confetes()

#Inicializando a janela principal
janela = Tk()
janela.title("Olá gostaria Batalha Naval - Bordo Divas")
janela.geometry("800x800")

#Caminho para o GIF (use barras normais ou duplas barras invertidas)
gif_imagem = Image.open("C:/Users/Vivia/OneDrive/Pictures/Saved Pictures/csilla-rodonyi-underwater-019.gif")


#Converter o gif para um formato compativel para o Tkinter
frames = []
try:
    for frame in range(gif_imagem.n_frames):
        gif_imagem.seek(frame) #Seleciona o frame atual da animação com base na iteração do loop
        frame_image = ImageTk.PhotoImage(gif_imagem.copy())
        frames.append(frame_image)
except Exception as erro:
    print("Erro ao carregar o GIF:", erro)

canvas = Canvas(janela, width=800, height=800)
canvas.grid(row=0, column=0, rowspan=20, columnspan=20)

# Função para animar o GIF
def animar_gif(frame=0):
    canvas.delete("all")
    
    #Desenha o próximo quadro do GIF
    canvas.create_image(0, 0, image=frames[frame], anchor="nw")
    
    #Atualiza o quadro de animação
    next_frame = (frame + 1) % len(frames)  #Faz a animacao voltar a 0
    janela.after(100, animar_gif, next_frame)

animar_gif()

#Criando tabuleiros
tabuleiro_jogador = criar_tabuleiro()
tabuleiro_oponente = criar_tabuleiro()
colocar_navios(tabuleiro_oponente)

#Cabeçalho das colunas
for j in range(TAMANHO_TABULEIRO):
    coluna_label = Label(janela, text=str(j), font=("Verdana", 12, "bold"), bg="white")
    coluna_label.grid(row=0, column=j + 2)

#Cabeçalho das linhas e tabuleiro do jogador
grid_labels = []
for i in range(TAMANHO_TABULEIRO):
    linha_label = Label(janela, text=str(i), font=("Verdana", 12, "bold"), bg="white")
    linha_label.grid(row=i + 1, column=1)
    linha_labels = []
    for j in range(TAMANHO_TABULEIRO):
        cell_label = Label(janela, text="~", width=4, height=2, borderwidth=1, relief="solid", font=('Verdana', 12))
        cell_label.grid(row=i + 1, column=j + 2, padx=2, pady=1, sticky="nsew")
        linha_labels.append(cell_label)
    grid_labels.append(linha_labels)

#Labels e entradas para coordenadas
linha_label = Label(janela, text="Linha (0-4):", font=("Verdana", 14), bg="white")
linha_label.grid(row=6, column=0, padx=5, pady=5)
entry_linha = Entry(janela)
entry_linha.grid(row=6, column=1, padx=5, pady=5)

coluna_label = Label(janela, text="Coluna (0-4):", font=("Verdana", 14), bg="white")
coluna_label.grid(row=7, column=0, padx=5, pady=5)
entry_coluna = Entry(janela)
entry_coluna.grid(row=7, column=1, padx=5, pady=5)

#Botão de ataque
botao = Button(janela, text="Atacar", command=acao_botao)
botao.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

#Botões de bombas
bomba_linha_button = Button(janela, text="Bomba (Linha)", command=usar_bomba_linha)
bomba_linha_button.grid(row=10, column=0, padx=10, pady=10)

bomba_coluna_button = Button(janela, text="Bomba (Coluna)", command=usar_bomba_coluna)
bomba_coluna_button.grid(row=10, column=1, padx=10, pady=10)

# Exibição de bombas restantes
bomba_label = Label(janela, text=f"Bombas restantes: {BOMBAS}", bg="white", font=("Verdana", 12))
bomba_label.grid(row=11, column=0, columnspan=2, pady=10)

# Exibição do resultado
resultado_label = Label(janela, text="", font=("Verdana", 14), bg="white")
resultado_label.grid(row=9, column=0, columnspan=2, padx=5, pady=10)

# Inicializar a interface
janela.mainloop()


