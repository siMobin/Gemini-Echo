const sendButton = document.getElementById('send-button');
const messageInput = document.getElementById('message-input');
const messagesContainer = document.getElementById('messages');
const mediaInput = document.getElementById('media-input'); // file input for media

sendButton.addEventListener('click', sendMessage);

messageInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    } else if (event.key === 'Enter' && event.shiftKey) {
        messageInput.value += '\n';
    }
});

function sendMessage() {
    const message = messageInput.value.trim();
    const mediaFile = mediaInput ? mediaInput.files[0] : null; // Safely check if mediaInput exists

    if (message === '' && !mediaFile) return; // Don't send if message and media are both empty

    addMessage(message, 'user');
    messageInput.value = ''; // Clear the message input

    const formData = new FormData();
    formData.append("message", message); // Append message to FormData
    if (mediaFile) {
        formData.append("media", mediaFile); // Attach the media file if it exists
    }

    // Debugging: Log FormData to check if it's sending correctly
    for (let [key, value] of formData.entries()) {
        console.log(`${key}: ${value}`);
    }

    // Send the data
    fetch('/chat', {
        method: 'POST',
        body: formData // Send the form data (including media if selected)
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

    mediaInput.value = '';  // Reset the media input field after submitting
}


function addMessage(message, sender) {
    const messageElement = document.createElement('md-block');
    messageElement.classList.add('message');
    messageElement.classList.add(`${sender}-message`);
    messageElement.textContent = message;
    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
