import pandas as pd
import streamlit as st
from io import BytesIO

# Função para carregar dados da planilha CSV
@st.cache_data
def load_data(file):
    df = pd.read_csv(file, on_bad_lines='skip', delimiter=';')
    return df

# Limpar nomes das colunas
def clean_column_names(df):
    df.columns = df.columns.str.replace(' ', '_').str.replace('"', '').str.replace(';', '')
    return df

# Título do dashboard
st.title('Dashboard de Dados da Planilha CSV')

# Upload da planilha CSV
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    # Carregar os dados
    df = load_data(uploaded_file)
    df = clean_column_names(df)

    # Mostrar a planilha carregada
    st.header('Dados da Planilha')
    st.dataframe(df)

  

    # Filtro por coluna "Matrícula"
    st.sidebar.header('Filtro por Matrícula')
    if 'Matrícula' in df.columns:
        matricula = st.sidebar.selectbox('Selecione a Matrícula', df['Matrícula'].unique())
        df_filtrado = df[df['Matrícula'] == matricula]
        st.sidebar.dataframe(df_filtrado)
    else:
        st.write('A coluna "Matrícula" não está presente no dataset.')

    # Função para converter dataframe em Excel
    def convert_df_to_excel(df):
        excel_file = BytesIO()
        with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
            # Write only selected columns to Excel
            df[['Unidade_de_Negócio_-_Nome', 'Matrícula', 'Nro_Medidor_Antigo', 'Endereço']].to_excel(writer, index=False)
        excel_file.seek(0)
        return excel_file.getvalue()

    # Botão para exportar planilha
    excel_data = convert_df_to_excel(df)
    st.sidebar.download_button(
        label="Exportar Planilha para Excel",
        data=excel_data,
        file_name='planilha_exportada.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
