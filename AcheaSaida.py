from pathlib import Path
from typing import Any

import pandas as pd
from flask import Flask, abort, redirect, render_template, request, session, url_for


BASE_DIR = Path(__file__).resolve().parent
PLANILHA = BASE_DIR / "troubleshooting.xlsx"
app = Flask(__name__, template_folder="Templates")
app.config["SECRET_KEY"] = "ache-a-saida-local"


class PlanilhaInvalida(ValueError):
    """Erro legível para problemas na base de conhecimento."""


def texto(valor: Any) -> str:
    if pd.isna(valor):
        return ""
    return str(valor).strip()


def carregar_planilha(path: Path | str) -> dict[str, dict[str, dict[str, str]]]:
    """Converte cada aba preenchida em um fluxo validado de nós."""
    arquivo = Path(path)
    if not arquivo.exists():
        raise PlanilhaInvalida(f"Planilha não encontrada: {arquivo.name}")

    estrutura = {}
    avisos = []
    colunas = {"ID", "Tipo", "Texto", "Próx. Sim", "Próx. Não"}
    for nome_aba, dataframe in pd.read_excel(arquivo, sheet_name=None).items():
        if dataframe.empty:
            continue
        if not colunas.issubset(dataframe.columns):
            faltantes = ", ".join(sorted(colunas - set(dataframe.columns)))
            raise PlanilhaInvalida(f"A aba '{nome_aba}' não possui: {faltantes}")

        fluxo = {}
        for _, linha in dataframe.iterrows():
            node_id = texto(linha["ID"])
            tipo = texto(linha["Tipo"]).lower()
            if not node_id or node_id in fluxo:
                raise PlanilhaInvalida(f"ID vazio ou repetido na aba '{nome_aba}'")
            if tipo == "pergunta":
                fluxo[node_id] = {"tipo": "pergunta", "texto": texto(linha["Texto"]), "sim": texto(linha["Próx. Sim"]), "nao": texto(linha["Próx. Não"])}
            elif tipo == "solucao":
                fluxo[node_id] = {"tipo": "solucao", "texto": texto(linha["Texto"]), "sim": "", "nao": ""}
            else:
                raise PlanilhaInvalida(f"Tipo inválido '{tipo}' na aba '{nome_aba}'")

        if "q1" not in fluxo:
            raise PlanilhaInvalida(f"A aba '{nome_aba}' precisa de um nó inicial q1")
        fluxo_valido = True
        for node_id, node in fluxo.items():
            for resposta in ("sim", "nao") if node["tipo"] == "pergunta" else ():
                if not node[resposta] or node[resposta] not in fluxo:
                    avisos.append(f"A aba '{nome_aba}' foi ignorada: referência inválida em {node_id}/{resposta}")
                    fluxo_valido = False
        if not fluxo_valido:
            continue
        estrutura[nome_aba] = fluxo
    carregar_planilha.avisos = avisos
    return estrutura


try:
    fluxos = carregar_planilha(PLANILHA)
    erro_planilha = "; ".join(getattr(carregar_planilha, "avisos", [])) or None
except PlanilhaInvalida as erro:
    fluxos = {}
    erro_planilha = str(erro)


def fluxo_ou_404(aplicacao: str) -> dict[str, dict[str, str]]:
    fluxo = fluxos.get(aplicacao)
    if not fluxo:
        abort(404, description="Aplicação não encontrada.")
    return fluxo


@app.route("/")
def index():
    return render_template("Index.html", aplicacoes=sorted(fluxos), erro_planilha=erro_planilha)


@app.route("/<aplicacao>/")
def iniciar_fluxo(aplicacao):
    fluxo_ou_404(aplicacao)
    session["historico"] = []
    return redirect(url_for("mostrar_no", aplicacao=aplicacao, node_id="q1"))


@app.route("/<aplicacao>/<node_id>")
def mostrar_no(aplicacao, node_id):
    fluxo = fluxo_ou_404(aplicacao)
    node = fluxo.get(node_id)
    if not node:
        abort(404, description="Passo não encontrado na planilha.")
    historico = session.get("historico", [])
    if not historico or historico[-1] != node_id:
        historico.append(node_id)
        session["historico"] = historico[-20:]
    perguntas_respondidas = sum(1 for item in historico if fluxo.get(item, {}).get("tipo") == "pergunta")
    total_perguntas = sum(1 for item in fluxo.values() if item["tipo"] == "pergunta")
    anterior = historico[-2] if len(historico) > 1 else None
    return render_template("flow.html", aplicacao=aplicacao, node=node, node_id=node_id, anterior=anterior, progresso=perguntas_respondidas, total_perguntas=total_perguntas)


@app.post("/responder")
def responder():
    aplicacao = request.form.get("aplicacao", "")
    node_id = request.form.get("node_id", "")
    resposta = request.form.get("resposta", "").lower()
    fluxo = fluxo_ou_404(aplicacao)
    node = fluxo.get(node_id)
    if not node or node["tipo"] != "pergunta" or resposta not in ("sim", "nao"):
        abort(400, description="Resposta inválida para este passo.")
    return redirect(url_for("mostrar_no", aplicacao=aplicacao, node_id=node[resposta]))


@app.get("/voltar/<aplicacao>")
def voltar(aplicacao):
    fluxo_ou_404(aplicacao)
    historico = session.get("historico", [])
    if len(historico) < 2:
        return redirect(url_for("iniciar_fluxo", aplicacao=aplicacao))
    historico.pop()
    session["historico"] = historico
    return redirect(url_for("mostrar_no", aplicacao=aplicacao, node_id=historico[-1]))


@app.errorhandler(404)
def pagina_404(erro):
    return render_template("error.html", titulo="Página não encontrada", mensagem=erro.description), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
