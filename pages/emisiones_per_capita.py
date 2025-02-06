import pandas as pd
import plotly.express as px
from dash import dcc, html, register_page

register_page(__name__, path="/emisiones-per-capita")  # Registrar la página

# Cargar datos
file_path = "CO2.xlsx"
data_per_capita = pd.read_excel(file_path, sheet_name="fossil_CO2_per_capita_by_countr")

# Transformar datos
data_per_capita = data_per_capita.melt(id_vars=["ISOcode", "Country"], var_name="Year", value_name="CO2 Emissions per Capita")
data_per_capita["Year"] = data_per_capita["Year"].astype(int)

# Crear gráfico
fig_per_capita = px.line(
    data_per_capita, x="Year", y="CO2 Emissions per Capita", color="Country",
    title="Emisiones de CO₂ per Cápita por País"
)

layout = html.Div([
    html.H2("Emisiones de CO₂ per Cápita", className="text-center"),
    dcc.Graph(figure=fig_per_capita)
])
