import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import random
import os
import csv
import pyperclip  # Biblioteca para copiar para a área de transferência
import cv2  # Biblioteca OpenCV para captura de vídeo

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

    # Verifica desgaste
    if desgaste_atual > 90:
        alerta_label.configure(
            text=f"ALERTA: Desgaste crítico ({desgaste_atual}%)!",
            text_color="orange"
        )
        print(f"ALERTA: Desgaste crítico ({desgaste_atual}%)!")

    # Verifica carga
    elif carga_atual > 900:
        alerta_label.configure(
            text=f"ALERTA: Carga excessiva ({carga_atual} kg)!",
            text_color="red"
        )
        print(f"ALERTA: Carga excessiva ({carga_atual} kg)!")
    else:
        alerta_label.configure(text="Sistema estável.", text_color="green")

# Função para atualizar gráficos
def atualizar_graficos(axs, canvas):
    axs[0].clear()
    axs[0].plot(historico_velocidade, label="Velocidade (m/s)", color="blue")
    axs[0].set_title("Velocidade")
    axs[0].legend()

    axs[1].clear()
    axs[1].plot(historico_desgaste, label="Desgaste (%)", color="orange")
    axs[1].set_title("Níveis de Desgaste")
    axs[1].legend()

    axs[2].clear()
    axs[2].plot(historico_carga, label="Carga (kg)", color="green")
    axs[2].set_title("Carga Transportada")
    axs[2].legend()

    canvas.draw()

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
    relatorio_window.geometry("600x400")
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

def ragos_furos():
    ragos_furos_window = ctk.CTkToplevel(root)
    ragos_furos_window.title("Ragos e Furos")
    ragos_furos_window.geometry("400x300")
    
    # Configura para garantir que a janela de "Ragos e Furos" fique no topo
    ragos_furos_window.lift()
    ragos_furos_window.attributes('-topmost', True)
    ragos_furos_window.focus_force()
    ragos_furos_window.grab_set()

    titulo_label = ctk.CTkLabel(ragos_furos_window, text="Informações sobre Ragos e Furos", font=("Helvetica", 16, "bold"))
    titulo_label.pack(pady=20)

    info_label = ctk.CTkLabel(ragos_furos_window, text="Aqui serão exibidos dados sobre Ragos e Furos.", font=("Helvetica", 12))
    info_label.pack(pady=10)

    fechar_button = ctk.CTkButton(ragos_furos_window, text="Fechar", command=ragos_furos_window.destroy)
    fechar_button.pack(pady=20)

def desalinhamento():
    desalinhamento_window = ctk.CTkToplevel(root)
    desalinhamento_window.title("Desalinhamento")
    desalinhamento_window.geometry("400x300")
    
    # Configura para garantir que a janela de "Desalinhamento" fique no topo
    desalinhamento_window.lift()
    desalinhamento_window.attributes('-topmost', True)
    desalinhamento_window.focus_force()
    desalinhamento_window.grab_set()

    titulo_label = ctk.CTkLabel(desalinhamento_window, text="Informações sobre Desalinhamento", font=("Helvetica", 16, "bold"))
    titulo_label.pack(pady=20)

    info_label = ctk.CTkLabel(desalinhamento_window, text="Aqui serão exibidos dados sobre Desalinhamento.", font=("Helvetica", 12))
    info_label.pack(pady=10)

    fechar_button = ctk.CTkButton(desalinhamento_window, text="Fechar", command=desalinhamento_window.destroy)
    fechar_button.pack(pady=20)

def abrir_graficos():
    grafico_window = ctk.CTkToplevel(root)
    grafico_window.title("Gráficos de Dados Históricos")
    grafico_window.geometry("800x600")

    # Configura para garantir que a janela de "Gráficos" fique no topo
    graf

