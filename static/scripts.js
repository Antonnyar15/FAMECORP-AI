// Função para enviar a mensagem
function sendMessage() {
    const userMessageInput = document.getElementById("userMessage");
    const sendBtn = document.getElementById("sendBtn");

    const userMessage = userMessageInput.value;

    if (userMessage.trim() !== "") {
        displayMessage(userMessage, 'user');
        userMessageInput.value = "";

        // Desabilitar envio e mostrar "aguarde"
        sendBtn.disabled = true;
        userMessageInput.disabled = true;
        document.getElementById("waitingMessage").style.display = "block";
        startDots();

        // Enviar para o Flask
        fetch("/send_message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: userMessage }),
        })
        .then(response => response.json())
        .then(data => {
            displayMessage(data.response, 'bot');
        })
        .catch(error => {
            console.error("Erro:", error);
            displayMessage("Ocorreu um erro. Tente novamente.", 'bot');
        })
        .finally(() => {
            // Reabilitar envio e esconder "aguarde"
            sendBtn.disabled = false;
            userMessageInput.disabled = false;
            document.getElementById("waitingMessage").style.display = "none";
            stopDots();
            userMessageInput.focus();
        });
    }
}

// Exibir mensagem no chat
function displayMessage(message, sender) {
    const chatBox = document.getElementById("chatBox");
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", sender);
    messageElement.innerText = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Detectar Enter
function handleKeyPress(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Animação de "..."
let dotInterval;
let dotCount = 0;

function startDots() {
    dotCount = 0;
    dotInterval = setInterval(() => {
        dotCount = (dotCount + 1) % 4;
        document.getElementById("dots").textContent = ".".repeat(dotCount);
    }, 500);
}

function stopDots() {
    clearInterval(dotInterval);
    document.getElementById("dots").textContent = "";
}

// Iniciar com mensagem da IA
window.onload = function () {
    displayMessage("FAME está pronta para conversar! ✨", 'bot');
};
