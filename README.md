# 🔍 Auditoria Estatística — Caso Incêndio & FLB

Sistema interativo em Python + Streamlit para análise de fraude em seguro por manipulação amostral do Fator de Lucro Bruto (FLB).

---

## 📋 Pré-requisitos

- Python 3.9 ou superior
- pip

---

## 🚀 Como executar

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Execute a aplicação

```bash
streamlit run app.py ou python -m streamlit run app.py
```

O navegador abrirá automaticamente em `http://localhost:8501`.

---

## 📂 Como usar

1. Na **barra lateral (sidebar)**, clique em **"Carregar base de dados"**
2. Faça upload do arquivo **`Incêndio.xls`**
3. Navegue pelas 5 abas de análise

---

## 🗂️ Estrutura das Abas

| Aba | Conteúdo |
|-----|----------|
| 📊 Visão Geral do FLB | Comparativo entre FLB real vs alegado + impacto financeiro |
| 📐 Análise de Assimetria | Histograma, boxplot, outliers e medidas de tendência central |
| 🚨 Indícios de Fraude | Simulação de Monte Carlo (1.000 amostras) + evidências de viés |
| ⚡ Risco & Confiabilidade | Amplitude, variância, desvio-padrão, CV e violin plot |
| 🏛️ Governança | 6 propostas de governança + resumo executivo pericial |

---

## 📊 Colunas esperadas no arquivo Excel

O sistema identifica automaticamente as colunas por nome (flexível). As colunas esperadas são:

- **Mês** do faturamento
- **Código** do atendimento
- **Faturamento** por atendimento (R$)
- **Lucro** obtido no atendimento (R$)
- **FLB** / Margem de lucro (%)

> Se a coluna FLB não existir, ela será calculada automaticamente como `Lucro / Faturamento × 100`.

---

## ⚙️ Parâmetros Configuráveis (Sidebar)

| Parâmetro | Padrão |
|-----------|--------|
| FLB alegado pela empresa | 50,8% |
| Teto da seguradora | 48,0% |
| Impacto financeiro por 1% de FLB | R$ 1.600.000 |
| Tamanho da amostra 1 (empresa) | 134 |
| Tamanho da amostra 2 (empresa) | 119 |

---

## 🎓 Contexto Acadêmico

**PBL 1 — Estatística Decisória · UNDB 2026/1**

Caso: Uma empresa em São Luís-MA foi destruída por incêndio e alegou FLB médio de 50,8% para fins de reembolso do seguro. A seguradora contestou, afirmando que o FLB raramente excede 48%. Este sistema realiza a auditoria estatística sobre a população de 3.005 atendimentos de 2023.

---

## 🛠️ Stack Tecnológica

- **Streamlit** — Interface web interativa
- **Pandas** — Manipulação de dados
- **NumPy** — Computação numérica
- **Plotly** — Visualizações interativas
- **xlrd / openpyxl** — Leitura de arquivos Excel
