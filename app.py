import os
import subprocess
import sys

import pandas as pd
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

if get_script_run_ctx(suppress_warning=True) is None:
    subprocess.run([sys.executable, "-m", "streamlit", "run", os.path.abspath(__file__)])
    sys.exit()

from career_expert.base_conhecimento import carregar_base
from career_expert.gaps import analisar_gaps, estimar_semanas
from career_expert.motor import avaliar_ranking, calcular_compatibilidade

st.set_page_config(page_title="Consultor de Carreiras em TI", page_icon="🧭")

base = carregar_base()
rotulos = [
    "1 - Nenhuma",
    "2 - Pouca",
    "3 - Média",
    "4 - Alta",
    "5 - Muita",
]

if "passo" not in st.session_state:
    st.session_state.passo = 1
    st.session_state.nome = ""
    st.session_state.conhecimentos = []
    st.session_state.horas = 10
    for pergunta in base["perguntas"]:
        st.session_state["sl_" + pergunta["id"]] = rotulos[2]

for chave in list(st.session_state.keys()):
    st.session_state[chave] = st.session_state[chave]


def ir_para(passo):
    st.session_state.passo = passo


def mostrar_perguntas(etapa):
    for pergunta in base["perguntas"]:
        if pergunta["etapa"] != etapa:
            continue
        st.select_slider(pergunta["texto"], options=rotulos, key="sl_" + pergunta["id"])


def pegar_respostas():
    respostas = {}
    for pergunta in base["perguntas"]:
        escolha = st.session_state["sl_" + pergunta["id"]]
        respostas[pergunta["id"]] = rotulos.index(escolha) + 1
    return respostas


def mostrar_plano(trilha, ranking_item):
    st.write(trilha["descricao"])

    st.markdown("**Por que essa trilha?**")
    if ranking_item["a_favor"]:
        for texto in ranking_item["a_favor"]:
            st.write("✅ " + texto)
    else:
        st.write("Nenhuma pergunta teve nota alta para esta trilha.")
    for texto in ranking_item["contra"]:
        st.write("⚠️ Ponto de atenção: " + texto)
    for rid, descricao, valor in ranking_item["ajustes"]:
        sinal = "+" if valor > 0 else ""
        st.write("📏 Regra " + rid + ": " + descricao + " (" + sinal + str(valor) + " pontos)")

    gaps = analisar_gaps(base, ranking_item["id"], st.session_state.conhecimentos)

    st.markdown("**Análise de lacunas para o nível Júnior**")
    col1, col2 = st.columns(2)
    col1.metric("Preparo atual", str(gaps["preparo"]) + "%")
    semanas = estimar_semanas(gaps["horas_total"], st.session_state.horas)
    col2.metric("Tempo estimado", str(semanas) + " semanas")

    linhas = []
    for item in gaps["tem"]:
        linhas.append({"Competência": item["nome"], "Situação": "✅ Você já tem", "Horas": 0})
    for item in gaps["faltam"]:
        linhas.append({"Competência": item["nome"], "Situação": "❌ Falta", "Horas": item["horas"]})
    st.dataframe(pd.DataFrame(linhas), hide_index=True)

    st.markdown("**Roadmap: o que estudar primeiro**")
    if gaps["faltam"]:
        numero = 1
        for item in gaps["faltam"]:
            st.write(str(numero) + ". " + item["nome"] + " (~" + str(item["horas"]) + "h)")
            numero = numero + 1
    else:
        st.write("Você já cobre todas as competências básicas desta trilha. Foque em projetos e certificações.")

    st.markdown("**Certificações sugeridas**")
    for cert in gaps["certificacoes"]:
        st.write("🎓 " + cert)
    st.caption("Confira preço e disponibilidade atual antes de contratar qualquer certificação.")

    st.markdown("**Projetos para o portfólio no GitHub**")
    for projeto in gaps["projetos"]:
        st.write("💻 " + projeto)


st.title("🧭 Consultor Avançado de Carreiras em TI")
st.caption("Sistema especialista com pontuação ponderada · UNIPAC Barbacena")

passo = st.session_state.passo

if passo <= 3:
    st.progress(passo / 3, text="Passo " + str(passo) + " de 3")

if passo == 1:
    st.subheader("Passo 1: Perfil pessoal")
    st.text_input("Seu nome", key="nome")
    st.multiselect(
        "Quais destes conhecimentos você já tem?",
        list(base["competencias"]),
        key="conhecimentos",
        format_func=lambda c: base["competencias"][c]["nome"],
    )
    st.slider("Quantas horas por semana você pode estudar?", 2, 40, key="horas")
    st.button("Próximo ➡️", on_click=ir_para, args=(2,), type="primary")

elif passo == 2:
    st.subheader("Passo 2: Afinidades técnicas")
    st.write("Dê uma nota de 1 (nenhuma afinidade) a 5 (muita afinidade).")
    mostrar_perguntas(2)
    col1, col2 = st.columns(2)
    col1.button("⬅️ Voltar", on_click=ir_para, args=(1,))
    col2.button("Próximo ➡️", on_click=ir_para, args=(3,), type="primary")

elif passo == 3:
    st.subheader("Passo 3: Objetivos de carreira")
    st.write("Dê uma nota de 1 (nada a ver comigo) a 5 (tudo a ver comigo).")
    mostrar_perguntas(3)
    col1, col2 = st.columns(2)
    col1.button("⬅️ Voltar", on_click=ir_para, args=(2,))
    col2.button("🔎 Ver meu resultado", on_click=ir_para, args=(4,), type="primary")

else:
    nome = st.session_state.nome or "visitante"
    respostas = pegar_respostas()
    ranking = calcular_compatibilidade(base, respostas)

    st.subheader("Resultado de " + nome)

    for aviso in avaliar_ranking(ranking, respostas):
        st.warning(aviso)

    colunas = st.columns(3)
    posicao = 1
    for coluna in colunas:
        item = ranking[posicao - 1]
        coluna.metric(str(posicao) + "º lugar", str(item["percentual"]) + "%", item["nome"], delta_color="off")
        posicao = posicao + 1

    st.markdown("**Compatibilidade com as 10 trilhas (%)**")
    tabela = pd.DataFrame(
        {"Compatibilidade (%)": [item["percentual"] for item in ranking]},
        index=[item["nome"] for item in ranking],
    )
    st.bar_chart(tabela)

    st.markdown("## Plano de ação")
    abas = st.tabs([str(i + 1) + "º " + ranking[i]["nome"] for i in range(3)])
    for i in range(3):
        with abas[i]:
            mostrar_plano(ranking[i], ranking[i])

    st.button("🔄 Refazer o teste", on_click=ir_para, args=(1,))
