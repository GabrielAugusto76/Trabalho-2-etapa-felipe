import json
from pathlib import Path

CAMINHO = Path(__file__).resolve().parent.parent / "dados" / "regras_carreiras.json"


def carregar_base(caminho=CAMINHO):
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)
