import os 
import customtkinter as ctk  
import cv2
import math
from PIL import Image, ImageTk
from ultralytics import YOLO

# Caminho para o logotipo
image_path = r"C:\Users\pamme\OneDrive\Documentos\IFES.jpg"

# Carrega o modelo YOLO treinado
model = YOLO("C:/Users/pamme/Documents/curso_Tkinter/dataset_eu/train10/weights/best.pt")

# Criar a janela principal
janela = ctk.CTk()
janela.title("Sistema Supervisório - Correia Transportadora")
janela.state("zoomed")  # Maximiza a janela
janela.resizable(True, True)

# Novo tamanho dos frames
largura_frame = 500
altura_frame = 300

# Novas posições para centralizar os frames (ajustadas para o novo tamanho)
posicoes = [
    (0.30, 0.30),  # Frame 1
    (0.70, 0.30),  # Frame 2
    (0.30, 0.75),  # Frame 3
    (0.70, 0.75)   # Frame 4 (com YOLO)
]

frames = []
titulos = ["Operação Da Correia", "Desalinhamento", "Posição da Correia", "Rasgos e Furos"]

for i, (relx, rely) in enumerate(posicoes):
    frame = ctk.CTkFrame(master=janela, width=largura_frame, height=altura_frame, 
                         fg_color="white", border_width=3, border_color="black", corner_radius=20)
    frame.place(relx=relx, rely=rely, anchor="center")
    frames.append(frame)

    titulo = ctk.CTkLabel(frame, text=titulos[i], font=("Arial", 16, "bold"), text_color="black")
    titulo.place(x=10, y=10)

# Webcam Labels (ajustados para o novo tamanho)
video_label = ctk.CTkLabel(frames[1], text="", width=480, height=260, fg_color="white")
video_label.place(x=10, y=30)  

video_label4 = ctk.CTkLabel(frames[3], text="", width=480, height=260, fg_color="white")
video_label4.place(x=10, y=30)

# Captura da webcam
cap = cv2.VideoCapture(0)
executando_yolo = False  # Flag para controlar exibição YOLO

def exibir_frame_simples():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (480, 260))
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        video_label.configure(image=img)
        video_label.image = img
    janela.after(10, exibir_frame_simples)

# Exibir vídeo com YOLO no Frame 4
def exibir_video_frame4():
    if not executando_yolo:
        return

    ret, frame = cap.read()
    if ret:
        results = model(frame)
        annotated_frame = results[0].plot()

        D = 30
        FOV = 60
        L_real = 2 * D * math.tan(math.radians(FOV / 2))
        L_imagem = 640
        cm_por_pixel = L_real / L_imagem

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                largura_px = x2 - x1
                altura_px = y2 - y1
                largura_cm = largura_px * cm_por_pixel
                altura_cm = altura_px * cm_por_pixel
                class_id = int(box.cls[0])
                class_name = model.names[class_id]

                cv2.putText(
                    annotated_frame,
                    f"L: {largura_cm:.1f}cm H: {altura_cm:.1f}cm",
                    (x1, y1 - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 1
                )

        frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (480, 260))
        img = ImageTk.PhotoImage(Image.fromarray(frame))

        video_label4.configure(image=img)
        video_label4.image = img

    janela.after(10, exibir_video_frame4)

# Fecha a aplicação corretamente
def fechar():
    cap.release()
    cv2.destroyAllWindows()
    janela.destroy()

janela.protocol("WM_DELETE_WINDOW", fechar)

# Logo no topo
def adicionar_logo(tela):
    frame_logo = ctk.CTkFrame(tela)
    frame_logo.pack(fill="x", pady=0, anchor="nw")

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

adicionar_logo(janela)

# Titulo Principal
titulo_principal = ctk.CTkLabel(janela, text="GAIN - GAINTECH - ROBOTECH", 
                                font=("Arial", 24, "bold"), text_color="black")
titulo_principal.place(x=560, y=10)

# Titulo nome dos integrantes
titulo_nomes = ctk.CTkLabel(janela, text="Desenvolvedores: Pammela V. Ribeiro - Amanda - Diego ", 
                                font=("Arial", 22, "bold"), text_color="black")
titulo_nomes.place(x=460, y=50)

# =====================
# BOTÕES DENTRO DO FRAME 1
# =====================
frame_botoes = ctk.CTkFrame(frames[0], fg_color="transparent")
frame_botoes.place(relx=0.5, rely=0.6, anchor="center")

botao_ligar = ctk.CTkButton(frame_botoes, text="Ligar", font=("Helvetica", 12), fg_color="green", 
                            command=lambda: [globals().__setitem__('executando_yolo', True), exibir_video_frame4()])
botao_ligar.pack(pady=5, fill="x")

botao_desligar = ctk.CTkButton(frame_botoes, text="Desligar", font=("Helvetica", 12), fg_color="red", 
                               command=lambda: globals().__setitem__('executando_yolo', False))
botao_desligar.pack(pady=5, fill="x")

botao_historico = ctk.CTkButton(frame_botoes, text="Histórico", font=("Helvetica", 12), fg_color="blue", 
                                command=lambda: print("Visualizar Histórico"))
botao_historico.pack(pady=5, fill="x")

# Iniciar exibições
exibir_frame_simples()

# Loop principal
janela.mainloop()