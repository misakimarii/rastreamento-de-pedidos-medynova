from datetime import timedelta


PRAZO_CIDADES = {
    "RECIFE": 1,
    "OLINDA": 1,
    "JABOATAO DOS GUARARAPES": 1,
    "PAULISTA": 1,

    "JOAO PESSOA": 1,
    "CABEDELO": 1,
    "BAYEUX": 1,

    "NATAL": 1,
    "PARNAMIRIM": 1,

    "MACEIO": 1,
    "ARACAJU": 2,
    "SALVADOR": 2,
    "FORTALEZA": 2,

    "SAO LUIS": 2,
    "BELEM": 2,

    "MANAUS": 4,
    "MACAPA": 4,
    "PORTO VELHO": 4,
    "BOA VISTA": 4,
    "RIO BRANCO": 4,

    "PALMAS": 3,

    "BRASILIA": 2,
    "GOIANIA": 2,
    "CUIABA": 3,
    "CAMPO GRANDE": 3,

    "CURITIBA": 3,
    "FLORIANOPOLIS": 3,
    "PORTO ALEGRE": 3,

    "VITORIA": 3,
    "BELO HORIZONTE": 2,
    "RIO DE JANEIRO": 2,
    "SAO PAULO": 2,
}


PRAZO_ESTADOS = {
    "PE": 4,
    "PB": 2,
    "RN": 3,
    "AL": 3,
    "SE": 4,
    "BA": 4,
    "CE": 4,
    "MA": 4,

    "AM": 6,
    "AP": 6,
    "PA": 4,
    "RO": 6,
    "RR": 6,
    "AC": 6,
    "TO": 5,

    "DF": 4,
    "GO": 4,
    "MT": 5,
    "MS": 5,

    "PR": 5,
    "SC": 5,
    "RS": 5,

    "ES": 5,
    "MG": 4,
    "RJ": 4,
    "SP": 4,
}


def calcular_previsao(pedido, eventos):

    if not eventos:
        return None

    cidade = (pedido.cidade or "").upper().strip()
    estado = (pedido.uf or "").upper().strip()  

    if cidade in PRAZO_CIDADES:
        dias = PRAZO_CIDADES[cidade]

    elif estado in PRAZO_ESTADOS:
        dias = PRAZO_ESTADOS[estado]

    else:
        dias = 3

    ultima_data = eventos[-1].data_evento

    previsao = ultima_data + timedelta(days=dias)

    return previsao.strftime("%d/%m")