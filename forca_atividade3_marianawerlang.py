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
