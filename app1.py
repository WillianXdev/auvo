import streamlit as st
import pandas as pd

# Carregar os dados
file_equipamentos = "equipamentos_31_03_2025.xlsx"
file_respostas = "Respostas_#_STS36693_22_SEDUC_-_Preventiva_Mensal_-_B2G_01_03_2025_a_31_03_2025 (1).xls"

df_equipamentos = pd.read_excel(file_equipamentos, sheet_name="equipamentos_31 03 2025")
df_respostas = pd.read_excel(file_respostas, sheet_name="Respostas # STS36693 22 SEDUC -")

# Normalizar os identificadores
df_equipamentos["Identificador"] = df_equipamentos["Identificador"].astype(str).str.strip()
df_respostas["Identificador"] = df_respostas["Identificador"].astype(str).str.strip()

# Unir os dataframes
merged_df = pd.merge(df_respostas, df_equipamentos, on="Identificador", suffixes=("_resposta", "_equipamento"))

# Agrupar por colaborador
colaboradores = merged_df["Colaborador_resposta"].dropna().unique()
st.title("Equipamentos e Respostas por Colaborador")

colaborador_escolhido = st.selectbox("Selecione o colaborador:", sorted(colaboradores))

if colaborador_escolhido:
    col_df = merged_df[merged_df["Colaborador_resposta"] == colaborador_escolhido]
    clientes = col_df["Cliente_resposta"].unique()

    for cliente in clientes:
        with st.expander(f"{cliente}"):
            cliente_df = col_df[col_df["Cliente_resposta"] == cliente]
            equipamentos = cliente_df["Equipamento"].unique()

            equipamento_escolhido = st.selectbox(f"Equipamentos para {cliente}", equipamentos, key=f"{cliente}")

            dados_equipamento = cliente_df[cliente_df["Equipamento"] == equipamento_escolhido]
            st.write("### Informações do Equipamento")
            st.dataframe(dados_equipamento[[
                "Identificador", "Data da tarefa", "Hora resposta", "CUMPRIMENTO DOS ITENS MENCIONADOS",
                "CORRENTE (AFERIÇÃO MENSAL)", "TENSÃO (AFERIÇÃO MENSAL)", "Descrição"
            ]].drop_duplicates())

            st.write("### Fotos")
            for coluna in dados_equipamento.columns:
                if not dados_equipamento[coluna].empty:
                    valor = dados_equipamento[coluna].iloc[0]
                    if isinstance(valor, str) and valor.startswith("http"):
                        st.image(valor, caption=coluna, use_column_width=True)
