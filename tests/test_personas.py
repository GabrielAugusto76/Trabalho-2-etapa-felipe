from career_expert.base_conhecimento import carregar_base
from career_expert.motor import calcular_compatibilidade

base = carregar_base()


def perfil(**notas):
    respostas = {}
    for pergunta in base["perguntas"]:
        respostas[pergunta["id"]] = 3
    respostas.update(notas)
    return respostas


PERSONAS = {
    "ana_analitica": (
        perfil(q_mat=5, q_ia=5, q_logica=4, q_dados=4, q_design=2, q_pessoas=2),
        "ciencia_dados",
    ),
    "bruno_seguranca": (
        perfil(q_seguranca=5, q_infra=5, q_detalhe=4, q_design=1, q_pessoas=2),
        "ciberseguranca",
    ),
    "carla_frontend": (
        perfil(q_design=5, q_usuario=5, q_infra=1, q_mat=2),
        "frontend",
    ),
    "diego_produto": (
        perfil(q_pessoas=5, q_gestao=5, q_negocio=5, q_usuario=4, q_logica=2, q_infra=1),
        "produto",
    ),
    "eduardo_backend": (
        perfil(q_apis=5, q_logica=5, q_dados=3, q_design=1, q_usuario=3),
        "backend",
    ),
    "fernanda_eng_dados": (
        perfil(q_dados=5, q_automacao=4, q_logica=4, q_ia=2, q_mat=3, q_design=1),
        "eng_dados",
    ),
    "gabriel_devops": (
        perfil(q_infra=5, q_automacao=5, q_incidentes=5, q_nuvem=3, q_design=1),
        "devops",
    ),
    "helena_cloud": (
        perfil(q_infra=5, q_nuvem=5, q_pessoas=4, q_automacao=3, q_design=1),
        "cloud",
    ),
    "igor_mobile": (
        perfil(q_mobile=5, q_design=4, q_usuario=5, q_infra=1),
        "mobile",
    ),
    "julia_qa": (
        perfil(q_testes=5, q_detalhe=5, q_automacao=3, q_design=2),
        "qa",
    ),
}


def test_persona_recebe_trilha_esperada():
    for nome, (respostas, esperado) in PERSONAS.items():
        ranking = calcular_compatibilidade(base, respostas)
        assert ranking[0]["id"] == esperado, nome + ": obteve " + ranking[0]["id"]


def test_todas_as_10_trilhas_sao_cobertas():
    esperadas = set()
    for respostas, esperado in PERSONAS.values():
        esperadas.add(esperado)
    assert len(esperadas) == 10


def test_ranking_tem_10_trilhas_ordenadas():
    ranking = calcular_compatibilidade(base, PERSONAS["ana_analitica"][0])
    assert len(ranking) == 10
    for i in range(9):
        assert ranking[i]["percentual"] >= ranking[i + 1]["percentual"]


def test_percentuais_ficam_entre_0_e_100():
    for respostas, esperado in PERSONAS.values():
        for item in calcular_compatibilidade(base, respostas):
            assert 0 <= item["percentual"] <= 100


def test_trilha_vencedora_tem_justificativa():
    for respostas, esperado in PERSONAS.values():
        ranking = calcular_compatibilidade(base, respostas)
        assert len(ranking[0]["a_favor"]) > 0


def test_penalidade_de_matematica_baixa_para_ciencia_de_dados():
    sem_penalidade = calcular_compatibilidade(base, perfil(q_mat=3, q_ia=5, q_dados=5))
    com_penalidade = calcular_compatibilidade(base, perfil(q_mat=1, q_ia=5, q_dados=5))
    ds_sem = [i for i in sem_penalidade if i["id"] == "ciencia_dados"][0]
    ds_com = [i for i in com_penalidade if i["id"] == "ciencia_dados"][0]
    assert ds_com["percentual"] < ds_sem["percentual"]
    assert len(ds_com["ajustes"]) > 0
