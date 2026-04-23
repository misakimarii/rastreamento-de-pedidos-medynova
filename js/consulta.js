const form = document.getElementById('form-consulta');

function getApiBase() {
    const isArquivoLocal = window.location.protocol === "file:";
    const isLocalhost = ["127.0.0.1", "localhost"].includes(window.location.hostname);

    if (isArquivoLocal || isLocalhost) {
        return "http://127.0.0.1:8000";
    }

    return "";
}

const API_BASE = getApiBase();

form.addEventListener('submit', async function (e) {
    e.preventDefault();

    const nf = document.getElementById('nf').value;

    try {
        const response = await fetch(`${API_BASE}/rastreamento/${nf}`);
        const data = await response.json();

        if (!response.ok || data.erro || !data.eventos) {
            window.location.href = 'erro.html';
            return;
        }

        localStorage.setItem('pedido', JSON.stringify(data));
        window.location.href = 'resultado.html';

    } catch (error) {
        window.location.href = 'erro.html';
    }
});