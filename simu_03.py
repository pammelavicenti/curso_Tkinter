import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import random
import os

# Configuração do tema customtkinter
ctk.set_appearance_mode("light")  # Modos: "dark", "light"
ctk.set_default_color_theme("blue")

# Dados históricos simulados
historico_velocidade = [0]
historico_desgaste = [0]
historico_carga = [0]

# Caminho absoluto para o logotipo
image_path = r"C:\Users\Pammela\Documents\curso_Tkinter\IFES.jpg"

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

# Funções para os botões
def ligar_sistema():
    status_label.configure(text="Status: Ligado", text_color="green")
    ultima_acao_label.configure(text="Última ação tomada: Sistema Ligado")

def desligar_sistema():
    status_label.configure(text="Status: Desligado", text_color="red")
    ultima_acao_label.configure(text="Última ação tomada: Sistema Desligado")

def gerar_relatorio():
    print("Relatório gerado!")

def atualizar_dados_historicos():
    # Simula dados dinâmicos
    historico_velocidade.append(random.randint(1, 10))
    historico_desgaste.append(random.randint(0, 100))
    historico_carga.append(random.randint(100, 1000))

    # Mantém apenas os últimos 20 pontos para simplificar
    if len(historico_velocidade) > 20:
        historico_velocidade.pop(0)
        historico_desgaste.pop(0)
        historico_carga.pop(0)

    root.after(1000, atualizar_dados_historicos)  # Atualiza a cada 1 segundo

def abrir_graficos():
    # Cria uma nova janela para exibir os gráficos
    grafico_window = ctk.CTkToplevel(root)
    grafico_window.title("Gráficos de Dados Históricos")
    grafico_window.geometry("800x600")

    # Cria a figura para os gráficos
    fig, axs = plt.subplots(3, 1, figsize=(8, 6))
    fig.tight_layout(pad=4.0)

    # Embeda o gráfico no Tkinter
    canvas = FigureCanvasTkAgg(fig, grafico_window)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Atualiza os gráficos dinamicamente
    def loop_atualizacao():
        atualizar_graficos(axs, canvas)
        grafico_window.after(1000, loop_atualizacao)

    loop_atualizacao()

# Janela principal
root = ctk.CTk()
root.title("Sistema Supervisório - Correia Transportadora")
root.geometry("900x700")
root.resizable(False, False)

# Frame para o logotipo
frame_logo = ctk.CTkFrame(root)
frame_logo.pack(fill="x", pady=2, anchor="nw")

# Adicionar logotipo
try:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Imagem não encontrada no caminho: {image_path}")

    img = Image.open(image_path).resize((180, 100))  # Redimensione se necessário
    logo_image = ImageTk.PhotoImage(img)

    logo_label = ctk.CTkLabel(frame_logo, image=logo_image, text="")
    logo_label.image = logo_image
    logo_label.pack(anchor="nw")
except Exception as e:
    print(f"Erro ao carregar a imagem: {e}")
    logo_label = ctk.CTkLabel(frame_logo, text="Logo não encontrada", font=("Helvetica", 10), text_color="red")
    logo_label.pack(anchor="nw")

# Título
titulo_label = ctk.CTkLabel(root, text="Controle Da Correia Transportadora", font=("Helvetica", 16, "bold"))
titulo_label.pack(pady=10)

# Frames para organizar a interface
frame_superior = ctk.CTkFrame(root)
frame_superior.pack(pady=10)

frame_central = ctk.CTkFrame(root)
frame_central.pack(pady=10)

frame_inferior = ctk.CTkFrame(root)
frame_inferior.pack(pady=10)

# Botões de controle (Ligar/Desligar)
comando_frame = ctk.CTkFrame(frame_superior)
comando_frame.pack(side="left", padx=20)

botao_ligar = ctk.CTkButton(comando_frame, text="Ligar", font=("Helvetica", 12), fg_color="green", command=ligar_sistema)
botao_ligar.pack(pady=5)

botao_desligar = ctk.CTkButton(comando_frame, text="Desligar", font=("Helvetica", 12), fg_color="red", command=desligar_sistema)
botao_desligar.pack(pady=5)

ultima_acao_label = ctk.CTkLabel(comando_frame, text="Última ação tomada: -", font=("Helvetica", 10))
ultima_acao_label.pack(pady=5)

# Indicadores de status
status_frame = ctk.CTkFrame(frame_superior)
status_frame.pack(side="left", padx=20)

status_label = ctk.CTkLabel(status_frame, text="Status: Desligado", font=("Helvetica", 12), text_color="red")
status_label.pack(pady=10)

# Monitoramento de parâmetros
parametros_frame = ctk.CTkFrame(frame_central)
parametros_frame.pack(fill="x", padx=20, pady=10)

parametro_velocidade = ctk.CTkLabel(parametros_frame, text="Velocidade: 0 m/s", font=("Helvetica", 10))
parametro_velocidade.pack(anchor="w", pady=5)

parametro_desgaste = ctk.CTkLabel(parametros_frame, text="Níveis de Desgaste: Normal", font=("Helvetica", 10))
parametro_desgaste.pack(anchor="w", pady=5)

parametro_carga = ctk.CTkLabel(parametros_frame, text="Carga Transportada: 0 kg", font=("Helvetica", 10))
parametro_carga.pack(anchor="w", pady=5)

# Relatórios e gráficos
relatorios_frame = ctk.CTkFrame(frame_inferior)
relatorios_frame.pack(fill="x", padx=20, pady=10)

botao_relatorio = ctk.CTkButton(relatorios_frame, text="Gerar Relatório", font=("Helvetica", 12), command=gerar_relatorio)
botao_relatorio.pack(pady=5)

botao_grafico = ctk.CTkButton(relatorios_frame, text="Exibir Gráficos", font=("Helvetica", 12), command=abrir_graficos)
botao_grafico.pack(pady=5)

# Rodapé com a data
data_label = ctk.CTkLabel(root, text="06/01/2025 - Quinta-feira", font=("Helvetica", 10, "italic"))
data_label.pack(side="bottom", pady=10)

# Atualiza os dados históricos
atualizar_dados_historicos()

# Loop principal da aplicação
root.mainloop()
