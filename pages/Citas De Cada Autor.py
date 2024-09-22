import streamlit as st

st.set_page_config(
    page_title="Citaciones de Cada Autor",
    page_icon="📄" 
)

st.header("Citaciones De Cada Autor")

option = st.selectbox(
    "Selecciona un investigador: ",
    st.session_state["dataframes"].keys()
)

st.dataframe(st.session_state['dataframes'][option])

st.markdown("Aqui iria una grafiquita, si tuviera una.")