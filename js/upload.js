document.addEventListener("DOMContentLoaded", async () => {
    const dropArea = document.getElementById("drop-area");
    const fileInput = document.getElementById("fileInput");
    const fileName = document.getElementById("file-name");
    const btnEnviar = document.getElementById("btn-enviar");
    const uploadMsg = document.getElementById("upload-msg");

    let arquivoSelecionado = null;

    try {
        const authResponse = await fetch("http://127.0.0.1:8000/admin/me", {
            method: "GET",
            credentials: "include"
        });

        if (!authResponse.ok) {
            window.location.href = "admin-login.html";
            return;
        }

        const authData = await authResponse.json();
        if (!authData.success || !authData.is_admin) {
            window.location.href = "admin-login.html";
            return;
        }

    } catch (error) {
        window.location.href = "admin-login.html";
        return;
    }

    if (!dropArea || !fileInput || !fileName || !btnEnviar || !uploadMsg) {
        console.error("Elementos da tela de upload não encontrados.");
        return;
    }

    dropArea.addEventListener("click", () => {
        fileInput.click();
    });

    dropArea.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            fileInput.click();
        }
    });

    fileInput.addEventListener("change", () => {
        if (fileInput.files.length > 0) {
            definirArquivo(fileInput.files[0]);
        }
    });

    ["dragenter", "dragover"].forEach((eventName) => {
        dropArea.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropArea.classList.add("dragover");
        });
    });

    ["dragleave", "drop"].forEach((eventName) => {
        dropArea.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropArea.classList.remove("dragover");
        });
    });

    dropArea.addEventListener("drop", (e) => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            definirArquivo(files[0]);
        }
    });

    function definirArquivo(file) {
        if (!file.name.toLowerCase().endsWith(".csv")) {
            arquivoSelecionado = null;
            fileInput.value = "";
            fileName.textContent = "Arquivo inválido. Envie um CSV.";
            uploadMsg.textContent = "";
            uploadMsg.className = "upload-msg erro";
            return;
        }

        arquivoSelecionado = file;
        fileName.textContent = file.name;
        uploadMsg.textContent = "";
        uploadMsg.className = "upload-msg";
    }

    btnEnviar.addEventListener("click", enviarArquivo);

    async function enviarArquivo() {
        if (!arquivoSelecionado) {
            uploadMsg.textContent = "Selecione um arquivo CSV antes de enviar.";
            uploadMsg.className = "upload-msg erro";
            return;
        }

        const formData = new FormData();
        formData.append("file", arquivoSelecionado);

        btnEnviar.disabled = true;
        btnEnviar.textContent = "Enviando...";
        uploadMsg.textContent = "";
        uploadMsg.className = "upload-msg";

        try {
            const response = await fetch("http://127.0.0.1:8000/upload-planilha", {
                method: "POST",
                credentials: "include",
                body: formData
            });

            const texto = await response.text();

            let data;
            try {
                data = JSON.parse(texto);
            } catch {
                data = null;
            }

            if (!response.ok) {
                uploadMsg.textContent =
                    (data && (data.detail || data.mensagem)) ||
                    `Erro no servidor (${response.status})`;
                uploadMsg.className = "upload-msg erro";
                return;
            }

            if (!data || !data.success) {
                uploadMsg.textContent =
                    (data && (data.detail || data.mensagem)) ||
                    "Erro ao enviar planilha.";
                uploadMsg.className = "upload-msg erro";
                return;
            }

            uploadMsg.textContent = "Planilha enviada, substituída e importada com sucesso.";
            uploadMsg.className = "upload-msg sucesso";

            arquivoSelecionado = null;
            fileInput.value = "";
            fileName.textContent = "Nenhum arquivo selecionado";

        } catch (error) {
            console.error("ERRO FETCH UPLOAD:", error);
            uploadMsg.textContent = "Erro de conexão com o servidor.";
            uploadMsg.className = "upload-msg erro";
        } finally {
            btnEnviar.disabled = false;
            btnEnviar.textContent = "Enviar planilha";
        }
    }
});

const btnLogout = document.getElementById("btn-logout");

if (btnLogout) {
    btnLogout.addEventListener("click", async () => {
        await fetch("http://127.0.0.1:8000/admin/logout", {
            method: "POST",
            credentials: "include"
        });

        window.location.href = "admin-login.html";
    });
}