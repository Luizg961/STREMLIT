

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import statistics as sts

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



#MOSTRANDO OS DADOS TRATADOS DEPOIS DE FAZER ANALISE EXPLORATORIA
tratou_id = False
st.title("App Interativo de Tratamento de Dados")
st.sidebar.title("OPÇOES DE TRATRAMENTOS")
if st.sidebar.checkbox("Remover IDs Duplicados"):
    quantidade_antes = base.shape[0]
    base.drop_duplicates(subset='ID', keep='first', inplace=True)
    quantidade_depois = base.shape[0]
    st.sidebar.success(f'{quantidade_antes - quantidade_depois} registro removido com sucesso')
    tratou_id = True

#------------------------------------------------
#TRATANDO OS NULOS


if st.sidebar.checkbox("Preencher salários nulos com a mediana"):
    mediana_Salario_na = sts.median(base["SALARIO"].dropna())
    base["SALARIO"] = base["SALARIO"].fillna(mediana_Salario_na)
    st.sidebar.success(f"Salários nulos preenchidos com a mediana ({mediana_Salario_na}")
    st.write(base.isnull().sum())

if st.sidebar.checkbox("Preencher gênero nulo com valor Da Moda"):
    base["GENERO"].fillna("Masculino", inplace=True)
    st.sidebar.success("Gênero nulo preenchido como 'Masculino")
    st.write(base.isnull().sum())



#----------------------------------
#IDADE

tratou_idade =False
if st.sidebar.checkbox("CORRIGIR IDADE QUA NAO SAO POSSIVEIS"):
    mediana_idade = sts.median(base['IDADE'])
    base.loc[(base['IDADE'] <0) | (base['IDADE'] >110), 'IDADE'] = mediana_idade
    st.sidebar.success(f"Idades fora do intervalo 0-110 substituídas pela mediana ({mediana_idade})")
    tratou_idade = True

if tratou_idade:
    st.subheader("DISTRIBUIÇAO DAS IDADES")
    fig, ax = plt.subplots(figsize=(8,4))
    sns.boxplot(data=base, x='IDADE', ax=ax)
    ax.set_title("DISTRIBUÇAO DE IDADE TRATADO")
    st.pyplot(fig)

#_--------------------------
#ESTADOS

tratando_estado = False
if st.sidebar.checkbox("CORRIGIR ESTADOS PELA MODA"):
    base.loc[base["ESTADOS"].isin(["RP","SP","TD"]), "ESTADOS"] = "RS"
    st.sidebar.success("NOMES CORRIGIDOS PELA MODA RS")
    tratando_estado = True

if tratando_estado:
    st.subheader("DISTRIBUIÇAO DOS ESTADOS FICARAM")
    fig, ax = plt.subplots(figsize=(10, 6))
    base["ESTADOS"].value_counts().plot(kind='bar')
    plt.xticks(rotation=45)
    ax.set_title("ESTADOS TRATADOS")
    st.pyplot(fig)

#------------------------------------------------------------
#GENEROS
tratando_genero =False

if st.sidebar.checkbox("PADRONIZANDO VALORES DE GÊNERO"):
    base.loc[base['GENERO'] == 'F', 'GENERO'] = 'Feminino'
    base.loc[base['GENERO'] == 'Fem', 'GENERO'] = 'Feminino'
    base.loc[base['GENERO'] == 'M', 'GENERO'] = 'Masculino'
    st.sidebar.success("Valores de gênero padronizados.") 
    tratando_genero = True

if tratando_genero:
    st.subheader("DISTRIBUÇAO DE GENERO FICOU")
    fig,ax = plt.subplots(figsize=(10,6))
    base["GENERO"].value_counts().plot(kind="bar")
    plt.xticks(rotation=45)
    ax.set_title("GENEROS PADRONIZADOS")
    st.pyplot(fig)

#------------------------------------------------
#OUTLIERS
salario_tratado=False
if st.sidebar.checkbox("Tratar salários fora do padrão (outliers)"):
    desvio = sts.stdev(base['SALARIO'])
    mediana_salario = sts.median(base["SALARIO"])
    base.loc[base["SALARIO"] >= 2* desvio, "SALARIO"] = mediana_salario
    st.sidebar.success(f"Salários acima de 2 desvios Padrao substituídos pela mediana ({mediana_salario})")
    salario_tratado=True

if salario_tratado:
    st.subheader("DISTRIBUÇAO DE SALARIO " )
    fig, ax = plt.subplots(figsize=(10,6))
    sns.boxplot(data=base, x="SALARIO" , ax=ax)
    ax.set_title("DESTRIBUIÇAO DE SALARIO TRATADO")
    st.pyplot(fig)


 # Exportar CSV
    st.download_button(
        label="📥 Baixar CSV tratado",
        data=base.to_csv(index=False).encode('utf-8'),
        file_name='dados_tratados.csv',
        mime='text/csv'
    )







    




       

