import re

# Lista de palavras ou padrões bloqueados
PALAVRAS_BLOQUEADAS = [
    r"\bconselho jurídico\b",
    r"\brecomendação médica\b",
    r"\binformação confidencial\b"
]

def guardian_sail(response: str) -> str:
    """Verifica se a resposta contém palavras proibidas e bloqueia se necessário."""
    for padrao in PALAVRAS_BLOQUEADAS:
        if re.search(padrao, response, re.IGNORECASE):
            return "Desculpe, não posso fornecer essa informação. Consulte um profissional adequado."
    return response
