import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# Crear la app con soporte multipágina
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH], use_pages=True)

# Estilos personalizados para un efecto moderno
NAVBAR_STYLE = {
    "position": "sticky",
    "top": "0",
    "width": "100%",
    "zIndex": "1000",
    "background": "rgba(37, 93, 184, 0.8)",  # Azul con transparencia
    "backdropFilter": "blur(10px)",  # Efecto glassmorphism
    "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.2)",  # Sombra suave
    "padding": "10px 20px",
}

NAV_LINK_STYLE = {
    "color": "white",
    "padding": "10px 15px",
    "borderRadius": "8px",
    "transition": "0.3s",
    "fontSize": "18px",
    "fontWeight": "bold",
    "textDecoration": "none",
}

NAV_LINK_HOVER = {
    "backgroundColor": "rgba(255, 255, 255, 0.2)",  # Efecto hover transparente
}

# Navbar con efecto Glassmorphism
navbar = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H3("🏭 CO₂ emissions around the world", style={"color": "white"}), width="auto"),
            dbc.Col(
                dbc.Nav([
                    dcc.Link("Home", href="/", style=NAV_LINK_STYLE, className="nav-item"),
                    dcc.Link("Country Emissions", href="/emisiones-totales", style=NAV_LINK_STYLE, className="nav-item"),
                    dcc.Link("Year Emissions", href="/emisiones-year", style=NAV_LINK_STYLE, className="nav-item"),
                ], className="d-flex gap-3 justify-content-end"),
                width=True
            )
        ], align="center")
    ], fluid=True)
], style=NAVBAR_STYLE)

# Layout principal con navbar mejorado
app.layout = dbc.Container([
    navbar,
    html.Br(),
    dash.page_container  # Aquí se renderizan las páginas
], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)
