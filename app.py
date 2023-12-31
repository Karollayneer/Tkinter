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
    def printCliente(self):
        webbrowser.open("cliente.pdf")
    def gerandoRelatClente(self):
        self.c = canvas.Canvas("cliente.pdf")

        self.codRel = self.cod_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.telRel = self.tel_entry.get()
        self.cidRel = self.cid_entry.get()
       
        self.c.setFont("Helvetica-Bold",24)
        self.c.drawString(200, 790, 'Ficha do Cliente')

        self.c.setFont("Helvetica-Bold",19)
        self.c.drawString(50,700, 'Codigo: ')
        self.c.drawString(50,670, 'Nome: ' )
        self.c.drawString(50,640, 'Telefone: ')
        self.c.drawString(50,610, 'Cidade: ')

        self.c.setFont("Helvetica",16)
        self.c.drawString(150,700, self.codRel)
        self.c.drawString(150,670, self.nomeRel)
        self.c.drawString(150,640, self.telRel)
        self.c.drawString(150,610, self.cidRel)

        self.c.rect(20, 720, 550, 200, fill=False, stroke=True)

        self.c.rect(20, 550, 550, 1, fill=False, stroke=True)

        self.c.showPage()
        self.c.save()
        self.printCliente()

class Funcs():
    def limpa_tela(self):
        self.cod_entry.delete(0,END)
        self.nome_entry.delete(0,END)
        self.tel_entry.delete(0,END)
        self.cid_entry.delete(0,END)
    def conecta_bd (self):
        self.conn = sqlite3.connect("CLientes.bd")
        self.cursor = self.conn.cursor(); print ("banco de dados criado")
    def desconectar_bd(self):
        self.conn.close() ; print ("Desconectando banco de dados")
    def montaTabelas(self):
        self.conecta_bd(); print("conectando ao banco de dados.")
        #criando tabela
        self.cursor.execute ("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                telefone iNTEGER(20),
                cidade CHAR(40)
            );
        """)
        self.conn.commit()
        self.desconectar_bd()
    def variaveis(self):
        self.cod = self.cod_entry.get()
        self.nome = self.nome_entry.get()
        self.tel = self.tel_entry.get()
        self.cid = self.cid_entry.get()
    def add_cliente(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO clientes(nome_cliente, telefone, cidade)
            VALUES(?, ?, ?)""", (self.nome, self.tel, self.cid))
        self.conn.commit()
        self.desconectar_bd()
        self.select_lista()
        self.limpa_tela()
    def select_lista(self):
        self.ListaCli.delete(*self.ListaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes
            ORDER BY cod DESC; """)

        for i in lista:
            self.ListaCli.insert("",END, values=i)
        self.desconectar_bd()
    def busca_cliente(self):
        self.conecta_bd()
        self.ListaCli.delete(*self.ListaCli.get_children())
        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(
            """SELECT cod, nome_cliente, telefone, cidade FROM clientes
            WHERE nome_cliente LIKE ? ORDER BY nome_cliente ASC""", ('%' + nome,))

        buscarnomeCli = self.cursor.fetchall()
        for i in buscarnomeCli:
            self.ListaCli.insert("", END, values=i)
        self.limpa_tela()

        self.desconectar_bd()
    def OnDoubleClick(self, event):
        self.limpa_tela()
        self.ListaCli.selection()
        for n in self.ListaCli.selection():
            col1, col2, col3, col4 = self.ListaCli.item(n, 'values')
            self.cod_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.tel_entry.insert(END, col3)
            self.cid_entry.insert(END, col4)
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ?""", (self.cod,))
        self.conn.commit()
        self.desconectar_bd()
        self.limpa_tela()
        self.select_lista()
    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""UPDATE clientes SET nome_cliente =?, telefone =?, cidade =? 
            WHERE cod=? """, (self.nome, self.tel, self.cid, self.cod))
        self.conn.commit()
        self.desconectar_bd()
        self.select_lista()
        self.limpa_tela()
    def Menus (self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label="Opções", menu= filemenu)
        menubar.add_cascade(label="Relatorios", menu= filemenu2)

        filemenu.add_command(label="Sair", command= Quit)
        filemenu.add_command(label="Limpar cliente", command=self.limpa_tela)

        filemenu2.add_command(label="ficha do cliente", command=self.gerandoRelatClente)

class Application(Funcs, Relatorios):
    def __init__(self):
        self.root = root
        self.tela( )
        self.frame_da_tela()
        self.criando_botoes()
        self.lis_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()

        root.mainloop()

    def tela (self):
        self.root.title("Cadastro Cliente")
        self.root.configure(background='#34344e')
        self.root.geometry("788x588")
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=500, height=400)

    def frame_da_tela (self):
        self.frame_1 = Frame(self.root, bd = 4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=3)
        self.frame_1.place(relx= 0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.root, bd = 4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=2)
        self.frame_2.place(relx= 0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def criando_botoes(self):
        self.canvas_bt = Canvas(self.frame_1, bd=0, bg= '#1e3743', highlightbackground = 'gray',
            highlightthickness=3)
        self.canvas_bt.place(relx=0.19, rely=0.08, relwidth=0.22, relheight=0.19)

        self.bt_limpar = Button(self.frame_1, text='Limpar', bd=4, bg= '#107bd2', fg= 'white',
                                activebackground='#108ecb', activeforeground="white"
                                , font=( 'verdana',8,'bold'),command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_buscar = Button(self.frame_1, text='Buscar', bd=4, bg= '#107bd2', fg= 'white', font=( 'verdana',8,'bold'), command=self.busca_cliente)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_novo = Button(self.frame_1, text='Novo', bd=4, bg= '#107bd2', fg= 'white', font=( 'verdana',8,'bold'),command=self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)

        

        self.bt_alterar = Button(self.frame_1, text='Alterar', bd=4, bg= '#107bd2', fg= 'white', font=( 'verdana',8,'bold'),command=self.altera_cliente)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_apagar = Button(self.frame_1, text='Apagar', bd=4, bg= '#107bd2', fg= 'white', font=( 'verdana',8,'bold'),command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

            #Criando label cod
        self.lb_cod = Label(self.frame_1, text='Codigo', bg='#dfe3ee' )
        self.lb_cod.place(relx=0.05, rely=0.05 )
        self.cod_entry = Entry(self.frame_1,)
        self.cod_entry.place(relx=0.05, rely=0.15, relwidth=0.08, relheight=0.08 )
         
            #Criando label nome
        self.lb_nome = Label(self.frame_1, text='Nome', bg='#dfe3ee' )
        self.lb_nome.place(relx=0.05, rely=0.35 )
        self.nome_entry = Entry(self.frame_1,)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.8, )

            #Criando label telefone
        self.lb_tel = Label(self.frame_1, text='Telefone', bg='#dfe3ee' )
        self.lb_tel.place(relx=0.05, rely=0.6 )
        self.tel_entry = Entry(self.frame_1,)
        self.tel_entry.place(relx=0.05, rely=0.7, relwidth=0.4, )

            #Criando label cidade
        self.lb_cid = Label(self.frame_1, text='Cidade', bg='#dfe3ee' )
        self.lb_cid.place(relx=0.5, rely=0.6 )
        self.cid_entry = Entry(self.frame_1,)
        self.cid_entry.place(relx=0.5, rely=0.7, relwidth=0.4, )

    def lis_frame2(self):
        self.ListaCli = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4"))
        self.ListaCli.heading("#0", text="")
        self.ListaCli.heading("#1", text="Codigo")
        self.ListaCli.heading("#2", text="Nome")
        self.ListaCli.heading("#3", text="Telefone")
        self.ListaCli.heading("#4", text="Cidade")

        self.ListaCli.column("#0", width=1)
        self.ListaCli.column("#1", width=50)
        self.ListaCli.column("#2", width=200)
        self.ListaCli.column("#3", width=125)
        self.ListaCli.column("#4", width=125)

        self.ListaCli.place(relx=0.01,rely=0.1, relwidth=0.95, relheight=.85)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.ListaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.ListaCli.bind("<Double-1>",self.OnDoubleClick)



Application()