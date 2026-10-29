#!/usr/bin/env bash
set -e

case "$1" in
  1)
    [ -d .git ] || git init -b main
    git add .gitignore dados/regras_carreiras.json docs/matriz_decisao.md
    git commit -m "feat: base de conhecimento em JSON e matriz de pesos (Fase 1)"
    ;;
  2)
    git add career_expert/__init__.py career_expert/base_conhecimento.py career_expert/motor.py
    git commit -m "feat: motor de inferência com pontuação ponderada, ajustes e Top 3 (Fase 2)"
    ;;
  3)
    git add career_expert/gaps.py
    git commit -m "feat: análise de gaps e estimativa de tempo de estudo (Fase 3)"
    ;;
  4)
    git add app.py executar.py
    git rm -q --ignore-unmatch career_expert/engine.py career_expert/questions.py career_expert/compat.py career_expert/personas.py
    git commit -m "feat: interface Streamlit em etapas com Top 3, gráfico e roadmap (Fase 4)"
    ;;
  5)
    git add docs/prints tests/__init__.py tests/test_personas.py tests/test_casos_limite.py requirements.txt README.md fazer_commits_v2.sh
    git rm -q --ignore-unmatch fazer_commits.sh
    git commit -m "test/docs: personas, casos limite, requirements e README (Fase 5)"
    ;;
  *)
    echo "Uso: bash fazer_commits_v2.sh [1|2|3|4|5]"
    exit 1
    ;;
esac

git log --oneline | head -5
