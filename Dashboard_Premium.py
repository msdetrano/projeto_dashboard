import pandas as pd
import altair as alt
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

# Carregar os dados do arquivo Excel (substitua pelo seu caminho e nome de arquivo)
fonteCsv = pd.read_excel('dadosPremium.xlsx')

# Processamento dos dados
contagem_chamados_analista = fonteCsv['Designado Nome completo'].value_counts().reset_index()
contagem_chamados_analista.columns = ['Designado Nome completo', 'Quantidade']

contagem_chamados_prioridade = fonteCsv['Prioridade'].value_counts().reset_index()
contagem_chamados_prioridade.columns = ['Prioridade', 'Quantidade']

contagem_chamados_grupo = fonteCsv['Grupo de central de serviços Nome completo'].value_counts().reset_index()
contagem_chamados_grupo.columns = ['Grupo de central de serviços', 'Quantidade']

fonteCsv['Hora de Criação'] = pd.to_datetime(fonteCsv['Hora de Criação'], errors='coerce')
fonteCsv['Hora da solução'] = pd.to_datetime(fonteCsv['Hora da solução'], errors='coerce')
fonteCsv['Tempo de resolução'] = (fonteCsv['Hora da solução'] - fonteCsv['Hora de Criação']).dt.total_seconds() / 3600  # Converter minutos para horas
tempo_medio_resolucao = fonteCsv.groupby('Designado Nome completo')['Tempo de resolução'].mean().reset_index().round(2)

# Interface Streamlit
st.set_page_config(layout="wide")  # Configura a página para layout amplo
st.title('Dashboard de Volumetria de Chamados de Incidentes de Operações')
st.markdown('<i>Visualização dos Dados dos Chamados</i>', unsafe_allow_html=True)  # Subtítulo em itálico

# Estilizar o sidebar com CSS (se necessário)
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #FFFACD; /* Cor de fundo */
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1); /* Sombra suave */
    }
    .sidebar .sidebar-content .sidebar-section {
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content .stSelectbox, 
    .sidebar .sidebar-content .stTextInput, 
    .sidebar .sidebar-content .stNumberInput {
        background-color: #FFFFE0; /* Cor dos inputs */
        border-radius: 5px;
        font-size: 14pt;
    }
    .sidebar .sidebar-content .stSelectbox > div {
        border-radius: 5px;
    }
    .sidebar .sidebar-content .stButton {
        background-color: #FFD700; /* Cor do botão */
        color: #333333; /* Cor do texto do botão */
        border-radius: 5px;
        font-size: 14pt;
        font-weight: bold;
    }
    .sidebar .sidebar-content img {
        width: 100%;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Adicionar o logo da Premium no topo do sidebar
# URL da imagem desejada
url_imagem = "logo.png"

# Exibir a imagem no sidebar
st.sidebar.image(url_imagem, width=200)

# Adicionar filtros laterais para ano, mês e dia
st.sidebar.header("Filtros")

anos_disponiveis = sorted(fonteCsv['Hora de Criação'].dt.year.unique())
ano_selecionado = st.sidebar.selectbox('Selecione o Ano', ['Ano Todo'] + anos_disponiveis)

if ano_selecionado != 'Ano Todo':
    dados_filtrados = fonteCsv[fonteCsv['Hora de Criação'].dt.year == ano_selecionado]
else:
    dados_filtrados = fonteCsv.copy()

# Função para filtrar por mês
def filtrar_por_mes(dados, mes):
    if mes == 'Mês Todo':
        return dados
    else:
        return dados[dados['Hora de Criação'].dt.month_name() == mes]

# Função para filtrar por dia
def filtrar_por_dia(dados, dia):
    if dia == 'Dia Todo':
        return dados
    else:
        return dados[dados['Hora de Criação'].dt.day == dia]

# Se houver dados filtrados pelo ano selecionado, então mostrar filtros de mês e dia
if not dados_filtrados.empty:
    meses_disponiveis = ['Mês Todo'] + sorted(dados_filtrados['Hora de Criação'].dt.month_name().unique())
    mes_selecionado = st.sidebar.selectbox('Selecione o Mês', meses_disponiveis)

    dados_filtrados = filtrar_por_mes(dados_filtrados, mes_selecionado)

    if mes_selecionado != 'Mês Todo':
        dias_disponiveis = ['Dia Todo'] + sorted(dados_filtrados['Hora de Criação'].dt.day.unique())
        dia_selecionado = st.sidebar.selectbox('Selecione o Dia', dias_disponiveis)

        dados_filtrados = filtrar_por_dia(dados_filtrados, dia_selecionado)

# Atualizar contagens e tempo médio de resolução com dados filtrados
contagem_chamados_analista = dados_filtrados['Designado Nome completo'].value_counts().reset_index()
contagem_chamados_analista.columns = ['Designado Nome completo', 'Quantidade']

contagem_chamados_prioridade = dados_filtrados['Prioridade'].value_counts().reset_index()
contagem_chamados_prioridade.columns = ['Prioridade', 'Quantidade']

contagem_chamados_grupo = dados_filtrados['Grupo de central de serviços Nome completo'].value_counts().reset_index()
contagem_chamados_grupo.columns = ['Grupo de central de serviços', 'Quantidade']

tempo_medio_resolucao = dados_filtrados.groupby('Designado Nome completo')['Tempo de resolução'].mean().reset_index().round(2)

# Funções para gerar gráficos com cores pastel
def gerar_grafico_barra(df, x, y, title):
    return alt.Chart(df).mark_bar().encode(
        x=alt.X(x, sort='-y'),
        y=y,
        color=alt.Color(x, legend=None, scale=alt.Scale(scheme='pastel1')),  # Adicionar cores pastel aos gráficos de barra
        tooltip=[x, y]
    ).properties(
        width=300,
        height=300,
        title=title
    )

def gerar_grafico_pizza(df, theta, color, title):
    return alt.Chart(df).mark_arc().encode(
        theta=theta,
        color=alt.Color(color, scale=alt.Scale(scheme='pastel1')),
        tooltip=[color, theta]
    ).properties(
        width=300,
        height=300,
        title=title
    ).interactive()

# Gerar os gráficos
grafico_barra_analista = gerar_grafico_barra(contagem_chamados_analista, 'Designado Nome completo', 'Quantidade', 'Chamados por Analista')
grafico_barra_prioridade = gerar_grafico_barra(contagem_chamados_prioridade, 'Prioridade', 'Quantidade', 'Chamados por Prioridade')
grafico_barra_grupo = gerar_grafico_barra(contagem_chamados_grupo, 'Grupo de central de serviços', 'Quantidade', 'Chamados por Grupo de Central de Serviços')
grafico_pizza_prioridade = gerar_grafico_pizza(contagem_chamados_prioridade, 'Quantidade', 'Prioridade', 'Distribuição por Prioridade')

# Exibir os gráficos na interface
# Layout de 2 linhas por 2 colunas
linha1_col1, linha1_col2 = st.columns(2)
linha2_col1, linha2_col2 = st.columns(2)

# Gráficos da primeira linha
with linha1_col1:
    st.altair_chart(grafico_barra_analista, use_container_width=True)

with linha1_col2:
    st.altair_chart(grafico_pizza_prioridade, use_container_width=True)

# Gráficos da segunda linha
with linha2_col1:
    st.altair_chart(grafico_barra_prioridade, use_container_width=True)

with linha2_col2:
    st.altair_chart(grafico_barra_grupo, use_container_width=True)

# Gráfico de tempo médio de resolução
st.subheader('Tempo Médio de Resolução por Analista')
st.altair_chart(
    alt.Chart(tempo_medio_resolucao).mark_bar().encode(
        x='Designado Nome completo',
        y='Tempo de resolução',
        color=alt.Color('Designado Nome completo', legend=None, scale=alt.Scale(scheme='pastel1')),  # Adicionar cores pastel aos gráficos de barra
        tooltip=['Designado Nome completo', 'Tempo de resolução']
    ).properties(
        width=700,
        height=300,
        title='Tempo Médio de Resolução por Analista (em horas)'
    ), 
    use_container_width=True
)

# Lista de analistas e quantidade de chamados atendidos
st.subheader('Lista de Analistas e Quantidade de Chamados Atendidos')

# Configurar a visualização com AgGrid
gb = GridOptionsBuilder.from_dataframe(contagem_chamados_analista)
gb.configure_pagination(paginationAutoPageSize=True)  # Paginação automática
gb.configure_side_bar()  # Barra lateral
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)  # Configuração das colunas padrão

# Ajustar a altura e a largura da tabela para se adaptar ao container
grid_options = gb.build()
AgGrid(
    contagem_chamados_analista,
    gridOptions=grid_options,
)
