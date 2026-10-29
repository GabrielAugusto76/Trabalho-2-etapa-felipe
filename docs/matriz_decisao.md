# Matriz de Decisão (Fase 1: Engenharia do Conhecimento)

Toda a base de conhecimento fica em [`dados/regras_carreiras.json`](../dados/regras_carreiras.json). O código Python apenas lê esse arquivo, então é possível mudar pesos, perguntas e trilhas sem alterar o motor.

## Como a pontuação funciona

1. O usuário dá uma nota de 1 a 5 em cada pergunta (escala Likert).
2. Para cada trilha: `pontos = soma(nota × peso)` das perguntas que têm peso para ela.
3. Pesos positivos aproximam o perfil da trilha; **pesos negativos penalizam perfis conflitantes**.
4. A pontuação vira porcentagem entre o pior e o melhor resultado possíveis da trilha: `(pontos - mínimo) / (máximo - mínimo) × 100`.
5. As **regras de ajuste** somam ou subtraem pontos percentuais em situações específicas (penalidades e desempates).
6. O resultado é limitado entre 0% e 100% e ordenado, formando o Top 3.

## Legenda das trilhas

| Sigla | Trilha |
|---|---|
| BE | Desenvolvimento Back-end |
| FE | Desenvolvimento Front-end & UI/UX |
| DS | Ciência de Dados e Machine Learning |
| DE | Engenharia de Dados |
| SEC | Cibersegurança (Security / Pentesting) |
| DO | DevOps & SRE |
| CL | Computação em Nuvem (Cloud Architecture) |
| MO | Desenvolvimento Mobile |
| QA | Engenharia de Qualidade e Testes (QA) |
| PM | Gestão de Produtos (Product Management) |

## Pesos das perguntas por trilha

| Pergunta | Passo | BE | FE | DS | DE | SEC | DO | CL | MO | QA | PM |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Resolver problemas com lógica e algoritmos | 2 | +3 | +1 | +1 | +2 | +1 | +1 |  | +2 | +1 |  |
| Matemática e estatística | 2 |  | -1 | +3 | +1 | +1 |  |  |  |  |  |
| Criar modelos de inteligência artificial e previsões | 2 |  |  | +3 | -1 |  |  |  |  |  |  |
| Trabalhar com grandes volumes de dados | 2 | +1 |  | +2 | +3 |  |  |  |  |  |  |
| Construir APIs, regras de negócio e bancos de dados | 2 | +3 |  |  | +1 |  |  |  | +1 |  |  |
| Design visual e experiência do usuário | 2 | -1 | +3 |  | -1 | -1 | -1 |  | +2 |  | +1 |
| Criar aplicativos para celular | 2 |  | +1 |  |  |  |  |  | +3 |  |  |
| Infraestrutura, servidores e redes | 2 |  | -1 | -1 | +1 | +2 | +3 | +3 | -1 |  |  |
| Automatizar tarefas repetitivas e entregas de software | 2 |  |  |  | +2 |  | +3 | +1 |  | +2 |  |
| Segurança e proteção contra invasões | 2 |  |  |  |  | +3 | +1 | +1 |  |  |  |
| Planejar arquiteturas escaláveis e custos de nuvem | 2 | +1 |  |  | +1 |  | +2 | +3 |  |  |  |
| Testar sistemas e encontrar falhas | 2 |  |  |  |  | +1 | +1 |  |  | +3 |  |
| Ver o usuário usando algo que eu criei | 3 | +1 | +2 |  |  |  |  |  | +2 |  | +2 |
| Investigar detalhes e descobrir a causa de problemas | 3 | +1 |  |  |  | +2 | +1 |  |  | +2 |  |
| Conversar com clientes e equipes | 3 | -1 | +1 |  | -1 | -1 |  | +1 |  |  | +3 |
| Priorizar o que construir e tomar decisões de produto | 3 |  |  |  |  |  |  |  |  |  | +3 |
| Entender resultado de negócio e métricas | 3 |  |  | +1 |  |  |  | +1 |  |  | +2 |
| Resolver incidentes e atuar em plantões | 3 |  |  |  |  | +1 | +2 | +1 |  |  |  |

Passo 2 = afinidades técnicas; Passo 3 = objetivos de carreira.

## Regras de ajuste (penalidades e desempates)

| ID | Condição | Trilha | Ajuste (pontos %) |
|---|---|---|---|
| A01 | q_mat <= 2 | DS | -15 |
| A02 | q_ia <= 2 | DS | -10 |
| A03 | q_design <= 2 | FE | -15 |
| A04 | q_mobile <= 2 | MO | -10 |
| A05 | q_seguranca <= 2 | SEC | -15 |
| A06 | q_infra <= 2 | DO | -10 |
| A07 | q_infra <= 2 | CL | -10 |
| A08 | q_pessoas <= 2 | PM | -15 |
| A09 | q_testes <= 2 | QA | -15 |
| A10 | q_dados <= 2 | DE | -15 |
| A11 | q_apis <= 2 | BE | -10 |
| A12 | q_mat >= 4 e q_ia >= 4 | DS | +8 |
| A13 | q_dados >= 4 e q_ia <= 3 | DE | +8 |
| A14 | q_infra >= 4 e q_nuvem >= 4 | CL | +6 |
| A15 | q_infra >= 4 e q_automacao >= 4 | DO | +6 |

## Pontos de ambiguidade tratados

| Par confundível | Como o sistema desempata |
|---|---|
| Cientista de Dados × Engenheiro de Dados | Pesos de `q_mat`, `q_ia` e `q_dados` e regras A12/A13 |
| DevOps × Cloud | Pesos de `q_automacao`, `q_incidentes` e `q_nuvem` e regras A14/A15 |
| Front-end × Mobile | Peso de `q_mobile` e regra A04 |
| Dados + Web (perfil misto) | Sistema mostra o Top 3 e avisa quando há empate parcial (diferença de até 5 pontos) |

## Estrutura do JSON

```
escala        -> rótulos das notas de 1 a 5
trilhas       -> id, nome e descrição das 10 trilhas
perguntas     -> id, etapa (2 ou 3), texto e pesos por trilha
ajustes       -> regras com condições (pergunta, operador, valor), trilha e ajuste
competencias  -> nome e horas estimadas de estudo de cada competência
planos        -> por trilha: competências do nível Júnior, certificações e projetos
```
