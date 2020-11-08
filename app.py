import tkinter
import socket
from threading import Thread

janela = tkinter.Tk()
janela.title('Client')
janela.geometry("500x500")
janela["bg"] = "cyan"

SERVER = 'localhost'
NOME = 'CLIENT'
HOST = SERVER

def receive():
    while True:
        try:
            data = tcp.recv(1024)
            if data.decode() == '':
                break
            txt.insert('end', '\n' + data.decode())
            txt.see('end')
            print(data.decode())
        except:
            pass


def sendmsg(msg, name):
    try:
        tcp.send(str(name + ' => ' + msg).encode())
    except:
        txt.insert('end', '\n ERRO: Algo teu errado')


def envio_enter(event):
    msg = text.get()
    if msg != "":
        txt.insert('end', "\nVocê => " + msg)
        sendmsg(msg, NOME)
        txt.see("end")
        text.delete(0, 'end')
        print(msg)

def envio():
    msg = text.get()
    if msg != "":
        txt.insert('end', "\nVocê => " + msg)
        sendmsg(msg, NOME)
        txt.see("end")
        text.delete(0, 'end')
        print(msg)

def configWindow():

    def configip():
        global NOME
        if nameEntry.get() != '':
            NOME = nameEntry.get()
        SERVER = ipConfigEntry.get()
        if SERVER != '':
            close()
            connect(SERVER)
        newWindow.destroy()


    newWindow = tkinter.Toplevel(janela)
    newWindow.geometry('170x160')
    tkinter.Label(newWindow, text=f"ip do host - Atual = {HOST}").pack(pady=5)
    ipConfigEntry = tkinter.Entry(newWindow)
    tkinter.Label(newWindow, text=f'Seu nome - Atual = {NOME}').pack(pady=26)
    nameEntry = tkinter.Entry(newWindow)
    nameEntry.place(x=20, y=78, height=25)
    ipButton = tkinter.Button(newWindow, text='ok', command=configip)
    ipButton.place(relx=0.7, rely=0.7, width=30, height=30)
    ipConfigEntry.place(x=20, y=30, height=25)

def close():
    try:
        janela.title(f'{NOME} - Sem conexão')
        tcp.close()
    except:
        pass

def connect(host):
    global HOST
    HOST = host               # Endereco IP do Servidor
    print(type(HOST))
    PORT = 5000                 # Porta que o Servidor esta
    global tcp
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    try:
        tcp.connect(dest)
        janela.title(f'{NOME} - Conectado a {HOST}')
    except:
        configWindow()


txt = tkinter.Text(janela)
txt["bg"] = "cyan"
txt.place(relx=0.01, rely=0.01, width=480)

text = tkinter.Entry(janela)
text.place(relx=0.2, rely=0.9, height=25, width=300)

button = tkinter.Button(janela, text="enviar", command=envio)
button.place(bordermode= "outside",relx=0.82, rely=0.9, height=25, width=75)

main_menu = tkinter.Menu(janela)
main_menu.add_command(label='config', command=configWindow)
main_menu.add_command(label='close', command=close)
janela.config(menu=main_menu)

janela.bind('<Return>', envio_enter)


receive_thread = Thread(target=receive)

receive_thread.start()

janela.mainloop()
sendmsg('closecon98', NOME)
close()
