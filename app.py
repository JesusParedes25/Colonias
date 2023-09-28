import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
import gdown
# Cargar los archivos CSV en DataFrames
# URLs de los archivos CSV en Google Drive
url_colonias = "https://drive.google.com/uc?id=17YNIyLvX0Qgje8wL9NVgNzRPgJLqD5lK"
url_llamadas = "https://drive.google.com/uc?id=1Y7kwkgkdoAFSnNEugHxCAAiu2qxBI_4v"

# Descargar los archivos CSV desde Google Drive
gdown.download(url_colonias, "colonias_sigeh.csv", quiet=False)
gdown.download(url_llamadas, "llamadas_por_colonia.csv", quiet=False)

# Cargar los archivos CSV en DataFrames
df_colonias = pd.read_csv("colonias_sigeh.csv")
llamadas_por_colonia_df = pd.read_csv("llamadas_por_colonia.csv")
# ... (Código para procesar los datos y crear los widgets)

# Crear la aplicación Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Visualización de Llamadas de Seguridad Pública"),
    html.Label("Selecciona un Municipio:"),
    dcc.Dropdown(
        id='municipio-dropdown',
        options=[{'label': municipio, 'value': municipio} for municipio in llamadas_por_colonia_df['MUNICIPIO'].unique()],
        value=llamadas_por_colonia_df['MUNICIPIO'].unique()[0]
    ),
    html.Label("Selecciona una Colonia:"),
    dcc.Dropdown(id='colonia-dropdown'),
    dcc.Graph(id='llamadas-grafico')
])

# Función para actualizar las opciones de colonia según el municipio seleccionado
@app.callback(
    Output('colonia-dropdown', 'options'),
    [Input('municipio-dropdown', 'value')]
)
def actualizar_colonias(municipio):
    colonias = llamadas_por_colonia_df[llamadas_por_colonia_df['MUNICIPIO'] == municipio]['COLONIAS.x'].unique()
    return [{'label': colonia, 'value': colonia} for colonia in colonias]

# Función para mostrar el gráfico de las 10 llamadas más comunes para la colonia seleccionada
@app.callback(
    Output('llamadas-grafico', 'figure'),
    [Input('colonia-dropdown', 'value'),
     Input('municipio-dropdown', 'value')]
)
def mostrar_grafico(colonia, municipio):
    llamadas_comunes = llamadas_por_colonia_df[
        (llamadas_por_colonia_df['MUNICIPIO'] == municipio) &
        (llamadas_por_colonia_df['COLONIAS.x'] == colonia)
    ]
    llamadas_comunes = llamadas_comunes.iloc[:, 4:].sum().nlargest(10)
    fig = {
        'data': [
            {'x': llamadas_comunes.index, 'y': llamadas_comunes.values, 'type': 'bar'}
        ],
        'layout': {
            'title': f'Top 10 Llamadas más Comunes en {colonia}, {municipio}',
            'xaxis': {'title': 'Tipo de Llamada'},
            'yaxis': {'title': 'Número de Llamadas'},
            'height': 600
        }
    }
    return fig