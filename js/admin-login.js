const form = document.getElementById("admin-login-form");
const loginMsg = document.getElementById("login-msg");

function getApiBase() {
    const isArquivoLocal = window.location.protocol === "file:";
    const isLocalhost = ["127.0.0.1", "localhost"].includes(window.location.hostname);

    if (isArquivoLocal || isLocalhost) {
        return "http://127.0.0.1:8000";
    }

    return "";
}

const API_BASE = getApiBase();

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    loginMsg.textContent = "";

    try {
        const response = await fetch(`${API_BASE}/admin/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({ username, password })
        });

        const texto = await response.text();
        console.log("STATUS LOGIN:", response.status);
        console.log("RESPOSTA LOGIN:", texto);

        let data;
        try {
            data = JSON.parse(texto);
        } catch {
            data = null;
        }

        if (!response.ok || !data || !data.success) {
            loginMsg.textContent =
                (data && (data.detail || data.mensagem)) ||
                `Erro no login (${response.status})`;
            return;
        }

        window.location.href = "upload.html";

    } catch (error) {
        console.error("ERRO LOGIN:", error);
        loginMsg.textContent = "Erro de conexão com o servidor.";
    }
});