"""
=============================================================================
 AUDITORIA ESTATÍSTICA — CASO INCÊNDIO & FLB
 Sistema Interativo para Análise de Fraude em Seguro
 Desenvolvido com Streamlit | Python
=============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─── CONFIG DA PÁGINA ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Auditoria FLB | Caso Incêndio",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CORES ───────────────────────────────────────────────────────────────────
AZUL_ESCURO   = "#0B1F3A"
AZUL_MEDIO    = "#112D4E"
AZUL_CARD     = "#163A5F"
DOURADO       = "#C8A951"
DOURADO_CLARO = "#E2C97E"
VERMELHO      = "#C0392B"
VERDE         = "#1A936F"
CINZA_TEXTO   = "#B0BEC5"
BRANCO        = "#F5F5F5"
GRID_COLOR    = "#1E3A5F"


def tema_layout(titulo: str = "", altura: int = 400) -> dict:
    """
    Retorna somente as chaves BASE do layout Plotly (sem xaxis/yaxis).
    Isso evita conflito quando update_layout() recebe yaxis= ou xaxis= extras.
    """
    return dict(
        paper_bgcolor=AZUL_ESCURO,
        plot_bgcolor="#0F2A45",
        font=dict(color=BRANCO, family="Georgia, serif"),
        title=dict(text=titulo, font=dict(color=DOURADO_CLARO, size=16)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=BRANCO)),
        margin=dict(t=60, b=40, l=40, r=20),
        height=altura,
    )


def estilizar_eixos(fig, x_title: str = "", y_title: str = ""):
    """Aplica estilo escuro padrão nos eixos após update_layout."""
    fig.update_xaxes(
        gridcolor=GRID_COLOR,
        zerolinecolor=GRID_COLOR,
        color=CINZA_TEXTO,
        title_text=x_title,
    )
    fig.update_yaxes(
        gridcolor=GRID_COLOR,
        zerolinecolor=GRID_COLOR,
        color=CINZA_TEXTO,
        title_text=y_title,
    )
    return fig


# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;600&display=swap');

  html, body, [class*="css"] {{
      background-color: {AZUL_ESCURO};
      color: {BRANCO};
      font-family: 'Source Sans 3', sans-serif;
  }}
  section[data-testid="stSidebar"] {{
      background-color: {AZUL_MEDIO};
      border-right: 2px solid {DOURADO};
  }}
  section[data-testid="stSidebar"] * {{ color: {BRANCO} !important; }}
  .stTabs [data-baseweb="tab-list"] {{
      gap: 4px; background-color: {AZUL_MEDIO};
      border-radius: 10px; padding: 6px;
  }}
  .stTabs [data-baseweb="tab"] {{
      background-color: transparent; color: {CINZA_TEXTO} !important;
      border-radius: 8px; padding: 10px 18px;
      font-family: 'Source Sans 3', sans-serif;
      font-weight: 600; font-size: 0.85rem; transition: all 0.3s ease;
  }}
  .stTabs [aria-selected="true"] {{
      background-color: {DOURADO} !important;
      color: {AZUL_ESCURO} !important;
  }}
  [data-testid="metric-container"] {{
      background-color: {AZUL_CARD};
      border: 1px solid rgba(200,169,81,0.3);
      border-radius: 12px; padding: 16px;
  }}
  [data-testid="metric-container"] label {{
      color: {CINZA_TEXTO} !important; font-size: 0.8rem;
  }}
  [data-testid="metric-container"] [data-testid="stMetricValue"] {{
      color: {DOURADO_CLARO} !important;
      font-family: 'Playfair Display', serif; font-size: 1.8rem !important;
  }}
  .main-header {{
      background: linear-gradient(135deg, {AZUL_MEDIO} 0%, #0D2137 100%);
      border-left: 5px solid {DOURADO}; border-radius: 0 12px 12px 0;
      padding: 28px 32px; margin-bottom: 28px;
  }}
  .main-header h1 {{
      font-family: 'Playfair Display', serif; font-size: 2rem;
      font-weight: 900; color: {DOURADO_CLARO}; margin: 0 0 6px 0;
  }}
  .main-header p {{ color: {CINZA_TEXTO}; font-size: 0.95rem; margin: 0; }}
  .section-title {{
      font-family: 'Playfair Display', serif; font-size: 1.35rem;
      color: {DOURADO_CLARO}; border-bottom: 2px solid rgba(200,169,81,0.35);
      padding-bottom: 8px; margin: 24px 0 16px 0;
  }}
  .info-box {{
      background-color: rgba(17,45,78,0.8); border-left: 4px solid {DOURADO};
      border-radius: 0 10px 10px 0; padding: 16px 20px;
      margin: 12px 0; font-size: 0.92rem; line-height: 1.7;
  }}
  .alert-box {{
      background-color: rgba(192,57,43,0.15); border-left: 4px solid {VERMELHO};
      border-radius: 0 10px 10px 0; padding: 16px 20px;
      margin: 12px 0; font-size: 0.92rem; line-height: 1.7;
  }}
  .success-box {{
      background-color: rgba(26,147,111,0.15); border-left: 4px solid {VERDE};
      border-radius: 0 10px 10px 0; padding: 16px 20px;
      margin: 12px 0; font-size: 0.92rem; line-height: 1.7;
  }}
  .kpi-card {{
      background: linear-gradient(135deg, {AZUL_CARD}, #0F2F50);
      border: 1px solid rgba(200,169,81,0.25); border-radius: 14px;
      padding: 22px; text-align: center; margin: 6px 0;
  }}
  .kpi-label {{
      font-family: 'Source Sans 3', sans-serif; font-size: 0.78rem;
      color: {CINZA_TEXTO}; text-transform: uppercase;
      letter-spacing: 1.2px; margin-bottom: 8px;
  }}
  .kpi-value {{
      font-family: 'Playfair Display', serif; font-size: 2rem;
      font-weight: 700; color: {DOURADO_CLARO};
  }}
  .kpi-delta {{ font-size: 0.82rem; margin-top: 6px; }}
  .kpi-red   {{ color: #E74C3C; }}
  .kpi-green {{ color: #2ECC71; }}
  .kpi-gold  {{ color: {DOURADO}; }}
  .verdict {{
      background: linear-gradient(135deg, rgba(192,57,43,0.25), rgba(192,57,43,0.05));
      border: 2px solid {VERMELHO}; border-radius: 12px;
      padding: 20px 28px; text-align: center;
      font-family: 'Playfair Display', serif; font-size: 1.1rem;
      color: #E74C3C; margin: 20px 0;
  }}
  [data-testid="stFileUploader"] {{
      background-color: {AZUL_CARD};
      border: 2px dashed rgba(200,169,81,0.4);
      border-radius: 10px; padding: 10px;
  }}
  hr {{ border-color: rgba(200,169,81,0.2); margin: 20px 0; }}
  footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


# ─── FUNÇÕES AUXILIARES ───────────────────────────────────────────────────────

def kpi_card(label: str, value: str, delta: str = "", color: str = "gold") -> str:
    delta_html = f'<div class="kpi-delta kpi-{color}">{delta}</div>' if delta else ""
    return f"""<div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>"""


def fmt_brl(val: float) -> str:
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_pct(val: float) -> str:
    return f"{val:.2f}%"


def calcular_moda(serie: pd.Series) -> float:
    return round(serie.round(2).mode()[0], 4)


@st.cache_data(show_spinner=False)
def processar_dados(uploaded_file) -> pd.DataFrame:
    """Lê XLS/XLSX e padroniza colunas com fallback por posição."""
    try:
        df = pd.read_excel(uploaded_file, engine="xlrd")
    except Exception:
        try:
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        except Exception as e:
            st.error(f"Não foi possível ler o arquivo: {e}")
            return None

    df.columns = [str(c).strip().replace("\xa0", "").replace("\n", " ") for c in df.columns]
    df = df.dropna(how="all")
    colunas_originais = list(df.columns)

    # ── Mapeamento por nome ─────────────────────────────────────────────
    mapa = {}
    for col in df.columns:
        cl = col.lower()
        if any(p in cl for p in ["mês", "mes", "month", "competencia", "competência"]):
            mapa[col] = "Mês"
        elif any(p in cl for p in ["código", "codigo", "cod.", "cod ", "atendimento", "nº", "numero", "número", "id"]):
            if "Código" not in mapa.values():
                mapa[col] = "Código"
        elif any(p in cl for p in ["faturamento", "receita", "venda", "fat.", "valor"]):
            mapa[col] = "Faturamento"
        elif any(p in cl for p in ["lucro", "profit", "resultado", "ganho"]):
            mapa[col] = "Lucro"
        elif any(p in cl for p in ["margem", "flb", "fator", "%", "percentual", "percent", "taxa"]):
            mapa[col] = "FLB"
    df = df.rename(columns=mapa)

    # ── Fallback por posição ─────────────────────────────────────────────
    # PBL: col0=Mês  col1=Código  col2=Faturamento  col3=Lucro  col4=FLB
    pos_map = {0: "Mês", 1: "Código", 2: "Faturamento", 3: "Lucro", 4: "FLB"}
    cols_now = list(df.columns)
    for pos, nome in pos_map.items():
        if nome not in df.columns and pos < len(cols_now):
            if cols_now[pos] not in pos_map.values():
                df = df.rename(columns={cols_now[pos]: nome})

    # ── Calcula FLB se ausente ───────────────────────────────────────────
    if "FLB" not in df.columns:
        if "Lucro" in df.columns and "Faturamento" in df.columns:
            df["FLB"] = (df["Lucro"] / df["Faturamento"]) * 100
        else:
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if num_cols:
                df["FLB"] = pd.to_numeric(df[num_cols[-1]], errors="coerce")
                st.warning(f"⚠️ Usando '{num_cols[-1]}' como FLB. Colunas originais: {colunas_originais}")
            else:
                st.error(f"Coluna FLB não encontrada. Colunas: {colunas_originais}")
                return None

    # ── Garante numéricos ────────────────────────────────────────────────
    for c in ["Faturamento", "Lucro", "FLB"]:
        if c in df.columns:
            if df[c].dtype == object:
                df[c] = df[c].astype(str).str.replace(",", ".").str.replace(r"[^\d.\-]", "", regex=True)
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(subset=["FLB"])
    df = df[df["FLB"] != 0]

    if len(df) == 0:
        st.error(f"Nenhum registro válido após limpeza. Colunas originais: {colunas_originais}")
        return None
    return df


def estatisticas_completas(serie: pd.Series) -> dict:
    q1, q3 = serie.quantile(0.25), serie.quantile(0.75)
    iqr = q3 - q1
    return {
        "Média":          serie.mean(),
        "Mediana":        serie.median(),
        "Moda":           calcular_moda(serie),
        "Desvio-Padrão":  serie.std(),
        "Variância":      serie.var(),
        "Amplitude":      serie.max() - serie.min(),
        "CV (%)":         (serie.std() / serie.mean()) * 100,
        "Mín":            serie.min(),
        "Máx":            serie.max(),
        "Q1":             q1,
        "Q3":             q3,
        "IQR":            iqr,
        "Limite Sup IQR": q3 + 1.5 * iqr,
        "Limite Inf IQR": q1 - 1.5 * iqr,
        "Assimetria":     serie.skew(),
        "Curtose":        serie.kurtosis(),
        "N":              len(serie),
    }


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding:10px 0 20px;">
        <div style="font-family:'Playfair Display',serif; font-size:1.4rem;
                    color:{DOURADO_CLARO}; font-weight:700;">🔍 Auditoria FLB</div>
        <div style="font-size:0.75rem; color:{CINZA_TEXTO}; margin-top:4px;">
            Caso Incêndio · Análise Estatística</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    uploaded_file = st.file_uploader(
        "📂 Carregar base de dados", type=["xls", "xlsx"],
        help="Arquivo Excel com os 3.005 atendimentos de 2023 (Incêndio.xls)"
    )

    st.markdown("---")
    st.markdown(f"<div style='font-size:0.78rem;color:{CINZA_TEXTO};'>⚙️ Parâmetros do Caso</div>",
                unsafe_allow_html=True)

    FLB_EMPRESA    = st.number_input("FLB alegado pela empresa (%)", value=50.8, step=0.1,
                                     min_value=0.0, max_value=100.0, format="%.1f")
    FLB_SEGURADORA = st.number_input("Teto da seguradora (%)", value=48.0, step=0.1,
                                     min_value=0.0, max_value=100.0, format="%.1f")
    IMPACTO_1PCT   = st.number_input("Impacto por 1% de FLB (R$)",
                                     value=1_600_000.0, step=100_000.0, format="%.0f")
    TAM_AMOSTRA1   = st.number_input("Tamanho amostra 1 (empresa)", value=134, step=1)
    TAM_AMOSTRA2   = st.number_input("Tamanho amostra 2 (empresa)", value=119, step=1)

    st.markdown("---")
    st.markdown(f"""
    <div style='font-size:0.72rem; color:{CINZA_TEXTO}; line-height:1.6;'>
        📚 <b>Referência</b><br>PBL 1 — Estatística Decisória<br>UNDB · 2026/1<br><br>
        Dados: população de 3.005 atendimentos (2023)
    </div>
    """, unsafe_allow_html=True)

    if uploaded_file is not None:
        with st.expander("🔎 Diagnóstico de Colunas"):
            try:
                _d = pd.read_excel(uploaded_file, engine="xlrd", nrows=3)
            except Exception:
                try:
                    _d = pd.read_excel(uploaded_file, engine="openpyxl", nrows=3)
                except Exception:
                    _d = None
            if _d is not None:
                st.markdown("**Colunas detectadas:**")
                for i, c in enumerate(_d.columns):
                    st.markdown(f"`col {i}` → `{c}`")
                st.markdown("**Primeiros registros:**")
                for _, row in _d.iterrows():
                    st.text(" | ".join([str(v)[:18] for v in row.values]))


# ─── CABEÇALHO ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="main-header">
    <h1>🔍 Auditoria Estatística — Caso Incêndio</h1>
    <p>Análise pericial do Fator de Lucro Bruto (FLB) · Investigação de manipulação amostral ·
    Subsídio técnico para decisão judicial</p>
</div>
""", unsafe_allow_html=True)


# ─── SEM ARQUIVO ──────────────────────────────────────────────────────────────
if uploaded_file is None:
    st.markdown(f"""
    <div class="info-box" style="text-align:center; padding:40px 30px;">
        <div style="font-size:3rem; margin-bottom:16px;">📂</div>
        <div style="font-family:'Playfair Display',serif; font-size:1.2rem;
                    color:{DOURADO_CLARO}; margin-bottom:10px;">Aguardando arquivo de dados</div>
        <div style="color:{CINZA_TEXTO}; font-size:0.9rem; line-height:1.8;">
            Utilize o painel lateral para carregar o arquivo <b>Incêndio.xls</b>.<br>
            O sistema processará automaticamente todos os 3.005 atendimentos de 2023.
        </div>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, (icon, titulo, desc) in zip(
        [c1, c2, c3],
        [("📋","Caso","Incêndio · São Luís-MA"),
         ("📊","Método","Estatística Descritiva"),
         ("⚖️","Objetivo","Detecção de Fraude Amostral")]
    ):
        with col:
            st.markdown(kpi_card(titulo, icon, desc, "gold"), unsafe_allow_html=True)
    st.stop()


# ─── PROCESSAMENTO ────────────────────────────────────────────────────────────
with st.spinner("Processando dados..."):
    df = processar_dados(uploaded_file)

if df is None or df.empty:
    st.error("Erro ao processar o arquivo. Verifique o formato e tente novamente.")
    st.stop()

flb               = df["FLB"]
est               = estatisticas_completas(flb)
outliers_sup_mask = flb > est["Limite Sup IQR"]
outliers_inf_mask = flb < est["Limite Inf IQR"]


# ─── ABAS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Visão Geral do FLB",
    "📐 Análise de Assimetria",
    "🚨 Indícios de Fraude",
    "⚡ Risco & Confiabilidade",
    "🏛️ Governança",
])


# ══════════════════════════════════════════════════════════════════════════════
#  ABA 1 — VISÃO GERAL DO FLB
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">📊 Comparativo de Estimativas do FLB</div>',
                unsafe_allow_html=True)

    flb_real           = est["Média"]
    diff_empresa       = FLB_EMPRESA - flb_real
    diff_seguradora    = FLB_EMPRESA - FLB_SEGURADORA
    impacto_empresa    = diff_empresa    * IMPACTO_1PCT
    impacto_seguradora = diff_seguradora * IMPACTO_1PCT

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("FLB Alegado (Empresa)", fmt_pct(FLB_EMPRESA),
                             "Estimativa contestada", "gold"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("FLB Real (Pop. 2023)", fmt_pct(flb_real),
                             f"N = {est['N']:,} atendimentos",
                             "green" if flb_real < FLB_EMPRESA else "red"),
                    unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("Teto Seguradora", fmt_pct(FLB_SEGURADORA),
                             "Referência contratual", "gold"), unsafe_allow_html=True)
    with c4:
        cor = "red" if diff_empresa > 0 else "green"
        st.markdown(kpi_card("Diferença (Empresa vs Real)",
                             f"{diff_empresa:+.2f}%",
                             fmt_brl(abs(impacto_empresa)) + " de impacto", cor),
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Gráfico de barras comparativo
    fig_bar = go.Figure()
    for lab, val, cor in zip(
        ["FLB Real (Pop. 2023)", "Teto Seguradora", "FLB Alegado (Empresa)"],
        [flb_real, FLB_SEGURADORA, FLB_EMPRESA],
        [VERDE, DOURADO, VERMELHO],
    ):
        fig_bar.add_trace(go.Bar(
            x=[lab], y=[val], marker_color=cor,
            text=f"{val:.2f}%", textposition="outside",
            textfont=dict(size=14, color=BRANCO), name=lab, width=0.35,
        ))
    fig_bar.add_hline(y=FLB_SEGURADORA, line_dash="dash", line_color=DOURADO, line_width=1.5,
                      annotation_text=f"Teto: {FLB_SEGURADORA}%", annotation_font_color=DOURADO)
    fig_bar.update_layout(**tema_layout("Comparativo de Estimativas do FLB (%)", 380),
                          showlegend=False)
    fig_bar.update_yaxes(range=[0, FLB_EMPRESA * 1.15], ticksuffix="%",
                         gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, color=CINZA_TEXTO)
    fig_bar.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, color=CINZA_TEXTO)
    st.plotly_chart(fig_bar, use_container_width=True)

    # Tabela impacto financeiro
    st.markdown('<div class="section-title">💰 Impacto Financeiro</div>', unsafe_allow_html=True)
    impacto_df = pd.DataFrame({
        "Comparação": ["FLB Empresa vs FLB Real (2023)", "FLB Empresa vs Teto Seguradora"],
        "Diferença (p.p.)": [f"{diff_empresa:+.2f}", f"{diff_seguradora:+.2f}"],
        "Impacto Financeiro Estimado": [fmt_brl(abs(impacto_empresa)), fmt_brl(abs(impacto_seguradora))],
        "Favorece": [
            "Empresa" if diff_empresa > 0 else "Seguradora",
            "Empresa" if diff_seguradora > 0 else "Seguradora",
        ],
    })
    st.dataframe(impacto_df, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div class="info-box">
        <b>📌 Interpretação:</b><br>
        O FLB médio real da população de 2023 é de <b>{fmt_pct(flb_real)}</b>, enquanto a empresa alegou
        <b>{fmt_pct(FLB_EMPRESA)}</b> — uma superestimativa de <b>{diff_empresa:+.2f} pontos percentuais</b>.
        Cada 1% de FLB representa <b>{fmt_brl(IMPACTO_1PCT)}</b> de reembolso adicional, o que implica
        um impacto de aproximadamente <b>{fmt_brl(abs(impacto_empresa))}</b> que a empresa receberia indevidamente.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">📋 Medidas de Tendência Central</div>',
                unsafe_allow_html=True)
    mc_df = pd.DataFrame({
        "Medida": ["Média", "Mediana", "Moda"],
        "Valor (%)": [f"{est['Média']:.4f}", f"{est['Mediana']:.4f}", f"{est['Moda']:.4f}"],
        "Interpretação": [
            "Valor esperado do FLB para qualquer atendimento",
            "50% dos atendimentos ficam abaixo deste valor",
            "Faixa de margem mais frequente na população",
        ],
    })
    st.dataframe(mc_df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ABA 2 — ANÁLISE DE ASSIMETRIA
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">📐 Distribuição e Forma da Curva do FLB</div>',
                unsafe_allow_html=True)

    col_a, col_b = st.columns([2, 1])
    with col_a:
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=flb, nbinsx=60, marker_color=AZUL_CARD,
            marker_line_color=DOURADO, marker_line_width=0.5,
            opacity=0.8, name="FLB", histnorm="probability density",
        ))
        for val, lab, cor in [
            (est["Média"],   f"Média ({est['Média']:.2f}%)",    VERMELHO),
            (est["Mediana"], f"Mediana ({est['Mediana']:.2f}%)", VERDE),
            (est["Moda"],    f"Moda ({est['Moda']:.2f}%)",      DOURADO),
        ]:
            fig_hist.add_vline(x=val, line_width=2, line_dash="dash", line_color=cor,
                               annotation_text=lab, annotation_font_color=cor,
                               annotation_font_size=11)
        fig_hist.update_layout(**tema_layout("Histograma do FLB — População Completa (2023)", 380))
        estilizar_eixos(fig_hist, "FLB (%)", "Densidade")
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_b:
        ass  = est["Assimetria"]
        curt = est["Curtose"]
        tipo_ass = ("Positiva (Cauda Direita)" if ass > 0.5
                    else "Negativa (Cauda Esquerda)" if ass < -0.5
                    else "Aproximadamente Simétrica")
        interp_ass = (
            "Maioria dos valores se concentra abaixo da média; existem atendimentos com margens excepcionalmente altas."
            if ass > 0.5 else
            "Maioria dos valores se concentra acima da média; há atendimentos com margens muito baixas."
            if ass < -0.5 else
            "A distribuição é razoavelmente equilibrada em torno da média."
        )
        tipo_curt = (
            "Leptocúrtica — Caudas pesadas, maior concentração central e presença de outliers extremos."
            if curt > 1 else
            "Platicúrtica — Distribuição mais achatada, dados mais dispersos."
            if curt < -1 else
            "Mesocúrtica — Próxima da distribuição normal."
        )
        st.markdown(f"""
        <div class="kpi-card" style="margin-top:0;">
            <div class="kpi-label">Coeficiente de Assimetria</div>
            <div class="kpi-value">{ass:.4f}</div>
            <div style="color:{CINZA_TEXTO}; font-size:0.8rem; margin-top:8px;">{tipo_ass}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Curtose (Excesso)</div>
            <div class="kpi-value">{curt:.4f}</div>
            <div style="color:{CINZA_TEXTO}; font-size:0.8rem; margin-top:8px;">{tipo_curt[:35]}...</div>
        </div>
        <div class="info-box" style="margin-top:12px; font-size:0.82rem;">
            <b>Assimetria:</b><br>{interp_ass}<br><br>
            <b>Curtose:</b><br>{tipo_curt}
        </div>
        """, unsafe_allow_html=True)

    # Boxplot
    st.markdown('<div class="section-title">📦 Boxplot e Detecção de Outliers</div>',
                unsafe_allow_html=True)
    n_out_sup = outliers_sup_mask.sum()
    n_out_inf = outliers_inf_mask.sum()
    n_out_tot = n_out_sup + n_out_inf

    fig_box = go.Figure()
    fig_box.add_trace(go.Box(
        y=flb, name="FLB Pop. Completa",
        marker_color=DOURADO, line_color=DOURADO_CLARO,
        fillcolor="rgba(200,169,81,0.15)", boxpoints="outliers",
        jitter=0.3, pointpos=-1.8,
        marker=dict(size=3, opacity=0.4, color=VERMELHO), whiskerwidth=0.5,
    ))
    fig_box.add_hline(y=FLB_EMPRESA, line_dash="dash", line_color=VERMELHO,
                      annotation_text=f"FLB Empresa: {FLB_EMPRESA}%",
                      annotation_font_color=VERMELHO)
    fig_box.add_hline(y=FLB_SEGURADORA, line_dash="dot", line_color=VERDE,
                      annotation_text=f"Teto Seguradora: {FLB_SEGURADORA}%",
                      annotation_font_color=VERDE)
    fig_box.update_layout(**tema_layout("Boxplot do FLB — Identificação de Outliers e Quartis", 420))
    estilizar_eixos(fig_box, "", "FLB (%)")
    st.plotly_chart(fig_box, use_container_width=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    for col, lab, val in zip(
        [c1, c2, c3, c4, c5],
        ["Q1 (25%)", "Mediana (Q2)", "Q3 (75%)", "IQR", "Outliers"],
        [est["Q1"], est["Mediana"], est["Q3"], est["IQR"], n_out_tot],
    ):
        with col:
            if lab == "Outliers":
                st.markdown(kpi_card(lab, str(val), f"{val/est['N']*100:.1f}% da pop.", "red"),
                            unsafe_allow_html=True)
            else:
                st.markdown(kpi_card(lab, f"{val:.2f}%", "", "gold"), unsafe_allow_html=True)

    st.markdown(f"""
    <div class="alert-box">
        <b>⚠️ Atenção — Outliers Superiores:</b><br>
        Foram identificados <b>{n_out_sup} atendimentos ({n_out_sup/est['N']*100:.1f}%)</b> com FLB
        acima do limite IQR ({est['Limite Sup IQR']:.2f}%). São exatamente esses atendimentos que,
        se selecionados propositalmente, inflariam a média amostral — a essência da acusação de fraude.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">📏 Aplicabilidade das Medidas de Tendência Central</div>',
                unsafe_allow_html=True)
    apl_df = pd.DataFrame({
        "Medida": ["Média", "Mediana", "Moda"],
        "Valor": [f"{est['Média']:.4f}%", f"{est['Mediana']:.4f}%", f"{est['Moda']:.4f}%"],
        "Sensível a Outliers": ["Sim ⚠️", "Não ✅", "Não ✅"],
        "Recomendação": [
            "Use com cautela — outliers distorcem o resultado",
            "Melhor medida central para esta distribuição assimétrica",
            "Útil para identificar o FLB mais recorrente na operação",
        ],
    })
    st.dataframe(apl_df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ABA 3 — INDÍCIOS DE FRAUDE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">🚨 Análise de Viés Amostral</div>',
                unsafe_allow_html=True)

    TAM_TOTAL    = int(TAM_AMOSTRA1 + TAM_AMOSTRA2)
    N_SIMULACOES = 1000
    medias_sim   = np.array([
        flb.sample(n=TAM_TOTAL, random_state=i).mean()
        for i in range(N_SIMULACOES)
    ])
    p_valor_aprox = (medias_sim >= FLB_EMPRESA).mean()
    media_dist    = medias_sim.mean()
    std_dist      = medias_sim.std()
    desvios       = (FLB_EMPRESA - media_dist) / std_dist

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("FLB Médio Simulado", fmt_pct(media_dist),
                             "Esperado aleatório", "green"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("FLB Alegado (Empresa)", fmt_pct(FLB_EMPRESA),
                             "Valor questionado", "red"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("Desvios-Padrão acima", f"{desvios:.1f}σ",
                             "Da média simulada", "red"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card("P(FLB ≥ 50,8%) aleatório",
                             f"{p_valor_aprox*100:.2f}%", "Prob. de ocorrência casual", "red"),
                    unsafe_allow_html=True)

    # Histograma simulações Monte Carlo
    fig_sim = go.Figure()
    fig_sim.add_trace(go.Histogram(
        x=medias_sim, nbinsx=50, marker_color=AZUL_CARD,
        marker_line_color=DOURADO, marker_line_width=0.5,
        opacity=0.85, name="Amostras Aleatórias", histnorm="probability density",
    ))
    fig_sim.add_vline(x=media_dist, line_color=VERDE, line_width=2, line_dash="dash",
                      annotation_text=f"Média simulada: {media_dist:.2f}%",
                      annotation_font_color=VERDE, annotation_font_size=11)
    fig_sim.add_vline(x=FLB_EMPRESA, line_color=VERMELHO, line_width=2.5,
                      annotation_text=f"FLB empresa: {FLB_EMPRESA}%",
                      annotation_font_color=VERMELHO, annotation_font_size=11)
    fig_sim.add_vline(x=FLB_SEGURADORA, line_color=DOURADO, line_width=1.5, line_dash="dot",
                      annotation_text=f"Teto: {FLB_SEGURADORA}%",
                      annotation_font_color=DOURADO, annotation_font_size=11)
    fig_sim.add_vrect(x0=float(FLB_EMPRESA) - 0.05, x1=float(medias_sim.max()) + 0.5,
                      fillcolor=VERMELHO, opacity=0.08, line_width=0)
    fig_sim.update_layout(
        **tema_layout(f"Distribuição de {N_SIMULACOES} Médias Amostrais Aleatórias (n={TAM_TOTAL})", 400)
    )
    estilizar_eixos(fig_sim, "FLB Médio Amostral (%)", "Densidade")
    st.plotly_chart(fig_sim, use_container_width=True)

    # Comparação amostras
    st.markdown('<div class="section-title">⚖️ Amostra Empresa vs Amostra Aleatória Real</div>',
                unsafe_allow_html=True)
    amostra_aleat = flb.sample(n=TAM_TOTAL, random_state=42)

    fig_comp = make_subplots(rows=1, cols=2,
                             subplot_titles=["Amostra Aleatória Real", "Amostra Tendenciosa (Empresa)"])
    fig_comp.add_trace(go.Histogram(
        x=amostra_aleat, nbinsx=30, marker_color=VERDE, opacity=0.7, name="Aleatória",
    ), row=1, col=1)
    fig_comp.add_trace(go.Histogram(
        x=flb[outliers_sup_mask].sample(min(TAM_TOTAL, outliers_sup_mask.sum()), random_state=1),
        nbinsx=30, marker_color=VERMELHO, opacity=0.7, name="Tendenciosa",
    ), row=1, col=2)
    fig_comp.update_layout(**tema_layout("", 380), showlegend=True)
    fig_comp.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR,
                          color=CINZA_TEXTO, title_text="FLB (%)")
    fig_comp.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR,
                          color=CINZA_TEXTO, title_text="Frequência")
    st.plotly_chart(fig_comp, use_container_width=True)

    comp_df = pd.DataFrame({
        "": ["FLB Médio", "FLB Mediano", "Desvio-Padrão", "Mínimo", "Máximo"],
        "Amostra Aleatória": [
            fmt_pct(amostra_aleat.mean()), fmt_pct(amostra_aleat.median()),
            fmt_pct(amostra_aleat.std()), fmt_pct(amostra_aleat.min()),
            fmt_pct(amostra_aleat.max()),
        ],
        "FLB Alegado (Empresa)": [fmt_pct(FLB_EMPRESA), "—", "—", "—", "—"],
        "Diferença": [f"{FLB_EMPRESA - amostra_aleat.mean():+.2f} p.p.", "—", "—", "—", "—"],
    })
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

    if p_valor_aprox < 0.05:
        st.markdown(f"""
        <div class="verdict">
            ⚖️ VEREDITO ESTATÍSTICO<br><br>
            A probabilidade de obter um FLB médio de {FLB_EMPRESA}% ou superior por pura
            aleatoriedade é de apenas <b>{p_valor_aprox*100:.2f}%</b>.<br>
            Evidência estatisticamente <b>muito forte</b> de manipulação amostral.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="success-box">
            A probabilidade de {p_valor_aprox*100:.2f}% não descarta seleção aleatória,
            mas outros indicadores devem ser avaliados em conjunto.
        </div>
        """, unsafe_allow_html=True)

    pct_empresa = (flb < FLB_EMPRESA).mean() * 100
    st.markdown(f"""
    <div class="alert-box">
        <b>📊 Análise Percentílica:</b><br>
        O FLB alegado de {FLB_EMPRESA}% encontra-se no percentil <b>{pct_empresa:.1f}°</b> da
        distribuição real. Ou seja, {pct_empresa:.1f}% de todos os atendimentos de 2023 possuem
        FLB abaixo do valor alegado.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ABA 4 — RISCO & CONFIABILIDADE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">⚡ Medidas de Dispersão e Risco Operacional</div>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(kpi_card("Amplitude", fmt_pct(est["Amplitude"]),
                             f"Min: {fmt_pct(est['Mín'])} · Max: {fmt_pct(est['Máx'])}",
                             "gold"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("Variância", f"{est['Variância']:.4f}",
                             "Variabilidade quadrática média", "red"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("Desvio-Padrão", fmt_pct(est["Desvio-Padrão"]),
                             "Dispersão média em torno da média", "red"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown(kpi_card("Coef. de Variação (CV)", fmt_pct(est["CV (%)"]),
                             "Dispersão relativa à média",
                             "red" if est["CV (%)"] > 30 else "gold"), unsafe_allow_html=True)
    with c5:
        st.markdown(kpi_card("IQR (Intervalo Interquartil)", fmt_pct(est["IQR"]),
                             f"Q1={est['Q1']:.2f}% · Q3={est['Q3']:.2f}%", "gold"),
                    unsafe_allow_html=True)
    with c6:
        n_out = (outliers_sup_mask | outliers_inf_mask).sum()
        st.markdown(kpi_card("Total de Outliers", str(n_out),
                             f"{n_out/est['N']*100:.1f}% da população", "red"),
                    unsafe_allow_html=True)

    # Gráfico por mês
    if "Mês" in df.columns:
        st.markdown('<div class="section-title">📅 Variabilidade do FLB por Período</div>',
                    unsafe_allow_html=True)
        try:
            mes_stats = df.groupby("Mês")["FLB"].agg(
                Media="mean", Desvio="std",
                Q1=lambda x: x.quantile(0.25),
                Mediana="median",
                Q3=lambda x: x.quantile(0.75)
            ).reset_index()
            fig_mes = go.Figure()
            fig_mes.add_trace(go.Bar(
                x=mes_stats["Mês"], y=mes_stats["Media"],
                marker_color=AZUL_CARD, marker_line_color=DOURADO, marker_line_width=1,
                name="FLB Médio",
                error_y=dict(type="data", array=mes_stats["Desvio"],
                             color=DOURADO_CLARO, thickness=1.5),
            ))
            fig_mes.add_hline(y=est["Média"], line_color=VERDE, line_dash="dash",
                              annotation_text=f"Média geral: {est['Média']:.2f}%",
                              annotation_font_color=VERDE)
            fig_mes.add_hline(y=FLB_EMPRESA, line_color=VERMELHO, line_dash="dot",
                              annotation_text=f"Alegado: {FLB_EMPRESA}%",
                              annotation_font_color=VERMELHO)
            fig_mes.update_layout(**tema_layout("FLB Médio por Mês (±1 Desvio-Padrão)", 380))
            estilizar_eixos(fig_mes, "Mês", "FLB (%)")
            st.plotly_chart(fig_mes, use_container_width=True)
        except Exception:
            st.info("Não foi possível gerar o gráfico por mês.")

    # Violin plot
    st.markdown('<div class="section-title">🎻 Distribuição de Densidade (Violin Plot)</div>',
                unsafe_allow_html=True)
    fig_vln = go.Figure()
    fig_vln.add_trace(go.Violin(
        y=flb, box_visible=True, line_color=DOURADO,
        fillcolor="rgba(200,169,81,0.15)", meanline_visible=True,
        name="FLB", points="outliers",
        marker=dict(color=VERMELHO, size=3, opacity=0.5),
    ))
    fig_vln.add_hline(y=FLB_EMPRESA, line_color=VERMELHO, line_dash="dash",
                      annotation_text=f"Empresa: {FLB_EMPRESA}%",
                      annotation_font_color=VERMELHO)
    fig_vln.update_layout(**tema_layout("Violin Plot do FLB — Densidade + Boxplot Integrado", 400))
    estilizar_eixos(fig_vln, "", "FLB (%)")
    st.plotly_chart(fig_vln, use_container_width=True)

    cv = est["CV (%)"]
    interp_cv = (
        "Baixa variabilidade — processo estável e previsível." if cv < 15 else
        "Variabilidade moderada — alguma instabilidade operacional." if cv < 30 else
        "Alta variabilidade — processo instável, risco operacional elevado."
    )
    st.markdown(f"""
    <div class="info-box">
        <b>📌 Interpretação do Risco:</b><br><br>
        <b>CV = {cv:.2f}%</b> → {interp_cv}<br><br>
        O desvio-padrão de <b>{fmt_pct(est['Desvio-Padrão'])}</b> indica que a rentabilidade dos
        atendimentos varia significativamente. Esse grau de heterogeneidade reforça que uma
        amostra tendenciosa pode distorcer substancialmente a média estimada.
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📋 Tabela Completa de Estatísticas Descritivas"):
        est_df = pd.DataFrame.from_dict(
            {k: [f"{v:.4f}" if isinstance(v, float) else str(v)] for k, v in est.items()},
            orient="index", columns=["Valor"],
        ).reset_index()
        est_df.columns = ["Estatística", "Valor"]
        st.dataframe(est_df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ABA 5 — GOVERNANÇA
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">🏛️ Propostas de Governança de Dados</div>',
                unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-box">
        <b>Contexto:</b> As evidências estatísticas revelaram fragilidades no processo de amostragem
        adotado pela empresa e na ausência de mecanismos de controle. As propostas abaixo estruturam
        um sistema robusto de governança para futuras auditorias e tomadas de decisão.
    </div>
    """, unsafe_allow_html=True)

    propostas = [
        {
            "icon": "🔒", "titulo": "1. Protocolo de Amostragem Auditável",
            "descricao": "Toda amostragem para fins de seguro deve utilizar <b>seleção aleatória sistematizada</b> com semente (seed) documentada e reproduzível. O código de amostragem deve ser arquivado e disponibilizado à seguradora.",
            "indicador": f"Meta: CV da amostra ≤ {est['CV (%)']:.1f}% (CV populacional)",
        },
        {
            "icon": "📊", "titulo": "2. Dashboard de Monitoramento de FLB em Tempo Real",
            "descricao": "Painel gerencial que monitore o FLB por mês e por faixa de faturamento. Alertas automáticos quando o FLB médio mensal superar <b>2 desvios-padrão</b> da média histórica.",
            "indicador": f"Limite de alerta: {est['Média'] + 2*est['Desvio-Padrão']:.2f}% (μ + 2σ)",
        },
        {
            "icon": "📋", "titulo": "3. Relatório Estatístico Obrigatório para Sinistros",
            "descricao": "Exigir relatório com média, mediana, desvio-padrão, coeficiente de variação, histograma e boxplot. A mediana deve ser o indicador primário em distribuições assimétricas.",
            "indicador": f"FLB de referência: Mediana = {est['Mediana']:.2f}% (mais robusto que a média)",
        },
        {
            "icon": "🔍", "titulo": "4. Auditoria Independente de Terceiros",
            "descricao": "Consultoria estatística independente para validar amostras em pedidos de seguro, confrontando com <b>1.000 simulações de Monte Carlo</b>. O FLB alegado deve estar no IC 95%.",
            "indicador": f"IC 95% esperado: [{medias_sim[25]:.2f}%, {medias_sim[974]:.2f}%]",
        },
        {
            "icon": "🗂️", "titulo": "5. Arquivamento Digital com Integridade Verificável",
            "descricao": "Registros armazenados com hash criptográfico (SHA-256) por atendimento, impossibilitando alteração retroativa. Backup redundante com retenção mínima de 5 anos.",
            "indicador": "Requisito: 100% dos registros com hash verificável",
        },
        {
            "icon": "📚", "titulo": "6. Treinamento em Letramento Estatístico",
            "descricao": "Capacitar gestão, controladoria e auditoria em estatística descritiva: distribuições assimétricas, identificação de outliers, diferença entre média e mediana.",
            "indicador": "Frequência: Semestral · Público: Auditoria, Controladoria, Direção",
        },
    ]

    for prop in propostas:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{AZUL_CARD},#0F2F50);
                    border:1px solid rgba(200,169,81,0.2); border-radius:14px;
                    padding:22px 26px; margin-bottom:16px;">
            <div style="font-family:'Playfair Display',serif; font-size:1.05rem;
                        color:{DOURADO_CLARO}; margin-bottom:10px;">
                {prop['icon']} {prop['titulo']}
            </div>
            <div style="color:{BRANCO}; font-size:0.9rem; line-height:1.75; margin-bottom:10px;">
                {prop['descricao']}
            </div>
            <div style="background-color:rgba(200,169,81,0.12); border-radius:8px;
                        padding:8px 14px; font-size:0.8rem; color:{DOURADO};">
                📌 <b>Indicador:</b> {prop['indicador']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Resumo executivo
    st.markdown('<div class="section-title">📝 Resumo Executivo para Tomada de Decisão</div>',
                unsafe_allow_html=True)
    flb_real = est["Média"]
    diff     = FLB_EMPRESA - flb_real
    impacto  = diff * IMPACTO_1PCT

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(17,45,78,0.9),rgba(11,31,58,0.9));
                border:2px solid rgba(200,169,81,0.4); border-radius:16px;
                padding:30px 36px; margin-top:10px;">
        <div style="font-family:'Playfair Display',serif; font-size:1.3rem;
                    color:{DOURADO_CLARO}; margin-bottom:18px; text-align:center;">
            ⚖️ Conclusão da Análise Pericial
        </div>
        <div style="color:{BRANCO}; font-size:0.93rem; line-height:1.9;">
            Com base na análise estatística da <b>população completa de {est['N']:,} atendimentos (2023)</b>:<br><br>
            <b>①</b> O FLB médio real é de <b>{flb_real:.4f}%</b>, significativamente inferior ao valor de
            <b>{FLB_EMPRESA}%</b> alegado pela empresa.<br><br>
            <b>②</b> A distribuição apresenta <b>assimetria de {est['Assimetria']:.4f}</b> e
            <b>{(outliers_sup_mask | outliers_inf_mask).sum()} outliers</b>, tornando a média
            sensível à seleção tendenciosa.<br><br>
            <b>③</b> Simulações de Monte Carlo ({N_SIMULACOES} amostras de n={TAM_TOTAL})
            indicam probabilidade de <b>{p_valor_aprox*100:.2f}%</b> de obter o FLB alegado por acaso —
            evidência <b>{'muito forte' if p_valor_aprox < 0.05 else 'insuficiente'}</b> de manipulação.<br><br>
            <b>④</b> O impacto financeiro estimado da superestimativa é de <b>{fmt_brl(abs(impacto))}</b>.<br><br>
            <b>Recomendação:</b> Utilizar o FLB mediano de <b>{est['Mediana']:.4f}%</b> como referência
            para o cálculo do sinistro, por ser mais robusto à presença de outliers.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center; margin-top:36px; padding-top:20px;
                border-top:1px solid rgba(200,169,81,0.2);
                font-size:0.75rem; color:{CINZA_TEXTO};">
        Sistema desenvolvido para fins acadêmicos · PBL 1 — Estatística Decisória · UNDB 2026/1<br>
        Análise baseada em estatística descritiva · Python + Streamlit + Plotly
    </div>
    """, unsafe_allow_html=True)