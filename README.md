# Fatores de Risco Cardiovascular

Dashboard interativo em Streamlit que analisa como medidas corporais e hábitos de vida se relacionam com diabetes e doença cardíaca.

**🔗 Link do app:** https://mmbcpraticaavd.streamlit.app/

Projeto desenvolvido na disciplina **Análise e Visualização de Dados** da **Cesar School** (2026.2), a partir da análise exploratória de dados (EDA) feita na Aula 11.

## Sobre os dados

- **Dataset:** Cardiovascular Diseases Risk Prediction (Kaggle), com cerca de 308 mil pacientes
- **Variáveis usadas:** altura, peso, IMC, consumo de álcool, frutas, vegetais verdes e batata frita, prática de exercício, histórico de tabagismo, diabetes, doença cardíaca, sexo e faixa etária
- **Tratamento (no notebook de EDA):** remoção de linhas duplicadas e de valores fisicamente impossíveis (altura fora de 120–220 cm e IMC fora de 13–80), além da criação das colunas de sexo e faixa etária em português

## Dashboards

O app tem duas abas:

### 1. Correlação e Distribuição
Mostra como os valores das variáveis quantitativas se distribuem e quais variáveis se relacionam entre si.
- Filtros: escolha das variáveis, intervalo de valores de cada variável e opção de separar por doença cardíaca
- Histogramas com a distribuição de cada variável
- Mapa de calor com a correlação de Spearman entre as variáveis

### 2. Indicadores de Risco
Compara a frequência de diabetes e de doença cardíaca entre pessoas com e sem três fatores de risco: obesidade, sedentarismo e tabagismo.
- Filtros: sexo e faixa etária
- 3 indicadores (KPIs):
  - Diabetes entre pessoas com obesidade
  - Diabetes entre quem não faz exercício
  - Doença cardíaca entre quem já fumou
- 3 gráficos:
  - Diabetes e doença cardíaca por faixa de peso (IMC)
  - Diabetes e exercício por faixa etária
  - Doença cardíaca e tabagismo por faixa etária

As métricas mostram **associação**, não causa. A justificativa de cada uma está em [`entregas/justificativa-metricas.md`](entregas/justificativa-metricas.md).

## Tecnologias

- Python
- pandas
- Streamlit
- Altair
- Jupyter Notebook (EDA com pandas, matplotlib, seaborn e scipy)
- Deploy no Streamlit Community Cloud

## Estrutura do repositório

| Pasta / arquivo | Conteúdo |
|---|---|
| `app.py` | Aplicação Streamlit com os dois dashboards |
| `src/data_loader.py` | Leitura do dataset tratado, com cache |
| `notebooks/` | Notebook da EDA original e notebook que exporta o dataset tratado |
| `data/clean/` | Dataset tratado, usado pelo app |
| `data/raw/` | Dataset bruto (não versionado) |
| `entregas/` | Rascunhos dos dois dashboards e justificativa das métricas |
| `prompts/` | Templates de prompt e declaração de uso de IA |
| `.streamlit/config.toml` | Identidade visual do app |

## Como rodar localmente

Requer Python 3.11 a 3.15.

```bash
git clone https://github.com/marimmbc/Pratica-Streamlit.git
cd Pratica-Streamlit

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

No Windows, ative o ambiente com `.venv\Scripts\activate`.


