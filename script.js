let socket;

document.getElementById('connect-btn').addEventListener('click', () => {
    const host = document.getElementById('host').value;
    const port = document.getElementById('port').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
        alert("Por favor, preencha o usuário e a senha.");
        return;
    }

    // Conectar ao servidor WebSocket
    socket = new WebSocket(`ws://${host}:${port}`);

    socket.onopen = () => {
        console.log('Conectado ao servidor');
        socket.send(JSON.stringify({ type: 'auth', username, password }));

        document.getElementById('login-section').classList.add('hidden');
        document.getElementById('chat-section').classList.remove('hidden');
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.type === 'auth' && data.status === 'fail') {
            alert('Autenticação falhou');
            socket.close();
            return;
        }

        const chatLog = document.getElementById('chat-log');
        const messageElement = document.createElement('div');
        messageElement.textContent = `${data.sender}: ${data.message}`;
        chatLog.appendChild(messageElement);
    };

    socket.onclose = () => {
        console.log('Desconectado do servidor');
        document.getElementById('login-section').classList.remove('hidden');
        document.getElementById('chat-section').classList.add('hidden');
    };
});

document.getElementById('send-btn').addEventListener('click', () => {
    const message = document.getElementById('message').value;
    const recipient = document.getElementById('recipient').value;

    if (!message) return;

    const data = {
        type: recipient ? 'private' : 'public',
        message: message,
        recipient: recipient
    };

    socket.send(JSON.stringify(data));
    document.getElementById('message').value = '';
});

document.getElementById('disconnect-btn').addEventListener('click', () => {
    socket.close();
});
