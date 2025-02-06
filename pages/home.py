import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Registrar la página como "homepage"
dash.register_page(__name__, path="/", name="Inicio")

# Cargar datos
file_path = "CO2.xlsx"
data_hoja2 = pd.read_excel(file_path, sheet_name="fossil_CO2_totals_by_country")

# Obtener el último año disponible
latest_year = data_hoja2.columns[-1]
print(f"Año más reciente: {latest_year}")

# Filtrar y ordenar los países según sus emisiones en el año más reciente
data_hoja2_sorted = data_hoja2[['Country', latest_year]].dropna().sort_values(by=latest_year, ascending=False).reset_index(drop=True)

# Obtener los 10 países con más emisiones
top_10_countries = data_hoja2_sorted.head(10)

# Redondear las emisiones a dos decimales (manteniéndolas en megatoneladas)
top_10_countries[latest_year] = top_10_countries[latest_year].round(2)

# Calcular el total de emisiones globales
total_emissions = data_hoja2[latest_year].sum()

# **Crear gráfico de pastel (Pie Chart) para los 5 países más contaminantes vs. el resto del mundo**
# Obtener los 5 países más contaminantes
top_5_countries = top_10_countries.head(5)

# Calcular el total de emisiones de los 5 países más contaminantes
total_top_5 = top_5_countries[latest_year].sum()

# Calcular el total de emisiones del resto del mundo
resto_mundo = total_emissions - total_top_5

# Datos para el gráfico de pastel
pie_data = pd.concat([ 
    top_5_countries[['Country', latest_year]].assign(Category='Top 5 Países'),
    pd.DataFrame({'Country': ['Resto del Mundo'], 'Category': ['Resto del Mundo'], latest_year: [resto_mundo]})
])

# Crear gráfico de pie (Pie Chart)
fig_pie = px.pie(
    pie_data,
    names='Country',
    values=latest_year,
    title=f"Porcentaje de Emisiones: Top 5 Países vs. Resto del Mundo ({latest_year})",
    labels={latest_year: 'Emisiones (Mt CO₂)'},
    hole=0.3,  # Esto crea un gráfico de "donut" (dona)
)

# Separar solo "Resto del Mundo" visualmente con una mínima separación
fig_pie.update_traces(pull=[0, 0, 0, 0, 0, 0.1])  # Los 5 países no tienen separación, solo el "Resto del Mundo" tiene una pequeña separación

# Layout de la página principal
layout = dbc.Container([
    html.H2(f"🌍 Countries with major CO₂ impact in {latest_year}", className="text-center mt-4"),
    
    dbc.Row([
        # Columna para la tabla
        dbc.Col([ 
            html.P(f"Ranking of CO₂ emissions in {latest_year} (units in Megatons).", 
                   className="text-center"),
            dash_table.DataTable(
                id="co2-ranking",
                columns=[{"name": str(col), "id": str(col)} for col in top_10_countries.columns],  # Aseguramos que los nombres son strings
                data=top_10_countries.to_dict("records"),
                style_table={"overflowX": "auto"},
                style_header={"backgroundColor": "#255db8", "color": "white", "fontWeight": "bold"},
                style_data={"backgroundColor": "white", "color": "black"},
                style_cell={"textAlign": "center", "padding": "10px"},
            )
        ], width=6),  # Coloca la tabla en el 50% de la pantalla
        
        # Columna para el gráfico de pie
        dbc.Col([ 
            html.P(f"Porcentaje de emisiones: Top 5 Países vs. Resto del Mundo en {latest_year} (en Megatoneladas)", className="text-center"),
            dcc.Graph(
                id="co2-pie-chart",
                figure=fig_pie
            )
        ], width=6),  # Coloca el gráfico en el 50% de la pantalla
    ], className="mt-4"),
], fluid=True)
