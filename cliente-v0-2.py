import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

# Função para gerenciar a recepção de mensagens
def receber_mensagens(cliente_socket):
    while True:
        try:
            mensagem = cliente_socket.recv(1024).decode('utf-8')
            if mensagem == "USERNAME":
                cliente_socket.send(username.encode('utf-8'))
            elif mensagem == "PASSWORD":
                cliente_socket.send(password.encode('utf-8'))
            elif mensagem == "SUCCESS":
                chat_log.insert(tk.END, "Autenticação bem-sucedida.\n")
            elif mensagem == "FAIL":
                chat_log.insert(tk.END, "Falha na autenticação.\n")
                cliente_socket.close()
                break
            else:
                chat_log.insert(tk.END, mensagem + "\n")
        except:
            chat_log.insert(tk.END, "Erro ao receber mensagem. Conexão encerrada.\n")
            cliente_socket.close()
            break

# Função para enviar uma mensagem
def enviar_mensagem():
    mensagem = entrada_msg.get()
    destinatario = entrada_dest.get()  # Destinatário
    entrada_msg.delete(0, tk.END)
    if destinatario:
        mensagem = f"PRIVATE:{destinatario}:{mensagem}"  # Formato da mensagem privada
    try:
        cliente_socket.send(mensagem.encode('utf-8'))
    except:
        chat_log.insert(tk.END, "Erro ao enviar mensagem.\n")

# Função para conectar ao servidor
def conectar_servidor():
    global cliente_socket, username, password
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((HOST, PORT))

    username = simpledialog.askstring("Usuário", "Digite seu nome de usuário:")
    password = simpledialog.askstring("Senha", "Digite sua senha:")

    thread_receber = threading.Thread(target=receber_mensagens, args=(cliente_socket,))
    thread_receber.start()

# Interface gráfica do cliente
def criar_interface_cliente():
    root = tk.Tk()
    root.title("Cliente")

    # Log do chat
    global chat_log
    chat_log = scrolledtext.ScrolledText(root, state='normal', wrap=tk.WORD, width=50, height=20)
    chat_log.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    # Entrada de mensagens
    global entrada_msg
    entrada_msg = tk.Entry(root, width=40)
    entrada_msg.grid(row=1, column=0, padx=10, pady=10)

    # Botão para enviar mensagem
    botao_enviar = tk.Button(root, text="Enviar", command=enviar_mensagem)
    botao_enviar.grid(row=1, column=1, padx=10, pady=10)

    # Entrada de destinatário
    global entrada_dest
    entrada_dest = tk.Entry(root, width=40)
    entrada_dest.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
    entrada_dest.insert(0, "Nome do destinatário (para mensagens privadas)")

    # Menu para conectar ao servidor
    menu = tk.Menu(root)
    root.config(menu=menu)

    servidor_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Servidor", menu=servidor_menu)
    servidor_menu.add_command(label="Conectar", command=conectar_servidor)

    root.mainloop()

if __name__ == "__main__":
    HOST = '192.168.0.11'
    PORT = 5000
    criar_interface_cliente()
