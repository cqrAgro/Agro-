"""
Scraper da cotação do boi gordo por estado (Pecuária.com.br).

O que faz:
1. Baixa a página de cotações
2. Encontra a tabela "Data / SP / MS / MG / GO / MT / RJ"
3. Junta com o histórico já salvo em data/historico.json
4. Salva de volta, sem duplicar datas que já existem

IMPORTANTE — antes de rodar isso de verdade:
- Confira o robots.txt do site (pecuaria.com.br/robots.txt) e os Termos de Uso
  antes de automatizar a coleta. Este script assume uso pessoal, de baixa
  frequência (1x/dia) e não comercial.
- O layout do site pode mudar. Se o script parar de achar a tabela, é o
  primeiro lugar a checar.
"""

import json
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

URL = "https://www.pecuaria.com.br/cotacoes.php"
DATA_FILE = Path("data/historico.json")

HEADERS = {
    # Troque o e-mail de contato pelo seu — é boa prática se identificar.
    "User-Agent": "Mozilla/5.0 (compatible; CotacaoBoiBot/1.0; +contato@seudominio.com.br)"
}

COLUNAS = ["SP", "MS", "MG", "GO", "MT", "RJ"]


def buscar_html() -> str:
    resp = requests.get(URL, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.text


def extrair_tabela(html: str) -> list[dict]:
    """Encontra a tabela de cotações por data e devolve uma lista de linhas."""
    soup = BeautifulSoup(html, "lxml")

    tabela = None
    for t in soup.find_all("table"):
        primeira_linha = t.find("tr")
        if primeira_linha and "SP" in primeira_linha.get_text():
            tabela = t
            break

    if tabela is None:
        raise RuntimeError(
            "Não encontrei a tabela de cotações. O site provavelmente mudou "
            "o layout — inspecione a página e ajuste extrair_tabela()."
        )

    linhas = tabela.find_all("tr")
    dados = []
    for linha in linhas[1:]:
        celulas = [c.get_text(strip=True) for c in linha.find_all(["td", "th"])]
        if len(celulas) < 7:
            continue
        data_str, *precos = celulas[:7]
        registro = {"data": data_str}
        registro.update(dict(zip(COLUNAS, precos)))
        dados.append(registro)

    return dados


def carregar_historico() -> list[dict]:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return []


def salvar_historico(historico: list[dict]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(historico, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def chave_data(item: dict):
    dia, mes, ano = item["data"].split("/")
    return (ano, mes, dia)


def main() -> None:
    html = buscar_html()
    linhas_novas = extrair_tabela(html)

    if not linhas_novas:
        print("Nenhuma linha encontrada na tabela — abortando sem alterar o histórico.")
        sys.exit(1)

    historico = carregar_historico()
    datas_existentes = {item["data"] for item in historico}

    adicionadas = 0
    for linha in linhas_novas:
        if linha["data"] not in datas_existentes:
            historico.append(linha)
            datas_existentes.add(linha["data"])
            adicionadas += 1

    historico.sort(key=chave_data)
    salvar_historico(historico)

    print(f"{adicionadas} nova(s) data(s) adicionada(s). Total no histórico: {len(historico)}.")


if __name__ == "__main__":
    main()
