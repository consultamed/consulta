import streamlit as st
import pandas as pd
import unicodedata

# Função para remover acentos e deixar lowercase
def normalizar(texto):
    if pd.isna(texto):
        return ""
    return ''.join(c for c in unicodedata.normalize('NFD', str(texto).lower())
                   if unicodedata.category(c) != 'Mn')

# Carregando os dados
@st.cache_data
def carregar_dados():
    df = pd.read_excel('consulta_medicamento999.xlsx')
    df['Princípio Normalizado'] = df['Princípio Ativo ou Descrição do Medicamento Notificado'].apply(normalizar)
    df['Nome Produto Normalizado'] = df['Nome do Produto'].apply(normalizar)
    return df

df = carregar_dados()

st.markdown("<h1 style='display: inline;'>🔎 Consulta de Medicamentos</h1>", unsafe_allow_html=True)

busca = st.text_input("Digite o nome do medicamento ou princípio ativo:")

if busca:
    busca_norm = normalizar(busca)
    resultado = df[(df['Situação da Regularização'] == 'Ativo') &
                   (
                    df['Princípio Normalizado'].str.contains(busca_norm) |
                    df['Nome Produto Normalizado'].str.contains(busca_norm)
                   )]
    
    if not resultado.empty:
        st.success(f"Foram encontrados {len(resultado)} resultados:")
        st.dataframe(resultado[['Nome do Produto',
                                 'Princípio Ativo ou Descrição do Medicamento Notificado',
                                 'Tipo de Regularização',
                                 'Empresa Detentora da Regularização']]
                                 .reset_index(drop=True))
    else:
        st.warning("Nenhum medicamento encontrado para essa busca.")
else:
    st.info("Digite um nome para buscar medicamentos ativos na ANVISA.")
