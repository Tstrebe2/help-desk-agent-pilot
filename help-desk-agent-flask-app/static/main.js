async function sendMessage() {
    const message = document.getElementById("user-input").value;
    const responseDiv = document.getElementById("response");

    responseDiv.innerHTML = "<em>Thinking...</em>";

    const response = await fetch("/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `message=${encodeURIComponent(message)}`
    });

    const data = await response.json();
    responseDiv.textContent = data.response;
    document.getElementById("user-input").value = "";
}

// Enable Enter to send, Shift+Enter to newline
document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.getElementById("user-input");

    textarea.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();  // prevent newline
            sendMessage();       // trigger send
        }
    });
});