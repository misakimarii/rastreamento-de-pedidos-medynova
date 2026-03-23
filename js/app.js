const form = document.getElementById('form-consulta');

form.addEventListener('submit', async function (e) {
    e.preventDefault();

    const nf = document.getElementById('nf').value;

    try {
        const response = await fetch('/api/consulta', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ chavenf: nf })
        });
        const data = await response.json();

        if (!response.ok) {
            window.location.href = 'erro.html';
            return;
        }

        localStorage.setItem('pedido', JSON.stringify(data));
        window.location.href = 'resultado.html';

    } catch (error) {
        window.location.href = 'erro.html';
    }
});