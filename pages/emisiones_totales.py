import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash_iconify import DashIconify

# Cargar datos
file_path = "CO2.xlsx"
xls = pd.ExcelFile(file_path)
data_totals = xls.parse('fossil_CO2_totals_by_country')
data_per_capita = xls.parse('fossil_CO2_per_capita_by_countr')

# Normalizar nombres de columnas
data_totals.columns = data_totals.columns.str.strip()
data_per_capita.columns = data_per_capita.columns.str.strip()

# Lista de países
countries = data_totals['Country'].dropna().unique()
dropdown_options_countries = [{'label': country, 'value': country} for country in countries]

# Crear la página de emisiones totales
dash.register_page(__name__, path="/emisiones-totales", name="Emisiones Totales")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([  # Columna izquierda para selección y datos generales
            dbc.Card([
                dbc.CardBody([
                    html.H4("Seleccione un país", className='card-title'),
                    dcc.Dropdown(id='country-selector', options=dropdown_options_countries, value=countries[0],
                                 placeholder='Seleccione un país')
                ], style={'background-color': 'white', 'border-radius': '4px'})
            ], className='mb-4'),
            
            dbc.Card([
                dbc.CardBody([
                    html.H5("Cambio porcentual desde 2015", className='card-title text-center'),
                    html.Div(
                        id='percentage-change', 
                        style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'height': '85px'}
                    )
                ], style={'background-color': 'white', 'border-radius': '4px'})
            ], className='mb-4'),
            
            dbc.Card([
                dbc.CardBody([
                    html.H5("Ranking de consumo per cápita", className='card-title text-center'),
                    html.Div(id='ranking-position', style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'height': '85px'})
                ], style={'background-color': 'white', 'border-radius': '4px'})
            ])
        ], width=4),
        
        dbc.Col([  # Columna derecha para el gráfico de emisiones
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='emissions-line-chart')
                ], style={'background-color': 'white', 'border-radius': '4px'})
            ])
        ], width=8)
    ])
])

# Callback para actualizar los datos del país seleccionado
@dash.callback(
    [dash.dependencies.Output('emissions-line-chart', 'figure'),
     dash.dependencies.Output('percentage-change', 'children'),
     dash.dependencies.Output('ranking-position', 'children')],
    [dash.dependencies.Input('country-selector', 'value')]
)
def update_graph_country(selected_country):

    data_hoja1 = pd.read_excel('CO2.xlsx', sheet_name='fossil_CO2_totals_by_country')
    data_h1 = data_hoja1.melt(id_vars=['ISOcode', 'Country'], var_name='Year', value_name='CO2 Emissions')

    data_hoja2 = pd.read_excel(file_path, sheet_name='fossil_CO2_per_capita_by_countr')
    latest_year = data_hoja2.columns[-1]

    # Ordenar los países según las emisiones
    data_hoja2_sorted = data_hoja2[['Country', latest_year]].dropna().sort_values(by=latest_year, ascending=False).reset_index()

    if selected_country is None:
        return {}, "Sin datos", "Sin datos"

    # Filtrar los datos del país seleccionado
    df_country = data_h1[data_h1['Country'] == selected_country]

    # Calcular el cambio porcentual desde 2015
    emissions_2015 = df_country[df_country['Year'] == 2015]['CO2 Emissions'].values
    emissions_latest = df_country.iloc[-1]['CO2 Emissions'] if not df_country.empty else None
    
    if emissions_2015.size > 0 and emissions_latest is not None:
        percentage_change = ((emissions_latest - emissions_2015[0]) / emissions_2015[0]) * 100
        percentage_text = html.Span(f"{percentage_change:.2f}%", style={'font-size': '2rem', 'font-weight': 'bold', 'margin-left': '8px'})
    else:
        percentage_text = "Insufficient data"

    # Estilo del ícono basado en el cambio porcentual
    if emissions_2015.size > 0 and emissions_latest is not None:
        if percentage_change > 0:
            icon = DashIconify(icon="mdi:arrow-up-bold", width=40, color="green")
        else:
            icon = DashIconify(icon="mdi:arrow-down-bold", width=40, color="red")
    else:
        icon = ""

    # Ranking del país seleccionado
    ranking = data_hoja2_sorted[data_hoja2_sorted['Country'] == selected_country]
    if not ranking.empty:
        rank_position = ranking.index[0] + 1  # Sumar 1 porque los índices comienzan en 0
        rank_text = html.Div([html.P(f"Puesto nº{rank_position}", style={'font-size': '2rem', 'font-weight': 'bold'})], 
                             style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'})
    else:
        rank_text = "Sin datos"

    # Crear gráfico de línea
    fig_country = px.line(
        df_country, x='Year', y='CO2 Emissions',
        title=f'Emisiones de CO₂ en {selected_country} por año',
        labels={'CO2 Emissions': 'Emisiones CO₂ (toneladas)'}
    )

    return fig_country, html.Div([icon, percentage_text], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}), rank_text
