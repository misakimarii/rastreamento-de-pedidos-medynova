const form = document.getElementById('form-consulta');

form.addEventListener('submit', async function (e) {
    e.preventDefault();

    const nf = document.getElementById('nf').value.trim();

    if (!nf) {
        window.location.href = 'erro.html';
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/rastreamento/${nf}`);
        const data = await response.json();

        console.log("RESPOSTA BACKEND:", data);

        if (!response.ok || data.erro) {
            window.location.href = 'erro.html';
            return;
        }

        localStorage.setItem('pedido', JSON.stringify(data));
        window.location.href = 'resultado.html';

    } catch (error) {
        console.error("ERRO NA CONSULTA:", error);
        window.location.href = 'erro.html';
    }
});