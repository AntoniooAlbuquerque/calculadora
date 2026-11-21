from tkinter import FLAT, RAISED, RIDGE, RIGHT, Button, Frame, Label, StringVar, Tk
from src.logic import calcular_expressao
from src.theme import (
    ALTURA_JANELA,
    COR_BOTAO_IGUAL,
    COR_BOTAO_NUMERICO,
    COR_BOTAO_OPERADOR,
    COR_FUNDO_JANELA,
    COR_FUNDO_VISOR,
    COR_TEXTO_CLARO,
    COR_TEXTO_ESCURO,
    FONTE_BOTAO,
    FONTE_VISOR,
    LARGURA_JANELA,
)


class CalculadoraApp:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("Calculadora")
        self.root.geometry(f"{LARGURA_JANELA}x{ALTURA_JANELA}")
        self.root.resizable(False, False)
        self.root.config(bg=COR_FUNDO_JANELA)

        self.valores_digitados = ""
        self.valor_texto = StringVar()

        self._criar_frames()
        self._criar_visor()
        self._criar_botoes()
        self._vincular_teclado()

    def _criar_frames(self):
        self.frame_tela = Frame(self.root, width=470, height=135, bg=COR_FUNDO_VISOR)
        self.frame_tela.grid(row=0, column=0)

        self.frame_corpo = Frame(self.root, width=470, height=501)
        self.frame_corpo.grid(row=1, column=0)

    def _criar_visor(self):
        self.app_label = Label(
            self.frame_tela,
            textvariable=self.valor_texto,
            width=18,
            height=3,
            padx=40,
            relief=FLAT,
            anchor="e",
            justify=RIGHT,
            font=FONTE_VISOR,
            bg=COR_FUNDO_VISOR,
            fg=COR_TEXTO_CLARO,
        )
        self.app_label.place(x=0, y=0)

    def entrar_valores(self, valor: str):
        if self.valores_digitados.startswith("Erro"):
            self.valores_digitados = ""
        self.valores_digitados += str(valor)
        self.valor_texto.set(self.valores_digitados)

    def calcular(self):
        resultado = calcular_expressao(self.valores_digitados)
        self.valores_digitados = "" if resultado.startswith("Erro") else resultado
        self.valor_texto.set(resultado)

    def limpar_tela(self):
        self.valores_digitados = ""
        self.valor_texto.set("")

    def apagar_ultimo(self):
        if self.valores_digitados.startswith("Erro"):
            self.limpar_tela()
            return
        self.valores_digitados = self.valores_digitados[:-1]
        self.valor_texto.set(self.valores_digitados)

    def _criar_botoes(self):
        botoes = [
            ("C", 32, 0, 0, COR_BOTAO_NUMERICO, COR_TEXTO_ESCURO, self.limpar_tela),
            ("%", 16, 230, 0, COR_BOTAO_NUMERICO, COR_TEXTO_ESCURO, lambda: self.entrar_valores("%")),
            ("/", 16, 350, 0, COR_BOTAO_OPERADOR, COR_TEXTO_CLARO, lambda: self.entrar_valores("/")),

            ("7", 16, 0, 100, COR_BOTAO_NUMERICO, COR_TEXTO_ESCURO, lambda: self.entrar_valores("7")),
            ("8", 16, 115, 100, COR_BOTAO_NUMERICO, COR_TEXTO_ESCURO, lambda: self.entrar_valores("8")),
            ("9", 16, 230, 100, COR_BOTAO_NUMERICO, COR_TEXTO_ESCURO, lambda: self.entrar_valores("9")),
            ("*", 16, 350, 100, COR_BOTAO_OPERADOR, COR_TEXTO_CLARO, lambda: self.entrar_valores("*")),

            ("4", 16, 0, 200, COR_BOTAO_NUMERICO, COR_TEXTO_ESCURO, lambda: self.entrar_valores("4")),
            ("5", 16, 115, 200, COR_BOTAO_NUMERICO, COR_TEXTO_ESCURO, lambda: self.entrar_valores("5")),
            ("6", 16, 230, 200, COR_BOTAO_NUMERICO, COR_TEXTO_ESCURO, lambda: self.entrar_valores("6")),
            ("-", 16, 350, 200, COR_BOTAO_OPERADOR, COR_TEXTO_CLARO, lambda: self.entrar_valores("-")),

            ("1", 16, 0, 300, COR_BOTAO_NUMERICO, COR_TEXTO_ESCURO, lambda: self.entrar_valores("1")),
            ("2", 16, 115, 300, COR_BOTAO_NUMERICO, COR_TEXTO_ESCURO, lambda: self.entrar_valores("2")),
            ("3", 16, 230, 300, COR_BOTAO_NUMERICO, COR_TEXTO_ESCURO, lambda: self.entrar_valores("3")),
            ("+", 16, 350, 300, COR_BOTAO_OPERADOR, COR_TEXTO_CLARO, lambda: self.entrar_valores("+")),

            ("0", 32, 0, 400, COR_BOTAO_NUMERICO, COR_TEXTO_ESCURO, lambda: self.entrar_valores("0")),
            (".", 16, 230, 400, COR_BOTAO_NUMERICO, COR_TEXTO_ESCURO, lambda: self.entrar_valores(".")),
            ("=", 16, 350, 400, COR_BOTAO_IGUAL, COR_TEXTO_CLARO, self.calcular),
        ]

        for texto, largura, pos_x, pos_y, bg, fg, cmd in botoes:
            btn = Button(
                self.frame_corpo,
                command=cmd,
                text=texto,
                width=largura,
                height=6,
                bg=bg,
                fg=fg,
                font=FONTE_BOTAO,
                relief=RAISED,
                overrelief=RIDGE,
            )
            btn.place(x=pos_x, y=pos_y)

    def _vincular_teclado(self):
        self.root.bind("<Key>", self._ao_pressionar_tecla)
        self.root.bind("<Return>", lambda _: self.calcular())
        self.root.bind("<BackSpace>", lambda _: self.apagar_ultimo())
        self.root.bind("<Escape>", lambda _: self.limpar_tela())

    def _ao_pressionar_tecla(self, event):
        if event.char in "0123456789+-*/.%":
            self.entrar_valores(event.char)
