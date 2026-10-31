import altair as alt
import pandas as pd
import streamlit as st

from src.data_loader import load_data

st.set_page_config(
    page_title="Fatores de Risco Cardiovascular",
    layout="wide",
)

st.title("Fatores de Risco Cardiovascular")

NOMES_VARIAVEIS = {
    "Height_(cm)": "Altura (cm)",
    "Weight_(kg)": "Peso (kg)",
    "BMI": "IMC",
    "Alcohol_Consumption": "Álcool (dias/mês)",
    "Fruit_Consumption": "Frutas (vezes/mês)",
    "Green_Vegetables_Consumption": "Vegetais verdes (vezes/mês)",
    "FriedPotato_Consumption": "Batata frita (vezes/mês)",
}
VARS_QUANT = list(NOMES_VARIAVEIS.values())

SEM_DOENCA = "Sem doença cardíaca"
COM_DOENCA = "Com doença cardíaca"

df = load_data().rename(columns=NOMES_VARIAVEIS)
df["Doença cardíaca"] = df["Heart_Disease"].map({"No": SEM_DOENCA, "Yes": COM_DOENCA})

COR_ROSA = "#ffd6d6"
COR_AZUL = "#0cc0df"
COR_CORAL = "#ff6b81"
COR_CONTORNO = "#8a93a6"

COR_SEM_DOENCA = COR_AZUL
COR_COM_DOENCA = COR_ROSA
COR_HISTOGRAMA = COR_ROSA
CORES_CLASSE = alt.Scale(domain=[SEM_DOENCA, COM_DOENCA], range=[COR_SEM_DOENCA, COR_COM_DOENCA])

LEGENDA_CLASSE = (
    f"**Legenda**  \n"
    f":color[■]{{foreground=\"{COR_SEM_DOENCA}\"}} {SEM_DOENCA}  \n"
    f":color[■]{{foreground=\"{COR_COM_DOENCA}\"}} {COM_DOENCA}"
)

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

aba1, aba2 = st.tabs(["Correlação e Distribuição", "Indicadores de Risco"])

with aba1:
    st.markdown(
        "Explore as medidas corporais e os hábitos alimentares dos pacientes: "
        "como os valores se distribuem e quais variáveis se relacionam entre si."
    )

    resumo = st.empty()

    with st.container(border=True):
        st.markdown("**Filtros**")
        col_variaveis, col_intervalos = st.columns([1.6, 3])

        with col_variaveis:
            variaveis = st.multiselect(
                "Variáveis analisadas",
                options=VARS_QUANT,
                default=VARS_QUANT,
                help="Escolha quais variáveis aparecem nos histogramas e na correlação.",
                key="variaveis",
            )

            separar_por_classe = st.toggle(
                "Separar por doença cardíaca",
                value=False,
                help="Pinta os histogramas de cores diferentes para pacientes com e sem doença cardíaca.",
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
                            var,
                            min_value=minimo,
                            max_value=maximo,
                            value=(minimo, maximo),
                            step=passo,
                            key=f"intervalo_{var}",
                            help=f"Mantém só os pacientes com {var} dentro deste intervalo.",
                        )

    df_filtrado = df
    for var, (inicio, fim) in intervalos.items():
        df_filtrado = df_filtrado[df_filtrado[var].between(inicio, fim)]

    resumo.caption(f"{len(df_filtrado):,} de {len(df):,} pacientes dentro dos intervalos escolhidos.")

    col_distribuicao, col_correlacao = st.columns([1.4, 1])

    with col_correlacao:
        st.subheader("Correlação entre as variáveis")
        st.caption(
            "Correlação de Spearman, de -1 a 1. Perto de 1: as duas variáveis aumentam juntas. "
            "Perto de -1: quando uma aumenta, a outra diminui. Perto de 0: não há relação."
        )

        if len(variaveis) < 2:
            st.warning("Selecione pelo menos 2 variáveis para calcular a correlação.")
        elif len(df_filtrado) < 30:
            st.warning("Poucos pacientes nos intervalos escolhidos para calcular a correlação.")
        else:
            corr = (
                df_filtrado[variaveis]
                .corr(method="spearman")
                .rename_axis(index="Variável 2", columns="Variável 1")
                .reset_index()
                .melt(id_vars="Variável 2", var_name="Variável 1", value_name="Correlação")
            )
            ordem = {var: i for i, var in enumerate(variaveis)}
            corr = corr[corr["Variável 2"].map(ordem) > corr["Variável 1"].map(ordem)]

            base = alt.Chart(corr).encode(
                x=alt.X(
                    "Variável 1:N",
                    title=None,
                    sort=variaveis[:-1],
                    axis=alt.Axis(labelAngle=-40, labelFontSize=12, labelLimit=180, labelOverlap=False),
                ),
                y=alt.Y(
                    "Variável 2:N",
                    title=None,
                    sort=variaveis[1:],
                    axis=alt.Axis(labelFontSize=12, labelLimit=200),
                ),
            )
            heatmap = base.mark_rect().encode(
                color=alt.Color(
                    "Correlação:Q",
                    title="Correlação",
                    scale=alt.Scale(
                        domain=[-1, -0.5, 0, 0.5, 1],
                        range=["#078ea6", COR_AZUL, "#ffffff", COR_ROSA, COR_CORAL
                    ],
                        interpolate="rgb",
                    ),
                    legend=alt.Legend(titleFontSize=13, labelFontSize=12),
                ),
                tooltip=["Variável 1", "Variável 2", alt.Tooltip("Correlação:Q", format=".2f")],
            )
            valores = base.mark_text(fontSize=15).encode(
                text=alt.Text("Correlação:Q", format=".2f"),
                color=alt.condition("datum['Correlação'] > 0.75", alt.value("white"), alt.value("black")),
            )

            st.altair_chart(
                (heatmap + valores).properties(height=400),
                width="stretch",
                alt="Mapa de calor da correlação de Spearman entre as variáveis selecionadas",
            )

    with col_distribuicao:
        st.subheader("Distribuição das variáveis")
        st.caption("Cada barra mostra quantos pacientes têm valores dentro daquela faixa.")

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
                    grupos = [faixas, df_filtrado["Doença cardíaca"]] if separar_por_classe else [faixas]
                    contagem = df_filtrado.groupby(grupos, observed=True).size().rename("Pacientes").reset_index()
                    contagem["De"] = contagem[var].map(lambda faixa: faixa.left).astype(float)
                    contagem["Até"] = contagem[var].map(lambda faixa: faixa.right).astype(float)
                    contagem = contagem.drop(columns=var)

                    histograma = (
                        alt.Chart(contagem)
                        .mark_bar(stroke=COR_CONTORNO, strokeWidth=0.6)
                        .encode(
                            x=alt.X("De:Q", bin="binned", title=var),
                            x2="Até:Q",
                            y=alt.Y("Pacientes:Q", title="Pacientes"),
                            tooltip=[
                                alt.Tooltip("De:Q", format=".1f"),
                                alt.Tooltip("Até:Q", format=".1f"),
                                alt.Tooltip("Pacientes:Q", format=","),
                            ],
                        )
                        .properties(height=200)
                    )
                    if separar_por_classe:
                        histograma = histograma.encode(
                            color=alt.Color("Doença cardíaca:N", scale=CORES_CLASSE, legend=None),
                            tooltip=[
                                "Doença cardíaca",
                                alt.Tooltip("De:Q", format=".1f"),
                                alt.Tooltip("Até:Q", format=".1f"),
                                alt.Tooltip("Pacientes:Q", format=","),
                            ],
                        )
                    else:
                        histograma = histograma.mark_bar(color=COR_HISTOGRAMA, stroke=COR_CONTORNO, strokeWidth=0.6)

                    with coluna:
                        st.altair_chart(histograma, width="stretch", alt=f"Histograma de {var}")

                if separar_por_classe and len(colunas) == 2 and len(variaveis[inicio : inicio + 2]) == 1:
                    colunas[1].markdown(LEGENDA_CLASSE)

with aba2:
    COR_DIABETES = COR_ROSA
    COR_DOENCA_CARDIACA = COR_AZUL
    FAIXAS_ETARIAS = ["<45", "45-54", "55-64", "65+"]
    CATEGORIAS_IMC = ["Abaixo do peso", "Peso normal", "Sobrepeso", "Obesidade"]

    st.markdown(
        "Compare a frequência de diabetes e de doença cardíaca entre pacientes "
        "com e sem três fatores de risco: obesidade, sedentarismo e tabagismo."
    )

    resumo_d2 = st.empty()

    with st.container(border=True):
        st.markdown("**Filtros**")
        col_sexo, col_faixa = st.columns([1, 2])
        with col_sexo:
            sexos = st.pills(
                "Sexo",
                options=["Feminino", "Masculino"],
                selection_mode="multi",
                key="d2_sexo",
                help="Deixe vazio para considerar todos.",
            )
        with col_faixa:
            faixas = st.pills(
                "Faixa etária (anos)",
                options=FAIXAS_ETARIAS,
                selection_mode="multi",
                key="d2_faixa",
                help="Deixe vazio para considerar todas.",
            )

    df_kpi = df
    if sexos:
        df_kpi = df_kpi[df_kpi["sexo_label"].isin(sexos)]
    if faixas:
        df_kpi = df_kpi[df_kpi["faixa_etaria"].isin(faixas)]

    resumo_d2.caption(f"{len(df_kpi):,} de {len(df):,} pacientes no recorte escolhido.")

    if df_kpi.empty:
        st.warning("Nenhum paciente no recorte escolhido.")
    else:
        tem_diabetes = df_kpi["Diabetes"] == "Yes"
        tem_doenca_cardiaca = df_kpi["Heart_Disease"] == "Yes"
        obeso = df_kpi["IMC"] >= 30
        pratica_exercicio = df_kpi["Exercise"] == "Yes"
        fumante = df_kpi["Smoking_History"] == "Yes"

        def taxa(condicao, grupo):
            return condicao[grupo].mean() if grupo.any() else None

        def cartao(coluna, titulo, condicao, grupo, nome_comparacao, explicacao):
            taxa_grupo = taxa(condicao, grupo)
            taxa_comparacao = taxa(condicao, ~grupo)
            with coluna:
                with st.container(border=True):
                    if taxa_grupo is None or taxa_comparacao is None:
                        st.metric(titulo, "—", help=explicacao)
                        st.caption("Sem pacientes suficientes nos dois grupos.")
                    else:
                        diferenca = (taxa_grupo - taxa_comparacao) * 100
                        st.metric(
                            titulo,
                            f"{taxa_grupo:.1%}",
                            delta=f"{diferenca:+.1f} p.p. vs {nome_comparacao} ({taxa_comparacao:.1%})",
                            delta_color="inverse",
                            help=explicacao,
                        )

        kpi1, kpi2, kpi3 = st.columns(3)
        cartao(
            kpi1,
            "Diabetes entre pessoas com obesidade",
            tem_diabetes,
            obeso,
            "sem obesidade",
            "Porcentagem de pessoas com diabetes entre quem tem IMC igual ou maior que 30. "
            "Pré-diabetes e diabetes gestacional não entram na conta.",
        )
        cartao(
            kpi2,
            "Diabetes entre quem não faz exercício",
            tem_diabetes,
            ~pratica_exercicio,
            "quem faz",
            "Porcentagem de pessoas com diabetes entre quem não pratica atividade física.",
        )
        cartao(
            kpi3,
            "Doença cardíaca entre quem já fumou",
            tem_doenca_cardiaca,
            fumante,
            "quem nunca fumou",
            "Porcentagem de pessoas com doença cardíaca entre quem tem histórico de tabagismo.",
        )
        st.caption(
            "p.p. = pontos percentuais: a diferença entre as duas porcentagens. "
            "Seta para cima indica que o grupo de risco tem mais casos."
        )

        st.subheader("Diabetes e doença cardíaca por faixa de peso")
        st.caption(
            "Faixas de IMC: abaixo do peso (< 18,5), peso normal (18,5 a 24,9), "
            "sobrepeso (25 a 29,9) e obesidade (30 ou mais)."
        )

        categoria_imc = pd.cut(
            df_kpi["IMC"],
            bins=[0, 18.5, 25, 30, float("inf")],
            right=False,
            labels=CATEGORIAS_IMC,
        )
        por_categoria = (
            pd.DataFrame(
                {
                    "Faixa de peso": categoria_imc,
                    "Diabetes": tem_diabetes,
                    "Doença cardíaca": tem_doenca_cardiaca,
                }
            )
            .groupby("Faixa de peso", observed=True)
            .agg(
                pacientes=("Diabetes", "size"),
                Diabetes=("Diabetes", "mean"),
                doenca=("Doença cardíaca", "mean"),
            )
            .rename(columns={"doenca": "Doença cardíaca", "pacientes": "Pacientes na faixa"})
            .reset_index()
            .melt(
                id_vars=["Faixa de peso", "Pacientes na faixa"],
                value_vars=["Diabetes", "Doença cardíaca"],
                var_name="Condição",
                value_name="Porcentagem",
            )
        )

        selecao = alt.selection_point(fields=["Faixa de peso"])

        barras = (
            alt.Chart(por_categoria)
            .mark_bar(stroke=COR_CONTORNO, strokeWidth=0.6)
            .encode(
                x=alt.X(
                    "Faixa de peso:N",
                    sort=CATEGORIAS_IMC,
                    title=None,
                    axis=alt.Axis(labelAngle=0, labelFontSize=13),
                ),
                xOffset=alt.XOffset("Condição:N"),
                y=alt.Y("Porcentagem:Q", title="% de pacientes", axis=alt.Axis(format="%")),
                color=alt.Color(
                    "Condição:N",
                    scale=alt.Scale(domain=["Diabetes", "Doença cardíaca"], range=[COR_DIABETES, COR_DOENCA_CARDIACA]),
                    legend=alt.Legend(title=None, orient="top", labelFontSize=13),
                ),
                opacity=alt.condition(selecao, alt.value(1), alt.value(0.35)),
                tooltip=[
                    "Faixa de peso:N",
                    "Condição:N",
                    alt.Tooltip("Porcentagem:Q", title="% de pacientes", format=".1%"),
                    alt.Tooltip("Pacientes na faixa:Q", format=","),
                ],
            )
            .add_params(selecao)
            .properties(height=380)
        )

        st.altair_chart(
            barras,
            width="stretch",
            alt="Gráfico de barras com a porcentagem de pacientes com diabetes e com doença cardíaca por faixa de peso",
        )
        st.caption("Clique numa faixa de peso para destacá-la. Clique fora das barras para desfazer.")


        COR_GRUPO_RISCO = COR_CORAL
    
        COR_GRUPO_REFERENCIA = "#7c9cff"

        def grafico_por_faixa(condicao, grupo, nome_risco, nome_referencia, nome_condicao):
            tabela = (
                pd.DataFrame(
                    {
                        "Faixa etária": df_kpi["faixa_etaria"],
                        "Grupo": grupo.map({True: nome_risco, False: nome_referencia}),
                        nome_condicao: condicao,
                    }
                )
                .groupby(["Faixa etária", "Grupo"], observed=True)
                .agg(Porcentagem=(nome_condicao, "mean"), Pacientes=(nome_condicao, "size"))
                .reset_index()
            )
            destaque = alt.selection_point(fields=["Faixa etária"])
            return (
                alt.Chart(tabela)
                .mark_bar(stroke=COR_CONTORNO, strokeWidth=0.6)
                .encode(
                    x=alt.X(
                        "Faixa etária:N",
                        sort=FAIXAS_ETARIAS,
                        title="Faixa etária (anos)",
                        axis=alt.Axis(labelAngle=0, labelFontSize=12),
                    ),
                    xOffset=alt.XOffset("Grupo:N", sort=[nome_risco, nome_referencia]),
                    y=alt.Y("Porcentagem:Q", title=f"% com {nome_condicao.lower()}", axis=alt.Axis(format="%")),
                    color=alt.Color(
                        "Grupo:N",
                        scale=alt.Scale(
                            domain=[nome_risco, nome_referencia],
                            range=[COR_GRUPO_RISCO, COR_GRUPO_REFERENCIA],
                        ),
                        legend=alt.Legend(title=None, orient="top", labelFontSize=12),
                    ),
                    opacity=alt.condition(destaque, alt.value(1), alt.value(0.35)),
                    tooltip=[
                        "Faixa etária:N",
                        "Grupo:N",
                        alt.Tooltip("Porcentagem:Q", title=f"% com {nome_condicao.lower()}", format=".1%"),
                        alt.Tooltip("Pacientes:Q", title="Pacientes no grupo", format=","),
                    ],
                )
                .add_params(destaque)
                .properties(height=320)
            )

        col_visual2, col_visual3 = st.columns(2)

        with col_visual2:
            st.subheader("Diabetes e exercício por idade")
            st.caption("% com diabetes em quem faz e em quem não faz exercício.")
            st.altair_chart(
                grafico_por_faixa(
                    tem_diabetes,
                    ~pratica_exercicio,
                    "Não faz exercício",
                    "Faz exercício",
                    "Diabetes",
                ),
                width="stretch",
                alt="Gráfico de barras com a porcentagem de diabetes entre quem faz e quem não faz exercício, por faixa etária",
            )

        with col_visual3:
            st.subheader("Doença cardíaca e tabagismo por idade")
            st.caption("% com doença cardíaca em quem já fumou e em quem nunca fumou.")
            st.altair_chart(
                grafico_por_faixa(
                    tem_doenca_cardiaca,
                    fumante,
                    "Já fumou",
                    "Nunca fumou",
                    "Doença cardíaca",
                ),
                width="stretch",
                alt="Gráfico de barras com a porcentagem de doença cardíaca entre quem já fumou e quem nunca fumou, por faixa etária",
            )

        st.caption("Clique numa faixa etária para destacá-la. Clique fora das barras para desfazer.")

        