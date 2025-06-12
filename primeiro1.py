

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Análise Exploratória com Dados CSV (USANDO STREAMLIT)")

# Caminho e separador
caminho_csv = 'Churn.csv'
sep_csv = ';'

# Carregar os dados
@st.cache_data
def carregar_dados():
    try:
        base = pd.read_csv(caminho_csv, sep=sep_csv)
        return base
    except FileNotFoundError:
        st.error(f"ARQUIVO NÃO ENCONTRADO: {caminho_csv}")
        return None

base = carregar_dados()

# Mostrar os dados
if base is not None:
    st.subheader("DADOS CARREGADOS")
    st.dataframe(base)

    # Trocar nomes das colunas
    base.columns = ["ID", "SCORE", "ESTADOS", "GENERO", "IDADE", "PATRIMONIO",
                    "SALDO", "PRODUTOS", "CARTAODECREDITO", "ATIVO", "SALARIO", "SAIU"]

    st.write("NOMES ALTERADOS COM SUCESSO:")
    st.write(base)

    # Variáveis categóricas
    variaveis_categoricas = ['GENERO', 'ESTADOS']
    variaveis_numericas = ['ID','SCORE','IDADE','PATRIMONIO','SALDO','PRODUTOS','CARTAODECREDITO','ATIVO','SALARIO','SAIU']

    # Valores nulos
    st.subheader("VALORES NULOS")
    st.write(base.isnull().sum())

    # Distribuição das variáveis categóricas
    st.subheader('Distribuição de Variáveis Categóricas')
    for coluna in variaveis_categoricas:
        fig, ax = plt.subplots(figsize=(10, 6))
        base[coluna].value_counts().plot(kind='bar')
        plt.xticks(rotation=45)
        st.subheader("INFORMAÇÕES GERAIS")
        st.pyplot(fig)
        st.write(base[coluna].describe())

    #VERIFICANDO VAIRVEIS NUMERICAS
    st.subheader("Distribuição de Variáveis NUMERICAS")
    for coluna in variaveis_numericas:
        if coluna in base.columns:
         st.write(f"Boxplot de {coluna}")
         fig, ax = plt.subplots(figsize=(8, 4))
         sns.boxplot(data=base, x=coluna, ax=ax)
         st.pyplot(fig)
         st.write(base[coluna].describe())

    



       

