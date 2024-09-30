import streamlit as st
import pandas as pd
import os

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Analisis Investigadores',
    page_icon='👩‍🔬',
)

# ---------------------------------------------------------------------------
# Load citation dataframes

folder_path = './datos_completos'


def compute_dataframes(folder_path: str) -> dict:
    txt_files = []
    for filename in os.listdir(folder_path):
        txt_files.append(filename)
    txt_files.sort()

    dataframes = {}
    for file in txt_files:
        df = pd.read_csv(f"{folder_path}/{file}")
        author = file.split('.')[0]
        dataframes[author] = df
    return dataframes


# Compute researches dataframes in case they dont exist yet
if 'dataframes' not in st.session_state:
    st.session_state["dataframes"] = compute_dataframes(folder_path)


# -----------------------------------------------------------------------------------
# Load patents dataframes
patentes_path = './patentes.csv'
df = pd.read_csv(patentes_path)
df = df.sort_values(by="Inventor")

if 'dataframe_patentes' not in st.session_state:
    st.session_state['dataframe_patentes'] = df

# -----------------------------------------------------------------------------------
# Cargar solamente la informacion de las citas de los investigadores que tienen patentes

inventors = st.session_state['dataframe_patentes'].Inventor.unique()

if 'dataframes_analisis_patentes' not in st.session_state:
    dataset_dict = {}
    for inventor in inventors:
        if inventor in st.session_state['dataframes']:
            dataset_dict[inventor] = st.session_state['dataframes'][inventor]
    st.session_state['dataframes_analisis_patentes'] = dataset_dict

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# 👩‍🔬 Analisis Investigadores 


Tomamos datos de las citas y publicaciones de algunos investigadores del portal [WebOfScience](https://webofscience.uam.elogim.com/wos/woscc/citation-report/3f8ad5bf-9246-4248-9bf4-df6a92255f89-010a8b6d63).
'''
