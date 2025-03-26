''' Criando caixas de texto (Textbox) usando o customtkinter'''

import customtkinter as ctk # Importando a biblioteca 


# Configurando a janela
janela = ctk.CTk() # Criar principal
janela.title("app teste")
janela.geometry("800x700")
janela.maxsize(width=900, height=550)
janela.minsize(width=500, height=300)
janela.resizable(width=False, height=False)

# Textbox Caixa de texto 
textbox = ctk.CTkTextbox(janela, width=300, height=350, scrollbar_button_color="green", scrollbar_button_hover_color="gray",
                         border_width=3, border_color="black", corner_radius=20, border_spacing=20)
textbox.pack()

textbox.insert("0.0", "Titulo\n\n" + "Ola, bla bla bla. \n\n"*50)


janela.mainloop()