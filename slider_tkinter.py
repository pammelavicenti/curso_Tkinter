''' Criando Slider usando o customtkinter'''

import customtkinter as ctk # Importando a biblioteca 


# Configurando a janela
janela = ctk.CTk() # Criar principal
janela.title("app teste")
janela.geometry("900x700")
janela.maxsize(width=900, height=550)
janela.minsize(width=500, height=300)
janela.resizable(width=False, height=False)

ctk.CTkLabel(janela, text="Curso de Customtkinter - Aula - 14 (Slider)", font=("arial bold", 20)).pack(pady=20, padx=5)

def slider_value(value):
    print(value)

slider = ctk.CTkSlider(janela, from_=0, to=100, command=slider_value)
slider.pack(pady=30)



janela.mainloop() # Rodando a janela