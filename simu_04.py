import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import random
import os
import csv
import pyperclip
import winsound  # Para adicionar som aos alertas
import time

# Configuração do tema customtkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Caminho para o logotipo
image_path = r"C:\Users\pamme\OneDrive\Documentos\IFES.jpg"

# Usuário e senha para autenticação
USUARIO = "admin"
SENHA = "1234"

# Dados históricos simulados
historico_velocidade = [0]
historico_desgaste = [0]
historico_carga = [0]

# Tamanho padronizado para as telas
TAMANHO_TELA = "800x600"

# Função para adicionar o logo
def adicionar_logo(tela):
    frame_logo = ctk.CTkFrame(tela)
    frame_logo.pack(fill="x", pady=2, anchor="nw")

    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Imagem não encontrada no caminho: {image_path}")

        img = Image.open(image_path).resize((180, 100))
        logo_image = ImageTk.PhotoImage(img)

        logo_label = ctk.CTkLabel(frame_logo, image=logo_image, text="") 
        logo_label.image = logo_image 
        logo_label.pack(anchor="nw")
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")
        logo_label = ctk.CTkLabel(frame_logo, text="Logo não encontrada", font=("Helvetica", 10), text_color="red")
        logo_label.pack(anchor="nw")

# Função para atualizar dados históricos
def atualizar_dados_historicos():
    historico_velocidade.append(random.randint(1, 10))
    historico_desgaste.append(random.randint(0, 100))
    historico_carga.append(random.randint(100, 1000))

    if len(historico_velocidade) > 20:
        historico_velocidade.pop(0)
        historico_desgaste.pop(0)
        historico_carga.pop(0)

    verificar_alertas()
    root.after(1000, atualizar_dados_historicos)

# Função para verificar alertas
def verificar_alertas():
    desgaste_atual = historico_desgaste[-1]
    carga_atual = historico_carga[-1]

    # Alerta de desgaste crítico
    if desgaste_atual > 90:
        alerta_label.configure(
            text=f"ALERTA: Desgaste crítico ({desgaste_atual}%)!",
            text_color="white",
            fg_color="orange"
        )
        alerta_label.after(500, lambda: alerta_label.configure(fg_color="red"))
        alerta_label.after(1000, lambda: alerta_label.configure(fg_color="orange"))
        mostrar_popup_alerta(f"ALERTA: Desgaste crítico ({desgaste_atual}%)!")
        tocar_alerta_sonoro()

    # Alerta de carga excessiva
    elif carga_atual > 900:
        alerta_label.configure(
            text=f"ALERTA: Carga excessiva ({carga_atual} kg)!",
            text_color="white",
            fg_color="red"
        )
        alerta_label.after(500, lambda: alerta_label.configure(fg_color="orange"))
        alerta_label.after(1000, lambda: alerta_label.configure(fg_color="red"))
        mostrar_popup_alerta(f"ALERTA: Carga excessiva ({carga_atual} kg)!")
        tocar_alerta_sonoro()

    # Sistema estável
    else:
        alerta_label.configure(
            text="Sistema estável.",
            text_color="white",
            fg_color="green"
        )

# Função para mostrar pop-up de alerta
def mostrar_popup_alerta(mensagem):
    popup = ctk.CTkToplevel(root)
    popup.title("Alerta")
    popup.geometry("300x100")
    popup.resizable(False, False)

    # Garante que o pop-up seja mostrado na frente da janela principal
    popup.lift()  # Levanta a janela pop-up
    popup.attributes('-topmost', True)  # Faz a janela ser sempre a mais superior
    popup.focus_force()  # Garante que o foco esteja na janela pop-up

    alerta_label = ctk.CTkLabel(popup, text=mensagem, font=("Helvetica", 12), text_color="red")
    alerta_label.pack(pady=20)

    fechar_button = ctk.CTkButton(popup, text="Fechar", command=popup.destroy)
    fechar_button.pack(pady=10)

    popup.after(5000, popup.destroy)  # Fecha o pop-up após 5 segundos


# Função para adicionar som aos alertas
def tocar_alerta_sonoro():
    winsound.Beep(1000, 1000)  # Toca um som de 1000Hz por 1 segundo

# Funções dos botões da tela principal
def ligar_sistema():
    status_label.configure(text="Status: Ligado", text_color="green")
    ultima_acao_label.configure(text="Última ação tomada: Sistema Ligado")

def desligar_sistema():
    status_label.configure(text="Status: Desligado", text_color="red")
    ultima_acao_label.configure(text="Última ação tomada: Sistema Desligado")

def gerar_relatorio():
    relatorio_window = ctk.CTkToplevel(root)
    relatorio_window.title("Relatório")
    relatorio_window.geometry(TAMANHO_TELA)
    relatorio_window.resizable(False, False)
    
    # Configura para garantir que a janela de "Relatório" fique no topo
    relatorio_window.lift()
    relatorio_window.attributes('-topmost', True)
    relatorio_window.focus_force()
    relatorio_window.grab_set()

    # Conteúdo do relatório
    titulo_label = ctk.CTkLabel(relatorio_window, text="Relatório do Sistema", font=("Helvetica", 16, "bold"))
    titulo_label.pack(pady=10)

    dados_relatorio = (
        f"Velocidades: {historico_velocidade}\n"
        f"Desgastes: {historico_desgaste}\n"
        f"Cargas: {historico_carga}\n"
    )

    historico_label = ctk.CTkLabel(
        relatorio_window,
        text=dados_relatorio,
        font=("Helvetica", 12),
        justify="left"
    )
    historico_label.pack(pady=10)

    # Função para copiar os dados para a área de transferência
    def copiar_dados():
        pyperclip.copy(dados_relatorio)
        mensagem_label.configure(text="Dados copiados para a área de transferência!", text_color="green")

    # Função para exportar os dados para um arquivo CSV
    def exportar_csv():
        caminho_arquivo = "relatorio.csv"
        with open(caminho_arquivo, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Velocidade", "Desgaste", "Carga"])
            for i in range(len(historico_velocidade)):
                writer.writerow([historico_velocidade[i], historico_desgaste[i], historico_carga[i]])

        mensagem_label.configure(text=f"Relatório exportado para {caminho_arquivo}", text_color="green")

    # Botões de copiar e exportar
    botao_copiar = ctk.CTkButton(relatorio_window, text="Copiar Dados", command=copiar_dados)
    botao_copiar.pack(pady=5)

    botao_exportar = ctk.CTkButton(relatorio_window, text="Exportar para CSV", command=exportar_csv)
    botao_exportar.pack(pady=5)

    fechar_button = ctk.CTkButton(relatorio_window, text="Fechar", command=lambda: fechar_relatorio(relatorio_window))
    fechar_button.pack(pady=20)

    # Label para mensagens
    mensagem_label = ctk.CTkLabel(relatorio_window, text="", font=("Helvetica", 10))
    mensagem_label.pack()

def fechar_relatorio(window):
    window.grab_release()  # Libera o bloqueio na janela principal
    window.destroy()

# Função para transição suave de telas
def animar_troca_tela(atual, nova):
    # Faz a tela atual desaparecer
    for i in range(100, 0, -1):
        atual.attributes("-alpha", i / 100)
        atual.update()
        time.sleep(0.02)
    
    # Fecha a tela atual
    atual.destroy()
    
    # Exibe a nova tela
    nova.attributes("-alpha", 0)
    nova.deiconify()  # Torna a nova janela visível
    for i in range(0, 101):
        nova.attributes("-alpha", i / 100)
        nova.update()
        time.sleep(0.02)

# Efeito de hover nos botões
def on_hover_button(button):
    button.configure(fg_color="lightblue")  # Mudando a cor de fundo quando o mouse passa sobre o botão

def on_leave_button(button):
    button.configure(fg_color="blue")  # Retornando a cor de fundo original quando o mouse sai

# Tela de Login
def criar_tela_login():
    login_window = ctk.CTk()
    login_window.title("Login")
    login_window.geometry(TAMANHO_TELA)
    login_window.resizable(False, False)

    adicionar_logo(login_window)  # Adiciona o logo na tela de login

    def autenticar():
        usuario = usuario_entry.get()
        senha = senha_entry.get()

        if usuario == USUARIO and senha == SENHA:
            login_window.destroy()
            nova_tela = criar_tela_principal()
            animar_troca_tela(login_window, nova_tela)
        else:
            mensagem_label.configure(text="Usuário ou senha incorretos!", text_color="red")

    titulo_label = ctk.CTkLabel(login_window, text="Sistema Supervisório", font=("Helvetica", 16, "bold"))
    titulo_label.pack(pady=20)

    usuario_label = ctk.CTkLabel(login_window, text="Usuário:", font=("Helvetica", 12))
    usuario_label.pack(pady=5)
    usuario_entry = ctk.CTkEntry(login_window, placeholder_text="Digite seu usuário")
    usuario_entry.pack(pady=5)

    senha_label = ctk.CTkLabel(login_window, text="Senha:", font=("Helvetica", 12))
    senha_label.pack(pady=5)
    senha_entry = ctk.CTkEntry(login_window, placeholder_text="Digite sua senha", show="*")
    senha_entry.pack(pady=5)

    mensagem_label = ctk.CTkLabel(login_window, text="", font=("Helvetica", 10))
    mensagem_label.pack(pady=5)

    login_button = ctk.CTkButton(login_window, text="Login", command=autenticar)
    login_button.pack(pady=20)

    # Adiciona efeito de hover no botão de login
    login_button.bind("<Enter>", lambda event: on_hover_button(login_button))
    login_button.bind("<Leave>", lambda event: on_leave_button(login_button))

    login_window.mainloop()

# Tela Principal
def criar_tela_principal():
    global root, alerta_label, ultima_acao_label, status_label
    root = ctk.CTk() 
    root.title("Tela Principal")
    root.geometry(TAMANHO_TELA)
    root.resizable(False, False)

    adicionar_logo(root)

    alerta_label = ctk.CTkLabel(root, text="Sistema estável.", text_color="white", fg_color="green", font=("Helvetica", 14))
    alerta_label.pack(pady=10)

    status_label = ctk.CTkLabel(root, text="Status: Desligado", text_color="red", font=("Helvetica", 14))
    status_label.pack(pady=5)

    ultima_acao_label = ctk.CTkLabel(root, text="Última ação tomada: Nenhuma", font=("Helvetica", 12))
    ultima_acao_label.pack(pady=10)

    # Botões da tela principal
    ligar_button = ctk.CTkButton(root, text="Ligar Sistema", command=ligar_sistema)
    ligar_button.pack(pady=5)

    desligar_button = ctk.CTkButton(root, text="Desligar Sistema", command=desligar_sistema)
    desligar_button.pack(pady=5)

    gerar_relatorio_button = ctk.CTkButton(root, text="Gerar Relatório", command=gerar_relatorio)
    gerar_relatorio_button.pack(pady=5)

    # Adiciona efeitos de hover nos botões
    ligar_button.bind("<Enter>", lambda event: on_hover_button(ligar_button))
    ligar_button.bind("<Leave>", lambda event: on_leave_button(ligar_button))

    desligar_button.bind("<Enter>", lambda event: on_hover_button(desligar_button))
    desligar_button.bind("<Leave>", lambda event: on_leave_button(desligar_button))

    gerar_relatorio_button.bind("<Enter>", lambda event: on_hover_button(gerar_relatorio_button))
    gerar_relatorio_button.bind("<Leave>", lambda event: on_leave_button(gerar_relatorio_button))

    # Atualiza os dados e alerta a cada segundo
    root.after(1000, atualizar_dados_historicos)

    root.mainloop()

# Inicia a tela de login
criar_tela_login()


