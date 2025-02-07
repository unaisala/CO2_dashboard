import pandas as pd
from dash import dcc, html, callback, Output, Input, register_page
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px

# Cargar datos
archivo_excel = pd.ExcelFile('CO2.xlsx')
data_hoja1 = pd.read_excel('CO2.xlsx', sheet_name='fossil_CO2_totals_by_country')

# Reestructurar los datos para facilitar la visualización por año
data_h1 = data_hoja1.melt(
    id_vars=['ISOcode', 'Country'],  # Columnas fijas
    var_name='Year',                 # Nueva columna con los años
    value_name='CO2 Emissions'       # Nueva columna con las emisiones
)

# Convertir años a enteros
data_h1['Year'] = data_h1['Year'].astype(int)

# Obtener los años disponibles
years = sorted(data_h1['Year'].unique(), reverse=True)

register_page(__name__, path="/emisiones-year")  # Registrar la página

# Layout de la página
layout = dbc.Container([
    html.H2("🌍 CO₂ Emissions by Year", className="text-center mt-4"),
    
    dbc.Row([
        dbc.Col([
            html.Label("Select a year:", className="fw-bold"),
            dcc.Dropdown(
                id='dropdown-year3',
                options=[{'label': str(year), 'value': year} for year in years],
                value=years[0],  # Seleccionar el año más reciente por defecto
                clearable=False
            ),
        ], width=3, style={"margin-bottom": "20px"}),  # Espaciado inferior

        dbc.Col([
            dcc.Graph(id='graph-world-map3')
        ], width=9),
    ], className="mt-3"),
], fluid=True)


@callback(
    Output('graph-world-map3', 'figure'),
    [Input('dropdown-year3', 'value')]
)
def update_world_map(selected_year):
    # Filtrar datos para el año seleccionado
    df_year = data_h1[data_h1['Year'] == selected_year]

    fig = go.Figure(data=go.Choropleth(
        locations=df_year['ISOcode'],
        locationmode='ISO-3',
        z=df_year['CO2 Emissions'],
        text=df_year['Country'] + ": " + df_year['CO2 Emissions'].astype(str) + " Mt",
        colorscale=list(reversed(px.colors.sequential.Inferno)),
        colorbar=dict(title="CO₂ Emissions (Mt)")
    ))

    # 🌍 **Configuración de la proyección en 3D**
    fig.update_geos(
        projection_type="orthographic",  # Globo terráqueo en 3D
        showland=True, landcolor="rgb(240, 240, 240)",  # Color de la tierra
        showocean=True, oceancolor="rgb(200, 220, 250)",  # Color del océano
        showframe=False,
        showcoastlines=True,
        coastlinecolor="rgb(50, 50, 50)"
    )

    # Configuración del diseño
    fig.update_layout(
        title=f'CO₂ Emissions by Country in {selected_year}',
        height=650,
        margin={"r":0, "t":40, "l":0, "b":0}
    )

    return fig