''' Criando Tabs (abas) usando o customtkinter'''

import customtkinter as ctk # Importando a biblioteca 
import cv2 


# Configurando a janela
from PIL import Image, ImageTk

janela = ctk.CTk() # Criar principal
janela.title("app teste")
janela.geometry("800x700")
janela.maxsize(width=900, height=550)
janela.minsize(width=500, height=300)
janela.resizable(width=False, height=False)

# Criando e posicionando corretamente os Frames
'''frame1 = ctk.CTkFrame(master=janela, width=350, height=200, fg_color="white", corner_radius=20)
frame1.place(x=40, y=80)  # Agora a variável frame1 contém o frame corretamente

frame2 = ctk.CTkFrame(master=janela, width=350, height=200, fg_color="white", corner_radius=20)
frame2.place(x=410, y=80)

frame3 = ctk.CTkFrame(master=janela, width=350, height=200, fg_color="white", corner_radius=20)
frame3.place(x=40, y=300)

frame4 = ctk.CTkFrame(master=janela, width=350, height=200, fg_color="white", corner_radius=20)
frame4.place(x=410, y=300)'''

# Criando abas no Tkinter (Tabview)
tabview = ctk.CTkTabview(janela, width=400, corner_radius=20, border_color="black", border_width=4)
tabview.pack() # pack serve para centralizar
tabview.add("Ligar") 
tabview.add("Desligar") 

# Adicionando elementos na nossa tab 
text = ctk.CTkLabel(tabview.tab("Ligar"), text="Acionamento para Ligar")
text.pack() # pack serve para centralizar

text = ctk.CTkLabel(tabview.tab("Desligar"), text="Acionamento para Desligar")
text.pack()


# Criando a Label dentro do frame1 onde a webcam será exibida
'''video_label = ctk.CTkLabel(frame1, text="", width=350, height=200)
video_label.place(x=0, y=0)  # Garante que a Label ocupa toda a área do frame

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
        
    janela.after(10, exibir_frame)  # Atualizar a cada 10ms

# Iniciar a exibição da webcam
exibir_frame()

# Função para liberar a webcam ao fechar a janela
def fechar():
    cap.release()
    cv2.destroyAllWindows()
    janela.destroy()

janela.protocol("WM_DELETE_WINDOW", fechar)'''

# Iniciar o loop principal
janela.mainloop()