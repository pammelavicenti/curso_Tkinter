import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import random
import os

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
    status_label.config(text="Status: Ligado", fg="green")
    ultima_acao_label.config(text="Última ação tomada: Sistema Ligado")

def desligar_sistema():
    status_label.config(text="Status: Desligado", fg="red")
    ultima_acao_label.config(text="Última ação tomada: Sistema Desligado")

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
    grafico_window = tk.Toplevel(root)
    grafico_window.title("Gráficos de Dados Históricos")
    grafico_window.geometry("800x600")

    # Cria a figura para os gráficos
    fig, axs = plt.subplots(3, 1, figsize=(8, 6))
    fig.tight_layout(pad=4.0)

    # Embeda o gráfico no Tkinter
    canvas = FigureCanvasTkAgg(fig, grafico_window)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Atualiza os gráficos dinamicamente
    def loop_atualizacao():
        atualizar_graficos(axs, canvas)
        grafico_window.after(1000, loop_atualizacao)

    loop_atualizacao()

# Janela principal
root = tk.Tk()
root.title("Sistema Supervisório - Correia Transportadora")
root.geometry("900x700")
root.resizable(False, False)

# Título
titulo_label = tk.Label(root, text="Controle Da Correia Transportadora", font=("Helvetica", 16, "bold"))
titulo_label.pack(pady=10)

# Adicionar logotipo
try:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Imagem não encontrada no caminho: {image_path}")
    
    img = Image.open(image_path).resize((150, 80))  # Redimensione se necessário
    logo_image = ImageTk.PhotoImage(img)

    logo_label = tk.Label(root, image=logo_image)
    logo_label.image = logo_image
    logo_label.pack(pady=10, anchor="nw")
except Exception as e:
    print(f"Erro ao carregar a imagem: {e}")
    logo_label = tk.Label(root, text="Logo não encontrada", font=("Helvetica", 10), fg="red")
    logo_label.pack(pady=10, anchor="nw")

# Frames para organizar a interface
frame_superior = tk.Frame(root)
frame_superior.pack(pady=10)

frame_central = tk.Frame(root)
frame_central.pack(pady=10)

frame_inferior = tk.Frame(root)
frame_inferior.pack(pady=10)

# Botões de controle (Ligar/Desligar)
comando_frame = tk.LabelFrame(frame_superior, text="Comando", font=("Helvetica", 12))
comando_frame.pack(side="left", padx=20)

botao_ligar = tk.Button(comando_frame, text="Ligar", font=("Helvetica", 12), bg="green", fg="white", command=ligar_sistema)
botao_ligar.pack(pady=5)

botao_desligar = tk.Button(comando_frame, text="Desligar", font=("Helvetica", 12), bg="red", fg="white", command=desligar_sistema)
botao_desligar.pack(pady=5)

ultima_acao_label = tk.Label(comando_frame, text="Última ação tomada: -", font=("Helvetica", 10))
ultima_acao_label.pack(pady=5)

# Indicadores de status
status_frame = tk.LabelFrame(frame_superior, text="Status", font=("Helvetica", 12))
status_frame.pack(side="left", padx=20)

status_label = tk.Label(status_frame, text="Status: Desligado", font=("Helvetica", 12), fg="red")
status_label.pack(pady=10)

# Monitoramento de parâmetros
parametros_frame = tk.LabelFrame(frame_central, text="Monitoramento de Parâmetros", font=("Helvetica", 12))
parametros_frame.pack(fill="x", padx=20, pady=10)

parametro_velocidade = tk.Label(parametros_frame, text="Velocidade: 0 m/s", font=("Helvetica", 10))
parametro_velocidade.pack(anchor="w", pady=5)

parametro_desgaste = tk.Label(parametros_frame, text="Níveis de Desgaste: Normal", font=("Helvetica", 10))
parametro_desgaste.pack(anchor="w", pady=5)

parametro_carga = tk.Label(parametros_frame, text="Carga Transportada: 0 kg", font=("Helvetica", 10))
parametro_carga.pack(anchor="w", pady=5)

# Relatórios e gráficos
relatorios_frame = tk.LabelFrame(frame_inferior, text="Relatórios e Gráficos", font=("Helvetica", 12))
relatorios_frame.pack(fill="x", padx=20, pady=10)

botao_relatorio = tk.Button(relatorios_frame, text="Gerar Relatório", font=("Helvetica", 12), command=gerar_relatorio)
botao_relatorio.pack(pady=5)

botao_grafico = tk.Button(relatorios_frame, text="Exibir Gráficos", font=("Helvetica", 12), command=abrir_graficos)
botao_grafico.pack(pady=5)

# Rodapé com a data
data_label = tk.Label(root, text="06/01/2025 - Quinta-feira", font=("Helvetica", 10, "italic"))
data_label.pack(side="bottom", pady=10)

# Atualiza os dados históricos
atualizar_dados_historicos()

# Loop principal da aplicação
root.mainloop()
