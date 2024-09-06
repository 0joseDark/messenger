import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

# Configurações iniciais padrão (podem ser alteradas pelo usuário via menu)
HOST = '127.0.0.1'
PORT = 5000

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
            print("Erro ao receber mensagem.")
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
        messagebox.showerror("Erro", "Não foi possível enviar a mensagem.")

# Função para conectar ao servidor
def conectar():
    global cliente_socket, username, password
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((HOST, PORT))
        
        username = simpledialog.askstring("Usuário", "Digite o nome de usuário:")
        password = simpledialog.askstring("Senha", "Digite a senha:", show="*")

        # Thread para receber mensagens
        thread_receber = threading.Thread(target=receber_mensagens, args=(cliente_socket,))
        thread_receber.start()
        messagebox.showinfo("Conexão", "Conectado ao servidor com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao conectar: {e}")

# Função para definir Host e Porta via Menu
def definir_host():
    global HOST
    HOST = simpledialog.askstring("Host", "Digite o endereço do Host:")
    if HOST:
        messagebox.showinfo("Host", f"Host configurado para {HOST}")

def definir_porta():
    global PORT
    try:
        PORT = int(simpledialog.askstring("Porta", "Digite a porta:"))
        messagebox.showinfo("Porta", f"Porta configurada para {PORT}")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido para a porta.")

# Interface gráfica do cliente
def criar_interface_cliente():
    global entrada_msg, chat_log, entrada_dest
    
    root = tk.Tk()
    root.title("Cliente Messenger")

    chat_log = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD, width=50, height=20)
    chat_log.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    tk.Label(root, text="Mensagem:").grid(row=1, column=0, padx=10, pady=5)
    entrada_msg = tk.Entry(root, width=30)
    entrada_msg.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Destinatário (opcional):").grid(row=2, column=0, padx=10, pady=5)
    entrada_dest = tk.Entry(root, width=30)
    entrada_dest.grid(row=2, column=1, padx=10, pady=5)

    botao_enviar = tk.Button(root, text="Enviar", command=enviar_mensagem)
    botao_enviar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Botão para conectar ao servidor
    botao_conectar = tk.Button(root, text="Ligar ao Servidor", command=conectar)
    botao_conectar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Menu do cliente
    menu = tk.Menu(root)
    root.config(menu=menu)

    # Menu Conexão com opções de Host e Porta
    conexao_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Conexão", menu=conexao_menu)
    conexao_menu.add_command(label="Definir Host", command=definir_host)
    conexao_menu.add_command(label="Definir Porta", command=definir_porta)
    conexao_menu.add_command(label="Ligar ao Servidor", command=conectar)

    root.mainloop()

if __name__ == "__main__":
    criar_interface_cliente()
