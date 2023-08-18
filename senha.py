from random import randint
import PySimpleGUI as sg

sg.theme("dark")

#ICON = "imagem/icon.ico"
ICON = "lib/imagem/icon.ico"
ARQUIVO = "lista_senha.txt"
COR_BOTAO = "red"
COR_BACK_POPUP = "white"
COR_TEXTO_POPUP = "black"
FONT = "calibri 11"
GERAL = "abcdefghijklmnopqrstuwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%&*-_0123456789"
LETRAS = "abcdefghijklmnopqrstuwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMERICO = "0123456789"
HEXADECIMAL = "0123456789ABCDEF"

layout = [
    [sg.T("Nome: "), sg.I(k="-NOME-", size=(20,1), pad=((30,0),(0)))],
    [sg.T("Caracteres:"), sg.Spin([i for i in range(1, 21)], k="-CARAC-", initial_value=8, size=(5,1))],
    [sg.Radio("Geral", "RADIO", default=True, k="-GERAL-"), 
     sg.Radio("Letras", "RADIO", k="-LETRAS-"), 
     sg.Radio("Números", "RADIO", k="-NUMEROS-"),
     sg.Radio("Hexadecimal", "RADIO", k="-HEXADECIMAL-")],
    [sg.B("Gerar senha"), sg.B("Salvar"), sg.B("Mostrar senhas")],
    [sg.Multiline(size=(35,7), k="-LIST-")]
]

window = sg.Window("Gerador de senha", layout, icon=ICON, font=FONT)

def valida_campo_vazio(valor: dict, nome: str):
    return True if str(valor[nome]).strip() == "" else False

def gera_senha(values: dict) -> None:
    lista = []

    if values["-GERAL-"]:
        pulo = 69
        caracteres = GERAL
    if values["-LETRAS-"]:
        pulo = 50
        caracteres = LETRAS
    if values["-NUMEROS-"]:
        pulo = 9
        caracteres = NUMERICO
    if values["-HEXADECIMAL-"]:
        pulo = 15
        caracteres = HEXADECIMAL

    for i in range(0, values["-CARAC-"]):
        num = randint(0, pulo)
        lista.append(caracteres[num])

    return lista

def salvar_senha(conteudo: str, linha: str) -> str:
    with open(ARQUIVO, "a") as f:
        f.write(f"{conteudo}\n{linha}\n")
        f.close()
    return "Senha salva!"

def mostrar_senhas():
    with open(ARQUIVO, "r") as f:
        for i in f.readlines():
            sg.Print(i, font=FONT, no_titlebar=True, grab_anywhere=True)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event.startswith("Gerar senha"):
        if valida_campo_vazio(values, "-NOME-"):
            sg.popup_ok("Campo 'nome' em branco!", 
                        no_titlebar=True, 
                        grab_anywhere=True, 
                        button_color=COR_BOTAO, 
                        background_color=COR_BACK_POPUP, 
                        text_color=COR_TEXTO_POPUP, 
                        font=FONT)
        else:
            lista = gera_senha(values)
            senha = ''.join(lista)
            nome = values["-NOME-"]

            window["-LIST-"].update(f"Nome: {str(nome).title()}\nSenha: {senha}")
    
    if event.startswith("Salvar"):
        conteudo = window["-LIST-"].get()
        linha = "="*40
        if conteudo == "":
            sg.popup_ok("Nenhuma senha foi gerada!", 
                        no_titlebar=True, 
                        grab_anywhere=True, 
                        button_color=COR_BOTAO, 
                        background_color=COR_BACK_POPUP, 
                        text_color=COR_TEXTO_POPUP, 
                        font=FONT)
        else:
            resposta = salvar_senha(conteudo, linha)
            sg.popup_ok(resposta, 
                        no_titlebar=True, 
                        grab_anywhere=True, 
                        button_color=COR_BOTAO, 
                        background_color=COR_BACK_POPUP, 
                        text_color=COR_TEXTO_POPUP, 
                        font=FONT)
    if event.startswith("Mostrar senhas"):
        mostrar_senhas()

window.close()
