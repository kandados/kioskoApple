# kioskoApp/utils.py

import requests
from bs4 import BeautifulSoup

def buscar_curiosidad_en_wikipedia(termino):
    url = f"https://es.wikipedia.org/wiki/{termino.replace(' ', '_')}"
    try:
        respuesta = requests.get(url, timeout=10)
        if respuesta.status_code != 200:
            return f"No se encontró la página para '{termino}'."

        sopa = BeautifulSoup(respuesta.text, 'html.parser')
        parrafos = sopa.find_all('p')

        for p in parrafos:
            texto = p.get_text().strip()
            if len(texto) > 100:
                return texto  # Primer párrafo informativo razonable

        return "No se encontraron datos relevantes."

    except Exception as e:
        return f"Error al buscar la curiosidad: {e}"
