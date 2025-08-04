marked.setOptions({
    gfm: true,
    breaks: true
});

function loadHistory() {
    const historyDiv = document.getElementById("chat-history");
    historyDiv.innerHTML = "";
    const history = JSON.parse(sessionStorage.getItem("chatHistory") || "[]");
    history.forEach(item => {
        const container = document.createElement("div");
        const senderLabel = document.createElement("strong");
        senderLabel.textContent = `${item.sender === "user" ? "You" : "Assistant"}:`;
        const message = document.createElement("div");
        message.innerHTML = marked.parse(item.text);
        container.appendChild(senderLabel);
        container.appendChild(message);
        historyDiv.appendChild(container);
    });
    historyDiv.scrollTop = historyDiv.scrollHeight;
}

function addToHistory(sender, text) {
    const history = JSON.parse(sessionStorage.getItem("chatHistory") || "[]");
    history.push({ sender: sender, text: text });
    sessionStorage.setItem("chatHistory", JSON.stringify(history));
    loadHistory();
}

async function sendMessage() {
    const inputBox = document.getElementById("user-input");
    const message = inputBox.value.trim();
    if (!message) {
        return;
    }

    const sendButton = document.querySelector("button[type='submit']");
    sendButton.disabled = true;

    addToHistory("user", message);
    inputBox.value = "";

    const historyDiv = document.getElementById("chat-history");
    const loadingDiv = document.createElement("div");
    loadingDiv.id = "loading-indicator";
    loadingDiv.innerHTML = "<div class='spinner-border text-primary' role='status'></div><span class='ms-2'>Processing...</span>";
    historyDiv.appendChild(loadingDiv);
    historyDiv.scrollTop = historyDiv.scrollHeight;

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `message=${encodeURIComponent(message)}`
        });

        const data = await response.json();
        loadingDiv.remove();
        addToHistory("assistant", data.response);
    } catch (error) {
        loadingDiv.remove();
        addToHistory("assistant", "An error occurred. Please try again.");
    } finally {
        sendButton.disabled = false;
    }
}

// Enable Enter to send, Shift+Enter to newline
document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.getElementById("user-input");
    loadHistory();

    textarea.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();  // prevent newline
            sendMessage();       // trigger send
        }
    });
});
