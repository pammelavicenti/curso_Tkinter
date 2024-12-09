from tkinter import *
from tkinter import ttk
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

root = Tk()

class Relatorios():
    def printCliente(self):  # Função para chamar e exibir o arquivo
        webbrowser.open("cliente.pdf")
    def geraRelatCliente(self):     # Função para fazer um PDF com os dados do clientes
        self.c = canvas.Canvas("cliente.pdf")

        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.foneRel = self.fone_entry.get()
        self.cidadeRel = self.cidade_entry.get()

        self.c.setFont("Helvetica-Bold", 24) 
        self.c.drawString(200, 790, 'Ficha do Cliente')

        self.c.setFont("Helvetica-Bold", 18) 
        self.c.drawString(50, 700, 'Código: ')
        self.c.drawString(50, 660, 'Nome: ')
        self.c.drawString(50, 630, 'Telefone: ')
        self.c.drawString(50, 600, 'Cidade: ')

        self.c.setFont("Helvetica", 18) 
        self.c.drawString(150, 700, self.codigoRel)
        self.c.drawString(150, 660, self.nomeRel)
        self.c.drawString(150, 630, self.foneRel)
        self.c.drawString(150, 600, self.cidadeRel)

        self.c.rect(20, 550, 550, 1, fill=False, stroke=True)  # Para criar linhas e espaçamentos na tela

        self.c.showPage()
        self.c.save()
        self.printCliente()

class Funcs():
    def limpa_tela(self):     # Função para apagar da tela

        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.fone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.bd")
        self.cursor = self.conn.cursor(); print("Conectando ao banco de dados")
    def desconecta_bd(self):
        self.conn.close(); print("Desconectando ao banco de dados")
    def montaTabelas(self):

        self.conecta_bd()
        ### Criar tabela 
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (    
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL, 
                telefone INTEGER(20),
                cidade CHAR(40)
            );
     
        """)
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd()
    def variaveis(self):      # Função de variaveis
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.fone = self.fone_entry.get()
        self.cidade = self.cidade_entry.get()
    def add_cliente(self):
        self.variaveis()
        
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, cidade)
            VALUES (?, ?, ?)""", (self.nome, self.fone, self.cidade))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())    
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes
            ORDER BY nome_cliente ASC; """) # Vai chamar essa lista em ordem alfabetica
        for i in lista:
            self.listaCli.insert("", END, values=i) 
        self.desconecta_bd()
    def OnDoubleClick(self, event): # Função para duplo clique, event vai dizer para o python que ele vai realizar um evento.
        self.limpa_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.fone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()
    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ?
            WHERE cod = ? """, (self.nome, self.fone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
class Application(Funcs, Relatorios):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()
    def tela(self): # Função da tela 
        self.root.title("Cadastro de clientes") #Titulo da aba da tela
        self.root.configure(background='#B0C4DE') # Cor da tela em hexadecimal
        self.root.geometry("700x500") # Tamanho da tela X * Y
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=700) # Valor máximo da largura da tela em vertical x horizontal
        self.root.minsize(width=500, height=400) # Valor mínimo da largura da tela em vertical x horizontal
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd= 4, bg= '#dfe3ee', highlightbackground='#759fe6', highlightthickness=2 ) # Cor da borda do frame
        self.frame_1.place(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.46)

        self.frame_2 = Frame(self.root, bd= 4, bg= '#dfe3ee', highlightbackground='#759fe6', highlightthickness=2 ) # bd = borda, bg = cor de fundo
        self.frame_2.place(relx= 0.02, rely= 0.5, relwidth= 0.96, relheight= 0.46)
    def widgets_frame1(self):

        # Criação do botão limpar
        self.bt_limpar = Button(self.frame_1, text= "Limpar", bd=2, bg = '#107db2', fg='white'
                                , font= ('verdana', 8, 'bold'), command= self.limpa_tela) # fg = Cor do texto do widgets
        self.bt_limpar.place(relx= 0.2, rely= 0.1, relwidth= 0.1, relheight= 0.15)
        # Criação do botão buscar
        self.bt_buscar = Button(self.frame_1, text= "Buscar", bd=2, bg = '#107db2', fg='white'
                                , font= ('verdana', 8, 'bold')) 
        self.bt_buscar.place(relx= 0.3, rely= 0.1, relwidth= 0.1, relheight= 0.15)
        # Criação do botão novo
        self.bt_novo = Button(self.frame_1, text= "Novo", bd=2, bg = '#107db2', fg='white'
                                , font= ('verdana', 8, 'bold'), command= self.add_cliente) 
        self.bt_novo.place(relx= 0.6, rely= 0.1, relwidth= 0.1, relheight= 0.15)
        # Criação do botão alterar
        self.bt_alterar = Button(self.frame_1, text= "Alterar", bd=2, bg = '#107db2', fg='white'
                                , font= ('verdana', 8, 'bold'), command= self.altera_cliente) 
        self.bt_alterar.place(relx= 0.7, rely= 0.1, relwidth= 0.1, relheight= 0.15)
        # Criação do botão apagar
        self.bt_apagar = Button(self.frame_1, text= "Apagar", bd=2, bg = '#107db2', fg='white'
                                , font= ('verdana', 8, 'bold'), command= self.deleta_cliente) 
        self.bt_apagar.place(relx= 0.8, rely= 0.1, relwidth= 0.1, relheight= 0.15)

        # Criação da label e entrada do código
        self.lb_codigo = Label(self.frame_1, text= "Código", bg= '#dfe3ee', fg = '#107db2')
        self.lb_codigo.place(relx= 0.05, rely= 0.05)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx= 0.05, rely= 0.15, relwidth= 0.08)

        # Criação da label e entrada do nome
        self.lb_nome = Label(self.frame_1, text= "Nome", bg= '#dfe3ee', fg = '#107db2')
        self.lb_nome.place(relx= 0.05, rely= 0.35)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx= 0.05, rely= 0.45, relwidth= 0.8) # Os numeros significam a porcentagem

         # Criação da label e entrada do telefone
        self.lb_fone = Label(self.frame_1, text= "Telefone", bg= '#dfe3ee', fg = '#107db2')
        self.lb_fone.place(relx= 0.05, rely= 0.6)

        self.fone_entry = Entry(self.frame_1)
        self.fone_entry.place(relx= 0.05, rely= 0.7, relwidth= 0.4)

         # Criação da label e entrada da cidade
        self.lb_cidade = Label(self.frame_1, text= "Cidade", bg= '#dfe3ee', fg = '#107db2')
        self.lb_cidade.place(relx= 0.5, rely= 0.6)

        self.cidade_entry = Entry(self.frame_1)
        self.cidade_entry.place(relx= 0.5, rely= 0.7, relwidth= 0.4)
    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height= 3, column= ("col1", "col2", "col3", "col4"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Código")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Telefone")
        self.listaCli.heading("#4", text="Cidade")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)

        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')  # Fazer uma barra de rolagem
        self.listaCli.configure(yscroll=self.scroolLista.set) 
        self.scroolLista.place(relx=0.96, rely=0.1,relwidth=0.04, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)
    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label= "Opções", menu = filemenu) # Criação de menu de tarefas  
        menubar.add_cascade(label= "Relatórios", menu = filemenu2) # Criação de menu de tarefas

        filemenu.add_command(label="Sair", command= Quit) # Criação de comando para sair da tela
        filemenu.add_command(label="Limpa Cliente", command= self.limpa_tela) # Criação de comando para limpar a tela

        filemenu2.add_command(label="Ficha do Cliente", command= self.geraRelatCliente)
        
Application()