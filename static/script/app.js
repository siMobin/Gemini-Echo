const sendButton = document.getElementById('send-button');
const messageInput = document.getElementById('message-input');
const messagesContainer = document.getElementById('messages');

sendButton.addEventListener('click', sendMessage);

// Handle the "Enter" and "Shift+Enter" behavior
messageInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        // Prevent default Enter behavior (which is to add a new line)
        event.preventDefault();
        sendMessage();
    } else if (event.key === 'Enter' && event.shiftKey) {
        // Allow Shift+Enter to insert a new line
        messageInput.value += '\n';
    }
});

function sendMessage() {
    const message = messageInput.value.trim();
    if (message === '') return;

    addMessage(message, 'user');
    messageInput.value = '';

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                addMessage(data.response, 'bot');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function addMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add(`${sender}-message`);
    messageElement.textContent = message;
    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
