import altair as alt
import pandas as pd
import streamlit as st

from src.data_loader import load_data

st.set_page_config(
    page_title="Correlação e Distribuição: Cardiovascular Diseases Risk",
    layout="wide",
)

st.title("Correlação e Distribuição das Variáveis Quantitativas: Cardiovascular Diseases Risk")

df = load_data()

VARS_QUANT = [
    "Height_(cm)",
    "Weight_(kg)",
    "BMI",
    "Alcohol_Consumption",
    "Fruit_Consumption",
    "Green_Vegetables_Consumption",
    "FriedPotato_Consumption",
]

st.markdown(
    """
    <style>
    .st-key-variaveis [data-testid="stMultiSelectTagsContainer"],
    .st-key-variaveis [data-testid="stMultiSelectTagsContainer"] > span[role="group"] {
        flex-wrap: wrap;
        overflow-x: hidden;
    }
    .st-key-variaveis div[role="group"]:has(> [data-testid="stMultiSelectTagsContainer"]) {
        height: auto !important;
        max-height: none !important;
        min-height: 2.5rem;
        align-items: flex-start;
        padding-top: 0.25rem;
        padding-bottom: 0.25rem;
    }
    .st-key-variaveis [data-testid="stMultiSelectTagsContainer"] {
        max-height: 9rem;
        overflow-y: auto;
        scrollbar-width: thin;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

resumo = st.empty()

with st.container(border=True):
    st.markdown("**Filtros**")
    col_variaveis, col_intervalos = st.columns([1.6, 3])

    with col_variaveis:
        variaveis = st.multiselect(
            "Variáveis Quantitativas",
            options=VARS_QUANT,
            default=VARS_QUANT,
            help="Selecione as variáveis quantitativas que deseja analisar no dashboard.",
            key="variaveis",
        )

        separar_por_classe = st.toggle(
            "Distinguir por Classe",
            value=False,
            help="Colore a distribuição pela classe (Heart_Disease: No ou Yes).",
        )

    intervalos = {}
    with col_intervalos:
        for inicio in range(0, len(variaveis), 3):
            colunas_slider = st.columns(3)
            for coluna, var in zip(colunas_slider, variaveis[inicio : inicio + 3]):
                if pd.api.types.is_integer_dtype(df[var]):
                    minimo, maximo, passo = int(df[var].min()), int(df[var].max()), 1
                else:
                    minimo, maximo, passo = float(df[var].min()), float(df[var].max()), 0.1
                with coluna:
                    intervalos[var] = st.slider(
                        f"Intervalo de {var}",
                        min_value=minimo,
                        max_value=maximo,
                        value=(minimo, maximo),
                        step=passo,
                        key=f"intervalo_{var}",
                    )

df_filtrado = df
for var, (inicio, fim) in intervalos.items():
    df_filtrado = df_filtrado[df_filtrado[var].between(inicio, fim)]

resumo.caption(f"{len(df_filtrado):,} de {len(df):,} pacientes dentro dos intervalos escolhidos.")

col_distribuicao, col_correlacao = st.columns([1.4, 1])

COR_ROSA = "#ffd6d6"
COR_AZUL = "#0cc0df"
COR_ROSA2 = "#cc007e"
COR_CONTORNO = "#8a93a6"

COR_NORMAL = COR_AZUL
COR_CARDIACO = COR_ROSA
COR_HISTOGRAMA = COR_ROSA
CORES_CLASSE = alt.Scale(domain=["No", "Yes"], range=[COR_NORMAL, COR_CARDIACO])

LEGENDA_CLASSE = (
    f"**Classe**  \n"
    f":color[■]{{foreground=\"{COR_NORMAL}\"}} Sem doença cardíaca (No)  \n"
    f":color[■]{{foreground=\"{COR_CARDIACO}\"}} Com doença cardíaca (Yes)"
)

with col_correlacao:
    st.subheader("Correlação (Spearman)")

    if len(variaveis) < 2:
        st.warning("Selecione pelo menos 2 variáveis para calcular a correlação.")
    elif len(df_filtrado) < 30:
        st.warning("Poucos pacientes nos intervalos escolhidos para calcular a correlação.")
    else:
        corr = (
            df_filtrado[variaveis]
            .corr(method="spearman")
            .rename_axis(index="var_y", columns="var_x")
            .reset_index()
            .melt(id_vars="var_y", var_name="var_x", value_name="correlacao")
        )
        ordem = {var: i for i, var in enumerate(variaveis)}
        corr = corr[corr["var_y"].map(ordem) > corr["var_x"].map(ordem)]

        base = alt.Chart(corr).encode(
            x=alt.X(
                "var_x:N",
                title=None,
                sort=variaveis[:-1],
                axis=alt.Axis(labelAngle=0, labelFontSize=14),
            ),
            y=alt.Y("var_y:N", title=None, sort=variaveis[1:], axis=alt.Axis(labelFontSize=14)),
        )
        heatmap = base.mark_rect().encode(
            color=alt.Color(
                "correlacao:Q",
                title="Spearman",
                scale=alt.Scale(
                    domain=[-1, -0.5, 0, 0.5, 1],
                    range=["#6cc9da", COR_AZUL, "#ffffff", COR_ROSA, "#f0959a"],
                    interpolate="rgb",
                ),
                legend=alt.Legend(titleFontSize=14, labelFontSize=13),
            ),
            tooltip=["var_x", "var_y", alt.Tooltip("correlacao:Q", format=".2f")],
        )
        valores = base.mark_text(fontSize=16).encode(
            text=alt.Text("correlacao:Q", format=".2f"),
            color=alt.value("black"),
        )

        st.altair_chart(
            (heatmap + valores).properties(height=380),
            width="stretch",
            alt="Mapa de calor (triângulo inferior, sem a diagonal) da correlação de Spearman entre as variáveis quantitativas selecionadas",
        )

with col_distribuicao:
    st.subheader("Distribuição")

    if not variaveis:
        st.warning("Selecione pelo menos 1 variável para ver a distribuição.")
    elif df_filtrado.empty:
        st.warning("Nenhum paciente dentro dos intervalos escolhidos.")
    else:
        if separar_por_classe and len(variaveis) % 2 == 0:
            st.markdown(LEGENDA_CLASSE)

        for inicio in range(0, len(variaveis), 2):
            colunas = st.columns(2)
            for coluna, var in zip(colunas, variaveis[inicio : inicio + 2]):
                faixas = pd.cut(df_filtrado[var], bins=20)
                grupos = [faixas, df_filtrado["Heart_Disease"]] if separar_por_classe else [faixas]
                contagem = df_filtrado.groupby(grupos, observed=True).size().rename("pacientes").reset_index()
                contagem["inicio"] = contagem[var].map(lambda faixa: faixa.left).astype(float)
                contagem["fim"] = contagem[var].map(lambda faixa: faixa.right).astype(float)
                contagem = contagem.drop(columns=var)

                histograma = (
                    alt.Chart(contagem)
                    .mark_bar(stroke=COR_CONTORNO, strokeWidth=0.6)
                    .encode(
                        x=alt.X("inicio:Q", bin="binned", title=var),
                        x2="fim:Q",
                        y=alt.Y("pacientes:Q", title="Pacientes"),
                        tooltip=[alt.Tooltip("pacientes:Q", title="Pacientes", format=",")],
                    )
                    .properties(height=200)
                )
                if separar_por_classe:
                    histograma = histograma.encode(
                        color=alt.Color("Heart_Disease:N", title="Classe", scale=CORES_CLASSE, legend=None),
                        tooltip=["Heart_Disease", alt.Tooltip("pacientes:Q", title="Pacientes", format=",")],
                    )
                else:
                    histograma = histograma.mark_bar(color=COR_HISTOGRAMA, stroke=COR_CONTORNO, strokeWidth=0.6)

                with coluna:
                    st.altair_chart(histograma, width="stretch", alt=f"Histograma da variável {var}")

            if separar_por_classe and len(colunas) == 2 and len(variaveis[inicio : inicio + 2]) == 1:
                colunas[1].markdown(LEGENDA_CLASSE)