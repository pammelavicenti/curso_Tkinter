''' Criando caixas de dialogo usando o customtkinter'''

import customtkinter as ctk # Importando a biblioteca 


# Configurando a janela
janela = ctk.CTk() # Criar principal
janela.title("app teste")
janela.geometry("800x700")
janela.maxsize(width=900, height=550)
janela.minsize(width=500, height=300)
janela.resizable(width=False, height=False)

# Caixa de dialogo


btn = ctk.CTkButton(janela, text="Abrir caixa de Dialogo")
btn.pack()


janela.mainloop()