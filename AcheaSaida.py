from flask import Flask, request, redirect, url_for, render_template
import pandas as pd

app = Flask(__name__)

fluxos = {}

def carregar_planilha(path):
    planilha = pd.read_excel(path, sheet_name=None)
    estrutura = {}
    
    for nome_aba, df in planilha.items():
        fluxo = {}
        df.fillna("", inplace=True)

        for _, linha in df.iterrows():
            node_id = linha["ID"]
            tipo = linha["Tipo"].strip().lower()
            texto = linha["Texto"]

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

@app.route('/')
def index():
    aplicacoes = list(fluxos.keys())
    return render_template("index.html", aplicacoes=aplicacoes)

@app.route('/<aplicacao>/')
def iniciar_fluxo(aplicacao):
    if aplicacao not in fluxos:
        return "Aplicação não encontrada.", 404
    return redirect(url_for("mostrar_pergunta", aplicacao=aplicacao, node_id="q1"))

@app.route('/<aplicacao>/<node_id>')
def mostrar_pergunta(aplicacao, node_id):
    fluxo = fluxos.get(aplicacao)
    if not fluxo or node_id not in fluxo:
        return "Passo não encontrado. Favor ajustar a lógica na tabela da planilha Troubleshooting.xlsx", 404

    node = fluxo[node_id]

    if "solucao" in node:
        return render_template("flow.html", solucao=node["solucao"], pergunta=None, node_id=None, aplicacao=aplicacao)
    else:
        return render_template("flow.html", pergunta=node["pergunta"], solucao=None, node_id=node_id, aplicacao=aplicacao)

@app.route('/responder', methods=['POST'])
def responder():
    aplicacao = request.form["aplicacao"]
    node_id = request.form["node_id"]
    resposta = request.form["resposta"]
    proximo_id = fluxos[aplicacao][node_id].get(resposta)

    if not proximo_id or proximo_id.lower() == "nan":
        return "Próximo passo inválido ou não encontrado. Favor ajustar a lógica na tabela da planilha Troubleshooting.xlsx", 404

    return redirect(url_for("mostrar_pergunta", aplicacao=aplicacao, node_id=proximo_id))

if __name__ == '__main__':
    fluxos = carregar_planilha("troubleshooting.xlsx")
    app.run(host='0.0.0.0', port=5000, debug=True)  
