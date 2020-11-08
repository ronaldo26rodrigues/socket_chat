import tkinter
import socket
from threading import Thread



HOST = 'localhost'              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)

def connect():
    global con
    con, cliente = tcp.accept()
    con.send(str('conectado').encode())
    print('Conectado por', cliente)
    janela.title(f'Server (Host) - Conectado por {cliente[0]}')

def receive():
    while True:
        connect()
        while True:
            try:
                data = con.recv(1024).decode()
            except:
                break
            if data != '':
                #print("data")
                if data == 'closecon98':
                    con.close()
                    print('aaaaaaaaaaaaaaababababbababa')
                    break
                txt.insert('end', '\n' + data)
                txt.see('end')
                print(data)
        txt.insert('end', '\nConexão encerrada')
        print('encerrando conexão')
        con.close()


def sendmsg(msg):
    try:
        con.send(str('Server (Host)=>' + msg).encode())
        print(con)
    except:
        pass

def envio_enter(event):
    msg = text.get()
    if msg != "":
        txt.insert('end', "\nVocê (Host) => " + msg)
        sendmsg(msg)
        txt.see("end")
        text.delete(0, 'end')
        print(msg)

def envio():
    msg = text.get()
    if msg != "":
        txt.insert('end', "\n" + msg)
        sendmsg(msg)
        txt.see("end")
        text.delete(0, 'end')
        print(msg)


janela = tkinter.Tk()
janela.geometry("500x500")
janela["bg"] = "pink"




#con, cliente = tcp.accept()

txt = tkinter.Text(janela)
txt["bg"] = "cyan"
txt.place(relx=0.01, rely=0.01)

text = tkinter.Entry(janela)
text.place(relx=0.2, rely=0.9, height=25, width=300)

button = tkinter.Button(janela, text="enviar", command=envio)
button.place(bordermode= "outside",relx=0.82, rely=0.9, height=25, width=75)

janela.bind('<Return>', envio_enter)

receive_thread = Thread(target=receive)
receive_thread.start()



janela.mainloop()
