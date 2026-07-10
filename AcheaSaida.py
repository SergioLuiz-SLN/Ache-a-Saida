from flask import Flask, request, redirect, url_for, render_template
import pandas as pd
import os

app = Flask(__name__, template_folder="Templates")

fluxos = {}

ARQUIVO_PLANILHA = "troubleshooting.xlsx"
ARQUIVO_ATENDIMENTOS = "atendimentos.csv"


def carregar_planilha(path):
    planilha = pd.read_excel(path, sheet_name=None)
    estrutura = {}

    for nome_aba, df in planilha.items():
        fluxo = {}
        df.fillna("", inplace=True)

        for _, linha in df.iterrows():
            node_id = str(linha["ID"]).strip()
            tipo = str(linha["Tipo"]).strip().lower()
            texto = str(linha["Texto"]).strip()

            if tipo == "pergunta":
                fluxo[node_id] = {
                    "pergunta": texto,
                    "sim": str(linha["Próx. Sim"]).strip(),
                    "nao": str(linha["Próx. Não"]).strip()
                }

            elif tipo == "solucao":
                fluxo[node_id] = {
                    "solucao": texto
                }

        estrutura[nome_aba] = fluxo

    return estrutura


def dados_dashboard_vazios():
    return {
        "total_atendimentos": 0,
        "taxa_resolucao": 0,
        "total_encaminhados": 0,
        "tempo_medio": 0,
        "problemas_recorrentes": [],
        "fluxos_utilizados": [],
        "atendimentos_por_dia": [],
        "tempo_medio_por_problema": []
    }


@app.route("/")
def index():
    aplicacoes = list(fluxos.keys())
    return render_template("index.html", aplicacoes=aplicacoes)


@app.route("/dashboard")
def dashboard():
    dados_vazios = dados_dashboard_vazios()

    if not os.path.isfile(ARQUIVO_ATENDIMENTOS):
        return render_template("dashboard.html", **dados_vazios)

    try:
        df = pd.read_csv(ARQUIVO_ATENDIMENTOS)
    except Exception:
        return render_template("dashboard.html", **dados_vazios)

    if df.empty:
        return render_template("dashboard.html", **dados_vazios)

    colunas_obrigatorias = [
        "data_hora",
        "problema",
        "fluxo",
        "status",
        "tempo_segundos",
        "caminho"
    ]

    for coluna in colunas_obrigatorias:
        if coluna not in df.columns:
            return render_template("dashboard.html", **dados_vazios)

    df["data_hora"] = pd.to_datetime(df["data_hora"], errors="coerce")
    df["tempo_segundos"] = pd.to_numeric(
        df["tempo_segundos"],
        errors="coerce"
    ).fillna(0)

    df = df.dropna(subset=["data_hora"])

    if df.empty:
        return render_template("dashboard.html", **dados_vazios)

    df["data"] = df["data_hora"].dt.date

    total_atendimentos = len(df)
    total_resolvidos = len(df[df["status"] == "Resolvido"])
    total_encaminhados = len(df[df["status"] == "Encaminhado"])

    if total_atendimentos > 0:
        taxa_resolucao = round((total_resolvidos / total_atendimentos) * 100, 2)
    else:
        taxa_resolucao = 0

    tempo_medio = round(df["tempo_segundos"].mean() / 60, 2)

    problemas_recorrentes = (
        df["problema"]
        .value_counts()
        .head(5)
        .reset_index()
        .values
        .tolist()
    )

    fluxos_utilizados = (
        df["fluxo"]
        .value_counts()
        .head(5)
        .reset_index()
        .values
        .tolist()
    )

    atendimentos_por_dia = (
        df.groupby("data")
        .size()
        .reset_index(name="quantidade")
        .values
        .tolist()
    )

    tempo_medio_por_problema_df = (
        df.groupby("problema")["tempo_segundos"]
        .mean()
        .div(60)
        .round(2)
        .reset_index(name="tempo_medio_minutos")
        .sort_values(by="tempo_medio_minutos", ascending=False)
        .head(10)
    )

    maior_tempo = tempo_medio_por_problema_df["tempo_medio_minutos"].max()

    tempo_medio_por_problema = []

    for _, linha in tempo_medio_por_problema_df.iterrows():
        tempo = float(linha["tempo_medio_minutos"])

        if maior_tempo > 0:
            percentual = round((tempo / maior_tempo) * 100, 2)
        else:
            percentual = 0

        tempo_medio_por_problema.append({
            "problema": linha["problema"],
            "tempo_medio": tempo,
            "percentual": percentual
        })

    return render_template(
        "dashboard.html",
        total_atendimentos=total_atendimentos,
        taxa_resolucao=taxa_resolucao,
        total_encaminhados=total_encaminhados,
        tempo_medio=tempo_medio,
        problemas_recorrentes=problemas_recorrentes,
        fluxos_utilizados=fluxos_utilizados,
        atendimentos_por_dia=atendimentos_por_dia,
        tempo_medio_por_problema=tempo_medio_por_problema
    )


@app.route("/<aplicacao>/")
def iniciar_fluxo(aplicacao):
    if aplicacao not in fluxos:
        return "Aplicação não encontrada.", 404

    return redirect(url_for("mostrar_pergunta", aplicacao=aplicacao, node_id="q1"))


@app.route("/<aplicacao>/<node_id>")
def mostrar_pergunta(aplicacao, node_id):
    fluxo = fluxos.get(aplicacao)

    if not fluxo or node_id not in fluxo:
        return (
            "Passo não encontrado. "
            "Favor ajustar a lógica na tabela da planilha Troubleshooting.xlsx"
        ), 404

    node = fluxo[node_id]

    if "solucao" in node:
        return render_template(
            "flow.html",
            solucao=node["solucao"],
            pergunta=None,
            node_id=None,
            aplicacao=aplicacao
        )

    return render_template(
        "flow.html",
        pergunta=node["pergunta"],
        solucao=None,
        node_id=node_id,
        aplicacao=aplicacao
    )


@app.route("/responder", methods=["POST"])
def responder():
    aplicacao = request.form.get("aplicacao")
    node_id = request.form.get("node_id")
    resposta = request.form.get("resposta")

    fluxo_atual = fluxos.get(aplicacao)

    if fluxo_atual is None:
        return "Aplicação não encontrada.", 404

    if node_id not in fluxo_atual:
        return "Passo não encontrado.", 404

    node_atual = fluxo_atual.get(node_id)
    proximo_id = node_atual.get(resposta)

    if not proximo_id or str(proximo_id).lower() == "nan":
        return (
            "Próximo passo inválido ou não encontrado. "
            "Favor ajustar a lógica na tabela da planilha Troubleshooting.xlsx"
        ), 404

    return redirect(
        url_for(
            "mostrar_pergunta",
            aplicacao=aplicacao,
            node_id=proximo_id
        )
    )


if __name__ == "__main__":
    if not os.path.isfile(ARQUIVO_PLANILHA):
        raise FileNotFoundError(f"Arquivo {ARQUIVO_PLANILHA} não encontrado.")

    fluxos = carregar_planilha(ARQUIVO_PLANILHA)

    app.run(host="0.0.0.0", port=5000, debug=True)