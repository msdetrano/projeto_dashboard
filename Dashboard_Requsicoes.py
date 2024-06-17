import pandas as pd
import altair as alt
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

# Carregar os dados do arquivo Excel
file_path = 'requisicoes.xlsx'
fonteCsv = pd.read_excel(file_path)

# Processamento inicial dos dados
def processar_dados(dados):
    contagem_chamados_analista = dados['Designado Nome completo'].value_counts().reset_index()
    contagem_chamados_analista.columns = ['Designado Nome completo', 'Quantidade']

    contagem_chamados_prioridade = dados['Prioridade'].value_counts().reset_index()
    contagem_chamados_prioridade.columns = ['Prioridade', 'Quantidade']

    contagem_chamados_grupo = dados['Grupo designado Nome completo'].value_counts().reset_index()
    contagem_chamados_grupo.columns = ['Grupo designado Nome completo', 'Quantidade']

    return contagem_chamados_analista, contagem_chamados_prioridade, contagem_chamados_grupo

# Função para filtrar os dados com base no ano, mês e dia selecionados
def filtrar_dados(fonte, ano=None, mes=None, dia=None):
    dados_filtrados = fonte.copy()
    
    if ano:
        dados_filtrados = dados_filtrados[dados_filtrados['MNS Próximo tempo previsto'].dt.year == ano]
    if mes:
        dados_filtrados = dados_filtrados[dados_filtrados['MNS Próximo tempo previsto'].dt.month == mes]
    if dia:
        dados_filtrados = dados_filtrados[dados_filtrados['MNS Próximo tempo previsto'].dt.day == dia]
    
    return dados_filtrados

# Processar os dados iniciais
(contagem_chamados_analista, contagem_chamados_prioridade, contagem_chamados_grupo) = processar_dados(fonteCsv)

# Interface Streamlit
st.set_page_config(layout="wide")
st.title('Dashboard de Análise de Requisições')
st.markdown('<i>Visualização dos Dados de Requisições</i>', unsafe_allow_html=True)

# Sidebar - Filtros
st.sidebar.title('Filtros')
anos = st.sidebar.multiselect('Selecionar Anos', sorted(fonteCsv['MNS Próximo tempo previsto'].dt.year.unique()))
meses = st.sidebar.multiselect('Selecionar Meses', sorted(fonteCsv['MNS Próximo tempo previsto'].dt.month.unique()))
dias = st.sidebar.multiselect('Selecionar Dias', sorted(fonteCsv['MNS Próximo tempo previsto'].dt.day.unique()))

# Aplicar filtros aos dados
dados_filtrados = fonteCsv.copy()
if anos:
    dados_filtrados = dados_filtrados[dados_filtrados['MNS Próximo tempo previsto'].dt.year.isin(anos)]
if meses:
    dados_filtrados = dados_filtrados[dados_filtrados['MNS Próximo tempo previsto'].dt.month.isin(meses)]
if dias:
    dados_filtrados = dados_filtrados[dados_filtrados['MNS Próximo tempo previsto'].dt.day.isin(dias)]

# Processar os dados filtrados
(contagem_chamados_analista, contagem_chamados_prioridade, contagem_chamados_grupo) = processar_dados(dados_filtrados)

# Gráficos
grafico_barra_analista = alt.Chart(contagem_chamados_analista).mark_bar().encode(
    x=alt.X('Designado Nome completo', sort='-y'),
    y='Quantidade',
    color=alt.Color('Designado Nome completo', legend=None, scale=alt.Scale(scheme='pastel1')),
    tooltip=['Designado Nome completo', 'Quantidade']
).properties(
    width=600,
    height=400,
    title='Chamados por Analista'
)

grafico_barra_prioridade = alt.Chart(contagem_chamados_prioridade).mark_bar().encode(
    x=alt.X('Prioridade', sort='-y'),
    y='Quantidade',
    color=alt.Color('Prioridade', legend=None, scale=alt.Scale(scheme='pastel1')),
    tooltip=['Prioridade', 'Quantidade']
).properties(
    width=600,
    height=400,
    title='Chamados por Prioridade'
)

grafico_barra_grupo = alt.Chart(contagem_chamados_grupo).mark_bar().encode(
    x=alt.X('Grupo designado Nome completo', sort='-y'),
    y='Quantidade',
    color=alt.Color('Grupo designado Nome completo', legend=None, scale=alt.Scale(scheme='pastel1')),
    tooltip=['Grupo designado Nome completo', 'Quantidade']
).properties(
    width=600,
    height=400,
    title='Chamados por Grupo Designado'
)

# Exibir os gráficos na interface
st.altair_chart(grafico_barra_analista, use_container_width=True)
st.altair_chart(grafico_barra_prioridade, use_container_width=True)
st.altair_chart(grafico_barra_grupo, use_container_width=True)

# Tabela interativa com AgGrid
st.subheader('Lista de Analistas e Quantidade de Chamados Atendidos')

gb = GridOptionsBuilder.from_dataframe(contagem_chamados_analista)
gb.configure_pagination(paginationAutoPageSize=True)
gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)

grid_options = gb.build()
AgGrid(
    contagem_chamados_analista,
    gridOptions=grid_options,
)
