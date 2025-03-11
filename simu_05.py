import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import random
import os
import csv
import cv2
import pyperclip  # Biblioteca para copiar para a área de transferência
import math
from ultralytics import YOLO

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

# Carrega o modelo YOLO treinado
model = YOLO("C:/Users/pamme/Documents/curso_Tkinter/dataset_eu/train10/weights/best.pt")


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

# Função para video de monitoramento
def exibir_video():
    video_window = ctk.CTkToplevel(root)
    video_window.title("Monitoramento por Vídeo")
    video_window.geometry("800x600")
    
    label_video = ctk.CTkLabel(video_window, font=("Helvetica", 12))
    label_video.pack()

    cap = cv2.VideoCapture(0)  # Use 0 para webcam padrão

    # Definir valores conhecidos para cálculo das dimensões
    D = 30  # Distância da câmera ao objeto em cm
    FOV = 60  # Campo de visão em graus
    L_real = 2 * D * math.tan(math.radians(FOV / 2))
    L_imagem = 640  # Largura da imagem capturada pela câmera
    cm_por_pixel = L_real / L_imagem

    def atualizar_frame():
        ret, frame = cap.read()
        if ret:
            # Realiza a detecção de objetos no frame capturado
            results = model(frame)

            # Obtém o frame com as caixas desenhadas
            annotated_frame = results[0].plot()

            # Percorre todas as detecções
            for r in results:
                for box in r.boxes:
                    # Coordenadas da caixa delimitadora (x1, y1, x2, y2)
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # Calcula a largura e altura da bounding box em pixels
                    largura_px = x2 - x1
                    altura_px = y2 - y1

                    # Converte para centímetros
                    largura_cm = largura_px * cm_por_pixel
                    altura_cm = altura_px * cm_por_pixel

                    # Obtém o nome da classe detectada
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]

                    # Define as posições para o texto
                    text_pos = (x1, y1 - 10)
                    name_pos = (x1, y1 + 15)

                    # Exibe largura e altura (em cm) acima do nome do objeto
                    cv2.putText(
                        annotated_frame, 
                        f"L: {largura_cm:.1f}cm H: {altura_cm:.1f}cm", 
                        (x1, y1 - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.5, (0, 255, 0), 1
                    )

                    # Exibe largura e altura no terminal
                    print(f"Objeto detectado: {class_name} - Largura: {largura_cm:.1f} cm, Altura: {altura_cm:.1f} cm")

            frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            label_video.configure(image=imgtk)
            label_video.imgtk = imgtk
            video_window.after(10, atualizar_frame)
        else:
            fechar_video()

    def fechar_video():
        cap.release()
        video_window.destroy()

    atualizar_frame()

    botao_fechar = ctk.CTkButton(video_window, text="Fechar", command=fechar_video)
    botao_fechar.pack(pady=10)

    video_window.protocol("WM_DELETE_WINDOW", fechar_video)  # Fecha corretamente ao clicar no X


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
    grafico_window.lift()
    grafico_window.attributes('-topmost', True)
    grafico_window.focus_force()
    grafico_window.grab_set()

    fig, axs = plt.subplots(3, 1, figsize=(8, 6))
    fig.tight_layout(pad=4.0)

    canvas = FigureCanvasTkAgg(fig, grafico_window)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    def loop_atualizacao():
        atualizar_graficos(axs, canvas)
        grafico_window.after(1000, loop_atualizacao)

    loop_atualizacao()

# Tela de Login
def criar_tela_login():
    login_window = ctk.CTk()
    login_window.title("Login")
    login_window.geometry("800x600")
    login_window.resizable(False, False)

    adicionar_logo(login_window)  # Adiciona o logo na tela de login

    def autenticar():
        usuario = usuario_entry.get()
        senha = senha_entry.get()

        if usuario == USUARIO and senha == SENHA:
            login_window.destroy()
            criar_tela_principal()
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

    botao_login = ctk.CTkButton(login_window, text="Entrar", command=autenticar)
    botao_login.pack(pady=20)

    mensagem_label = ctk.CTkLabel(login_window, text="", font=("Helvetica", 10))
    mensagem_label.pack()

    login_window.mainloop()

# Tela Principal
def criar_tela_principal():
    global root, status_label, ultima_acao_label, alerta_label
    root = ctk.CTk()
    root.title("Sistema Supervisório - Correia Transportadora")
    root.geometry("900x700")
    root.resizable(False, False)

    adicionar_logo(root)  # Adiciona o logo na tela principal

    titulo_label = ctk.CTkLabel(root, text="Controle Da Correia Transportadora", font=("Helvetica", 16, "bold"))
    titulo_label.pack(pady=10)

    alerta_label = ctk.CTkLabel(root, text="Sistema estável.", font=("Helvetica", 12), text_color="green")
    alerta_label.pack(pady=10)

    frame_superior = ctk.CTkFrame(root)
    frame_superior.pack(pady=10)

    comando_frame = ctk.CTkFrame(frame_superior)
    comando_frame.pack(side="left", padx=20)

    botao_ligar = ctk.CTkButton(comando_frame, text="Ligar", font=("Helvetica", 12), fg_color="green", command=ligar_sistema)
    botao_ligar.pack(pady=5)

    botao_desligar = ctk.CTkButton(comando_frame, text="Desligar", font=("Helvetica", 12), fg_color="red", command=desligar_sistema)
    botao_desligar.pack(pady=5)

    ultima_acao_label = ctk.CTkLabel(comando_frame, text="Última ação tomada: -", font=("Helvetica", 10))
    ultima_acao_label.pack(pady=5)

    status_frame = ctk.CTkFrame(frame_superior)
    status_frame.pack(side="left", padx=20)

    status_label = ctk.CTkLabel(status_frame, text="Status: Desligado", font=("Helvetica", 12), text_color="red")
    status_label.pack(pady=10)

    botao_grafico = ctk.CTkButton(root, text="Exibir Gráficos", font=("Helvetica", 12), command=abrir_graficos)
    botao_grafico.pack(pady=20)

    botao_relatorio = ctk.CTkButton(root, text="Gerar Relatório", font=("Helvetica", 12), command=gerar_relatorio)
    botao_relatorio.pack(pady=20)

    botao_ragos_furos = ctk.CTkButton(root, text="Ragos e Furos", font=("Helvetica", 12), command=ragos_furos)
    botao_ragos_furos.pack(pady=20)

    botao_desalinhamento = ctk.CTkButton(root, text="Desalinhamento", font=("Helvetica", 12), command=desalinhamento)
    botao_desalinhamento.pack(pady=20)

    botao_video = ctk.CTkButton(root, text="Monitoramento por Vídeo", font=("Helvetica", 12), command=exibir_video)
    botao_video.pack(pady=20)

    atualizar_dados_historicos()
    root.mainloop()

# Inicia a tela de login
criar_tela_login()