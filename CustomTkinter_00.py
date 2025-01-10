from tkinter import *
import customtkinter 

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()

root.title('Tkinter.com - Custom Tkinter!')
#root.iconbitmap('images/codemy.ico')
root.geometry('600x350')

def hello():
    my_label.configure(text=my_button.cget("text"))


my_button = customtkinter.CTkButton(root, 
    text="Hello World!", # Texto do Botão
    command=hello,
    height=50, # Altura do botão
    width=100,  # Largura do botão
    font=("Helvetica", 14), # Fonte e tamanho da letra do botão 
    text_color="black", # Cor do texto do Botão
    fg_color="red", # Cor do Botão vermelho
    hover_color="green", # Cor do botão fica verde quando passar o mouse
    corner_radius=50, # Arredondamento do botão
    border_width=5, # Borda do botão
    border_color="yellow", # Mudar a cor da borda do botão
    ) 

my_button.pack(pady=80)

my_label = customtkinter.CTkLabel(root, text="")
my_label.pack(pady=20)



root.mainloop()