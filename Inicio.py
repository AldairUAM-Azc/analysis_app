import streamlit as st
import pandas as pd
import math
from pathlib import Path
import os

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Analisis Investigadores',
    page_icon='👩‍🔬', 
)

# ---------------------------------------------------------------------------
# Load the data

folder_path = './datos_completos'

def compute_dataframes(folder_path: str) -> dict:
    txt_files = []
    for filename in os.listdir(folder_path):
        txt_files.append(filename)
    txt_files.sort()

    dataframes = {}
    for file in txt_files:
        df = pd.read_csv(f"{folder_path}/{file}")

        # Delete <i> tags from titles
        df['Title'] = df['Title'].str.replace('<i>', '').str.replace('</i>', '')

        # Get columns from 2000 to 2023
        years_to_keep = [str(year) for year in range(2000, 2024)]

        # columns_to_keep = ['Title', 'Average per Year', 'Total Citations'] + years_to_keep
        new_df = pd.DataFrame()
        new_df["Titulos de publicaciones"] = df[['Title']]
        for year in years_to_keep:
            if year in df.columns:
                new_df[year] = df[year]
        new_df['Promedio por Año'] = df['Average per Year']
        new_df['Total de Citas'] = df['Total Citations']
        author = file.split('.')[0]
        dataframes[author] = new_df
    return dataframes    

# Compute researches dataframes in case they dont exist yet
if 'dataframes' not in st.session_state:
    # Compute your DataFrames here
    st.session_state["dataframes"] = compute_dataframes(folder_path)
    

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# 👩‍🔬 Analisis Investigadores 


Tomamos datos de las citas y publicaciones de algunos investigadores del portal [WebOfScience](https://webofscience.uam.elogim.com/wos/woscc/citation-report/3f8ad5bf-9246-4248-9bf4-df6a92255f89-010a8b6d63).
'''

# Add some spacing
''
''

# min_value = gdp_df['Year'].min()
# max_value = gdp_df['Year'].max()

# from_year, to_year = st.slider(
#     'Which years are you interested in?',
#     min_value=min_value,
#     max_value=max_value,
#     value=[min_value, max_value])

# countries = gdp_df['Country Code'].unique()

# if not len(countries):
#     st.warning("Select at least one country")

# selected_countries = st.multiselect(
#     'Which countries would you like to view?',
#     countries,
#     ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'])

# ''
# ''
# ''

# # Filter the data
# filtered_gdp_df = gdp_df[
#     (gdp_df['Country Code'].isin(selected_countries))
#     & (gdp_df['Year'] <= to_year)
#     & (from_year <= gdp_df['Year'])
# ]
# 
# st.header('GDP over time', divider='gray')
# 
# ''
# 
# st.line_chart(
#     filtered_gdp_df,
#     x='Year',
#     y='GDP',
#     color='Country Code',
# )

# ''
# ''


# first_year = gdp_df[gdp_df['Year'] == from_year]
# last_year = gdp_df[gdp_df['Year'] == to_year]

# st.header(f'GDP in {to_year}', divider='gray')

# ''

# cols = st.columns(4)

# for i, country in enumerate(selected_countries):
#     col = cols[i % len(cols)]

#     with col:
#         first_gdp = first_year[first_year['Country Code']
#                                == country]['GDP'].iat[0] / 1000000000
#         last_gdp = last_year[last_year['Country Code']
#                              == country]['GDP'].iat[0] / 1000000000

#         if math.isnan(first_gdp):
#             growth = 'n/a'
#             delta_color = 'off'
#         else:
#             growth = f'{last_gdp / first_gdp:,.2f}x'
#             delta_color = 'normal'

#         st.metric(
#             label=f'{country} GDP',
#             value=f'{last_gdp:,.0f}B',
#             delta=growth,
#             delta_color=delta_color
# )
