import math


def analisar_gaps(base, trilha_id, conhecimentos):
    plano = base["planos"][trilha_id]
    tem = []
    faltam = []

    for comp_id in plano["competencias_junior"]:
        comp = base["competencias"][comp_id]
        item = {"id": comp_id, "nome": comp["nome"], "horas": comp["horas"]}
        if comp_id in conhecimentos:
            tem.append(item)
        else:
            faltam.append(item)

    total = len(plano["competencias_junior"])
    preparo = round(len(tem) / total * 100)

    horas_total = 0
    for item in faltam:
        horas_total = horas_total + item["horas"]

    return {
        "tem": tem,
        "faltam": faltam,
        "preparo": preparo,
        "horas_total": horas_total,
        "certificacoes": plano["certificacoes"],
        "projetos": plano["projetos"],
    }


def estimar_semanas(horas_total, horas_por_semana):
    if horas_total == 0:
        return 0
    return math.ceil(horas_total / horas_por_semana)
