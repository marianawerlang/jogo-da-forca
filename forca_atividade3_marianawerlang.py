# Tarefa 04 - Jogo da Forca com Interface Gráfica
# Disciplina: Introdução à Ciência da Computação
# Aluno: Mariana Werlang Moraes - 25204855
# Data: 17/11/2026


import PySimpleGUI as sg
import random


# Função responsável por carregar uma palavra aleatória
# do arquivo correspondente à dificuldade escolhida
def carregar_palavra(dificuldade):
    arquivo = f"{dificuldade}.txt"

    try:
        with open(arquivo, 'r', encoding='utf-8') as f:

            # Remove espaços e converte para maiúsculo
            palavras = [linha.strip().upper() for linha in f.readlines()]

        # Escolhe uma palavra aleatória da lista
        return random.choice(palavras)

    except FileNotFoundError:
        sg.popup("Arquivo de palavras não encontrado!")
        return ""


# Cria toda a interface gráfica do jogo
def criar_layout():

    layout = [

        # Escolha da dificuldade
        [
            sg.Text("Selecione a Dificuldade:"),

            sg.Radio(
                "Fácil",
                "DIFICULDADE",
                key="-FACIL-",
                default=True
            ),

            sg.Radio(
                "Difícil",
                "DIFICULDADE",
                key="-DIFICIL-"
            )
        ],

        # Botão para iniciar uma nova partida
        [sg.Button("Iniciar Jogo")],

        # Área onde a forca será desenhada
        [sg.Canvas(key="-FORCA-", size=(250, 250))],

        # Palavra secreta exibida parcialmente
        [sg.Text(
            "",
            key="-PALAVRA-",
            font=("Helvetica", 22)
        )],

        # Contador de erros
        [sg.Text("Erros: 0/6", key="-ERROS-")],

        # Primeira linha do teclado
        [sg.Button(letra, size=(4, 2))
         for letra in "ABCDEFGHIJKLM"],

        # Segunda linha do teclado
        [sg.Button(letra, size=(4, 2))
         for letra in "NOPQRSTUVWXYZ"]
    ]

    return layout


# Desenha a forca conforme a quantidade de erros
def desenhar_forca(canvas, erros):

    c = canvas.TKCanvas

    # Limpa o desenho anterior
    c.delete("all")

    # Estrutura fixa da forca
    c.create_line(20, 220, 180, 220, width=3)  # base
    c.create_line(50, 220, 50, 20, width=3)    # poste
    c.create_line(50, 20, 140, 20, width=3)    # topo
    c.create_line(140, 20, 140, 50, width=3)   # corda

    # A cada erro desenha uma parte do corpo

    if erros >= 1:
        c.create_oval(120, 50, 160, 90, width=2)  # cabeça

    if erros >= 2:
        c.create_line(140, 90, 140, 140, width=2)  # corpo

    if erros >= 3:
        c.create_line(140, 100, 110, 120, width=2)  # braço esquerdo

    if erros >= 4:
        c.create_line(140, 100, 170, 120, width=2)  # braço direito

    if erros >= 5:
        c.create_line(140, 140, 120, 170, width=2)  # perna esquerda

    if erros >= 6:
        c.create_line(140, 140, 160, 170, width=2)  # perna direita


# Cria a janela principal
window = sg.Window(
    "Jogo da Forca",
    criar_layout()
)

# Variáveis do jogo
palavra = ""
descobertas = []
letras_usadas = []
erros = 0

# Loop principal do programa
while True:

    # Captura eventos da interface
    event, values = window.read()

    # Fecha o programa ao clicar no X
    if event == sg.WIN_CLOSED:
        break

    # Inicia uma nova partida
    if event == "Iniciar Jogo":

        # Verifica qual dificuldade foi escolhida
        dificuldade = "facil" if values["-FACIL-"] else "dificil"

        # Carrega palavra aleatória
        palavra = carregar_palavra(dificuldade)

        if palavra:

            # Cria lista com traços representando as letras ocultas
            descobertas = ["_" for _ in palavra]

            # Reinicia variáveis do jogo
            letras_usadas = []
            erros = 0

            # Atualiza interface
            window["-PALAVRA-"].update(" ".join(descobertas))
            window["-ERROS-"].update("Erros: 0/6")

            desenhar_forca(window["-FORCA-"], 0)

    # Verifica se foi clicada alguma letra
    elif event in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

        # Só permite jogar se existir uma partida ativa
        if palavra:

            # Impede repetir letras já utilizadas
            if event in letras_usadas:
                continue

            # Registra a letra utilizada
            letras_usadas.append(event)

            # Verifica se a letra está na palavra
            if event in palavra:

                # Revela todas as ocorrências da letra
                for i, letra in enumerate(palavra):

                    if letra == event:
                        descobertas[i] = letra

                # Atualiza a palavra na tela
                window["-PALAVRA-"].update(
                    " ".join(descobertas)
                )

                # Verifica vitória
                if "_" not in descobertas:

                    sg.popup(
                        "Parabéns!",
                        "Você venceu!"
                    )

                    # Encerra a partida atual
                    palavra = ""

            else:

                # Incrementa o contador de erros
                erros += 1

                # Atualiza desenho da forca
                desenhar_forca(
                    window["-FORCA-"],
                    erros
                )

                # Atualiza contador visual
                window["-ERROS-"].update(
                    f"Erros: {erros}/6"
                )

                # Verifica derrota
                if erros >= 6:

                    sg.popup(
                        "Fim de jogo!",
                        f"A palavra era: {palavra}"
                    )

                    # Encerra a partida atual
                    palavra = ""

# Fecha a janela ao terminar o programa
window.close()