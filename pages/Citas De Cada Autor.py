import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd

st.set_page_config(
    page_title="Citaciones de Cada Autor",
    page_icon="📄"
)

def get_min_max_years(df: pd.DataFrame) -> tuple[int, int]:
    """
    Returns a tuple with the min and max years found in the df.
    """
    years_columns = [col for col in df.columns if col.isdigit()]
    if years_columns:
        min_year = int(min(years_columns))
        max_year = int(max(years_columns))
    return (min_year, max_year)


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a slim version of the full df. 
    Only Title, Average per Year, all years, and Total Citations
    """
    # Delete <i> tags from titles
    df['Title'] = df['Title'].str.replace('<i>', '').str.replace('</i>', '')

    # Get columns from 2000 to 2023
    # years_to_keep = [str(year) for year in range(2000, 2024)]

    new_df = pd.DataFrame()
    new_df["Titulos de publicaciones"] = df[['Title']]
    for year in [year for year in df.columns if year.isdigit()]:
      if year in df.columns:
        new_df[year] = df[year]
    new_df['Promedio por Año'] = df['Average per Year']
    new_df['Total de Citas'] = df['Total Citations']
    return new_df


def build_plot(df: pd.DataFrame, anio_inicio: int, anio_fin: int) -> Figure:
    """
    Plots the publications per year based on the range anio_inicio and anio_fin.
    """

    # Filtrar las columnas de años
    years = [str(year) for year in range(anio_inicio, anio_fin + 1)]

   # Initialize a DataFrame to hold publications and citations for each year
    publications = pd.Series(0, index=years, dtype='int64')
    citations_per_year = pd.Series(0, index=years, dtype='float64')

    # Populate the publications and citations for the years present in the DataFrame
    for year in years:
        if year in df.columns:
            publications[year] = df[year].sum()
            # Adjust as needed
            citations_per_year[year] = df.loc[df[year].notnull(
            ), 'Average per Year'].mean()

    # Crear la gráfica
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Graficar el número de publicaciones como barras
    ax1.bar(publications.index, publications.values,
            color='purple', alpha=0.5, label='Publications')
    ax1.set_xlabel('Year')
    plt.xticks(rotation=90)
    ax1.set_ylabel('Publications', color='purple')
    ax1.tick_params(axis='y', labelcolor='purple')
    

    # Crear otro eje Y para las citas
    #ax2 = ax1.twinx()
    #ax2.plot(citations_per_year.index, citations_per_year.values,
    #         color='blue', label='Citations per Year', linewidth=2)
    #ax2.set_ylabel('Citations per Year', color='blue')
    #ax2.tick_params(axis='y', labelcolor='blue')

    # Título y leyenda
    plt.title('Times Cited and Publications Over Time')
    fig.legend(loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=2)
    return fig


#---------------------------------------------------------------------------------------
# START PAGE CONSTRUCTION
st.header("Citaciones De Cada Autor")

# Pick a researcher
option = st.selectbox(
    "Selecciona un investigador: ",
    st.session_state["dataframes"].keys(),
    index=200
)

# Get dataframe of selected option
current_df = st.session_state['dataframes'][option]
years_in_df = [int(year) for year in current_df.columns if year.isdigit()]
min_year = min(years_in_df)-1
max_year = max(years_in_df)

# Show dataframe table
st.dataframe(clean_df(current_df))

# Select range of plot
anio_inicio, anio_fin = st.select_slider(
    'Select the range of years:',
    options=range(min_year, max_year + 1),
    value=(min_year, max_year)  # Default range
)

# Show plot
st.pyplot(build_plot(current_df, anio_inicio, anio_fin))
