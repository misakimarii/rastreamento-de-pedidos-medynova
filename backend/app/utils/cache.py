from datetime import datetime, timedelta

cache_rastreamento = {}

TEMPO_CACHE = timedelta(minutes=5)


def get_cache(numero_nf):
    item = cache_rastreamento.get(numero_nf)

    if not item:
        return None

    if datetime.now() - item["timestamp"] > TEMPO_CACHE:
        del cache_rastreamento[numero_nf]
        return None

    return item["data"]


def set_cache(numero_nf, data):
     cache_rastreamento[numero_nf] = {
         "data": data,
         "timestamp": datetime.now()
     }