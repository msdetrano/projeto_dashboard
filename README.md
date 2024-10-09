
![image](https://github.com/user-attachments/assets/c9be3b7b-141b-4905-9829-ad28c6f143f1)
![image](https://github.com/user-attachments/assets/423d59cd-7403-4a59-a540-732a90e1ef51)


# Dashboard de Análise de Chamados de Incidentes de Operações

Este repositório contém uma aplicação desenvolvida em Python usando Streamlit para análise de chamados de incidentes em operações. A aplicação oferece uma visualização interativa dos dados dos chamados, permitindo que os usuários explorem informações sobre o tempo médio de resolução e a quantidade de chamados atendidos por analista.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação utilizada para o desenvolvimento da aplicação.
- **Streamlit**: Framework para a criação de aplicações web interativas.
- **Pandas**: Biblioteca para manipulação e análise de dados.
- **Altair**: Biblioteca para visualização de dados.
- **st_aggrid**: Biblioteca para exibição de tabelas interativas.

## Funcionalidades

- **Visualização dos Dados dos Chamados**: Apresentação de dados sobre os chamados de incidentes.
- **Tempo Médio de Resolução por Analista**: Gráficos que mostram o tempo médio que cada analista leva para resolver os chamados.
- **Lista de Analistas e Quantidade de Chamados Atendidos**: Tabela que exibe a quantidade de chamados atendidos por cada analista.

## Como Executar a Aplicação

Para rodar a aplicação localmente, siga os passos abaixo:

1. Clone o repositório:

   ```bash
   $  git clone https://github.com/msdetrano/projeto_dashboard.git
   $  cd projeto_dashboard/
   $  python -m venv venv
   $  source venv/bin/activate  # Linux ou macOS
   $  venv\Scripts\activate  # Windows
   $  pip install -r requirements.txt
   $  streamlit run app.py


projeto_dashboard/
│
├── app.py                 # Arquivo principal da aplicação Streamlit
├── requirements.txt       # Dependências do projeto
└── data/                  # Pasta para armazenar os dados (se necessário)


  


