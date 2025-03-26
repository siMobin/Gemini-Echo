const sendButton = document.getElementById('send-button');
const messageInput = document.getElementById('message-input');
const messagesContainer = document.getElementById('messages');
const mediaInput = document.getElementById('media-input');
const inputContainer = document.getElementById('input-container');

let mediaPreview = null; // Stores floating preview

sendButton.addEventListener('click', sendMessage);
mediaInput.addEventListener('change', previewMedia);

messageInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    } else if (event.key === 'Enter' && event.shiftKey) {
        messageInput.value += '\n';
    }
});

let fileKeywords = { videos: [], images: [], audios: [] };

fetch('/get-keywords')
    .then(response => response.json())
    .then(data => {
        fileKeywords = data; // Store JSON data globally
    })
    .catch(error => console.error('Error fetching JSON:', error));


function previewMedia() {
    if (mediaPreview) {
        mediaPreview.remove(); // Remove existing preview
    }

    const file = mediaInput.files[0];
    if (!file) return;

    const fileURL = URL.createObjectURL(file);
    const fileType = file.type.split('/')[0];

    mediaPreview = document.createElement('div');
    mediaPreview.classList.add('file-input-preview');
    mediaPreview.innerHTML = `<span class="remove-preview">&times;</span>`; // Close button

    const removePreview = mediaPreview.querySelector('.remove-preview');
    removePreview.addEventListener('click', () => {
        mediaPreview.remove();
        mediaPreview = null;
        mediaInput.value = ''; // Reset file input
    });

    let mediaElement;
    if (fileType === 'image') {
        mediaElement = document.createElement('img');
        mediaElement.src = fileURL;
    } else if (fileType === 'video') {
        mediaElement = document.createElement('video');
        mediaElement.src = fileURL;
        mediaElement.controls = false;
        mediaElement.autoplay = true;
        mediaElement.loop = true;
        mediaElement.muted = false;
    } else if (fileType === 'audio') {
        mediaElement = document.createElement('audio');
        mediaElement.src = fileURL;
        mediaElement.controls = true;
        mediaElement.autoplay = true;
        mediaElement.loop = true;
        mediaElement.muted = false;
    } else if (fileKeywords.documents.includes(`.${file.name.split('.').pop().toLowerCase()}`)) {
        mediaElement = document.createElement('p');
        mediaElement.innerHTML = `<span class="file-icon"><i class="fa-solid fa-file"></i></span> <span class="file-name">${file.name}</span>`;

    } else {
        mediaElement = document.createElement('p');
        mediaElement.textContent = 'Unsupported file type';
    }

    mediaPreview.appendChild(mediaElement);
    document.body.appendChild(mediaPreview); // Make it float above everything

    positionPreview();
}

function positionPreview() {
    if (!mediaPreview) return;
    const rect = inputContainer.getBoundingClientRect();
    mediaPreview.style.top = `${rect.top - 80}px`; // Adjust position above input
    mediaPreview.style.left = `${rect.left + 10}px`; // Align with input
}

function sendMessage() {
    const message = messageInput.value.trim();
    const mediaFile = mediaInput.files.length > 0 ? mediaInput.files[0] : null;

    if (!message && !mediaFile) return;

    const mediaURL = mediaFile ? URL.createObjectURL(mediaFile) : null;
    addMessage(message, 'user', mediaURL, mediaFile ? mediaFile.name : null);

    // Clear input fields
    messageInput.value = '';
    mediaInput.value = '';
    if (mediaPreview) {
        mediaPreview.remove();
        mediaPreview = null;
    }

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
                addMessage(data.response, 'bot', data.media || null, data.mediaName || null, data.image_path || null);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function addMessage(message, sender, media = null, mediaName = null, imagePath = null) {
    const messageWrapper = document.createElement('section');
    messageWrapper.classList.add('message', `${sender}-message`);

    if (message) {
        const textElement = document.createElement('md-block');
        textElement.textContent = message;
        messageWrapper.appendChild(textElement);
    }

    if (media && mediaName) {
        const mediaContainer = document.createElement('div');
        mediaContainer.classList.add('media-container');

        if (message) {
            mediaContainer.appendChild(document.createElement('br'));
        }

        const mediaElement = document.createElement('div');
        const extension = mediaName.split('.').pop().toLowerCase();

        if (fileKeywords.images.includes(`.${extension}`)) {
            mediaElement.innerHTML = `<img src="${media}" alt="">`;
        } else if (fileKeywords.videos.includes(`.${extension}`)) {
            mediaElement.innerHTML = `<video controls><source src="${media}" type="video/${extension}"></video>`;
        } else if (fileKeywords.audios.includes(`.${extension}`)) {
            mediaElement.innerHTML = `<audio controls><source src="${media}" type="audio/${extension}"></audio>`;
        } else if (fileKeywords.documents.includes(`.${extension}`)) {
            mediaElement.innerHTML = `<span class="file-icon"><i class="fa-solid fa-file"></i></span> <span class="file-name">${mediaName}</span>`;
        } else {
            mediaElement.innerHTML = `<p style="color: red; font-weight: bold; font-style: italic; font-size: 12px;">Unsupported file type: ${extension}</p>`;
        }

        mediaContainer.appendChild(mediaElement);
        messageWrapper.appendChild(mediaContainer);
    }

    if (imagePath) {
        const imageElement = document.createElement('a');
        imageElement.href = imagePath;
        imageElement.download = imagePath.split('/').pop();
        imageElement.innerHTML = `<img class="generated-image" src="${imagePath}" alt="Generated Image">`;
        messageWrapper.appendChild(imageElement);
    }

    messagesContainer.appendChild(messageWrapper);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
