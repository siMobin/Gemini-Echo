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
    const mediaFile = mediaInput.files.length > 0 ? mediaInput.files[0] : null;

    if (!message && !mediaFile) return;

    // Convert media file to a temporary URL for preview
    const mediaURL = mediaFile ? URL.createObjectURL(mediaFile) : null;

    // Ensure message and media stay together under 'user'
    addMessage(message, 'user', mediaURL, mediaFile ? mediaFile.name : null);

    // Clear input fields
    messageInput.value = '';
    mediaInput.value = '';

    // Send to server
    const formData = new FormData();
    formData.append("message", message);
    if (mediaFile) {
        formData.append("media", mediaFile);
    }

    fetch('/chat', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                addMessage(data.response, 'bot', data.media || null, data.mediaName || null);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function addMessage(message, sender, media = null, mediaName = null) {
    const messageWrapper = document.createElement('section');
    messageWrapper.classList.add('message', `${sender}-message`);

    // Append text if available
    if (message) {
        const textElement = document.createElement('md-block');
        textElement.textContent = message;
        messageWrapper.appendChild(textElement);
    }

    // Append media
    if (media && mediaName) {
        const mediaContainer = document.createElement('div');
        mediaContainer.classList.add('media-container');

        if (message) {
            mediaContainer.appendChild(document.createElement('br')); // Add break if there's text
        }

        const mediaElement = document.createElement('div');
        const extension = mediaName.split('.').pop().toLowerCase();

        if (['png', 'jpg', 'jpeg', 'gif', 'webp'].includes(extension)) {
            mediaElement.innerHTML = `<img src="${media}" alt="">`;
        } else if (['mp4', 'webm', 'ogg'].includes(extension)) {
            mediaElement.innerHTML = `<video controls><source src="${media}" type="video/${extension}"></video>`;
        } else if (['mp3', 'wav', 'ogg'].includes(extension)) {
            mediaElement.innerHTML = `<audio controls><source src="${media}" type="audio/${extension}"></audio>`;
        } else {
            mediaElement.innerHTML = `<p style="color: red; font-weight: bold; font-style: italic; font-size: 12px;">Unsupported file type: ${extension}</p>`;
        }

        mediaContainer.appendChild(mediaElement);
        messageWrapper.appendChild(mediaContainer);
    }

    messagesContainer.appendChild(messageWrapper);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
