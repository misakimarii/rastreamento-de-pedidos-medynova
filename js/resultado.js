const data = JSON.parse(localStorage.getItem('pedido'));

if (!data) {
    window.location.href = 'erro.html';
}

const elementoPrevisao = document.getElementById("previsao");
const steps = document.querySelectorAll(".status-step");
const dataElements = document.querySelectorAll(".status-data");
const titulo = document.querySelector(".card h2");

function formatarDataHora(evento) {
    if (!evento) return "";

    const dataBruta = evento.data || "";
    const horaBruta = evento.hora || "";

    if (dataBruta.includes(" ") && dataBruta.includes("-")) {
        const [dataParte, horaParte] = dataBruta.split(" ");
        const [ano, mes, dia] = dataParte.split("-");
        return `${dia}/${mes}/${ano} <br> ${horaParte}`;
    }

    if (dataBruta.includes("-")) {
        const [ano, mes, dia] = dataBruta.split("-");
        return `${dia}/${mes}/${ano} <br> ${horaBruta}`;
    }

    return `${dataBruta} <br> ${horaBruta}`;
}

function getEvento(tipo) {
    if (!data.eventos || !Array.isArray(data.eventos)) return null;

    const filtrados = data.eventos.filter(e => {
        const s = (e.status || "").toLowerCase();

        if (tipo === 1) {
            return s.includes("emissao");
        }

        if (tipo === 2) {
            return s.includes("transferencia");
        }

        if (tipo === 3) {
            return s.includes("em rota de entrega") || s.includes("rota de entrega");
        }

        if (tipo === 4) {
            return (
                s.includes("entrega realizada") ||
                s.includes("comprovante de entrega") ||
                s.includes("comprovante de entrega - recebido")
            );
        }

        return false;
    });

    return filtrados.length ? filtrados[0] : null;
}

const previsao = data.previsao_entrega;

if (previsao) {
    elementoPrevisao.innerText = `Previsão de entrega: ${previsao}`;
} else if (data.status) {
    elementoPrevisao.innerText = data.status;
} else {
    elementoPrevisao.innerText = "Previsão de entrega: não disponível";
}

if (!data.eventos || data.eventos.length === 0) {
    titulo.innerText = data.status || "Pedido em processamento";

    steps.forEach((step) => {
        step.classList.add("inativo");
        step.classList.remove("ativo");
    });

    dataElements.forEach((el) => {
        el.innerHTML = "";
    });

} else {
    const eventosPorEtapa = [
        getEvento(1),
        getEvento(2),
        getEvento(3),
        getEvento(4)
    ];

    let nivel = 0;
    eventosPorEtapa.forEach((e, i) => {
        if (e) nivel = i + 1;
    });

    if (nivel === 4) {
        titulo.innerText = "Entrega concluída";
    } else if (nivel === 3) {
        titulo.innerText = "Saiu para entrega";
    } else if (nivel === 2) {
        titulo.innerText = "Em transporte";
    } else if (nivel === 1) {
        titulo.innerText = "Pedido coletado";
    } else {
        titulo.innerText = "Pedido em processamento";
    }

    steps.forEach((step, index) => {
        if (index < nivel) {
            step.classList.add("ativo");
            step.classList.remove("inativo");

            const evento = eventosPorEtapa[index];

            if (evento) {
                dataElements[index].innerHTML = formatarDataHora(evento);
            } else {
                dataElements[index].innerHTML = "";
            }
        } else {
            step.classList.add("inativo");
            step.classList.remove("ativo");
            dataElements[index].innerHTML = "";
        }
    });
}