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
