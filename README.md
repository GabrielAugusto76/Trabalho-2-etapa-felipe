# 🧭 Consultor Avançado de Carreiras em TI

Sistema especialista com **pontuação ponderada** que analisa o perfil do usuário (notas de 1 a 5), calcula a **compatibilidade percentual com 10 trilhas de TI**, mostra o **Top 3**, identifica **lacunas de competências** (skill gaps) para o nível Júnior e gera um **roadmap** com tecnologias, certificações e projetos de portfólio.

> Trabalho da disciplina de **Inteligência Artificial** — Ciência da Computação, UNIPAC Barbacena.

## Trilhas
Back-end · Front-end & UI/UX · Ciência de Dados e ML · Engenharia de Dados · Cibersegurança · DevOps & SRE · Computação em Nuvem · Mobile · QA · Gestão de Produtos

## Tecnologias
Python 3.10+ · Streamlit (interface em etapas) · Pandas (tabelas e gráfico) · JSON (base de conhecimento) · motor de inferência próprio por soma ponderada

## Instalação e execução

```bash
git clone https://github.com/GabrielAugusto76/Trabalho-2-etapa-felipe.git
cd Trabalho-2-etapa-felipe

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

A aplicação abre em `http://localhost:8501`. Se o comando `streamlit` não for reconhecido, use `python -m streamlit run app.py`.

Alternativa: rodar o arquivo `executar.py` (por exemplo, pelo botão de play do editor), que abre o Streamlit automaticamente.

## Testes

```bash
pytest -v
```

São 15 testes: 10 personas (uma por trilha, incluindo as 4 exigidas: analítico, infra/segurança, visual/front-end e negócios/produto), penalidades, e casos limite (perfil ambíguo dados + web, todas as notas iguais a 1, 3 ou 5, respostas ausentes, gaps zerados ou completos).

## Estrutura

```
├── app.py                       # Interface Streamlit em 3 passos + resultado
├── executar.py                  # Atalho: abre o app sem digitar o comando do Streamlit
├── dados/regras_carreiras.json  # Base de conhecimento (perguntas, pesos, ajustes, planos)
├── career_expert/
│   ├── base_conhecimento.py     # Carrega o JSON
│   ├── motor.py                 # Pontuação ponderada, ajustes, ranking e avisos
│   └── gaps.py                  # Análise de lacunas e estimativa de tempo
├── tests/                       # Personas e casos limite
├── docs/matriz_decisao.md       # Matriz de pesos e regras (Fase 1)
└── requirements.txt
```

## Como funciona

1. **Passo 1 (perfil pessoal):** nome, conhecimentos que já possui e horas de estudo por semana.
2. **Passo 2 (afinidades técnicas)** e **Passo 3 (objetivos de carreira):** 18 perguntas com notas de 1 a 5.
3. **Motor:** para cada trilha, soma `nota × peso` (pesos negativos penalizam perfis conflitantes), converte em porcentagem e aplica as regras de ajuste do JSON (penalidades e desempates).
4. **Resultado:** Top 3 com porcentagens, gráfico das 10 trilhas, avisos (empate parcial, perfil indefinido, baixa compatibilidade) e a justificativa dos pontos fortes e de atenção.
5. **Gaps e roadmap:** compara as competências do nível Júnior da trilha com o que o usuário já tem, lista o que estudar primeiro, estima o tempo e sugere certificações e projetos.

Os detalhes da pontuação e todos os pesos estão em [`docs/matriz_decisao.md`](docs/matriz_decisao.md).

## Fases do desenvolvimento

| Fase | O que foi feito | Arquivos |
|---|---|---|
| 1. Engenharia do conhecimento | Modelagem do JSON com perguntas, pesos e regras de ajuste | `dados/regras_carreiras.json`, `docs/matriz_decisao.md` |
| 2. Motor de inferência | Leitura do JSON, pontuação ponderada, ajustes e Top 3 | `career_expert/motor.py`, `career_expert/base_conhecimento.py` |
| 3. Gaps e roadmap | Análise de lacunas para o nível Júnior e plano de estudo | `career_expert/gaps.py` |
| 4. Interface web | Wizard em 3 passos no Streamlit com gráficos e plano | `app.py` |
| 5. Testes e casos limite | Personas, perfis ambíguos, empates e extremos | `tests/` |
## Observações
- Certificações e cursos sugeridos são pontos de partida; confira preço e disponibilidade antes de contratar.
- Para ajustar o sistema, edite o `dados/regras_carreiras.json`; não é preciso mexer no código Python.

## Autor
**Nome:** Gabriel Augusto Bedeschi Domingos · **Professor:** Felipe Roncalli de Paula Carneiro
**Matricula 241-007248

##Prints
<img width="580" height="477" alt="WhatsApp Image 2026-10-29 at 15 43 26 (5)" src="https://github.com/user-attachments/assets/462557c0-c4d9-4b4b-8bf1-5a71a6e85418" />
<img width="718" height="519" alt="WhatsApp Image 2026-10-29 at 15 43 26 (3)" src="https://github.com/user-attachments/assets/bc7aaafa-56e9-477c-bef4-5e9d944cafed" />
<img width="489" height="797" alt="WhatsApp Image 2026-10-29 at 15 43 26 (1)" src="https://github.com/user-attachments/assets/fd9fe3ea-7788-400a-b23d-c43b236d01aa" />
<img width="363" height="569" alt="WhatsApp Image 2026-10-29 at 15 43 26 (4)" src="https://github.com/user-attachments/assets/269c5dcc-e70f-45a7-b976-713a0663b6c7" />
<img width="319" height="797" alt="WhatsApp Image 2026-10-29 at 15 43 26 (2)" src="https://github.com/user-attachments/assets/e0585c11-730d-46d6-a09d-74b4c0875a28" />
<img width="369" height="703" alt="WhatsApp Image 2026-10-29 at 15 43 26" src="https://github.com/user-attachments/assets/db0a7e92-1f39-4c58-bbd0-84d5d994af25" />





