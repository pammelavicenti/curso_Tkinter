''' Criando frames na Tela usando o customtkinter'''

import os 
import customtkinter as ctk # Importando a biblioteca 
import cv2
from PIL import Image, ImageTk


janela = ctk.CTk() # Criar a nossa janela

# Caminho para o logotipo
image_path = r"C:\Users\pamme\OneDrive\Documentos\IFES.jpg"


# Configurando a janela principal
janela.title("Sistema Supervisório - Correia Transportadora")
janela.geometry("800x700")
janela.maxsize(width=900, height=550)
janela.minsize(width=500, height=300)
janela.resizable(width=False, height=False)

# Criando e posicionando corretamente os Frames
frame1 = ctk.CTkFrame(master=janela, width=350, height=200, fg_color="white", corner_radius=20)
frame1.place(x=40, y=80)  # Agora a variável frame1 contém o frame corretamente

frame2 = ctk.CTkFrame(master=janela, width=350, height=200, fg_color="white", corner_radius=20)
frame2.place(x=410, y=80)

frame3 = ctk.CTkFrame(master=janela, width=350, height=200, fg_color="white", corner_radius=20)
frame3.place(x=40, y=300)

frame4 = ctk.CTkFrame(master=janela, width=350, height=200, fg_color="white", corner_radius=20)
frame4.place(x=410, y=300)

# Criando a Label dentro do frame1 onde a webcam será exibida
video_label = ctk.CTkLabel(frame1, text="", width=330, height=180)
video_label.place(x=10, y=10)  # Garante que a Label ocupa toda a área do frame

# Criando a Label dentro do frame2 onde a webcam será exibida
video_label2 = ctk.CTkLabel(frame2, text="", width=330, height=180)
video_label2.place(x=10, y=10)


# Captura da webcam (0 = webcam padrão)
cap = cv2.VideoCapture(0)   

def exibir_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Converter de BGR para RGB
        frame = cv2.resize(frame, (350, 200))  # Ajustar o tamanho do frame
        img = ImageTk.PhotoImage(Image.fromarray(frame))  # Converter para PhotoImage
        
        video_label.configure(image=img)
        video_label.image = img  # Manter referência da imagem

        video_label2.configure(image=img)
        video_label2.image = img  # Manter referência
        
    janela.after(10, exibir_frame)  # Atualizar a cada 10ms

# Iniciar a exibição da webcam
exibir_frame()

# Função para liberar a webcam ao fechar a janela
def fechar():
    cap.release()
    cv2.destroyAllWindows()
    janela.destroy()

janela.protocol("WM_DELETE_WINDOW", fechar)

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

adicionar_logo(janela)

# Iniciar o loop principal
janela.mainloop()