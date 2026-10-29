def comparar(valor, operador, limite):
    if operador == "<=":
        return valor <= limite
    if operador == ">=":
        return valor >= limite
    if operador == "==":
        return valor == limite
    return False


def calcular_pontuacao_base(base, trilha_id, respostas):
    pontos = 0
    minimo = 0
    maximo = 0
    a_favor = []
    contra = []

    for pergunta in base["perguntas"]:
        peso = pergunta["pesos"].get(trilha_id, 0)
        if peso == 0:
            continue

        resposta = respostas.get(pergunta["id"], 3)
        pontos = pontos + resposta * peso

        if peso > 0:
            minimo = minimo + 1 * peso
            maximo = maximo + 5 * peso
        else:
            minimo = minimo + 5 * peso
            maximo = maximo + 1 * peso

        if peso > 0 and resposta >= 4:
            a_favor.append((peso * resposta, pergunta["texto"] + " (nota " + str(resposta) + ")"))
        if peso > 0 and resposta <= 2:
            contra.append((peso * (3 - resposta), pergunta["texto"] + " (nota " + str(resposta) + ")"))
        if peso < 0 and resposta >= 4:
            contra.append((-peso * resposta, pergunta["texto"] + " (nota " + str(resposta) + ", conflita com a trilha)"))

    percentual = (pontos - minimo) / (maximo - minimo) * 100
    return percentual, a_favor, contra


def aplicar_ajustes(base, trilha_id, respostas):
    total = 0
    aplicados = []

    for regra in base["ajustes"]:
        if regra["trilha"] != trilha_id:
            continue

        todas_verdadeiras = True
        for condicao in regra["condicoes"]:
            resposta = respostas.get(condicao["pergunta"], 3)
            if not comparar(resposta, condicao["op"], condicao["valor"]):
                todas_verdadeiras = False

        if todas_verdadeiras:
            total = total + regra["ajuste"]
            aplicados.append((regra["id"], regra["descricao"], regra["ajuste"]))

    return total, aplicados


def pegar_percentual(item):
    return item["percentual"]


def calcular_compatibilidade(base, respostas):
    resultados = []

    for trilha_id in base["trilhas"]:
        percentual, a_favor, contra = calcular_pontuacao_base(base, trilha_id, respostas)
        ajuste, aplicados = aplicar_ajustes(base, trilha_id, respostas)

        final = percentual + ajuste
        if final < 0:
            final = 0
        if final > 100:
            final = 100

        a_favor.sort(reverse=True)
        contra.sort(reverse=True)

        resultados.append({
            "id": trilha_id,
            "nome": base["trilhas"][trilha_id]["nome"],
            "descricao": base["trilhas"][trilha_id]["descricao"],
            "percentual": round(final, 1),
            "percentual_base": round(percentual, 1),
            "a_favor": [texto for _, texto in a_favor[:3]],
            "contra": [texto for _, texto in contra[:3]],
            "ajustes": aplicados,
        })

    resultados.sort(key=pegar_percentual, reverse=True)
    return resultados


def avaliar_ranking(ranking, respostas):
    avisos = []

    diferenca = ranking[0]["percentual"] - ranking[1]["percentual"]
    if diferenca <= 5:
        avisos.append(
            "Empate parcial: " + ranking[0]["nome"] + " e " + ranking[1]["nome"]
            + " ficaram a apenas " + str(round(diferenca, 1)) + " ponto(s) de distância. "
            "Considere as duas opções."
        )

    notas = list(respostas.values())
    if notas and max(notas) - min(notas) <= 1:
        avisos.append(
            "Suas notas ficaram muito parecidas entre si, então o perfil está pouco definido. "
            "Tente usar mais as notas extremas (1 e 5) para diferenciar o que você gosta do que não gosta."
        )

    if ranking[0]["percentual"] < 60:
        avisos.append("Nenhuma trilha passou de 60% de compatibilidade; trate o resultado como uma pista inicial.")

    return avisos
