# -*- coding: utf-8 -*-
"""
Consumer Insights / Customer Analytics — Diagnóstico de Churn
================================================================
Aplicação Streamlit para diagnóstico de negócio sobre churn de clientes.

Storytelling: Carteira → Churn → Perfil → Comportamento → Segmentação →
Priorização → Ação

Schema oficial (não alterar nomes de colunas):
    id, full_name, credit_sco, gender, age, occupation, balance,
    monthly_ir, address, origin_province, tenure_ye, married,
    nums_card, nums_service, active_member, last_active_date,
    last_transaction_month, created_date, exit, customer_segment,
    engagement_score, loyalty_level, digital_behavior, risk_score,
    risk_segment, cluster_group
"""

import io
import warnings
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy import stats

warnings.filterwarnings("ignore")

# =============================================================================
# CONFIGURAÇÃO GERAL
# =============================================================================

st.set_page_config(
    page_title="Consumer Insights | Diagnóstico de Churn",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

REQUIRED_COLUMNS = [
    "id", "full_name", "credit_sco", "gender", "age", "occupation",
    "balance", "monthly_ir", "address", "origin_province", "tenure_ye",
    "married", "nums_card", "nums_service", "active_member",
    "last_active_date", "last_transaction_month", "created_date", "exit",
    "customer_segment", "engagement_score", "loyalty_level",
    "digital_behavior", "risk_score", "risk_segment", "cluster_group",
]

# Paleta enxuta e profissional (evita excesso de cores)
COLOR_CHURN = "#D64550"      # vermelho — churn
COLOR_RETIDO = "#2E5EAA"     # azul — retido
COLOR_NEUTRAL = "#7A8B99"    # cinza-azulado — neutro
COLOR_ACCENT = "#1B998B"     # verde-azulado — destaque positivo
COLOR_WARN = "#E8A33D"       # âmbar — atenção
SEQ_SCALE = ["#EAF2FB", "#B7D0EE", "#7FA9DD", "#4C7FC4", "#2E5EAA", "#1A3E7A"]
DIVERGING = [COLOR_RETIDO, "#C9D6E3", COLOR_CHURN]

px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = [COLOR_RETIDO, COLOR_CHURN, COLOR_ACCENT, COLOR_WARN, COLOR_NEUTRAL]

CUSTOM_CSS = """
<style>
    .block-container {padding-top: 1.6rem; padding-bottom: 2rem; max-width: 1400px;}
    h1, h2, h3 {font-family: 'Segoe UI', sans-serif; font-weight: 600;}
    h1 {font-size: 1.9rem; color: #16324F;}
    h2 {font-size: 1.35rem; color: #16324F; border-bottom: 2px solid #EEF2F6; padding-bottom: 6px; margin-top: 2.2rem;}
    h3 {font-size: 1.05rem; color: #2E5EAA;}
    .subtitle {color: #5B6B79; font-size: 0.95rem; margin-top: -10px; margin-bottom: 1.2rem;}
    div[data-testid="stMetric"] {
        background: #FFFFFF; border: 1px solid #E7ECF1; border-radius: 10px;
        padding: 14px 16px 10px 16px; box-shadow: 0 1px 3px rgba(20,40,70,0.05);
    }
    div[data-testid="stMetricLabel"] {font-size: 0.82rem; color: #5B6B79;}
    div[data-testid="stMetricValue"] {font-size: 1.5rem; color: #16324F;}
    .insight-box {
        background: #F4F8FC; border-left: 4px solid #2E5EAA; border-radius: 6px;
        padding: 10px 14px; margin-bottom: 8px; font-size: 0.93rem; color: #2A3B4D;
    }
    .insight-box.warn {border-left-color: #E8A33D; background: #FDF7EC;}
    .insight-box.alert {border-left-color: #D64550; background: #FCEEEF;}
    .insight-box.good {border-left-color: #1B998B; background: #EBF7F5;}
    .reco-card {
        background: #FFFFFF; border: 1px solid #E7ECF1; border-radius: 10px;
        padding: 14px 18px; margin-bottom: 12px;
    }
    .reco-priority-alta {border-left: 5px solid #D64550;}
    .reco-priority-media {border-left: 5px solid #E8A33D;}
    .reco-priority-baixa {border-left: 5px solid #7A8B99;}
    .section-note {color: #7A8B99; font-size: 0.85rem; font-style: italic;}
    footer {visibility: hidden;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =============================================================================
# 1. CARGA E TRATAMENTO DE DADOS
# =============================================================================

def generate_sample_data(n=6000, seed=42):
    """Gera uma base sintética fiel ao schema oficial, apenas para demonstração
    quando nenhum arquivo é carregado. Deve ser substituída pela base real."""
    rng = np.random.default_rng(seed)

    segments = ["Alto Valor", "Padrão", "Emergente", "Baixo Engajamento"]
    seg_weights = [0.15, 0.40, 0.25, 0.20]
    loyalty_levels = ["Bronze", "Prata", "Ouro", "Platina"]
    digital_behaviors = ["Digital Intenso", "Digital Moderado", "Baixa Adoção Digital", "Não Digital"]
    risk_segments = ["Baixo Risco", "Risco Moderado", "Alto Risco"]
    provinces = ["São Paulo", "Rio de Janeiro", "Minas Gerais", "Paraná", "Bahia",
                 "Rio Grande do Sul", "Pernambuco", "Ceará", "Santa Catarina", "Goiás"]
    occupations = ["Assalariado CLT", "Autônomo", "Empresário", "Servidor Público",
                   "Aposentado", "Estudante", "Profissional Liberal"]

    n = int(n)
    customer_segment = rng.choice(segments, size=n, p=seg_weights)
    age = np.clip(rng.normal(40, 13, n), 18, 85).astype(int)
    tenure_ye = np.clip(rng.exponential(4.5, n), 0, 25).astype(int)
    engagement_score = np.clip(rng.normal(55, 22, n), 0, 100).astype(int)
    nums_service = np.clip(rng.poisson(2.3, n), 0, 8)
    nums_card = np.clip(rng.poisson(1.4, n), 0, 5)
    active_member = rng.random(n) < 0.62
    credit_sco = np.clip(rng.normal(650, 90, n), 300, 900).astype(int)
    balance = np.clip(rng.gamma(2.2, 6500, n), 0, None).round(2)
    monthly_ir = np.clip(rng.gamma(3, 1800, n), 300, None).round(2)
    married = (rng.random(n) < 0.55).astype(int)
    gender = rng.choice(["Feminino", "Masculino"], size=n)
    risk_score = np.clip(rng.beta(2, 5, n) * 100, 0, 100).round(1)
    cluster_group = rng.integers(0, 5, n)

    # risk_segment coerente com risk_score
    risk_segment = pd.cut(risk_score, bins=[-1, 33, 66, 101],
                           labels=risk_segments).astype(str)

    # loyalty coerente com tenure/engagement
    loyalty_score = (tenure_ye * 2 + engagement_score / 2) + rng.normal(0, 8, n)
    loyalty_level = pd.qcut(loyalty_score, 4, labels=loyalty_levels).astype(str)

    digital_behavior = rng.choice(digital_behaviors, size=n, p=[0.28, 0.32, 0.25, 0.15])

    created_date = pd.to_datetime("2019-01-01") + pd.to_timedelta(
        rng.integers(0, 2400, n), unit="D")
    max_date = pd.Timestamp("2025-12-31")
    last_active_offset = rng.exponential(60, n).astype(int)
    last_active_date = pd.Series(max_date - pd.to_timedelta(np.clip(last_active_offset, 0, 900), unit="D"))
    created_date = pd.Series(created_date)
    last_active_date = last_active_date.where(last_active_date >= created_date, created_date)
    last_transaction_month = rng.integers(0, 13, n)

    # Probabilidade latente de churn (para gerar 'exit' de forma realista,
    # correlacionada com engajamento, atividade, utilização e tenure)
    days_inactive = (max_date - last_active_date).dt.days
    logit = (
        -1.1
        - 0.020 * engagement_score
        - 0.55 * active_member.astype(int)
        - 0.12 * nums_service
        - 0.05 * tenure_ye
        + 0.006 * days_inactive
        + 0.010 * risk_score
        + rng.normal(0, 0.6, n)
    )
    prob_churn = 1 / (1 + np.exp(-logit))
    exit_flag = rng.random(n) < prob_churn

    df = pd.DataFrame({
        "id": np.arange(1, n + 1),
        "full_name": [f"Cliente {i:05d}" for i in range(1, n + 1)],
        "credit_sco": credit_sco,
        "gender": gender,
        "age": age,
        "occupation": rng.choice(occupations, size=n),
        "balance": balance,
        "monthly_ir": monthly_ir,
        "address": [f"Endereço {i}" for i in range(1, n + 1)],
        "origin_province": rng.choice(provinces, size=n),
        "tenure_ye": tenure_ye,
        "married": married,
        "nums_card": nums_card,
        "nums_service": nums_service,
        "active_member": active_member,
        "last_active_date": last_active_date,
        "last_transaction_month": last_transaction_month,
        "created_date": created_date,
        "exit": exit_flag,
        "customer_segment": customer_segment,
        "engagement_score": engagement_score,
        "loyalty_level": loyalty_level,
        "digital_behavior": digital_behavior,
        "risk_score": risk_score,
        "risk_segment": risk_segment,
        "cluster_group": cluster_group,
    })
    return df


@st.cache_data(show_spinner=False)
def load_data(file_bytes=None, file_name=None):
    """Carrega a base a partir de upload (CSV/Parquet) ou gera dados de
    demonstração caso nenhum arquivo seja fornecido."""
    if file_bytes is not None:
        if file_name.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_bytes))
        elif file_name.endswith(".parquet"):
            df = pd.read_parquet(io.BytesIO(file_bytes))
        else:
            raise ValueError("Formato de arquivo não suportado. Use CSV ou Parquet.")
        source = "upload"
    else:
        df = generate_sample_data()
        source = "sample"
    return df, source


def validate_schema(df):
    """Valida presença das colunas oficiais. Retorna lista de colunas ausentes."""
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    return missing


@st.cache_data(show_spinner=False)
def clean_data(df):
    """Tratamento de dados: nulos, duplicidades, tipos, categorias, outliers,
    datas e validação das variáveis centrais. Retorna (df_limpo, log_de_tratamento)."""
    log = []
    df = df.copy()

    # Duplicidades por id
    if "id" in df.columns:
        dup = df.duplicated(subset=["id"]).sum()
        if dup > 0:
            df = df.drop_duplicates(subset=["id"], keep="first")
            log.append(f"Removidas {dup} linhas duplicadas com base em `id`.")

    # Tipos — booleans podem vir como string/0-1
    for bool_col in ["active_member", "exit"]:
        if bool_col in df.columns:
            if df[bool_col].dtype != bool:
                df[bool_col] = df[bool_col].map(
                    {True: True, False: False, "True": True, "False": False,
                     "true": True, "false": False, 1: True, 0: False,
                     "1": True, "0": False, "Yes": True, "No": False,
                     "yes": True, "no": False}
                ).fillna(df[bool_col])
                try:
                    df[bool_col] = df[bool_col].astype(bool)
                except Exception:
                    pass
            n_null = df[bool_col].isna().sum()
            if n_null > 0:
                log.append(f"`{bool_col}` possui {n_null} valores nulos/ inválidos após conversão.")

    # Datas
    for date_col in ["last_active_date", "created_date"]:
        if date_col in df.columns:
            before_na = df[date_col].isna().sum()
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)
            after_na = df[date_col].isna().sum()
            if after_na > before_na:
                log.append(f"`{date_col}`: {after_na - before_na} valores não puderam ser convertidos para data.")

    # Numéricos essenciais
    numeric_cols = ["credit_sco", "age", "balance", "monthly_ir", "tenure_ye",
                     "nums_card", "nums_service", "engagement_score", "risk_score",
                     "cluster_group", "last_transaction_month"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Nulos em colunas-chave para o diagnóstico
    key_cols = ["exit", "active_member", "customer_segment", "engagement_score"]
    key_cols = [c for c in key_cols if c in df.columns]
    n_before = len(df)
    n_null_key = df[key_cols].isna().any(axis=1).sum() if key_cols else 0
    if n_null_key > 0:
        log.append(
            f"{n_null_key} registros possuem valores nulos em variáveis-chave "
            f"({', '.join(key_cols)}) e foram excluídos do diagnóstico "
            f"({n_null_key/n_before:.1%} da base)."
        )
        df = df.dropna(subset=key_cols)

    # Categorias — strip / padronização leve
    cat_cols = ["customer_segment", "gender", "occupation", "origin_province",
                "loyalty_level", "digital_behavior", "risk_segment"]
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Outliers extremos (idade e tenure fora de faixa plausível) — apenas sinalizados
    if "age" in df.columns:
        n_out = ((df["age"] < 16) | (df["age"] > 100)).sum()
        if n_out > 0:
            log.append(f"{n_out} registros com `age` fora da faixa plausível (16–100) foram identificados (não removidos automaticamente).")

    df = df.reset_index(drop=True)
    return df, log


# =============================================================================
# 2. FUNÇÕES DE APOIO — FAIXAS, FILTROS, KPIs
# =============================================================================

def build_age_band(age):
    bins = [0, 29, 39, 49, 59, 200]
    labels = ["18–29", "30–39", "40–49", "50–59", "60+"]
    return pd.cut(age, bins=bins, labels=labels)


def build_tenure_band(tenure):
    bins = [-1, 1, 3, 6, 10, 200]
    labels = ["0–1 ano", "2–3 anos", "4–6 anos", "7–10 anos", "10+ anos"]
    return pd.cut(tenure, bins=bins, labels=labels)


def build_engagement_band(engagement):
    # Faixas baseadas em quartis da distribuição observada
    try:
        return pd.qcut(engagement, 4, labels=["Muito Baixo", "Baixo", "Médio", "Alto"], duplicates="drop")
    except ValueError:
        return pd.cut(engagement, bins=4, labels=["Muito Baixo", "Baixo", "Médio", "Alto"])


def prepare_derived_columns(df, ref_date=None):
    df = df.copy()
    df["age_band"] = build_age_band(df["age"])
    df["tenure_band"] = build_tenure_band(df["tenure_ye"])
    df["engagement_band"] = build_engagement_band(df["engagement_score"])
    df["status_label"] = df["active_member"].map({True: "Ativo", False: "Inativo"})
    df["churn_label"] = df["exit"].map({True: "Churn", False: "Retido"})
    if "last_active_date" in df.columns and df["last_active_date"].notna().any():
        ref = ref_date or df["last_active_date"].max()
        df["dias_desde_ultima_atividade"] = (ref - df["last_active_date"]).dt.days
    return df


def apply_filters(df, filters):
    """Aplica dinamicamente os filtros selecionados na sidebar."""
    out = df.copy()
    for col, value in filters.items():
        if value is None or value == "Todos":
            continue
        if col == "status_label":
            out = out[out["status_label"] == value]
        elif col == "churn_label":
            out = out[out["churn_label"] == value]
        else:
            out = out[out[col] == value]
    return out


def safe_div(a, b):
    return a / b if b not in (0, None) and not pd.isna(b) and b != 0 else 0.0


def calculate_kpis(df):
    total = len(df)
    churn_n = int(df["exit"].sum()) if total else 0
    churn_rate = safe_div(churn_n, total)
    active_n = int(df["active_member"].sum()) if total else 0
    avg_engagement = df["engagement_score"].mean() if total else 0.0
    avg_services = df["nums_service"].mean() if total else 0.0
    return {
        "total": total,
        "churn_n": churn_n,
        "churn_rate": churn_rate,
        "active_n": active_n,
        "avg_engagement": avg_engagement,
        "avg_services": avg_services,
    }


def calculate_churn(df, group_col):
    """Retorna tabela agregada de churn por grupo, com taxa de churn e
    participação no churn total."""
    if df.empty or group_col not in df.columns:
        return pd.DataFrame()
    total_churn = df["exit"].sum()
    g = df.groupby(group_col, observed=True).agg(
        clientes=("id", "count"),
        churn=("exit", "sum"),
    ).reset_index()
    g["taxa_churn"] = g.apply(lambda r: safe_div(r["churn"], r["clientes"]), axis=1)
    g["participacao_churn"] = g["churn"].apply(lambda c: safe_div(c, total_churn))
    g = g.sort_values("taxa_churn", ascending=False).reset_index(drop=True)
    return g


def generate_segment_analysis(df, group_col, extra_aggs=None):
    """Agregação genérica por grupo com métricas de negócio padrão."""
    if df.empty or group_col not in df.columns:
        return pd.DataFrame()
    aggs = dict(
        clientes=("id", "count"),
        churn=("exit", "sum"),
        engagement_medio=("engagement_score", "mean"),
        servicos_medio=("nums_service", "mean"),
        tenure_medio=("tenure_ye", "mean"),
    )
    g = df.groupby(group_col, observed=True).agg(**aggs).reset_index()
    g["taxa_churn"] = g.apply(lambda r: safe_div(r["churn"], r["clientes"]), axis=1)
    return g.sort_values("taxa_churn", ascending=False).reset_index(drop=True)


def fmt_pct(x):
    return f"{x:.1%}"


def fmt_num(x):
    return f"{x:,.0f}".replace(",", ".")


# =============================================================================
# 3. INSIGHTS AUTOMÁTICOS
# =============================================================================

def generate_insights(df, kpis):
    """Gera insights textuais dinâmicos com base no recorte filtrado atual."""
    insights = []
    if df.empty:
        return ["Nenhum dado disponível para o recorte selecionado."]

    overall_rate = kpis["churn_rate"]

    # Segmento com maior churn acima da média
    seg = calculate_churn(df, "customer_segment")
    if not seg.empty:
        top = seg.iloc[0]
        if top["taxa_churn"] > overall_rate and top["clientes"] >= 10:
            insights.append((
                "alert",
                f"O segmento **{top[seg.columns[0]]}** apresenta churn de "
                f"{fmt_pct(top['taxa_churn'])}, acima da média da carteira "
                f"({fmt_pct(overall_rate)}), concentrando {fmt_pct(top['participacao_churn'])} "
                f"do total de cancelamentos."
            ))

    # Ativo vs Inativo
    if "status_label" in df.columns:
        st_tab = calculate_churn(df, "status_label")
        if set(["Ativo", "Inativo"]).issubset(set(st_tab[st_tab.columns[0]])):
            ativo = st_tab[st_tab[st_tab.columns[0]] == "Ativo"]["taxa_churn"].values
            inativo = st_tab[st_tab[st_tab.columns[0]] == "Inativo"]["taxa_churn"].values
            if len(ativo) and len(inativo) and inativo[0] > ativo[0]:
                ratio = safe_div(inativo[0], ativo[0]) if ativo[0] > 0 else None
                txt = (f"Clientes **inativos** apresentam churn de {fmt_pct(inativo[0])}, "
                       f"contra {fmt_pct(ativo[0])} entre os ativos")
                if ratio:
                    txt += f" — uma exposição {ratio:.1f}x maior."
                else:
                    txt += "."
                insights.append(("alert", txt))

    # Engajamento
    if "engagement_band" in df.columns:
        eng_tab = calculate_churn(df, "engagement_band")
        eng_tab = eng_tab.dropna(subset=[eng_tab.columns[0]])
        if len(eng_tab) >= 2:
            ordered = eng_tab.set_index(eng_tab.columns[0]).reindex(
                ["Muito Baixo", "Baixo", "Médio", "Alto"]).dropna()
            if len(ordered) >= 2 and ordered["taxa_churn"].iloc[0] > ordered["taxa_churn"].iloc[-1]:
                insights.append((
                    "alert",
                    f"Clientes com engajamento **Muito Baixo** apresentam taxa de churn de "
                    f"{fmt_pct(ordered['taxa_churn'].iloc[0])}, contra {fmt_pct(ordered['taxa_churn'].iloc[-1])} "
                    f"entre os de engajamento **Alto** — o churn diminui à medida que o engajamento aumenta."
                ))

    # Utilização de serviços
    if "nums_service" in df.columns:
        corr_df = df[["nums_service"]].copy()
        corr_df["exit_num"] = df["exit"].astype(int)
        low_service = df[df["nums_service"] <= df["nums_service"].median()]
        high_service = df[df["nums_service"] > df["nums_service"].median()]
        if len(low_service) > 5 and len(high_service) > 5:
            r_low = low_service["exit"].mean()
            r_high = high_service["exit"].mean()
            if r_low > r_high:
                insights.append((
                    "warn",
                    f"Clientes com **menor número de serviços contratados** apresentam churn de "
                    f"{fmt_pct(r_low)}, superior aos {fmt_pct(r_high)} observados entre clientes com "
                    f"maior utilização."
                ))

    # Loyalty
    if "loyalty_level" in df.columns:
        loy = calculate_churn(df, "loyalty_level")
        if not loy.empty:
            worst = loy.iloc[0]
            best = loy.iloc[-1]
            if worst["taxa_churn"] > best["taxa_churn"] and worst["clientes"] >= 10:
                insights.append((
                    "warn",
                    f"O nível de lealdade **{worst[loy.columns[0]]}** concentra a maior taxa de churn "
                    f"({fmt_pct(worst['taxa_churn'])}), enquanto **{best[loy.columns[0]]}** apresenta a menor "
                    f"({fmt_pct(best['taxa_churn'])})."
                ))

    # Risco — checagem empírica (não assumir)
    if "risk_segment" in df.columns:
        risk_tab = calculate_churn(df, "risk_segment")
        if not risk_tab.empty:
            top_risk = risk_tab.iloc[0]
            label_col = risk_tab.columns[0]
            if "alto" in str(top_risk[label_col]).lower() or "high" in str(top_risk[label_col]).lower():
                insights.append((
                    "good" if top_risk["taxa_churn"] > overall_rate else "warn",
                    f"O segmento de risco **{top_risk[label_col]}** apresenta a maior taxa de churn "
                    f"({fmt_pct(top_risk['taxa_churn'])}), confirmando associação entre risco atribuído e saída."
                ))
            else:
                insights.append((
                    "warn",
                    f"O segmento com maior churn não é necessariamente o de maior risco declarado "
                    f"(**{top_risk[label_col]}**, {fmt_pct(top_risk['taxa_churn'])}) — a variável `risk_score` "
                    f"deve ser interpretada com cautela como preditor isolado de churn."
                ))

    # Tenure
    if "tenure_band" in df.columns:
        ten_tab = calculate_churn(df, "tenure_band")
        ten_tab = ten_tab.dropna(subset=[ten_tab.columns[0]])
        if not ten_tab.empty:
            top_ten = ten_tab.iloc[0]
            insights.append((
                "warn",
                f"A faixa de tenure **{top_ten[ten_tab.columns[0]]}** concentra a maior taxa de churn "
                f"({fmt_pct(top_ten['taxa_churn'])}), indicando um momento crítico no ciclo de relacionamento."
            ))

    if not insights:
        insights.append(("good", "Não foram identificados desvios relevantes de churn entre os grupos no recorte atual."))

    return insights


# =============================================================================
# 4. SIDEBAR — UPLOAD E FILTROS
# =============================================================================

with st.sidebar:
    st.markdown("### 📁 Base de dados")
    uploaded_file = st.file_uploader(
        "Carregar base (CSV ou Parquet)", type=["csv", "parquet"],
        help="A base deve seguir exatamente o schema oficial documentado no README.")
    st.caption("Se nenhum arquivo for carregado, uma base sintética de demonstração é utilizada.")
    st.markdown("---")

file_bytes = uploaded_file.read() if uploaded_file else None
file_name = uploaded_file.name if uploaded_file else None

try:
    raw_df, data_source = load_data(file_bytes, file_name)
except Exception as e:
    st.error(f"Erro ao carregar o arquivo: {e}")
    st.stop()

missing_cols = validate_schema(raw_df)
if missing_cols:
    st.error(
        "A base carregada não segue o schema oficial. Colunas ausentes: "
        + ", ".join(f"`{c}`" for c in missing_cols)
    )
    st.stop()

df_clean, treatment_log = clean_data(raw_df)

if df_clean.empty:
    st.error("Após o tratamento de dados, não restaram registros válidos para análise.")
    st.stop()

df_full = prepare_derived_columns(df_clean)

with st.sidebar:
    if data_source == "sample":
        st.warning("⚠️ Utilizando base sintética de demonstração — carregue sua base real acima.")

    st.markdown("### 🔍 Filtros da análise")

    def sb_selectbox(label, col, df_source):
        options = ["Todos"] + sorted(df_source[col].dropna().unique().tolist(), key=str)
        return st.selectbox(label, options, key=f"filter_{col}")

    f_segment = sb_selectbox("Segmento do cliente", "customer_segment", df_full)
    f_status = st.selectbox("Status do cliente", ["Todos", "Ativo", "Inativo"], key="filter_status")
    f_churn = st.selectbox("Churn", ["Todos", "Churn", "Retido"], key="filter_churn")
    f_loyalty = sb_selectbox("Nível de fidelidade", "loyalty_level", df_full)
    f_digital = sb_selectbox("Comportamento digital", "digital_behavior", df_full)
    f_risk = sb_selectbox("Segmento de risco", "risk_segment", df_full)
    f_gender = sb_selectbox("Gênero", "gender", df_full)
    f_occupation = sb_selectbox("Ocupação", "occupation", df_full)
    f_province = sb_selectbox("Estado de origem", "origin_province", df_full)

    age_band_options = ["Todos"] + [b for b in ["18–29", "30–39", "40–49", "50–59", "60+"]
                                     if b in df_full["age_band"].astype(str).unique()]
    f_age_band = st.selectbox("Faixa etária", age_band_options, key="filter_age")

    tenure_band_options = ["Todos"] + [b for b in ["0–1 ano", "2–3 anos", "4–6 anos", "7–10 anos", "10+ anos"]
                                        if b in df_full["tenure_band"].astype(str).unique()]
    f_tenure_band = st.selectbox("Faixa de tenure", tenure_band_options, key="filter_tenure")

    st.markdown("---")
    with st.expander("🧹 Log de tratamento de dados"):
        if treatment_log:
            for msg in treatment_log:
                st.caption(f"• {msg}")
        else:
            st.caption("Nenhum tratamento adicional foi necessário.")

filters = {
    "customer_segment": f_segment,
    "status_label": f_status,
    "churn_label": f_churn,
    "loyalty_level": f_loyalty,
    "digital_behavior": f_digital,
    "risk_segment": f_risk,
    "gender": f_gender,
    "occupation": f_occupation,
    "origin_province": f_province,
    "age_band": f_age_band,
    "tenure_band": f_tenure_band,
}

df = apply_filters(df_full, filters)

# =============================================================================
# 5. HEADER
# =============================================================================

st.markdown("# 📊 Consumer Insights — Diagnóstico de Churn")
st.markdown(
    '<p class="subtitle">Carteira → Churn → Perfil → Comportamento → Segmentação → '
    'Priorização → Ação</p>', unsafe_allow_html=True
)

if df.empty:
    st.warning("Nenhum registro encontrado para a combinação de filtros selecionada. Ajuste os filtros na barra lateral.")
    st.stop()

kpis = calculate_kpis(df)

# =============================================================================
# 6. KPIs PRINCIPAIS
# =============================================================================

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Clientes", fmt_num(kpis["total"]))
k2.metric("Churn", fmt_num(kpis["churn_n"]))
k3.metric("Taxa de Churn", fmt_pct(kpis["churn_rate"]))
k4.metric("Clientes Ativos", fmt_num(kpis["active_n"]))
k5.metric("Engajamento Médio", f"{kpis['avg_engagement']:.1f}")
k6.metric("Utilização de Serviços", f"{kpis['avg_services']:.2f}")

# =============================================================================
# 7. DIAGNÓSTICO EXECUTIVO
# =============================================================================

st.markdown("## Diagnóstico da Carteira")

c1, c2, c3 = st.columns([1, 1.3, 1.1])

with c1:
    st.markdown("##### Retidos vs Churn")
    churn_counts = df["churn_label"].value_counts().reindex(["Retido", "Churn"]).fillna(0)
    fig = go.Figure(go.Pie(
        labels=churn_counts.index, values=churn_counts.values, hole=0.55,
        marker=dict(colors=[COLOR_RETIDO, COLOR_CHURN]),
        textinfo="label+percent", sort=False,
    ))
    fig.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=300)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("##### Churn por Customer Segment")
    seg_churn = calculate_churn(df, "customer_segment")
    fig = px.bar(seg_churn, x="taxa_churn", y="customer_segment", orientation="h",
                 text=seg_churn["taxa_churn"].apply(fmt_pct), color_discrete_sequence=[COLOR_RETIDO])
    fig.update_traces(textposition="outside", marker_color=COLOR_RETIDO)
    fig.update_layout(xaxis_tickformat=".0%", yaxis_title="", xaxis_title="Taxa de churn",
                       margin=dict(t=10, b=10, l=10, r=10), height=300,
                       yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(fig, use_container_width=True)

with c3:
    st.markdown("##### Churn por Status (Active Member)")
    status_churn = calculate_churn(df, "status_label")
    fig = px.bar(status_churn, x="status_label", y="taxa_churn",
                 text=status_churn["taxa_churn"].apply(fmt_pct),
                 color="status_label", color_discrete_map={"Ativo": COLOR_ACCENT, "Inativo": COLOR_CHURN})
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, yaxis_tickformat=".0%", xaxis_title="", yaxis_title="Taxa de churn",
                       margin=dict(t=10, b=10, l=10, r=10), height=300)
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# 8. CONCENTRAÇÃO DO CHURN
# =============================================================================

st.markdown("## Concentração do Churn por Segmento")
st.markdown(
    '<p class="section-note">Taxa de churn = churn do segmento / total do segmento · '
    'Participação no churn = churn do segmento / churn total da carteira.</p>',
    unsafe_allow_html=True
)

conc = calculate_churn(df, "customer_segment").rename(columns={"customer_segment": "Segmento"})
conc_display = conc.copy()
conc_display["taxa_churn"] = conc_display["taxa_churn"].apply(fmt_pct)
conc_display["participacao_churn"] = conc_display["participacao_churn"].apply(fmt_pct)
conc_display.columns = ["Segmento", "Clientes", "Churn", "Taxa de Churn", "Participação no Churn Total"]
st.dataframe(conc_display, use_container_width=True, hide_index=True)

# =============================================================================
# 9. PERFIL DOS CLIENTES QUE SAEM
# =============================================================================

st.markdown("## Perfil: Churn vs Retidos")

profile_vars = {
    "age": "Idade", "credit_sco": "Score de Crédito", "balance": "Saldo",
    "monthly_ir": "Renda Mensal", "tenure_ye": "Tenure (anos)",
    "nums_card": "Nº de Cartões", "nums_service": "Nº de Serviços",
    "engagement_score": "Engajamento", "risk_score": "Risk Score",
}
rows = []
for col, label in profile_vars.items():
    if col in df.columns:
        churn_vals = df.loc[df["exit"], col]
        ret_vals = df.loc[~df["exit"], col]
        rows.append({
            "Variável": label,
            "Média — Churn": round(churn_vals.mean(), 2),
            "Média — Retidos": round(ret_vals.mean(), 2),
            "Mediana — Churn": round(churn_vals.median(), 2),
            "Mediana — Retidos": round(ret_vals.median(), 2),
        })
profile_df = pd.DataFrame(rows)
st.dataframe(profile_df, use_container_width=True, hide_index=True)

# Insight textual não-causal, dinâmico
profile_insights = []
for r in rows:
    diff = r["Média — Churn"] - r["Média — Retidos"]
    direction = "inferior" if diff < 0 else "superior"
    if abs(diff) > 0:
        profile_insights.append(
            f"Clientes que cancelaram apresentam **{r['Variável']}** médio {direction} "
            f"aos clientes retidos ({r['Média — Churn']:.1f} vs {r['Média — Retidos']:.1f})."
        )
if profile_insights:
    with st.expander("Ver leitura descritiva por variável"):
        for txt in profile_insights:
            st.markdown(f'<div class="insight-box">{txt}</div>', unsafe_allow_html=True)
st.caption("As comparações acima são descritivas e não implicam relação causal.")

# =============================================================================
# 10. ANÁLISE DE ENGAJAMENTO
# =============================================================================

st.markdown("## Engajamento × Churn")

eng_tab = generate_segment_analysis(df, "engagement_band")
eng_order = ["Muito Baixo", "Baixo", "Médio", "Alto"]
eng_tab["engagement_band"] = pd.Categorical(eng_tab["engagement_band"], categories=eng_order, ordered=True)
eng_tab = eng_tab.sort_values("engagement_band")

c1, c2 = st.columns([1.4, 1])
with c1:
    fig = px.bar(eng_tab, x="engagement_band", y="taxa_churn",
                 text=eng_tab["taxa_churn"].apply(fmt_pct), color_discrete_sequence=[COLOR_RETIDO])
    fig.update_traces(marker_color=COLOR_RETIDO, textposition="outside")
    fig.update_layout(yaxis_tickformat=".0%", xaxis_title="Faixa de engajamento", yaxis_title="Taxa de churn",
                       margin=dict(t=10, b=10, l=10, r=10), height=340)
    st.plotly_chart(fig, use_container_width=True)
with c2:
    disp = eng_tab.copy()
    disp["taxa_churn"] = disp["taxa_churn"].apply(fmt_pct)
    disp = disp.rename(columns={
        "engagement_band": "Faixa", "clientes": "Clientes", "churn": "Churn",
        "taxa_churn": "Taxa de Churn", "engagement_medio": "Engaj. Médio",
        "servicos_medio": "Serviços Médio", "tenure_medio": "Tenure Médio"
    })[["Faixa", "Clientes", "Churn", "Taxa de Churn", "Engaj. Médio"]]
    st.dataframe(disp, use_container_width=True, hide_index=True)

# =============================================================================
# 11. ANÁLISE DE UTILIZAÇÃO
# =============================================================================

st.markdown("## Utilização de Serviços × Churn")

serv_tab = calculate_churn(df, "nums_service").rename(columns={"nums_service": "Nº de Serviços"})
c1, c2 = st.columns([1.4, 1])
with c1:
    fig = px.line(serv_tab.sort_values("Nº de Serviços"), x="Nº de Serviços", y="taxa_churn",
                   markers=True)
    fig.update_traces(line_color=COLOR_RETIDO, marker=dict(size=8, color=COLOR_CHURN))
    fig.update_layout(yaxis_tickformat=".0%", yaxis_title="Taxa de churn",
                       margin=dict(t=10, b=10, l=10, r=10), height=320)
    st.plotly_chart(fig, use_container_width=True)
with c2:
    if "nums_card" in df.columns:
        card_tab = calculate_churn(df, "nums_card").rename(columns={"nums_card": "Nº de Cartões"})
        fig = px.bar(card_tab.sort_values("Nº de Cartões"), x="Nº de Cartões", y="taxa_churn",
                     text=card_tab.sort_values("Nº de Cartões")["taxa_churn"].apply(fmt_pct))
        fig.update_traces(marker_color=COLOR_NEUTRAL, textposition="outside")
        fig.update_layout(yaxis_tickformat=".0%", yaxis_title="Taxa de churn",
                           margin=dict(t=10, b=10, l=10, r=10), height=320)
        st.plotly_chart(fig, use_container_width=True)

low_srv = df[df["nums_service"] <= df["nums_service"].median()]["exit"].mean()
high_srv = df[df["nums_service"] > df["nums_service"].median()]["exit"].mean()
direction_txt = "maior" if low_srv > high_srv else "menor"
st.markdown(
    f'<div class="insight-box">Clientes com utilização de serviços abaixo da mediana apresentam '
    f'{direction_txt} taxa de churn ({fmt_pct(low_srv)}) em comparação aos de utilização acima da '
    f'mediana ({fmt_pct(high_srv)}).</div>', unsafe_allow_html=True
)

# =============================================================================
# 12. ANÁLISE DIGITAL
# =============================================================================

st.markdown("## Comportamento Digital × Churn")

dig_tab = generate_segment_analysis(df, "digital_behavior")
c1, c2 = st.columns([1.3, 1])
with c1:
    fig = px.bar(dig_tab, x="digital_behavior", y="taxa_churn",
                 text=dig_tab["taxa_churn"].apply(fmt_pct), color_discrete_sequence=[COLOR_RETIDO])
    fig.update_traces(marker_color=COLOR_RETIDO, textposition="outside")
    fig.update_layout(yaxis_tickformat=".0%", xaxis_title="", yaxis_title="Taxa de churn",
                       margin=dict(t=10, b=10, l=10, r=10), height=340,
                       xaxis=dict(categoryorder="total descending"))
    st.plotly_chart(fig, use_container_width=True)
with c2:
    disp = dig_tab.copy()
    disp["taxa_churn"] = disp["taxa_churn"].apply(fmt_pct)
    disp = disp.rename(columns={
        "digital_behavior": "Comportamento", "clientes": "Clientes", "churn": "Churn",
        "taxa_churn": "Taxa de Churn", "engagement_medio": "Engaj. Médio", "servicos_medio": "Serviços Médio"
    })[["Comportamento", "Clientes", "Churn", "Taxa de Churn", "Engaj. Médio", "Serviços Médio"]]
    st.dataframe(disp, use_container_width=True, hide_index=True)

# =============================================================================
# 13. ANÁLISE DE LOYALTY
# =============================================================================

st.markdown("## Loyalty Level × Churn")

loy_tab = generate_segment_analysis(df, "loyalty_level")
c1, c2 = st.columns([1.3, 1])
with c1:
    fig = px.bar(loy_tab, x="loyalty_level", y="taxa_churn",
                 text=loy_tab["taxa_churn"].apply(fmt_pct), color_discrete_sequence=[COLOR_RETIDO])
    fig.update_traces(marker_color=COLOR_RETIDO, textposition="outside")
    fig.update_layout(yaxis_tickformat=".0%", xaxis_title="", yaxis_title="Taxa de churn",
                       margin=dict(t=10, b=10, l=10, r=10), height=340,
                       xaxis=dict(categoryorder="total descending"))
    st.plotly_chart(fig, use_container_width=True)
with c2:
    disp = loy_tab.copy()
    disp["taxa_churn"] = disp["taxa_churn"].apply(fmt_pct)
    disp = disp.rename(columns={
        "loyalty_level": "Loyalty", "clientes": "Clientes", "churn": "Churn",
        "taxa_churn": "Taxa de Churn", "engagement_medio": "Engaj. Médio", "tenure_medio": "Tenure Médio"
    })[["Loyalty", "Clientes", "Churn", "Taxa de Churn", "Engaj. Médio", "Tenure Médio"]]
    st.dataframe(disp, use_container_width=True, hide_index=True)

# =============================================================================
# 14. ANÁLISE DE RISCO
# =============================================================================

st.markdown("## Risco × Churn")
st.markdown('<p class="section-note">A relação entre risco atribuído e churn é verificada empiricamente, não assumida.</p>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown("##### Risk Segment × Taxa de Churn")
    risk_tab = calculate_churn(df, "risk_segment")
    fig = px.bar(risk_tab, x="risk_segment", y="taxa_churn",
                 text=risk_tab["taxa_churn"].apply(fmt_pct), color_discrete_sequence=[COLOR_WARN])
    fig.update_traces(marker_color=COLOR_WARN, textposition="outside")
    fig.update_layout(yaxis_tickformat=".0%", xaxis_title="", yaxis_title="Taxa de churn",
                       margin=dict(t=10, b=10, l=10, r=10), height=320)
    st.plotly_chart(fig, use_container_width=True)
with c2:
    st.markdown("##### Distribuição do Risk Score")
    fig = px.histogram(df, x="risk_score", color="churn_label", barmode="overlay", nbins=30,
                        color_discrete_map={"Churn": COLOR_CHURN, "Retido": COLOR_RETIDO}, opacity=0.65)
    fig.update_layout(xaxis_title="Risk score", yaxis_title="Clientes", legend_title="",
                       margin=dict(t=10, b=10, l=10, r=10), height=320)
    st.plotly_chart(fig, use_container_width=True)

risk_disp = risk_tab.rename(columns={"risk_segment": "Risk Segment"}).copy()
risk_disp["risk_score_medio"] = df.groupby("risk_segment", observed=True)["risk_score"].mean().reindex(risk_disp["Risk Segment"]).values
risk_disp_fmt = risk_disp.copy()
risk_disp_fmt["taxa_churn"] = risk_disp_fmt["taxa_churn"].apply(fmt_pct)
risk_disp_fmt["participacao_churn"] = risk_disp_fmt["participacao_churn"].apply(fmt_pct)
risk_disp_fmt["risk_score_medio"] = risk_disp_fmt["risk_score_medio"].round(1)
risk_disp_fmt = risk_disp_fmt.rename(columns={
    "Risk Segment": "Risk Segment", "clientes": "Clientes", "churn": "Churn",
    "taxa_churn": "Taxa de Churn", "participacao_churn": "Participação no Churn",
    "risk_score_medio": "Risk Score Médio"
})
st.dataframe(risk_disp_fmt, use_container_width=True, hide_index=True)

# =============================================================================
# 15. ANÁLISE DE ATIVIDADE
# =============================================================================

st.markdown("## Atividade × Churn")

act_tab = generate_segment_analysis(df, "status_label")
c1, c2 = st.columns(2)
with c1:
    disp = act_tab.copy()
    disp["taxa_churn"] = disp["taxa_churn"].apply(fmt_pct)
    disp = disp.rename(columns={
        "status_label": "Status", "clientes": "Clientes", "churn": "Churn",
        "taxa_churn": "Taxa de Churn", "engagement_medio": "Engaj. Médio", "servicos_medio": "Utilização Média"
    })[["Status", "Clientes", "Churn", "Taxa de Churn", "Engaj. Médio", "Utilização Média"]]
    st.dataframe(disp, use_container_width=True, hide_index=True)

with c2:
    if "dias_desde_ultima_atividade" in df.columns:
        st.markdown("##### Dias desde a última atividade × Churn")
        d = df.dropna(subset=["dias_desde_ultima_atividade"]).copy()
        try:
            d["faixa_inatividade"] = pd.qcut(d["dias_desde_ultima_atividade"], 5, duplicates="drop")
        except ValueError:
            d["faixa_inatividade"] = pd.cut(d["dias_desde_ultima_atividade"], 5)
        inact_tab = calculate_churn(d, "faixa_inatividade")
        inact_tab["faixa_inatividade"] = inact_tab["faixa_inatividade"].astype(str)
        fig = px.bar(inact_tab, x="faixa_inatividade", y="taxa_churn",
                     text=inact_tab["taxa_churn"].apply(fmt_pct), color_discrete_sequence=[COLOR_CHURN])
        fig.update_traces(marker_color=COLOR_CHURN, textposition="outside")
        fig.update_layout(yaxis_tickformat=".0%", xaxis_title="Dias desde a última atividade", yaxis_title="Taxa de churn",
                           margin=dict(t=10, b=10, l=10, r=10), height=320)
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# 16. ANÁLISE DE TENURE
# =============================================================================

st.markdown("## Tenure × Churn")

ten_tab = generate_segment_analysis(df, "tenure_band")
ten_order = ["0–1 ano", "2–3 anos", "4–6 anos", "7–10 anos", "10+ anos"]
ten_tab["tenure_band"] = pd.Categorical(ten_tab["tenure_band"], categories=ten_order, ordered=True)
ten_tab = ten_tab.sort_values("tenure_band")

fig = px.bar(ten_tab, x="tenure_band", y="taxa_churn",
             text=ten_tab["taxa_churn"].apply(fmt_pct), color_discrete_sequence=[COLOR_RETIDO])
fig.update_traces(marker_color=COLOR_RETIDO, textposition="outside")
fig.update_layout(yaxis_tickformat=".0%", xaxis_title="Tempo de relacionamento", yaxis_title="Taxa de churn",
                   margin=dict(t=10, b=10, l=10, r=10), height=320)
st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# 17. SEGMENTAÇÃO CRUZADA
# =============================================================================

st.markdown("## Diagnóstico Cruzado")
st.markdown('<p class="section-note">Cruzamento priorizado por relevância: Customer Segment × Status × Loyalty.</p>', unsafe_allow_html=True)

cross_cols = ["customer_segment", "status_label", "loyalty_level"]
cross_tab = df.groupby(cross_cols, observed=True).agg(
    clientes=("id", "count"),
    churn=("exit", "sum"),
    engagement_medio=("engagement_score", "mean"),
    servicos_medio=("nums_service", "mean"),
    tenure_medio=("tenure_ye", "mean"),
).reset_index()
cross_tab = cross_tab[cross_tab["clientes"] >= 5]  # remove combinações com baixa representatividade
cross_tab["taxa_churn"] = cross_tab.apply(lambda r: safe_div(r["churn"], r["clientes"]), axis=1)
cross_tab = cross_tab.sort_values("taxa_churn", ascending=False).head(20)

cross_disp = cross_tab.copy()
cross_disp["taxa_churn"] = cross_disp["taxa_churn"].apply(fmt_pct)
cross_disp["engagement_medio"] = cross_disp["engagement_medio"].round(1)
cross_disp["servicos_medio"] = cross_disp["servicos_medio"].round(2)
cross_disp["tenure_medio"] = cross_disp["tenure_medio"].round(1)
cross_disp = cross_disp.rename(columns={
    "customer_segment": "Customer Segment", "status_label": "Status", "loyalty_level": "Loyalty",
    "clientes": "Clientes", "churn": "Churn", "taxa_churn": "Taxa de Churn",
    "engagement_medio": "Engaj. Médio", "servicos_medio": "Serviços Médio", "tenure_medio": "Tenure Médio"
})
st.caption("Top 20 combinações por taxa de churn (mínimo de 5 clientes por combinação).")
st.dataframe(cross_disp, use_container_width=True, hide_index=True)

# =============================================================================
# 18. GRUPOS PRIORITÁRIOS PARA RETENÇÃO
# =============================================================================

st.markdown("## Grupos Prioritários para Retenção")
st.markdown(
    '<p class="section-note">Fórmula do score de prioridade — combina volume de clientes, taxa de churn '
    'e vulnerabilidade comportamental (baixo engajamento e baixa utilização), todos normalizados entre 0 e 1: <br>'
    '<code>score = 0.4 × taxa_churn_norm + 0.3 × volume_norm + 0.15 × (1 − engajamento_norm) + '
    '0.15 × (1 − utilização_norm)</code></p>',
    unsafe_allow_html=True
)

prio = generate_segment_analysis(df, "customer_segment")
if not prio.empty and len(prio) > 1:
    def norm(s):
        rng_ = s.max() - s.min()
        return (s - s.min()) / rng_ if rng_ > 0 else pd.Series(0.5, index=s.index)

    prio["taxa_churn_norm"] = norm(prio["taxa_churn"])
    prio["volume_norm"] = norm(prio["clientes"])
    prio["engagement_norm"] = norm(prio["engagement_medio"])
    prio["servicos_norm"] = norm(prio["servicos_medio"])
    prio["prioridade_score"] = (
        0.40 * prio["taxa_churn_norm"] + 0.30 * prio["volume_norm"]
        + 0.15 * (1 - prio["engagement_norm"]) + 0.15 * (1 - prio["servicos_norm"])
    )
    prio = prio.sort_values("prioridade_score", ascending=False)
    prio["Prioridade"] = pd.cut(prio["prioridade_score"], bins=[-0.01, 0.33, 0.66, 1.01],
                                 labels=["Baixa", "Média", "Alta"])

    prio_disp = prio.copy()
    prio_disp["taxa_churn"] = prio_disp["taxa_churn"].apply(fmt_pct)
    prio_disp["engagement_medio"] = prio_disp["engagement_medio"].round(1)
    prio_disp["servicos_medio"] = prio_disp["servicos_medio"].round(2)
    prio_disp["tenure_medio"] = prio_disp["tenure_medio"].round(1)
    prio_disp["prioridade_score"] = prio_disp["prioridade_score"].round(3)
    prio_disp = prio_disp.rename(columns={
        "customer_segment": "Grupo", "clientes": "Clientes", "churn": "Churn",
        "taxa_churn": "Taxa de Churn", "engagement_medio": "Engajamento",
        "servicos_medio": "Utilização", "tenure_medio": "Tenure", "prioridade_score": "Score"
    })[["Grupo", "Clientes", "Churn", "Taxa de Churn", "Engajamento", "Utilização", "Tenure", "Score", "Prioridade"]]
    st.dataframe(prio_disp, use_container_width=True, hide_index=True)
else:
    st.info("Amostra insuficiente para calcular grupos prioritários no recorte atual.")

# =============================================================================
# 19. MATRIZ DE PRIORIZAÇÃO
# =============================================================================

st.markdown("## Matriz de Priorização")

matrix = calculate_churn(df, "customer_segment")
if not matrix.empty:
    matrix = matrix.merge(
        df.groupby("customer_segment", observed=True)["engagement_score"].mean().rename("engagement_medio"),
        on="customer_segment", how="left"
    )
    avg_pop = matrix["clientes"].median()
    avg_rate = matrix["taxa_churn"].median()

    fig = px.scatter(
        matrix, x="clientes", y="taxa_churn", size="churn", color="customer_segment",
        hover_data={"customer_segment": True, "clientes": True, "churn": True,
                    "taxa_churn": ":.1%", "engagement_medio": ":.1f"},
        size_max=55,
    )
    fig.add_vline(x=avg_pop, line_dash="dot", line_color=COLOR_NEUTRAL)
    fig.add_hline(y=avg_rate, line_dash="dot", line_color=COLOR_NEUTRAL)
    fig.update_layout(yaxis_tickformat=".0%", xaxis_title="Quantidade de clientes", yaxis_title="Taxa de churn",
                       margin=dict(t=10, b=10, l=10, r=10), height=440, legend_title="Segmento")
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Quadrante superior direito (alta população + alta taxa de churn) = Alta prioridade · "
        "Superior esquerdo ou inferior direito = Atenção · Inferior esquerdo (baixa população + baixo churn) = Baixa prioridade."
    )

# =============================================================================
# 20. CLUSTERS
# =============================================================================

st.markdown("## Perfil dos Clusters")

if "cluster_group" in df.columns:
    clu = df.groupby("cluster_group", observed=True).agg(
        clientes=("id", "count"), churn=("exit", "sum"),
        engagement=("engagement_score", "mean"), services=("nums_service", "mean"),
        tenure=("tenure_ye", "mean"), risk=("risk_score", "mean"),
    ).reset_index()
    clu["taxa_churn"] = clu.apply(lambda r: safe_div(r["churn"], r["clientes"]), axis=1)
    clu = clu.sort_values("taxa_churn", ascending=False)

    c1, c2 = st.columns([1.2, 1])
    with c1:
        fig = px.bar(clu, x="cluster_group", y="taxa_churn",
                     text=clu["taxa_churn"].apply(fmt_pct), color_discrete_sequence=[COLOR_RETIDO])
        fig.update_traces(marker_color=COLOR_RETIDO, textposition="outside")
        fig.update_xaxes(type="category")
        fig.update_layout(yaxis_tickformat=".0%", xaxis_title="Cluster", yaxis_title="Taxa de churn",
                           margin=dict(t=10, b=10, l=10, r=10), height=340)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        clu_disp = clu.copy()
        clu_disp["taxa_churn"] = clu_disp["taxa_churn"].apply(fmt_pct)
        for c in ["engagement", "services", "tenure", "risk"]:
            clu_disp[c] = clu_disp[c].round(2)
        clu_disp = clu_disp.rename(columns={
            "cluster_group": "Cluster", "clientes": "Clientes", "churn": "Churn", "taxa_churn": "Taxa de Churn",
            "engagement": "Engajamento", "services": "Serviços", "tenure": "Tenure", "risk": "Risk Score"
        })
        st.dataframe(clu_disp, use_container_width=True, hide_index=True)

# =============================================================================
# 21. ANÁLISE ESTATÍSTICA
# =============================================================================

st.markdown("## Análise Estatística")

def cramers_v(confusion_matrix):
    chi2 = stats.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    denom = min((kcorr - 1), (rcorr - 1))
    return np.sqrt(phi2corr / denom) if denom > 0 else np.nan

cat_test_cols = ["customer_segment", "status_label", "loyalty_level", "digital_behavior", "risk_segment", "gender"]
stat_rows = []
for col in cat_test_cols:
    if col in df.columns and df[col].nunique() > 1:
        try:
            ct = pd.crosstab(df[col], df["exit"])
            chi2, p, dof, _ = stats.chi2_contingency(ct)
            v = cramers_v(ct)
            stat_rows.append({"Variável": col, "Teste": "Chi-square", "Estatística": round(chi2, 2),
                               "p-value": round(p, 4), "Cramér's V": round(v, 3)})
        except Exception:
            pass
stat_df = pd.DataFrame(stat_rows)

if not stat_df.empty:
    def interpret_p(p):
        return "Associação estatisticamente significativa" if p < 0.05 else "Sem evidência de associação significativa"
    stat_df["Interpretação"] = stat_df["p-value"].apply(interpret_p)
    st.dataframe(stat_df, use_container_width=True, hide_index=True)
    st.caption(
        "Chi-square avalia se existe associação estatística entre a variável categórica e o churn. "
        "Cramér's V mede a força dessa associação (0 = nenhuma, 1 = muito forte). "
        "Resultados indicam associação, não relação de causa e efeito."
    )

st.markdown("##### Variáveis Numéricas — Churn vs Retidos (Mann-Whitney U)")
num_test_cols = ["age", "credit_sco", "balance", "monthly_ir", "tenure_ye",
                  "nums_service", "engagement_score", "risk_score"]
num_rows = []
for col in num_test_cols:
    if col in df.columns:
        churn_vals = df.loc[df["exit"], col].dropna()
        ret_vals = df.loc[~df["exit"], col].dropna()
        if len(churn_vals) > 5 and len(ret_vals) > 5:
            try:
                u_stat, p = stats.mannwhitneyu(churn_vals, ret_vals, alternative="two-sided")
                num_rows.append({
                    "Variável": col, "Teste": "Mann-Whitney U", "Estatística": round(u_stat, 1),
                    "p-value": round(p, 4),
                    "Interpretação": "Diferença estatisticamente significativa" if p < 0.05 else "Sem diferença significativa"
                })
            except Exception:
                pass
if num_rows:
    st.dataframe(pd.DataFrame(num_rows), use_container_width=True, hide_index=True)

# =============================================================================
# 22. INSIGHTS AUTOMÁTICOS
# =============================================================================

st.markdown("## Principais Insights")

tone_class = {"alert": "alert", "warn": "warn", "good": "good"}
insight_list = generate_insights(df, kpis)
for item in insight_list:
    if isinstance(item, tuple):
        tone, txt = item
    else:
        tone, txt = "good", item
    st.markdown(f'<div class="insight-box {tone_class.get(tone, "")}">{txt}</div>', unsafe_allow_html=True)

# =============================================================================
# 23. RECOMENDAÇÕES DE NEGÓCIO
# =============================================================================

st.markdown("## Recomendações")

recommendations = []

# Engajamento
low_eng = df[df["engagement_band"] == "Muito Baixo"]
if len(low_eng) > 10:
    rate = low_eng["exit"].mean()
    recommendations.append({
        "diagnostico": "Baixo engajamento associado a maior churn.",
        "evidencia": f"Clientes com engajamento muito baixo apresentam {fmt_pct(rate)} de churn.",
        "acao": "Criar estratégia de reativação e aumento de frequência de uso (onboarding contínuo, gatilhos de uso, comunicação personalizada).",
        "prioridade": "Alta" if rate > kpis["churn_rate"] * 1.2 else "Média",
    })

# Inatividade
inactive = df[df["status_label"] == "Inativo"]
active = df[df["status_label"] == "Ativo"]
if len(inactive) > 10 and len(active) > 10:
    r_in, r_ac = inactive["exit"].mean(), active["exit"].mean()
    if r_in > r_ac:
        recommendations.append({
            "diagnostico": "Clientes inativos concentram maior exposição ao churn.",
            "evidencia": f"Inativos apresentam {fmt_pct(r_in)} de churn contra {fmt_pct(r_ac)} entre ativos.",
            "acao": "Implementar jornada de reativação para clientes que ultrapassam determinado período sem atividade.",
            "prioridade": "Alta" if r_in > r_ac * 1.5 else "Média",
        })

# Utilização de serviços
if low_srv > high_srv:
    recommendations.append({
        "diagnostico": "Baixa utilização de serviços associada a maior churn.",
        "evidencia": f"Clientes com utilização abaixo da mediana apresentam {fmt_pct(low_srv)} de churn contra {fmt_pct(high_srv)}.",
        "acao": "Incentivar cross-sell e adoção de serviços adicionais via jornadas orientadas por comportamento.",
        "prioridade": "Média",
    })

# Loyalty
if not loy_tab.empty:
    worst_loy = loy_tab.iloc[0]
    if worst_loy["taxa_churn"] > kpis["churn_rate"]:
        recommendations.append({
            "diagnostico": f"Nível de lealdade '{worst_loy['loyalty_level']}' concentra maior churn.",
            "evidencia": f"Taxa de churn de {fmt_pct(worst_loy['taxa_churn'])} neste grupo, frente a {fmt_pct(kpis['churn_rate'])} da carteira.",
            "acao": "Desenvolver programa de fidelização com benefícios progressivos para elevar o nível de lealdade.",
            "prioridade": "Alta" if worst_loy["taxa_churn"] > kpis["churn_rate"] * 1.3 else "Média",
        })

# Tenure crítico
if not ten_tab.empty:
    critical_tenure = ten_tab.sort_values("taxa_churn", ascending=False).iloc[0]
    if pd.notna(critical_tenure["tenure_band"]):
        recommendations.append({
            "diagnostico": f"Faixa de tenure '{critical_tenure['tenure_band']}' concentra maior risco de churn.",
            "evidencia": f"Taxa de churn de {fmt_pct(critical_tenure['taxa_churn'])} neste grupo.",
            "acao": "Reforçar acompanhamento e comunicação proativa nesse momento específico do ciclo de relacionamento.",
            "prioridade": "Média",
        })

if not recommendations:
    st.info("Nenhuma recomendação relevante identificada para o recorte atual — o comportamento de churn está próximo da média em todos os grupos analisados.")
else:
    for rec in recommendations:
        prio_class = f"reco-priority-{rec['prioridade'].lower()}"
        st.markdown(f"""
        <div class="reco-card {prio_class}">
            <b>Diagnóstico:</b> {rec['diagnostico']}<br>
            <b>Evidência:</b> {rec['evidencia']}<br>
            <b>Ação:</b> {rec['acao']}<br>
            <b>Prioridade:</b> {rec['prioridade']}
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.caption(
    f"Diagnóstico gerado sobre {fmt_num(kpis['total'])} clientes no recorte selecionado · "
    f"Fonte: {'base carregada pelo usuário' if data_source == 'upload' else 'base sintética de demonstração'}."
)
