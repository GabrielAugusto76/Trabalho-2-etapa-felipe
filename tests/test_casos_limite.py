from career_expert.base_conhecimento import carregar_base
from career_expert.gaps import analisar_gaps, estimar_semanas
from career_expert.motor import avaliar_ranking, calcular_compatibilidade
from tests.test_personas import perfil

base = carregar_base()


def ids_do_top3(ranking):
    ids = []
    for item in ranking[:3]:
        ids.append(item["id"])
    return ids


def test_perfil_ambiguo_dados_e_web():
    respostas = perfil(q_dados=5, q_mat=4, q_design=5, q_usuario=4, q_logica=4, q_apis=4)
    ranking = calcular_compatibilidade(base, respostas)
    top3 = ids_do_top3(ranking)

    assert "eng_dados" in top3 or "ciencia_dados" in top3
    assert "frontend" in top3

    avisos = avaliar_ranking(ranking, respostas)
    assert any("Empate parcial" in aviso for aviso in avisos)


def test_todas_as_notas_neutras_geram_aviso():
    respostas = perfil()
    ranking = calcular_compatibilidade(base, respostas)
    avisos = avaliar_ranking(ranking, respostas)
    assert ranking[0]["percentual"] == 50.0
    assert any("parecidas" in aviso for aviso in avisos)


def test_todas_as_notas_5_continuam_validas():
    respostas = {}
    for pergunta in base["perguntas"]:
        respostas[pergunta["id"]] = 5
    ranking = calcular_compatibilidade(base, respostas)
    assert len(ranking) == 10
    assert ranking[0]["percentual"] <= 100
    assert len(avaliar_ranking(ranking, respostas)) > 0


def test_todas_as_notas_1_continuam_validas():
    respostas = {}
    for pergunta in base["perguntas"]:
        respostas[pergunta["id"]] = 1
    ranking = calcular_compatibilidade(base, respostas)
    assert ranking[-1]["percentual"] >= 0
    assert len(avaliar_ranking(ranking, respostas)) > 0


def test_respostas_faltando_sao_tratadas_como_neutras():
    ranking = calcular_compatibilidade(base, {})
    assert ranking[0]["percentual"] == 50.0


def test_empate_e_desempatado_pela_ordem_da_base():
    ranking = calcular_compatibilidade(base, perfil())
    assert ranking[0]["id"] == "backend"


def test_gap_sem_nenhum_conhecimento():
    gaps = analisar_gaps(base, "backend", [])
    assert gaps["preparo"] == 0
    assert len(gaps["faltam"]) == len(base["planos"]["backend"]["competencias_junior"])
    assert gaps["horas_total"] > 0


def test_gap_com_todos_os_conhecimentos():
    todos = base["planos"]["devops"]["competencias_junior"]
    gaps = analisar_gaps(base, "devops", todos)
    assert gaps["preparo"] == 100
    assert gaps["faltam"] == []
    assert estimar_semanas(gaps["horas_total"], 10) == 0


def test_estimativa_de_semanas_arredonda_para_cima():
    assert estimar_semanas(25, 10) == 3
