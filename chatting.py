import tkinter
from tkinter import messagebox
import socket
from threading import Thread
from functools import partial
import sys

HOST = 'localhost'  # Endereco IP do Servidor
PORT = 5000         # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)


SERVER = 'localhost'
NOME = 'CLIENT'
HOST = SERVER

janela = tkinter.Tk()
janela.title('Chatting - bem vindo')
janela.geometry("500x500")
janela["bg"] = "cyan"

def receive(mode):
    """
    Mode code:
    0: Host \n
    1: Client \n
    2: closing
    """
    print('thread iniciada ' + str(set_mode))
    # client mode
    while True:
        while mode == 1:
            print('client iniciado')
            try:
                try:
                    data = tcp.recv(1024)
                except:
                    break
                print('erro')
                if data.decode() == '':
                    break
                txt.insert('end', '\n' + data.decode())
                txt.see('end')
                print(data.decode())
            except:
                break

        # host mode
        while mode == 0:
            print('hostmode')
            host()
            while True:
                try:

                    data = con.recv(1024).decode()
                except:
                    pass
                if data != '':
                    if data[-10:] == 'closecon98':
                        con.close()
                        main_menu.add_command(label='Host', command=init_host)
                        janela.title('Server - sem conexão')
                        break
                    txt.insert('end', '\n' + data)
                    txt.see('end')
                    print(data)
            txt.insert('end', '\nConexão encerrada')
            print('encerrando conexão')
            con.close()
            break
        if mode == 3:
            break
        break
        # closing

def connect(host):
    global HOST
    HOST = host  # Endereco IP do Servidor
    print(host)
    PORT = 5000  # Porta que o Servidor esta
    global tcp
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    try:
        tcp.connect(dest)
        receive_args = partial(receive, set_mode)
        receive_thread = Thread(target=receive_args)
        receive_thread.start()
        janela.title(f'{NOME} - Conectado a {HOST}')
    except:
        configWindow()

def sendmsg(mode, msg, name):
    if mode == 0:
        try:
            con.send(str('Server (Host)=>' + msg).encode())
            print(con, 'banana')
        except:
            pass

    if mode == 1:
        try:
            tcp.send(str(name + ' => ' + msg).encode())
        except:
            try:
                txt.insert('end', '\n ERRO: Algo teu errado')
            except:
                pass

def envio(mode):
    msg = text.get()
    print(mode)
    if msg != "":
        if mode == 0:
            txt.insert('end', "\n" + msg)
            sendmsg(set_mode, msg, NOME)
            txt.see("end")
            text.delete(0, 'end')
            print(msg)
        if mode == 1:
            txt.insert('end', "\nVocê => " + msg)
            sendmsg(set_mode, msg, NOME)
            txt.see("end")
            text.delete(0, 'end')
            print(msg)

def envio_enter(event):
    envio(set_mode)

def configWindow():

    def configip():
        global set_mode
        set_mode = 1
        SERVER = ipConfigEntry.get()
        if SERVER != '':
            close()
            connect(SERVER)
        # if set_mode == 0:
        #     connect(set_mode, SERVER)
        newWindow.destroy()

    # def setMode():
    #
    #     def setModeBut():
    #
    #         if modelist.get('anchor') == 'Host':
    #             set_mode = 0
    #         if modelist.get('anchor') == 'Client':
    #             set_mode = 1
    #         modeWin.destroy()
    #
    #
    #     modeWin = tkinter.Toplevel(newWindow)
    #     tkinter.Button(modeWin, text='ok', command=setModeBut).place(relx=0.35, y=50, height=40, width=40)
    #     modeWin.geometry('40x100')
    #     modelist = tkinter.Listbox(modeWin, selectmode='single', height=2, y=10)
    #     modelist.insert('end', 'Host')
    #     modelist.insert('end', 'Client')
    #     modelist.pack()



    newWindow = tkinter.Toplevel(janela)
    newWindow.geometry('170x160')
    tkinter.Label(newWindow, text=f"ip do host - Atual = {HOST}").pack(pady=5)
    ipConfigEntry = tkinter.Entry(newWindow)
    ipConfigEntry.place(x=20, y=30, height=25)

    # tkinter.Button(newWindow, text='mudar modo', command=setMode).place(x=20, y=120, width=120, height=30)
    ipButton = tkinter.Button(newWindow, text='ok', command=configip)
    ipButton.place(relx=0.7, rely=0.7, width=30, height=30)

def close():

    try:
        tcp.send('closecon98'.encode())
        con.send('closecon98'.encode())
        tcp.close()
        print('apagooooo')
    except:
        pass
    try:
        tcp.send('closecon98'.encode())
        con.send('closecon98'.encode())
        con.close()
        print('apapapapa')
    except:
        pass
    try:
        main_menu.delete('Host')
    except:
        janela.title(f'{NOME} - Sem conexão')
        main_menu.add_command(label='Host', command=init_host)

def host():
    print('hostclick')
    global con
    messagebox.showinfo(title='aguarde', message='aguardando conexão')
    con, cliente = tcp.accept()
    print('conectando')
    con.send(str('conectado').encode())
    print('Conectado por', cliente)
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    janela.title(f'Server (Hospedando em {local_ip}) - Conectado por {cliente[0]}')

def init_host():

    global set_mode
    set_mode = 0
    global tcp
    global HOST
    HOST = ''
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(1)
    receive_args = partial(receive, set_mode)
    receive_thread = Thread(target=receive_args)
    receive_thread.start()
    main_menu.delete("Host")

def profile():

    def profileEnd():
        global NOME

        if nameEntry.get() != '':
            NOME = nameEntry.get()

    profileWin = tkinter.Toplevel(janela)
    profileWin.geometry('170x160')
    tkinter.Label(profileWin, text=f'Seu nome - Atual = {NOME}').pack(pady=26)
    nameEntry = tkinter.Entry(profileWin)
    nameEntry.place(x=20, y=78, height=25)

    profileButton = tkinter.Button(profileWin, text='ok', command=profileEnd)
    profileButton.place(relx=0.7, rely=0.7, width=30, height=30)

txt = tkinter.Text(janela)
txt["bg"] = "cyan"
txt.place(relx=0.01, rely=0.01, width=480)

text = tkinter.Entry(janela)
text.place(relx=0.2, rely=0.9, height=25, width=300)

button = tkinter.Button(janela, text="enviar", command= lambda: envio(set_mode))
button.place(bordermode= "outside",relx=0.82, rely=0.9, height=25, width=75)

main_menu = tkinter.Menu(janela)
main_menu.add_command(label='Perfil', command=profile)
main_menu.add_command(label='Conectar', command=configWindow)
main_menu.add_command(label='close', command=close)
main_menu.add_command(label='Host', command=init_host)

janela.config(menu=main_menu)
janela.bind('<Return>', envio_enter)

janela.mainloop()

try:
    sendmsg(set_mode, 'closecon98', NOME)
    close()
except:
    pass

close = True
sys.exit()
