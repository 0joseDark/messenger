import socket
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import os

# Configurações do servidor
HOST = '127.0.0.1'
PORT = 5000
log_file = 'server_log.txt'
usuarios_file = 'usuarios.txt'

# Lista para armazenar conexões de clientes e nomes de usuários
clientes = []
usuarios = {}  # username: senha
conexoes = {}  # username: socket

# Função para carregar os usuários do arquivo
def carregar_usuarios():
    if os.path.exists(usuarios_file):
        with open(usuarios_file, 'r') as file:
            for line in file.readlines():
                username, password = line.strip().split(',')
                usuarios[username] = password

# Função para salvar novo usuário no arquivo
def salvar_usuario(username, password):
    with open(usuarios_file, 'a') as file:
        file.write(f"{username},{password}\n")

# Função para registrar logs no servidor
def registrar_log(mensagem):
    with open(log_file, 'a') as file:
        file.write(mensagem + "\n")

# Função para atualizar a lista de usuários logados na interface gráfica
def atualizar_lista_usuarios():
    lista_usuarios.delete(1.0, tk.END)  # Limpa a lista antes de atualizar
    for user in conexoes.keys():
        lista_usuarios.insert(tk.END, f"{user}\n")

# Função para enviar mensagem para um cliente específico
def enviar_para_cliente(cliente, mensagem):
    try:
        cliente.send(mensagem.encode('utf-8'))
    except:
        cliente.close()
        clientes.remove(cliente)

# Função para tratar mensagens de um cliente
def gerenciar_cliente(cliente, endereco):
    cliente.send("USERNAME".encode('utf-8'))
    username = cliente.recv(1024).decode('utf-8')
    cliente.send("PASSWORD".encode('utf-8'))
    password = cliente.recv(1024).decode('utf-8')

    if username in usuarios and usuarios[username] == password:
        cliente.send("SUCCESS".encode('utf-8'))
        conexoes[username] = cliente  # Associa o socket ao nome de usuário
        clientes.append(cliente)
        registrar_log(f"{username} ({endereco}) entrou no chat.")
        atualizar_lista_usuarios()  # Atualiza a lista de usuários logados
        chat_log.insert(tk.END, f"{username} entrou no chat.\n")
    else:
        cliente.send("FAIL".encode('utf-8'))
        cliente.close()
        return

    while True:
        try:
            msg = cliente.recv(1024).decode('utf-8')
            if msg == "exit":
                registrar_log(f"{username} ({endereco}) saiu do chat.")
                chat_log.insert(tk.END, f"{username} saiu do chat.\n")
                break
            
            # Verifica se a mensagem é privada
            if msg.startswith("PRIVATE:"):
                _, destinatario, mensagem = msg.split(':', 2)
                if destinatario in conexoes:
                    enviar_para_cliente(conexoes[destinatario], f"Mensagem privada de {username}: {mensagem}")
                    chat_log.insert(tk.END, f"{username} (privado para {destinatario}): {mensagem}\n")
                else:
                    enviar_para_cliente(cliente, f"Erro: Usuário {destinatario} não encontrado.")
                    chat_log.insert(tk.END, f"Erro: {username} tentou enviar mensagem para {destinatario}, mas não foi encontrado.\n")
            else:
                # Mensagem pública
                registrar_log(f"{username}: {msg}")
                chat_log.insert(tk.END, f"{username}: {msg}\n")
                for c in clientes:
                    if c != cliente:
                        enviar_para_cliente(c, f"{username}: {msg}")
        except:
            clientes.remove(cliente)
            cliente.close()
            del conexoes[username]  # Remove a conexão do dicionário de conexões
            atualizar_lista_usuarios()  # Atualiza a lista de usuários logados
            break

# Função para iniciar o servidor
def iniciar_servidor():
    global servidor
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()
    carregar_usuarios()
    chat_log.insert(tk.END, "Servidor iniciado. Aguardando conexões...\n")
    
    while True:
        cliente, endereco = servidor.accept()
        thread = threading.Thread(target=gerenciar_cliente, args=(cliente, endereco))
        thread.start()

# Interface gráfica do servidor
def criar_interface_servidor():
    def iniciar():
        threading.Thread(target=iniciar_servidor).start()

    def parar_servidor():
        servidor.close()
        messagebox.showinfo("Servidor", "Servidor parado.")

    def adicionar_usuario():
        username = simpledialog.askstring("Usuário", "Digite o nome do usuário:")
        password = simpledialog.askstring("Senha", "Digite a senha:")
        if username and password:
            usuarios[username] = password
            salvar_usuario(username, password)
            messagebox.showinfo("Usuário", f"Usuário {username} adicionado com sucesso.")

    root = tk.Tk()
    root.title("Servidor")

    # Logs do chat (ScrolledText)
    global chat_log
    chat_log = scrolledtext.ScrolledText(root, state='normal', wrap=tk.WORD, width=50, height=20)
    chat_log.grid(row=0, column=0, padx=10, pady=10)

    # Lista de usuários logados (ScrolledText)
    global lista_usuarios
    lista_usuarios = scrolledtext.ScrolledText(root, state='normal', wrap=tk.WORD, width=30, height=20)
    lista_usuarios.grid(row=0, column=1, padx=10, pady=10)
    lista_usuarios.insert(tk.END, "Usuários logados:\n")

    # Menu do servidor
    menu = tk.Menu(root)
    root.config(menu=menu)

    servidor_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Servidor", menu=servidor_menu)
    servidor_menu.add_command(label="Iniciar", command=iniciar)
    servidor_menu.add_command(label="Parar", command=parar_servidor)

    usuarios_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Usuários", menu=usuarios_menu)
    usuarios_menu.add_command(label="Adicionar usuário", command=adicionar_usuario)

    root.mainloop()

if __name__ == "__main__":
    criar_interface_servidor()
