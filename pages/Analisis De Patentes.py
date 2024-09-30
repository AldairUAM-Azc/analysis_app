import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import re 

# -------------------------------------------------------
# plot function
def plot_patente_citas(df_patentes: pd.DataFrame, df_citas: pd.DataFrame, patente: str) -> plt.figure:
    # Convert filing date to datetime
    df_patentes['Filing Date'] = pd.to_datetime(df_patentes['Filing Date'])

    # Find the row corresponding to the provided patent
    patent_row = df_patentes.loc[df_patentes['Patent'] == patente]

    # Check if the patent exists
    if patent_row.empty:
        raise ValueError(f"Patent '{patente}' not found in the DataFrame.")

    # Use the filing date of the specified patent
    first_patent_date = patent_row['Filing Date'].values[0]

    # Convert to a standard datetime object if necessary
    first_patent_date = pd.to_datetime(first_patent_date)

    # Define the year range for filtering (5 years before and after)
    start_year = first_patent_date.year - 5
    end_year = first_patent_date.year + 5

    # Get the current year to filter out future years
    current_year = datetime.now().year

    # Create a list of years to consider and filter out future years
    years = list(map(str, range(start_year, min(end_year + 1, current_year))))

    # Filter the citation columns to only include available years
    available_years = [year for year in years if year in df_citas.columns]

    # If there are no available years, create a default entry
    if not available_years:
        citation_counts = pd.DataFrame({'Year': [first_patent_date.year], 'Total Citations': [0]})
    else:
        # Sum the citations for the available years
        citation_counts = df_citas[available_years].sum().reset_index()
        citation_counts.columns = ['Year', 'Total Citations']

    # Convert Year to int for plotting
    citation_counts['Year'] = citation_counts['Year'].astype(int)

    # Create the figure for plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Check if there are any data to plot
    if not citation_counts.empty:
        ax.bar(citation_counts['Year'], citation_counts['Total Citations'], color='skyblue', label='Total Citations')

        # Adding the filing date as a vertical line
        ax.axvline(x=first_patent_date.year, color='red', linestyle='--', label='Filing Date')

        # Annotations
        ax.text(first_patent_date.year, max(citation_counts['Total Citations']) / 2, 
                'Filing Date\n' + first_patent_date.date().isoformat(), 
                color='red', ha='center')

    # Titles and labels
    ax.set_title(f'Total Citations for Publications (5 Years Before and After {first_patent_date.date()})')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Citations')
    ax.set_xticks(citation_counts['Year'])  # Set x-ticks to the years present in the data
    ax.grid(axis='y')
    ax.legend()

    # Return the figure
    return fig


# def plot_patente_citas(df_patentes: pd.DataFrame, df_citas: pd.DataFrame, patente: str) -> plt.figure:
    # Convert filing date to datetime
    df_patentes['Filing Date'] = pd.to_datetime(df_patentes['Filing Date'])

    # Let's use the first patent's filing date
    # first_patent_date = df_patentes.iloc[0]['Filing Date']

    # Find the row corresponding to the provided patent
    patent_row = df_patentes.loc[df_patentes['Patent'] == patente]

    # Check if the patent exists
    if patent_row.empty:
        raise ValueError(f"Patent '{patente}' not found in the DataFrame.")

    # Use the filing date of the specified patent
    first_patent_date = patent_row['Filing Date'].values[0]

    # Define the year range for filtering (5 years before and after)
    start_year = first_patent_date.year - 5
    end_year = first_patent_date.year + 5

    # Create a list of years to consider
    years = list(map(str, range(start_year, end_year + 1)))

    # Filter the citation columns to only include available years
    available_years = [year for year in years if year in df_citas.columns]

    # If there are no available years, create a default entry
    if not available_years:
        citation_counts = pd.DataFrame({'Year': [first_patent_date.year], 'Total Citations': [0]})
    else:
        # Sum the citations for the available years
        citation_counts = df_citas[available_years].sum().reset_index()
        citation_counts.columns = ['Year', 'Total Citations']

    # Convert Year to int for plotting
    citation_counts['Year'] = citation_counts['Year'].astype(int)

    # Create the figure for plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Check if there are any data to plot
    if not citation_counts.empty:
        ax.bar(citation_counts['Year'], citation_counts['Total Citations'], color='skyblue', label='Total Citations')

        # Adding the filing date as a vertical line
        ax.axvline(x=first_patent_date.year, color='red', linestyle='--', label='Filing Date')

        # Annotations
        ax.text(first_patent_date.year, max(citation_counts['Total Citations']) / 2, 
                'Filing Date\n' + first_patent_date.date().isoformat(), 
                color='red', ha='center')

    # Titles and labels
    ax.set_title(f'Total Citations for Publications (5 Years Before and After {first_patent_date.date()})')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Citations')
    ax.set_xticks(citation_counts['Year'])  # Set x-ticks to the years present in the data
    ax.grid(axis='y')
    ax.legend()

    # Return the figure
    return fig

#---------------------------------------------------------------------------------------
# START PAGE CONSTRUCTION
st.header("Analisis de Citas")

# Pick am imvemtor
option_inventor = st.selectbox(
    "Selecciona un inventor: ",
    st.session_state["dataframes_analisis_patentes"].keys()
)

option_patent = st.selectbox(
    "Selecciona una patente: ",
    [x + ' ' + y for x, y in zip(
        st.session_state["dataframe_patentes"][(st.session_state["dataframe_patentes"])["Inventor"] == option_inventor].Patent,
        st.session_state["dataframe_patentes"][(st.session_state["dataframe_patentes"])["Inventor"] == option_inventor]['Filing Date']
        )
    ]
)

st.pyplot(plot_patente_citas(
    st.session_state["dataframe_patentes"][(st.session_state["dataframe_patentes"])["Inventor"] == option_inventor],
    st.session_state['dataframes_analisis_patentes'][option_inventor],
    re.split(r"\s+", option_patent)[0]
))

