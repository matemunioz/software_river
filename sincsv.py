import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import base64
import io
import plotly.express as px 
from urllib.request import urlopen
import matplotlib
matplotlib.use('Agg')  # Configurar Matplotlib para usar el backend 'Agg'
import matplotlib.pyplot as plt
from PIL import Image
from mplsoccer import PyPizza, add_image, FontManager
import requests
from PIL import Image
from io import BytesIO
from dash.exceptions import PreventUpdate





app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/styles.css', 'assets/script.js'])
app.config.suppress_callback_exceptions = True
app.title = "Club Atlético River Plate"




# Leer los datos
df = pd.read_csv("todos_los_partidos-0.csv")

# Agrupar por 'Jugador' y 'Rival' y sumar las acciones
grouped_df = df.groupby(['Jugador', 'Rival']).agg({
    'Minutos Jugados': 'first', 
    '1v1D+': 'sum', '1v1D-': 'sum', '1v1O+': 'sum', '1v1O-': 'sum',
    'A+': 'sum', 'A-': 'sum', 'Adelante': 'sum', 'Afuera': 'sum',
    'Anticipos': 'sum', 'Arco': 'sum', 'Atras': 'sum', 'B+': 'sum',
    'B-': 'sum', 'Bloqueado': 'sum', 'Bloqueos': 'sum', 'CAsistencia': 'sum',
    'CCompletos': 'sum', 'CENTROS': 'sum', 'CIncompletos': 'sum', 'Clave': 'sum',
    'D+': 'sum', 'D-': 'sum', 'DAD+': 'sum', 'DAD-': 'sum', 'DADefensivo': 'sum',
    'DAO+': 'sum', 'DAO-': 'sum', 'DAOfensivo': 'sum', 'Defensivo': 'sum',
    'Despeje': 'sum', 'Duelos 1V1': 'sum', 'Duelos Aereos': 'sum', 'E+': 'sum',
    'E-': 'sum', 'Entradas': 'sum', 'Faltas Hechas': 'sum', 'Faltas Recibidas': 'sum',
    'Filtrado': 'sum', 'Gol': 'sum', 'I+': 'sum', 'I-': 'sum', 'Intercepciones': 'sum',
    'Intervencion Defensiva': 'sum', 'Largo Completo': 'sum', 'Largo Incompleto': 'sum',
    'Lateral': 'sum', 'NEGATIVO': 'sum', 'Ofensivo': 'sum',
    'PASES': 'sum', 'PCompletos': 'sum', 'PERDIDAS: xControl': 'sum', 
    'PERDIDAS: xGambeta': 'sum', 'PERDIDAS: xPase': 'sum', 'PIncompletos': 'sum',
    'POSITIVO': 'sum', 'Pie Inhabil': 'sum', 'R+': 'sum', 'R-': 'sum', 
    'RECUPERACION xIntervencion': 'sum', 'RECUPERACION xPosicional': 'sum',
    'Recepcion a espaldas del volante': 'sum', 'Recepcion al espacio': 'sum',
    'Recepcion entre Lineas': 'sum', 'Regates': 'sum', 'Ruptura en conduccion': 'sum',
    'Tactico': 'sum', 'Tiros': 'sum', 'Toques en Area Rival': 'sum'
}).reset_index()







app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/styles.css', 'assets/script.js'],
    assets_folder='assets',
    title="Club Atlético River Plate",
    update_title=None,
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

app.layout = html.Div(
    children=[
        html.Div(
            className='header',
            children=[
                html.A(
                    html.Img(src='assets/Branding/Escudo.png', className='logo'),
                    href='/'
                ),
                dcc.Tabs(
                    id='tabs',
                    value='individual',
                    children=[
                        dcc.Tab(
                            label='INDIVIDUAL',
                            value='individual',
                            className='tab-individual',
                            selected_className='tab-individual-selected',
                        ),                
                    ]
                ),
            ]
        ),
        html.Div(id='tabs-content')
    ]
)


# CONTENIDO INDIVIDUAL
contenido_individual = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='dropdown-division',
                options=[{'label': division, 'value': division} for division in df['División'].unique()],
                placeholder="Selecciona una división",
                className='dropdown',
                value='Cuarta'
            )
        ], style={'display': 'inline-block', 'width': '30%', 'margin': '10px'}),
        html.Div([
            dcc.Dropdown(
                id='dropdown-jugador',
                placeholder="Selecciona un jugador",
                className='dropdown'
            )
        ], style={'display': 'inline-block', 'width': '30%', 'margin': '10px'}),
        html.Div([
            dcc.Dropdown(
                id='dropdown-partidos',
                placeholder="Selecciona un partido",
                className='dropdown',
                multi=True,
                value=df['Rival'].unique()  # Todos los partidos seleccionados por defecto
            )
        ], style={'display': 'inline-block', 'width': '30%', 'margin': '10px'}),
    ], className='dropdown-container'),
    dcc.Store(id='store-filtro'),
    html.Div([
        html.Div([
            html.Div(id='player-image-container'),
            html.Div(id='player-name', className='player-name'),
            html.Div([
                html.Div([
                    html.Img(src='assets/Logos/cancha.png', className='imagen-cancha'),
                    html.Div(id='player-position', className='player-position'),
                    html.Img(src='assets/Logos/calendario.png', className='imagen-calendario'),
                    html.Div(id='player-fecha', className='player-fecha'),
                ], className='informacion-personal-container'),
                html.Div([
                    html.Img(src='assets/Logos/botin.png', className='imagen-botin'),
                    html.Div(id='player-pie', className='player-pie'),
                    html.Div([
                        html.Img(src='assets/Logos/Partidos_jugados.png', className='imagen-pj'),
                        html.Div(id='player-pj', className='player-pj'),
                    ], className='pj-container'),  # Nuevo contenedor para la imagen y el texto
                ], className='informacion-subjetiva-container'),
                html.Div([
                    html.Div([
                    html.Img(src='assets/Logos/asistencias.png', className='imagen-asistencias'),
                    html.Div(id='player-asistencias', className='player-asistencias'),
                    html.Img(src='assets/Logos/goles.png', className='imagen-goles'),
                    html.Div(id='player-goles', className='player-goles'),                    
                    ], className='pj-container'),  # Nuevo contenedor para la imagen y el texto
                ], className='informacion-subjetiva-container'),
            ], style={'height': '50px', 'width': '500px'})
        ], className='carta-jugador-container'),
        html.Div(id='radar-chart-container', className='radar-chart-container')
    ], className='perfil-container'),
    html.Div([
        html.H1('OFENSIVO', className='texto-seccion'),
        html.Div(className='linea')
    ], style={'margin-top': '10px',}),
    html.Div([
        html.Div([
            html.Button('Posición', id='button-posicion', n_clicks=0, className='button'),
            html.Button('División', id='button-division', n_clicks=0, className='button')
        ], style={'display': 'inline-block', 'justify-content': 'center', 'width': '100%', 'margin-left': '585px', 'margin-top': '40px'}),
    ], className='dropdown-container'),
    html.Div([
        html.Div([
            html.H1('DUELOS AEREOS GANADOS', className='titulo-barras-aereos-of'),
            html.Div(id='barras-duelos-aereos', className='grafico-barras-aereos-of'),
        ], style={'display': 'inline-block', 'justify-content': 'center', 'width': '30%'}),
        html.Div([
            html.H1('DUELOS 1V1 GANADOS', className='titulo-barras-1v1'),
            html.Div(id='barras-1v1-ofensivo', className='grafico-barras-1v1'),
        ], style={'display': 'inline-block', 'justify-content': 'center', 'width': '30%'}),
        html.Div([
            html.H1('PASES FILTRADOS', className='titulo-barras-pases'),
            html.Div(id='barras-indice-tactico', className='grafico-barras-indice-tactico'),
        ], style={'display': 'inline-block',  'justify-content': 'center', 'width': '30%'}),        
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-left': '-15px'}),
    html.Div([
        html.Div([
            html.H1('TIROS AL ARCO', className='titulo-barras-tiros-arco'),
            html.Div(id='barras-tiros-arco', className='grafico-barras-aereos-of'),
        ], style={'display': 'inline-block', 'justify-content': 'center', 'width': '30%'}),
        html.Div([
            html.H1('REGATES EFECTIVOS', className='titulo-barras-regates'),
            html.Div(id='barras-regates-ofensivo', className='grafico-barras-regates'),
        ], style={'display': 'inline-block', 'justify-content': 'center', 'width': '30%'}),
        html.Div([
            html.H1('PASES CLAVE', className='titulo-barras-pases'),
            html.Div(id='barras-pases-clave', className='grafico-barras-pases'),
        ], style={'display': 'inline-block',  'justify-content': 'center', 'width': '30%'}),        
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-left': '-15px'}),
    html.Div([
        dcc.Dropdown(
            id='dropdown-scatter-plot',
            options=[
                {'label': 'ASPECTOS GENERALES', 'value': '', 'disabled': True},##################################### QUE SEAN DESPLEGABLES
                {'label': 'Duelos Aéreos', 'value': 'duelos_aereos'},
                {'label': 'Duelos 1v1', 'value': 'duelos_1v1'},
                {'label': 'Tiros', 'value': 'tiros'},
                {'label': 'Regates', 'value': 'regates'},
                {'label': 'Pases', 'value': 'pases'},
                {'label': 'Pases largos', 'value': 'pases_largos'},
                {'label': 'ASPECTOS POSITIVOS', 'value': '', 'disabled': True},##################################### QUE SEAN DESPLEGABLES
                {'label': 'Peligro Esperado', 'value': 'peligro_esperado'},
                {'label': 'Peligro en 3/4', 'value': 'peligro_tate'},
                {'label': 'ASPECTOS NEGATIVOS', 'value': '', 'disabled': True},##################################### QUE SEAN DESPLEGABLES
                {'label': 'Exceso Gambeta', 'value': 'exceso_gambeta'},
                {'label': 'Perdidas', 'value': 'perdidas'},
            ],
            placeholder="Selecciona un filtro",
            className='dropdown',
            value='duelos_aereos',
        ),
    ], style={'width': '15%', 'margin-left': '70px', 'margin-top': '100px',}),
    html.Div([
        html.Div([
            dcc.Loading(
                id="loading-1",
                type="circle",
                color="red",
                children=html.Div([
                        dcc.Graph(
                            id='scatter-plot',
                            config={
                                'modeBarButtonsToRemove': [
                                    'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'
                                ],
                                'displaylogo': False  # Remove the "produced by Plotly" logo
                            }
                        )
                ])
            )
        ], style={'display': 'inline-block', 'width': '50%', 'margin-left': '40px', 'margin-top': '20px'}),        
        html.Div([
            html.H1(id='titulo-dropdown', className='titulo-dropdown'),
            html.Div([
                html.Div(id='effectiveness', className='datos1'),
                html.Div(id='x-start-value', className='datos2'),
                html.Div(id='y-start-value', className='datos3'),
                dcc.Store(id='store-x-stat-value'),
                dcc.Store(id='store-y-stat-value'),
            ], style={'display': 'flex', 'justify-content': 'center', 'margin-left': '120px'}),
            html.Div([
                html.Div("EFECTIVIDAD", className='texto-cuadrado'),
                html.Div(id='texto-eje-x', className='texto-cuadrado'),
                dcc.Store(id='store-x-axis-title'),
                html.Div(id='texto-eje-y', className='texto-cuadrado'),
                dcc.Store(id='store-y-axis-title'),                
            ], style={'display': 'flex', 'justify-content': 'center', 'margin-left': '-50px'}),
            dcc.Graph(id='bar-chart', config={'displayModeBar': False})
        ], style={'display': 'inline-block', 'width': '43%', 'background-color': '#ED192D', 'height': '500px', 'margin-left': '40px', 'margin-top': '20px'}), 
    ], style={'display': 'flex'}),
    html.Div([
        dcc.Loading(
            id="loading-1",
            type="circle",
            color="red",
            children=html.Div([
                dcc.Graph(
                    id='horizontal-bar-chart',
                    config={
                        'modeBarButtonsToRemove': [
                            'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'
                        ],
                        'displaylogo': False  # Remove the "produced by Plotly" logo
                    }
                )
            ])
        ),
        html.Div([
            html.Div(
                id='texto-maximos',
                className='texto-maximos',
                style={'background-color': 'black', 'width': '280px', 'height': '130px'}
            ),
            html.Div(
                id='texto-minimo',
                className='texto-minimos',
                style={'background-color': 'black', 'width': '280px', 'height': '130px', 'margin-left': '20px'}
            ),
        ], style={'display': 'flex', 'align-items': 'center', 'margin-left': '100px', 'margin-top': '-300px'}),
        dcc.Graph(
            id='line-chart',
            config={
                    'modeBarButtonsToRemove': [
                            'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'
                        ],
                        'displaylogo': False  # Remove the "produced by Plotly" logo
                    },
            style={'background-color': 'blue', 'width': '620px', 'height': '240px', 'margin-left': '-600px', 'margin-top': '140px'}
        ),
    ], style={'display': 'flex', 'align-items': 'center', 'margin-top': '50px', 'margin-left': '0px'}),
        html.Div([
        html.H1('DEFENSIVO', className='texto-seccion'),
        html.Div(className='linea')
    ], style={'margin-top': '10px',}),
        html.Div([
        html.Div([
            html.H1('DUELOS AEREOS GANADOS', className='titulo-barras-aereos-of'),
            html.Div(id='barras-duelos-aereosD', className='grafico-barras-aereos-of'),
        ], style={'display': 'inline-block', 'justify-content': 'center', 'width': '30%'}),
        html.Div([
            html.H1('DUELOS 1V1 GANADOS', className='titulo-barras-1v1'),
            html.Div(id='barras-1v1-ofensivoD', className='grafico-barras-1v1'),
        ], style={'display': 'inline-block', 'justify-content': 'center', 'width': '30%'}),
        html.Div([
            html.H1('RECUPERACIONES TRAS PERDIDA', className='titulo-barras-pases'),
            html.Div(id='barras-pases-claveD', className='grafico-barras-indice-tactico'),
        ], style={'display': 'inline-block',  'justify-content': 'center', 'width': '30%'}),        
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-left': '-15px'}),
    html.Div([
        dcc.Dropdown(
            id='dropdown-scatter-plotD',
            options=[
                {'label': 'Duelos Aéreos', 'value': 'duelos_aereosD'},
                {'label': 'Duelos 1vs1', 'value': 'duelos_1v1D'},
                {'label': 'Recuperaciones', 'value': 'recuperaciones'},
            ],
            placeholder="Selecciona un filtro",
            className='dropdown',
            value='duelos_aereosD',
        ),
    ], style={'width': '15%', 'margin-left': '70px', 'margin-top': '100px',}),
        html.Div([
        html.Div([
            dcc.Loading(
                id="loading-1D",
                type="circle",
                color="red",
                children=html.Div([
                        dcc.Graph(
                            id='scatter-plotD',
                        )
                ])
            )
        ], style={'display': 'inline-block', 'width': '50%', 'margin-left': '40px', 'margin-top': '20px'}),        
        html.Div([
            html.H1(id='titulo-dropdownD', className='titulo-dropdown'),
            html.Div([
                html.Div(id='effectivenessD', className='datos1'),
                html.Div(id='x-start-valueD', className='datos2'),
                html.Div(id='y-start-valueD', className='datos3'),
                dcc.Store(id='store-x-stat-valueD'),
                dcc.Store(id='store-y-stat-valueD'),
            ], style={'display': 'flex', 'justify-content': 'center', 'margin-left': '120px'}),
            html.Div([
                html.Div("EFECTIVIDAD", className='texto-cuadrado'),
                html.Div(id='texto-eje-xD', className='texto-cuadrado'),
                dcc.Store(id='store-x-axis-titleD'),
                html.Div(id='texto-eje-yD', className='texto-cuadrado'),
                dcc.Store(id='store-y-axis-titleD'),                
            ], style={'display': 'flex', 'justify-content': 'center', 'margin-left': '-50px'}),
            dcc.Graph(id='bar-chartD', config={'displayModeBar': False})
        ], style={'display': 'inline-block', 'width': '43%', 'background-color': '#ED192D', 'height': '500px', 'margin-left': '40px', 'margin-top': '20px'}), 
    ], style={'display': 'flex'}),
    html.Div([
        dcc.Loading(
            id="loading-1D",
            type="circle",
            color="red",
            children=html.Div([
                dcc.Graph(
                    id='horizontal-bar-chartD',
                )
            ])
        ),
        html.Div([
            html.Div(
                id='texto-maximosD',
                className='texto-maximos',
                style={'background-color': 'black', 'width': '280px', 'height': '130px'}
            ),
            html.Div(
                id='texto-minimoD',
                className='texto-minimos',
                style={'background-color': 'black', 'width': '280px', 'height': '130px', 'margin-left': '20px'}
            ),
        ], style={'display': 'flex', 'align-items': 'center', 'margin-left': '100px', 'margin-top': '-300px'}),
        dcc.Graph(
            id='line-chartD',
            config={
                        'modeBarButtonsToRemove': [
                            'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toImage'
                        ],
                        'displaylogo': False  # Remove the "produced by Plotly" logo
                    },
            style={'background-color': 'blue', 'width': '620px', 'height': '240px', 'margin-left': '-600px', 'margin-top': '100px'}
        ),
    ], style={'display': 'flex', 'align-items': 'center', 'margin-top': '50px', 'margin-left': '0px'}),
    html.Div([
    html.Div([
        dcc.Graph(
            id='cake-chart'
        )
    ], style={'width': '50%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(
            id='cake-tactico'
        )
    ], style={'width': '50%', 'display': 'inline-block'})
])    
])


# DEFENSIVE INTERVENTIONS PIE CHART
@app.callback(
    Output('cake-chart', 'figure'),
    [Input('dropdown-jugador', 'value'),
     Input('dropdown-partidos', 'value')]
)
def update_cake_chart(selected_jugador, selected_partidos):
    # Filter the DataFrame by the selected player and selected matches
    filtered_df = df[(df['Jugador'] == selected_jugador) & (df['Rival'].isin(selected_partidos))]

    if filtered_df.empty:
        return px.pie(
            names=['No Data'],
            values=[1],
            title=f'No Data Available'
        )

    # Get the minutes played in the selected matches
    M_jugados_total = filtered_df['Minutos Jugados'].sum()

    if M_jugados_total == 0:
        M_jugados_total = 1  # To avoid division by zero

    # Sum defensive interventions and adjust to 90 minutes
    interventions = {
        'Intercepciones': filtered_df['Intercepciones'].sum(),
        'Anticipos': filtered_df['Anticipos'].sum(),
        'Bloqueos': filtered_df['Bloqueos'].sum(),
        'Entradas': filtered_df['Entradas'].sum()
    }

    # Create the pie chart
    fig = px.pie(
        names=list(interventions.keys()),
        values=list(interventions.values()),
        title=f'Intervenciones Defensivas',
        color_discrete_sequence=['#360308', '#5c060f', '#910c19', '#b81222', '#ED192D'] 
    )

    return fig




# DEFENSIVE INTERVENTIONS PIE CHART
@app.callback(
    Output('cake-tactico', 'figure'),
    [Input('dropdown-jugador', 'value'),
     Input('dropdown-partidos', 'value')]
)
def update_cake_chart(selected_jugador, selected_partidos):
    # Filter the DataFrame by the selected player and selected matches
    filtered_df = df[(df['Jugador'] == selected_jugador) & (df['Rival'].isin(selected_partidos))]

    if filtered_df.empty:
        return px.pie(
            names=['No Data'],
            values=[1],
            title=f'No Data Available'
        )

    # Get the minutes played in the selected matches
    M_jugados_total = filtered_df['Minutos Jugados'].sum()

    if M_jugados_total == 0:
        M_jugados_total = 1  # To avoid division by zero

    # Sum tactical interventions
    interventions = {
        'Recepcion entre Lineas': filtered_df['Recepcion entre Lineas'].sum(),
        'Toques en Area Rival': filtered_df['Toques en Area Rival'].sum(),
        'Ruptura en conduccion': filtered_df['Ruptura en conduccion'].sum(),
        'Recepcion a espaldas del volante': filtered_df['Recepcion a espaldas del volante'].sum(),
        'Recepcion al espacio': filtered_df['Recepcion al espacio'].sum()
    }

    # Create the pie chart with custom colors
    fig = px.pie(
        names=list(interventions.keys()),
        values=list(interventions.values()),
        title=f'Intervenciones Tacticas',
        color_discrete_sequence=['#360308', '#5c060f', '#910c19', '#b81222', '#ED192D']  # Colores personalizados
    )

    return fig







# Function to generate a list of dark red colors
def generate_dark_red_colors(num_colors):
    from matplotlib.colors import to_hex
    import matplotlib.cm as cm
    import numpy as np

    cmap = cm.get_cmap('Reds', num_colors + 1)  # Get a color map from matplotlib with the desired number of colors
    colors = [to_hex(cmap(i)) for i in range(1, num_colors + 1)]  # Convert colors to hex format and skip the first color for a darker range

    return colors

# GRAFICO DE LINEAS
@app.callback(
    Output('line-chart', 'figure'),
    [Input('dropdown-scatter-plot', 'value'),
     Input('dropdown-jugador', 'value')]
)
def update_line_chart(selected_filter, selected_jugador):
    if selected_filter == 'duelos_aereos':
        selected_filter = 'DAO+'
        y_axis_title = 'Duelos Aéreos Ofensivos Totales'
    elif selected_filter == 'tiros':
        selected_filter = 'Arco'
        y_axis_title = 'Total de Tiros'
    elif selected_filter == 'duelos_1v1':
        selected_filter = '1v1O+'
        y_axis_title = 'Duelos 1v1 Ofensivos Ganados'
    elif selected_filter == 'perdidas':
        selected_filter = 'PERDIDAS'
        y_axis_title = 'Perdidas'
    elif selected_filter == 'pases':
        selected_filter = 'PCompletos'
        y_axis_title = 'Pases Completos'
    elif selected_filter == 'pases_largos':
        selected_filter = 'Largo Completo'
        y_axis_title = 'Pases Largos Completos'
    elif selected_filter == 'exceso_gambeta':
        selected_filter = 'PERDIDAS: xGambeta'
        y_axis_title = 'Perdidas por Gambeta'
    elif selected_filter == 'peligro_esperado':
        selected_filter = 'xT'
        y_axis_title = 'Peligro Esperado (xT)'
    elif selected_filter == 'regates':
        selected_filter = 'Regates'
        y_axis_title = 'Regates'
    elif selected_filter == 'peligro_tate':
        selected_filter = 'Filtrado'
        y_axis_title = 'Pases Filtrados'
    else:
        return {}

    if selected_jugador:
        jugador_df = df[df['Jugador'] == selected_jugador]
    else:
        jugador_df = df.copy()  # Si no hay jugador seleccionado, usar todo el DataFrame

    # Lista de columnas de cuartos
    quarters = ['1/4 de Hora', '2/4 de Hora', '3/4 de Hora', '4/4 de Hora']

    # Crear un DataFrame para acumular los resultados
    result_df_list = []

    for quarter in quarters:
        # Filtrar filas donde la acción ocurrió en el cuarto específico
        quarter_action_df = jugador_df[jugador_df[quarter] == 1]
        if not quarter_action_df.empty:
            # Agrupar por Rival y sumar la acción seleccionada para cada cuarto
            quarter_stats_df = quarter_action_df.groupby('Rival')[selected_filter].sum().reset_index()
            quarter_stats_df['Quarter'] = quarter
            result_df_list.append(quarter_stats_df)

    if not result_df_list:
        return {}

    # Concatenar todos los DataFrames de los cuartos
    result_df = pd.concat(result_df_list)

    # Generar una lista de colores rojos oscuros según el número de rivales únicos
    num_rivales = result_df['Rival'].nunique()
    dark_red_colors = generate_dark_red_colors(num_rivales)

    # Crear el gráfico de área con colores personalizados
    fig = px.area(
        result_df,
        x='Quarter',
        y=selected_filter,
        color='Rival',  # Agregar color por Rival para diferenciarlos
        line_shape='spline',
        labels={'Quarter': 'Cuarto de Juego', selected_filter: y_axis_title},
        color_discrete_sequence=dark_red_colors  # Usar una gama de colores rojos oscuros generada dinámicamente
    )

    fig.update_traces(marker_color='white')

    fig.update_layout(
        xaxis=dict(
            title=None,  # Eliminar título del eje x
            titlefont_size=12,
            tickfont_size=14,
            tickangle=0  # Cambiar el ángulo de los ticks a 0 para que estén horizontales
        ),
        yaxis=dict(
            title=None,  # Eliminar título del eje y
            titlefont_size=12,
            tickfont_size=14,
            gridcolor='white'  # Cambiar el color de las líneas horizontales a blanco
        ),
        font=dict(
            family="Gotham, sans-serif",
            size=17,
            color="black",
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=0, b=0, l=0, r=0),
        height=240,
        modebar=dict(
            remove=['zoom', 'pan', 'select', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']
        )
    )

    return fig



# Function to generate a list of dark red colors
def generate_dark_red_colors(num_colors):
    from matplotlib.colors import to_hex
    import matplotlib.cm as cm

    cmap = cm.get_cmap('Reds', num_colors + 1)  # Get a color map from matplotlib with the desired number of colors
    colors = [to_hex(cmap(i)) for i in range(1, num_colors + 1)]  # Convert colors to hex format and skip the first color for a darker range

    return colors

# GRAFICO DE LINEAS DEFENSIVO
@app.callback(
    Output('line-chartD', 'figure'),
    [Input('dropdown-scatter-plotD', 'value'),
     Input('dropdown-jugador', 'value')]
)
def update_line_chart(selected_filter, selected_jugador):
    if selected_filter == 'duelos_aereosD':
        selected_filter = 'DAD+'
        y_axis_title = 'Duelos Aéreos Defensivos Totales'
    elif selected_filter == 'duelos_1v1D':
        selected_filter = '1v1D+'
        y_axis_title = 'Duelos 1vs1 Defensivos Totales'
    elif selected_filter == 'recuperaciones':
        selected_filter = 'RECUPERACION xIntervencion'
        y_axis_title = 'Recuperaciones por intervención'
    else:
        return {}

    if selected_jugador:
        jugador_df = df[df['Jugador'] == selected_jugador]
    else:
        jugador_df = df.copy()  # Si no hay jugador seleccionado, usar todo el DataFrame

    # Lista de columnas de cuartos
    quarters = ['1/4 de Hora', '2/4 de Hora', '3/4 de Hora', '4/4 de Hora']

    # Crear un DataFrame para acumular los resultados
    result_df_list = []

    for quarter in quarters:
        # Filtrar filas donde la acción ocurrió en el cuarto específico
        quarter_action_df = jugador_df[jugador_df[quarter] == 1]
        if not quarter_action_df.empty:
            # Agrupar por Rival y sumar la acción seleccionada para cada cuarto
            quarter_stats_df = quarter_action_df.groupby('Rival')[selected_filter].sum().reset_index()
            quarter_stats_df['Quarter'] = quarter
            result_df_list.append(quarter_stats_df)

    if not result_df_list:
        return {}

    # Concatenar todos los DataFrames de los cuartos
    result_df = pd.concat(result_df_list)

    # Generar una lista de colores rojos oscuros según el número de rivales únicos
    num_rivales = result_df['Rival'].nunique()
    dark_red_colors = generate_dark_red_colors(num_rivales)

    # Crear el gráfico de área con colores personalizados
    fig = px.area(
        result_df,
        x='Quarter',
        y=selected_filter,
        color='Rival',  # Agregar color por Rival para diferenciarlos
        line_shape='spline',
        labels={'Quarter': 'Cuarto de Juego', selected_filter: y_axis_title},
        color_discrete_sequence=dark_red_colors  # Usar una gama de colores rojos oscuros generada dinámicamente
    )

    fig.update_traces(marker_color='white')

    fig.update_layout(
        xaxis=dict(
            title=None,  # Eliminar título del eje x
            titlefont_size=12,
            tickfont_size=14,
            tickangle=0  # Cambiar el ángulo de los ticks a 0 para que estén horizontales
        ),
        yaxis=dict(
            title=None,  # Eliminar título del eje y
            titlefont_size=12,
            tickfont_size=14,
            gridcolor='white'  # Cambiar el color de las líneas horizontales a blanco
        ),
        font=dict(
            family="Gotham, sans-serif",
            size=17,
            color="black",
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=0, b=0, l=0, r=0),
        height=240,
        modebar=dict(
            remove=['zoom', 'pan', 'select', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toImage']
        )
    )

    return fig





# CALLBACK PARA MODIFICAR LOS TEXTOS DE MAXIMO Y MINIMO POR PARTIDO
def get_statistic_text(selected_filter):
    if selected_filter == 'duelos_aereos':
        return 'Duelos Aéreos'
    elif selected_filter == 'tiros':
        return 'Arco'
    elif selected_filter == 'duelos_1v1':
        return 'Duelos 1v1'
    elif selected_filter == 'perdidas':
        return 'Perdidas'
    elif selected_filter == 'pases':
        return 'Pases'
    elif selected_filter == 'pases_largos':
        return 'Pases Largos'    
    elif selected_filter == 'exceso_gambeta':
        return 'Exceso de Gambeta'
    elif selected_filter == 'peligro_esperado':
        return 'Peligro Esperado'
    elif selected_filter == 'peligro_tate':
        return 'Peligro en 3/4'
    elif selected_filter == 'regates':
        return 'Regates'
    else:
        return 'Estadística Desconocida'


# CALLBACK PARA MODIFICAR LOS TEXTOS DE MAXIMO Y MINIMO POR PARTIDO DEFENSIVO
def get_statistic_textD(selected_filter):
    if selected_filter == 'duelos_aereosD':
        return 'Duelos Aéreos'
    elif selected_filter == 'duelos_1v1D':
        return 'Duelos 1VS1'
    elif selected_filter == 'recuperaciones':
        return 'Recuperaciones'
    else:
        return 'Estadística Desconocida'

# CALLBACK PARA MODIFICAR LOS TEXTOS DE MAXIMO Y MINIMO POR PARTIDO
@app.callback(
    [Output('texto-maximos', 'children'),
     Output('texto-minimo', 'children')],
    [Input('dropdown-scatter-plot', 'value'),
     Input('dropdown-jugador', 'value')]
)
def update_statistic_text(selected_filter, selected_jugador):
    statistic_text = get_statistic_text(selected_filter)
    
    # Filtrar el DataFrame según el jugador seleccionado
    if selected_jugador:
        jugador_df = df[df['Jugador'] == selected_jugador]
    else:
        jugador_df = df.copy()  # Usar todo el DataFrame si no hay jugador seleccionado

    # Filtrar el DataFrame según el filtro seleccionado
    if selected_filter == 'duelos_aereos':
        selected_filter = 'DAO+'
    elif selected_filter == 'tiros':
        selected_filter = 'Arco'        
    elif selected_filter == 'duelos_1v1':
        selected_filter = '1v1O+'
    elif selected_filter == 'perdidas':
        selected_filter = 'PERDIDAS'
    elif selected_filter == 'pases':
        selected_filter = 'PCompletos'
    elif selected_filter == 'pases_largos':
        selected_filter = 'Largo Completo'             
    elif selected_filter == 'exceso_gambeta':
        selected_filter = 'PERDIDAS: xGambeta'
    elif selected_filter == 'peligro_esperado':
        selected_filter = 'xT'
    elif selected_filter == 'peligro_tate':
        selected_filter = 'Filtrado'
    elif selected_filter == 'regates':
        selected_filter = 'Regates'

    # Agrupar por 'Rival' y tomar la primera fila de 'Minutos Jugados' de cada partido
    minutos_jugados_df = jugador_df.groupby('Rival')['Minutos Jugados'].first()

    # Agrupar por partido y sumar las estadísticas seleccionadas
    stats_df = jugador_df.groupby('Rival')[selected_filter].sum()

    # Unir los DataFrames de minutos jugados y estadísticas
    grouped_df = pd.concat([stats_df, minutos_jugados_df], axis=1)

    # Calcular las estadísticas por 90 minutos jugados
    grouped_df[selected_filter] = (90 / grouped_df['Minutos Jugados']) * grouped_df[selected_filter]

    # Encontrar el rival con la máxima y mínima cantidad de la acción seleccionada
    max_rival = grouped_df[selected_filter].idxmax()
    min_rival = grouped_df[selected_filter].idxmin()

    # Obtener las cantidades máxima y mínima
    if selected_filter == 'xT':
        max_value = '-'
        min_value = '-'
    else:
        max_value = int(grouped_df.loc[max_rival, selected_filter])
        min_value = int(grouped_df.loc[min_rival, selected_filter])

    # Estilo para el máximo rival
    max_rival_style = {'color': 'white', 'fontWeight': 'normal', 'fontSize': '23px', 'marginLeft': '10px'}

    # Estilo para el mínimo rival
    min_rival_style = {'color': 'white', 'fontWeight': 'normal', 'fontSize': '23px', 'marginLeft': '10px'}

    # Estilo para el texto en blanco
    white_text_style = {'color': 'white', 'fontSize': '23px', 'marginLeft': '10px', 'marginTop': '10px'}
    white_text_style2 = {'color': 'white', 'fontSize': '23px', 'marginLeft': '10px'}

    return (
        html.Div([
            html.Div(f'MÁXIMO', style=white_text_style),
            html.Div(statistic_text.upper(), style=white_text_style2),
            html.Div(f'{max_rival.upper()} ({max_value})', style=max_rival_style)  # upper aplicado aquí
        ]),
        html.Div([
            html.Div(f'MÍNIMO', style=white_text_style),
            html.Div(statistic_text.upper(), style=white_text_style2),
            html.Div(f'{min_rival.upper()} ({min_value})', style=min_rival_style)  # upper aplicado aquí
        ])
    )



# CALLBACK PARA MODIFICAR LOS TEXTOS DE MAXIMO Y MINIMO POR PARTIDO DEFENSIVO
@app.callback(
    [Output('texto-maximosD', 'children'),
     Output('texto-minimoD', 'children')],
    [Input('dropdown-scatter-plotD', 'value'),
     Input('dropdown-jugador', 'value')]
)
def update_statistic_text(selected_filter, selected_jugador):
    statistic_text = get_statistic_textD(selected_filter)
    
    # Filtrar el DataFrame según el jugador seleccionado
    if selected_jugador:
        jugador_df = df[df['Jugador'] == selected_jugador]
    else:
        jugador_df = df.copy()  # Usar todo el DataFrame si no hay jugador seleccionado

    # Filtrar el DataFrame según el filtro seleccionado
    if selected_filter == 'duelos_aereosD':
        selected_filter = 'DAD+'
    elif selected_filter == 'duelos_1v1D':
        selected_filter = '1v1D+'
    elif selected_filter == 'recuperaciones':
        selected_filter = 'RECUPERACION xIntervencion'

    # Agrupar por 'Rival' y tomar la primera fila de 'Minutos Jugados' de cada partido
    minutos_jugados_df = jugador_df.groupby('Rival')['Minutos Jugados'].first()

    # Agrupar por partido y sumar las estadísticas seleccionadas
    stats_df = jugador_df.groupby('Rival')[selected_filter].sum()

    # Unir los DataFrames de minutos jugados y estadísticas
    grouped_df = pd.concat([stats_df, minutos_jugados_df], axis=1)

    # Calcular las estadísticas por 90 minutos jugados
    grouped_df[selected_filter] = (90 / grouped_df['Minutos Jugados']) * grouped_df[selected_filter]

    # Encontrar el rival con la máxima y mínima cantidad de la acción seleccionada
    max_rival = grouped_df[selected_filter].idxmax()
    min_rival = grouped_df[selected_filter].idxmin()

    # Obtener las cantidades máxima y mínima
    max_value = int(grouped_df.loc[max_rival, selected_filter])
    min_value = int(grouped_df.loc[min_rival, selected_filter])

    # Estilo para el máximo rival
    max_rival_style = {'color': 'white', 'fontWeight': 'normal', 'fontSize': '23px', 'marginLeft': '10px'}

    # Estilo para el mínimo rival
    min_rival_style = {'color': 'white', 'fontWeight': 'normal', 'fontSize': '23px', 'marginLeft': '10px'}

    # Estilo para el texto en blanco
    white_text_style = {'color': 'white', 'fontSize': '23px', 'marginLeft': '10px', 'marginTop': '10px'}
    white_text_style2 = {'color': 'white', 'fontSize': '23px', 'marginLeft': '10px'}

    return (
        html.Div([
            html.Div(f'MÁXIMO', style=white_text_style),
            html.Div(statistic_text.upper(), style=white_text_style2),
            html.Div(f'{max_rival.upper()} ({max_value})', style=max_rival_style)  # upper aplicado aquí
        ]),
        html.Div([
            html.Div(f'MÍNIMO', style=white_text_style),
            html.Div(statistic_text.upper(), style=white_text_style2),
            html.Div(f'{min_rival.upper()} ({min_value})', style=min_rival_style)  # upper aplicado aquí
        ])
    )



# HORIZONTAL BAR CHART (RANKING)
@app.callback(
    Output('horizontal-bar-chart', 'figure'),
    [Input('dropdown-scatter-plot', 'value'),
     Input('dropdown-division', 'value'),
     Input('dropdown-partidos', 'value'),
     Input('store-filtro', 'data'),
     Input('store-x-axis-title', 'data'),
     Input('store-y-axis-title', 'data'),
     Input('scatter-plot', 'hoverData'),
     Input('dropdown-jugador', 'value')]
)
def update_horizontal_bar_chart(selected_filter, selected_division, selected_partidos, selected_filtro, x_axis_title,
                                y_axis_title, hoverData, selected_jugador):
    if selected_division:
        filtered_df = df[df['División'] == selected_division]
        if selected_partidos:
            filtered_df = filtered_df[filtered_df['Rival'].isin(selected_partidos)]
    else:
        filtered_df = df

    if selected_filter == 'duelos_aereos':
        filtered_df['DAOfensivo'] = filtered_df['DAO+']
        x_col = 'DAOfensivo'
        y_col = 'DAO+'
        filter_name = 'Duelos Aéreos Ofensivos'
    elif selected_filter == 'tiros':
        x_col = 'Tiros'
        y_col = 'Arco'
        filter_name = 'Tiros'
    elif selected_filter == 'duelos_1v1':
        x_col = 'Ofensivo'
        y_col = '1v1O+'
        filter_name = 'Duelos 1v1 Ofensivos'
    elif selected_filter == 'perdidas':
        x_col = 'PERDIDAS'
        y_col = 'PERDIDAS'
        filter_name = 'PERDIDAS'
    elif selected_filter == 'pases':
        x_col = 'PASES'
        y_col = 'PCompletos'
        filter_name = 'Pases'
    elif selected_filter == 'pases_largos':
        x_col = 'PASES LARGOS'
        y_col = 'Largo Completo'
        filter_name = 'Pases Largos'
    elif selected_filter == 'exceso_gambeta':
        y_col = '1v1O+'
        x_col = 'PERDIDAS: xGambeta'
        filter_name = 'Exceso de Gambeta'
    elif selected_filter == 'peligro_esperado':
        x_col = 'xT'
        y_col = 'xT'
        filter_name = 'Peligro Esperado'
    elif selected_filter == 'peligro_tate':
        x_col = 'Filtrado'
        y_col = 'Recepcion a espaldas del volante'
        filter_name = 'peligro en 3/4'
    elif selected_filter == 'regates':
        x_col = 'Regates'
        y_col = 'R+'
        filter_name = 'Regates'
    else:
        return {}

    if selected_partidos:
        selected_df = filtered_df[filtered_df['Rival'].isin(selected_partidos)]
    else:
        selected_df = filtered_df

    grouped_by_rival = selected_df.groupby(['Jugador', 'Rival']).agg({
        'Minutos Jugados': 'first',
        x_col: 'sum',
        y_col: 'sum',
        'Foto': 'first'
    }).reset_index()

    grouped_by_rival.fillna(0, inplace=True)

    if len(selected_partidos) > 1:
        grouped_df = grouped_by_rival.groupby('Jugador').agg({
            'Minutos Jugados': 'sum',
            x_col: 'sum',
            y_col: 'sum',
            'Foto': 'first'
        }).reset_index()
        grouped_df[x_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[x_col]
        grouped_df[y_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[y_col]
    else:
        grouped_df = grouped_by_rival
        grouped_df[x_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[x_col]
        grouped_df[y_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[y_col]

    grouped_df.fillna(0, inplace=True)
    grouped_df = grouped_df[grouped_df['Foto'].notna() & (grouped_df['Foto'] != '')]

    # Filtrar jugadores con más de 30 minutos por partido jugado
    if selected_partidos:
        grouped_df = grouped_df[grouped_df['Minutos Jugados'] / len(selected_partidos) > 30]

    # Redondear los valores antes de crear la gráfica, excepto para el filtro 'peligro esperado'
    if selected_filter != 'peligro_esperado':
        grouped_df[x_col] = grouped_df[x_col].round(2)
        grouped_df[y_col] = grouped_df[y_col].round(2)

    # Ordenar el DataFrame de menor a mayor
    grouped_df = grouped_df.sort_values(by=y_col, ascending=True)

    # Determine the selected player from the hover data
    selected_player = hoverData['points'][0]['hovertext'] if hoverData else None

    # Define bar colors
    bar_colors = ['red' if player == selected_jugador else '#737272' if value < 0 else 'black'
                  for player, value in zip(grouped_df['Jugador'], grouped_df[y_col])]

    # Create the horizontal bar chart
    fig = px.bar(
        grouped_df,
        y='Jugador',
        x=y_col,
        orientation='h',
        hover_name='Jugador'
    )

    fig.update_traces(marker=dict(color=bar_colors))

    # Calculate maximum bar width (for font size adjustment)
    max_bar_width = grouped_df[y_col].max()

    # Set the font size to be proportional to the maximum bar width
    font_size = max(10, min(20, max_bar_width / 2))  # Adjust this formula as needed

    # Ajustar el formato del hovertemplate según el filtro seleccionado
    if selected_filter == 'peligro_esperado':
        hover_template = "<b>%{hovertext}</b><br>" \
                         f"{y_axis_title}: %{{x:,.6f}}"  # Mostrar todos los decimales
    else:
        hover_template = "<b>%{hovertext}</b><br>" \
                         f"{y_axis_title}: %{{x:,.0f}}"  # Redondeo a entero

    fig.update_traces(
        hovertemplate=hover_template
    )

    # Disable the legend and titles, set background colors, and add dynamic title
    fig.update_layout(
        showlegend=False,
        title=dict(
            text=f'<b>RANKING {filter_name.upper()}</b>',
            font=dict(
                family="Gotham, sans-serif",
                size=27,
                color='black'
            )
        ),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    # Update y-axis to reflect the font size
    fig.update_yaxes(title_text='', tickfont=dict(size=font_size))  # Set the font size based on bar width
    fig.update_xaxes(title_text='')

    return fig

# HORIZONTAL BAR CHART (RANKING) DEFENSIVO
@app.callback(
    Output('horizontal-bar-chartD', 'figure'),
    [Input('dropdown-scatter-plotD', 'value'),
     Input('dropdown-division', 'value'),
     Input('dropdown-partidos', 'value'),
     Input('store-filtro', 'data'),
     Input('store-x-axis-titleD', 'data'),
     Input('store-y-axis-titleD', 'data'),
     Input('scatter-plotD', 'hoverData'),
     Input('dropdown-jugador', 'value')]
)
def update_horizontal_bar_chart(selected_filter, selected_division, selected_partidos, selected_filtro, x_axis_title,
                                y_axis_title, hoverData, selected_jugador):
    if selected_division:
        filtered_df = df[df['División'] == selected_division]
        if selected_partidos:
            filtered_df = filtered_df[filtered_df['Rival'].isin(selected_partidos)]
    else:
        filtered_df = df

    if selected_filter == 'duelos_aereosD':
        filtered_df['DADefensivo'] = filtered_df['DAD+']
        x_col = 'DADefensivo'
        y_col = 'DAD+'
        filter_name = 'Duelos Aéreos Defensivos'
    elif selected_filter == 'duelos_1v1D':
        filtered_df['Defensivo'] = filtered_df['1v1D+']
        x_col = 'Defensivo'
        y_col = '1v1D+'
        filter_name = 'Duelos 1vs1 Defensivos'
    elif selected_filter == 'recuperaciones':
        filtered_df['RECUPERACION xIntervencion'] = filtered_df['RECUPERACION xIntervencion']
        x_col = 'RECUPERACION xIntervencion'
        y_col = 'RECUPERACION xPosicional'
        filter_name = 'Recuperaciones'       
    else:
        return {}

    if selected_partidos:
        selected_df = filtered_df[filtered_df['Rival'].isin(selected_partidos)]

    grouped_by_rival = selected_df.groupby(['Jugador', 'Rival']).agg({
        'Minutos Jugados': 'first',
        x_col: 'sum',
        y_col: 'sum',
        'Foto': 'first'
    }).reset_index()

    grouped_by_rival.fillna(0, inplace=True)

    if len(selected_partidos) > 1:
        grouped_df = grouped_by_rival.groupby('Jugador').agg({
            'Minutos Jugados': 'sum',
            x_col: 'sum',
            y_col: 'sum',
            'Foto': 'first'
        }).reset_index()
        grouped_df[x_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[x_col]
        grouped_df[y_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[y_col]
    else:
        grouped_df = grouped_by_rival
        grouped_df[x_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[x_col]
        grouped_df[y_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[y_col]

    grouped_df.fillna(0, inplace=True)
    grouped_df = grouped_df[grouped_df['Foto'].notna() & (grouped_df['Foto'] != '')]

    # Filtrar jugadores que promedian más de 30 minutos por partido jugado
    grouped_df = grouped_df[grouped_df['Minutos Jugados'] / len(selected_partidos) > 30]

    # Ordenar el DataFrame de menor a mayor
    grouped_df = grouped_df.sort_values(by=y_col, ascending=True)

    # Determine the selected player from the hover data
    selected_player = hoverData['points'][0]['hovertext'] if hoverData else None

    # Define bar colors
    bar_colors = ['red' if player == selected_jugador else '#737272' if value < 0 else 'black'
                  for player, value in zip(grouped_df['Jugador'], grouped_df[y_col])]

    # Create the horizontal bar chart
    fig = px.bar(
        grouped_df,
        y='Jugador',
        x=y_col,
        orientation='h',
        hover_name='Jugador'
    )

    fig.update_traces(marker=dict(color=bar_colors))

    # Calculate maximum bar width (for font size adjustment)
    max_bar_width = grouped_df[y_col].max()

    # Set the font size to be proportional to the maximum bar width
    font_size = max(10, min(20, max_bar_width / 2))  # Adjust this formula as needed

    # Disable the legend and titles, set background colors, and add dynamic title
    fig.update_layout(
        showlegend=False,
        title=dict(
            text=f'<b>RANKING {filter_name.upper()}</b>',
            font=dict(
                family="Gotham, sans-serif",
                size=27,
                color='black'
            )
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        modebar=dict(
            remove=['zoom', 'pan', 'select', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toImage']
        )
    )

    # Update y-axis to reflect the font size
    fig.update_yaxes(title_text='', tickfont=dict(size=font_size))  # Set the font size based on bar width
    fig.update_xaxes(title_text='')

    return fig




# VERTICAL BAR CHART (CANTIDAD POR PARTIDO)
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('dropdown-scatter-plot', 'value'),
     Input('dropdown-jugador', 'value')]
)
def update_bar_chart(selected_filter, selected_jugador):
    if selected_filter == 'duelos_aereos':
        selected_filter = 'DAO+'
        filtered_df = df.groupby('Jugador')['DAO+'].sum().reset_index()
        x_axis_title = 'Jugador'
        y_axis_title = 'Duelos Aéreos Ofensivos Totales'
        title = ' '
    elif selected_filter == 'tiros':
        selected_filter = 'Arco'
        filtered_df = df.groupby('Jugador')['Arco'].sum().reset_index()
        x_axis_title = 'Jugador'
        y_axis_title = 'Total de Tiros'
        title = ' '
    elif selected_filter == 'duelos_1v1':
        selected_filter = '1v1O+'
        filtered_df = df.groupby('Jugador')['1v1O+'].sum().reset_index()
        x_axis_title = 'Jugador'
        y_axis_title = 'Duelos 1v1 Ofensivos Ganados'
        title = ' '
    elif selected_filter == 'perdidas':
        selected_filter = 'PERDIDAS'
        filtered_df = df.groupby('Jugador')['PERDIDAS'].sum().reset_index()
        x_axis_title = 'Jugador'
        y_axis_title = 'Perdidas'
        title = ' '    
    elif selected_filter == 'pases':
        selected_filter = 'PCompletos'
        filtered_df = df.groupby('Jugador')['PCompletos'].sum().reset_index()
        x_axis_title = 'Jugador'
        y_axis_title = 'Duelos 1v1 Ofensivos Ganados'
        title = ' '
    elif selected_filter == 'pases_largos':
        selected_filter = 'Largo Completo'
        filtered_df = df.groupby('Jugador')['Largo Completo'].sum().reset_index()
        x_axis_title = 'Jugador'
        y_axis_title = 'Pase Largo Completo'
        title = ' '                  
    elif selected_filter == 'exceso_gambeta':
        selected_filter = 'PERDIDAS: xGambeta'
        filtered_df = df.groupby('Jugador')['PERDIDAS: xGambeta'].sum().reset_index()
        x_axis_title = 'Jugador'
        y_axis_title = 'Perdidas por gambeta'
        title = ' ' 
    elif selected_filter == 'peligro_esperado':
        selected_filter = 'xT'
        filtered_df = df.groupby('Jugador')['xT'].sum().reset_index()
        x_axis_title = 'Jugador'
        y_axis_title = 'Peligro esperado'
        title = ' '
    elif selected_filter == 'regates':
        selected_filter = 'Regates'
        filtered_df = df.groupby('Jugador')['Regates'].sum().reset_index()
        x_axis_title = 'Jugador'
        y_axis_title = 'Regates'
        title = ' '              
    elif selected_filter == 'peligro_tate':
        selected_filter = 'Filtrado'
        filtered_df = df.groupby('Jugador')['Filtrado'].sum().reset_index()
        x_axis_title = 'Jugador'
        y_axis_title = 'Pase filtrado'
        title = ' '                             
    else:
        return {}

    if selected_jugador:
        jugador_df = df[df['Jugador'] == selected_jugador]
    else:
        jugador_df = df.copy()  # Si no hay jugador seleccionado, usar todo el DataFrame

    # Agrupar por 'Rival' y tomar la primera fila de 'Minutos Jugados' de cada partido
    minutos_jugados_df = jugador_df.groupby('Rival')['Minutos Jugados'].first()

    # Agrupar por partido y sumar las estadísticas seleccionadas
    stats_df = jugador_df.groupby('Rival')[selected_filter].sum()

    # Unir los DataFrames de minutos jugados y estadísticas
    grouped_df = pd.concat([stats_df, minutos_jugados_df], axis=1)

    # Calcular las estadísticas por 90 minutos jugados
    grouped_df[selected_filter] = (90 / grouped_df['Minutos Jugados']) * grouped_df[selected_filter]

    fig = px.bar(
        grouped_df.reset_index(),  # Reset index para que 'Rival' sea una columna
        x='Rival',
        y=selected_filter,
        title=title,
        labels={'Rival': 'Partido', selected_filter: selected_filter}
    )

    fig.update_traces(marker_color='white')

    fig.update_layout(
        xaxis=dict(
            title=' ',
            titlefont_size=12,
            tickfont_size=12,
            tickangle=0  # Cambiar el ángulo de los ticks a 0 para que estén horizontales
        ),
        yaxis=dict(
            title='',
            titlefont_size=12,
            tickfont_size=12,
            gridcolor='#ED192D'  # Cambiar el color de las líneas horizontales a rojo
        ),
        font=dict(
            family="Gotham, sans-serif",
            size=17,
            color="white",
            weight='bold'
        ),
        plot_bgcolor='#ED192D',
        paper_bgcolor='#ED192D',
        margin=dict(t=60, b=60, l=60, r=60),
        height=350
    )

    return fig


# VERTICAL BAR CHART (CANTIDAD POR PARTIDO) DEFENSIVO
@app.callback(
    Output('bar-chartD', 'figure'),
    [Input('dropdown-scatter-plotD', 'value'),
     Input('dropdown-jugador', 'value')]
)
def update_bar_chart(selected_filter, selected_jugador):
    if selected_filter == 'duelos_aereosD':
        selected_filter = 'DAD+'
        filtered_df = df.groupby('Jugador')['DAD+'].sum().reset_index()
        x_axis_title = 'Jugador'
        y_axis_title = 'Duelos Aéreos Defensivos Totales'
        title = ' '
    elif selected_filter == 'duelos_1v1D':
        selected_filter = '1v1D+'
        filtered_df = df.groupby('Jugador')['1v1D+'].sum().reset_index()
        x_axis_title = 'Jugador'
        y_axis_title = 'Duelos 1vs1 Defensivos Totales'
        title = ' '
    elif selected_filter == 'recuperaciones':
        selected_filter = 'RECUPERACION xIntervencion'
        filtered_df = df.groupby('Jugador')['RECUPERACION xIntervencion'].sum().reset_index()
        x_axis_title = 'Jugador'
        y_axis_title = 'Duelos 1vs1 Defensivos Totales'
        title = ' '           
                           
    else:
        return {}

    if selected_jugador:
        jugador_df = df[df['Jugador'] == selected_jugador]
    else:
        jugador_df = df.copy()  # Si no hay jugador seleccionado, usar todo el DataFrame

    # Agrupar por 'Rival' y tomar la primera fila de 'Minutos Jugados' de cada partido
    minutos_jugados_df = jugador_df.groupby('Rival')['Minutos Jugados'].first()

    # Agrupar por partido y sumar las estadísticas seleccionadas
    stats_df = jugador_df.groupby('Rival')[selected_filter].sum()

    # Unir los DataFrames de minutos jugados y estadísticas
    grouped_df = pd.concat([stats_df, minutos_jugados_df], axis=1)

    # Calcular las estadísticas por 90 minutos jugados
    grouped_df[selected_filter] = (90 / grouped_df['Minutos Jugados']) * grouped_df[selected_filter]

    fig = px.bar(
        grouped_df.reset_index(),  # Reset index para que 'Rival' sea una columna
        x='Rival',
        y=selected_filter,
        title=title,
        labels={'Rival': 'Partido', selected_filter: selected_filter}
    )

    fig.update_traces(marker_color='white')

    fig.update_layout(
        xaxis=dict(
            title=' ',
            titlefont_size=12,
            tickfont_size=12,
            tickangle=0  # Cambiar el ángulo de los ticks a 0 para que estén horizontales
        ),
        yaxis=dict(
            title='',
            titlefont_size=12,
            tickfont_size=12,
            gridcolor='#ED192D'  # Cambiar el color de las líneas horizontales a rojo
        ),
        font=dict(
            family="Gotham, sans-serif",
            size=17,
            color="white",
            weight='bold'
        ),
        plot_bgcolor='#ED192D',
        paper_bgcolor='#ED192D',
        margin=dict(t=60, b=60, l=60, r=60),
        height=350
    )

    return fig





# Función para recortar la imagen del jugador y convertirla a base64
def recortar_imagen(url):
    if not isinstance(url, str) or not url.startswith(('http://', 'https://')):
        print(f"Invalid URL: {url}")
        return None
    
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        
        width, height = img.size
        left = 0
        top = 0
        right = width
        bottom = height // 2
        
        img_cropped = img.crop((left, top, right, bottom))
        
        buffer = BytesIO()
        img_cropped.save(buffer, format="PNG")
        buffer.seek(0)
        
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        img_data = f"data:image/png;base64,{img_base64}"
        
        return img_data
    except Exception as e:
        print(f"Error processing image from {url}: {e}")
        return None




# SCATTER PLOT
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('dropdown-scatter-plot', 'value'),
     Input('dropdown-division', 'value'),
     Input('dropdown-partidos', 'value'),
     Input('store-filtro', 'data'),
     Input('store-x-axis-title', 'data'),
     Input('store-y-axis-title', 'data'),
     Input('dropdown-jugador', 'value')]  
)
def update_scatter_plot(selected_filter, selected_division, selected_partidos, selected_filtro, x_axis_title, y_axis_title, selected_jugador):
    # Obtener la posición del jugador seleccionado
    if selected_jugador:
        player_position = df[df['Jugador'] == selected_jugador]['Posición'].values[0]
    else:
        player_position = None

    if selected_filtro == 'division':
        if selected_division:
            filtered_df = df[df['División'] == selected_division]
            if selected_partidos:
                filtered_df = filtered_df[filtered_df['Rival'].isin(selected_partidos)]
        else:
            filtered_df = df
    elif selected_filtro == 'posicion' and player_position:
        filtered_df = df[df['Posición'] == player_position]
        if selected_partidos:
            filtered_df = filtered_df[filtered_df['Rival'].isin(selected_partidos)]
    else:
        filtered_df = df

    # Continuar con la lógica del gráfico
    if selected_filter == 'duelos_aereos':
        filtered_df['DAOfensivo'] = filtered_df['DAO+']
        x_col = 'DAOfensivo'
        y_col = 'DAO+'
    elif selected_filter == 'tiros':
        y_col = 'Arco'
        x_col = 'Tiros'
    elif selected_filter == 'duelos_1v1':
        x_col = 'Ofensivo'
        y_col = '1v1O+'
    elif selected_filter == 'perdidas':
        x_col = 'PERDIDAS: xPase'
        y_col = 'PERDIDAS: xGambeta'
    elif selected_filter == 'pases':
        x_col = 'PASES'
        y_col = 'PCompletos'
    elif selected_filter == 'pases_largos':
        x_col = 'PASES LARGOS'
        y_col = 'Largo Completo'
    elif selected_filter == 'exceso_gambeta':
        y_col = '1v1O+'
        x_col = 'PERDIDAS: xGambeta'
    elif selected_filter == 'peligro_esperado':
        x_col = 'xT'
        y_col = 'xT'
    elif selected_filter == 'peligro_tate':
        x_col = 'Filtrado'
        y_col = 'Recepcion a espaldas del volante'
    elif selected_filter == 'regates':
        x_col = 'Regates'
        y_col = 'R+'
    else:
        return {}, "", "", ""

    if selected_partidos:
        selected_df = filtered_df[filtered_df['Rival'].isin(selected_partidos)]
    else:
        selected_df = filtered_df

    grouped_by_rival = selected_df.groupby(['Jugador', 'Rival']).agg({
        'Minutos Jugados': 'first',
        x_col: 'sum',
        y_col: 'sum',
        'Foto': 'first'
    }).reset_index()

    grouped_by_rival.fillna(0, inplace=True)

    if len(selected_partidos) > 1:
        grouped_df = grouped_by_rival.groupby('Jugador').agg({
            'Minutos Jugados': 'sum',
            x_col: 'sum',
            y_col: 'sum',
            'Foto': 'first'
        }).reset_index()
        grouped_df[x_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[x_col]
        grouped_df[y_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[y_col]
    else:
        grouped_df = grouped_by_rival
        grouped_df[x_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[x_col]
        grouped_df[y_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[y_col]

    grouped_df.fillna(0, inplace=True)
    grouped_df = grouped_df[grouped_df['Foto'].notna() & (grouped_df['Foto'] != '')]

    # Filtrar jugadores con más de 30 minutos por partido jugado
    grouped_df = grouped_df[grouped_df['Minutos Jugados'] / len(selected_partidos) > 30]

    fig = px.scatter(
        grouped_df,
        x=x_col,
        y=y_col,
        title=' ',
        hover_name='Jugador',
        custom_data=['Jugador', x_col, y_col],
    )

    fig.update_traces(hoverlabel=dict(bgcolor="red", font=dict(color="white")))

    grouped_df['Efectividad'] = (grouped_df[y_col] / grouped_df[x_col].replace(0, np.nan)) * 100
    grouped_df.fillna(0, inplace=True)

    # Ajustar el formato del hovertemplate según el filtro seleccionado
    if selected_filter == 'peligro_esperado':
        hover_template = "<b>%{customdata[0]}</b><br>" \
        f"{x_axis_title}: %{{customdata[1]:,.6f}}<br>"  # Mostrar todos los decimales
        f"{y_axis_title}: %{{customdata[2]:,.6f}}<br>"  # Mostrar todos los decimales
    else:
        hover_template = "<b>%{customdata[0]}</b><br>" \
        f"{x_axis_title}: %{{customdata[1]:,.0f}}<br>"  # Redondeo a entero
        f"{y_axis_title}: %{{customdata[2]:,.0f}}<br>"  # Redondeo a entero

    fig.update_traces(
        hovertemplate=hover_template
    )

    fig.update_layout(
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
        font=dict(
            family="Gotham, sans-serif",
            size=17,
            color="#ED192D",
            weight='bold'
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        width=700,
        height=500,
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
    )

    fig.update_xaxes(
        showticklabels=False,
        showline=True,
        linewidth=4,
        linecolor='#ED192D',
        title_text=x_axis_title
    )
    fig.update_yaxes(
        showticklabels=False,
        showline=True,
        linewidth=4,
        linecolor='#ED192D',
        title_text=y_axis_title
    )

    x_mean = grouped_df[x_col].mean()
    y_mean = grouped_df[y_col].mean()
    x_range = [grouped_df[x_col].min(), grouped_df[x_col].max()]
    y_range = [grouped_df[y_col].min(), grouped_df[y_col].max()]

    fig.add_shape(
        type='line',
        x0=x_range[0],
        x1=x_range[1],
        y0=y_mean,
        y1=y_mean,
        line=dict(
            color='black',
            width=1,
            dash='dash',
        ),
        layer='below'
    )

    fig.add_shape(
        type='line',
        x0=x_mean,
        x1=x_mean,
        y0=y_range[0],
        y1=y_range[1],
        line=dict(
            color='black',
            width=1,
            dash='dash',
        ),
        layer='below'
    )

    fig.add_annotation(
        x=x_mean - (x_mean - x_range[0]) * 0.50,
        y=y_mean + (y_range[1] - y_mean) * 0.50,
        text="GRUPO 1",
        showarrow=False,
        font=dict(
            family="Gotham, sans-serif",
            size=17,
            color="grey",
        )
    )

    fig.add_annotation(
        x=x_mean + (x_range[1] - x_mean) * 0.50,
        y=y_mean + (y_range[1] - y_mean) * 0.50,
        text="GRUPO 2",
        showarrow=False,
        font=dict(
            family="Gotham, sans-serif",
            size=17,
            color="grey",
        )
    )

    fig.add_annotation(
        x=x_mean - (x_mean - x_range[0]) * 0.50,
        y=y_mean - (y_mean - y_range[0]) * 0.50,
        text="GRUPO 3",
        showarrow=False,
        font=dict(
            family="Gotham, sans-serif",
            size=17,
            color="grey",
        )
    )

    fig.add_annotation(
        x=x_mean + (x_range[1] - x_mean) * 0.50,
        y=y_mean - (y_mean - y_range[0]) * 0.50,
        text="GRUPO 4",
        showarrow=False,
        font=dict(
            family="Gotham, sans-serif",
            size=17,
            color="grey",
        )
    )

    for i, row in grouped_df.iterrows():
        img_buffer = recortar_imagen(row['Foto'])
        fig.add_layout_image(
            dict(
                source=img_buffer,
                xref="x",
                yref="y",
                x=row[x_col],
                y=row[y_col],
                sizex=(grouped_df[x_col].max() - grouped_df[x_col].min()) * 0.15,
                sizey=(grouped_df[y_col].max() - grouped_df[y_col].min()) * 0.15,
                xanchor="center",
                yanchor="middle"
            )
        )

    return fig





# SCATTER PLOT DEFENSIVO
@app.callback(
    Output('scatter-plotD', 'figure'),
    [Input('dropdown-scatter-plotD', 'value'),
     Input('dropdown-division', 'value'),
     Input('dropdown-partidos', 'value'),
     Input('store-filtro', 'data'),
     Input('store-x-axis-titleD', 'data'),
     Input('store-y-axis-titleD', 'data'),
     Input('dropdown-jugador', 'value')]  # Añadido input para seleccionar jugador
)
def update_scatter_plotD(selected_filter, selected_division, selected_partidos, selected_filtro, x_axis_title, y_axis_title, selected_jugador):
    if selected_division:
        filtered_df = df[df['División'] == selected_division]
        if selected_partidos:
            filtered_df = filtered_df[filtered_df['Rival'].isin(selected_partidos)]
    else:
        filtered_df = df

    if selected_filter == 'duelos_aereosD':
        filtered_df['DADefensivo'] = filtered_df['DADefensivo']
        x_col = 'DADefensivo'
        y_col = 'DAD+'
    elif selected_filter == 'duelos_1v1D':
        filtered_df['Defensivo'] = filtered_df['Defensivo']
        x_col = 'Defensivo'
        y_col = '1v1D+'
    elif selected_filter == 'recuperaciones':
        filtered_df['RECUPERACION xIntervencion'] = filtered_df['RECUPERACION xIntervencion']
        x_col = 'RECUPERACION xIntervencion'
        y_col = 'RECUPERACION xPosicional'                          
    else:
        return {}, "", "", ""

    if selected_partidos:
        selected_df = filtered_df[filtered_df['Rival'].isin(selected_partidos)]
    else:
        selected_df = filtered_df

    grouped_by_rival = selected_df.groupby(['Jugador', 'Rival']).agg({
        'Minutos Jugados': 'first',
        x_col: 'sum',
        y_col: 'sum',
        'Foto': 'first'
    }).reset_index()

    grouped_by_rival.fillna(0, inplace=True)

    if len(selected_partidos) > 1:
        grouped_df = grouped_by_rival.groupby('Jugador').agg({
            'Minutos Jugados': 'sum',
            x_col: 'sum',
            y_col: 'sum',
            'Foto': 'first'
        }).reset_index()
        grouped_df[x_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[x_col]
        grouped_df[y_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[y_col]
    else:
        grouped_df = grouped_by_rival
        grouped_df[x_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[x_col]
        grouped_df[y_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[y_col]

    grouped_df.fillna(0, inplace=True)
    grouped_df = grouped_df[grouped_df['Foto'].notna() & (grouped_df['Foto'] != '')]
    grouped_df = grouped_df[grouped_df['Minutos Jugados'] / len(selected_partidos) > 30]

    if selected_jugador:
        player_position = df[df['Jugador'] == selected_jugador]['Posición'].values[0]
    else:
        player_position = None

    fig = px.scatter(
        grouped_df,
        x=x_col,
        y=y_col,
        title=' ',
        hover_name='Jugador',
        custom_data=['Jugador', x_col, y_col],
    )

    fig.update_traces(hoverlabel=dict(bgcolor="red", font=dict(color="white")))

    grouped_df['Efectividad'] = (grouped_df[y_col] / grouped_df[x_col].replace(0, np.nan)) * 100
    grouped_df.fillna(0, inplace=True)

    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>"
                      f"{x_axis_title}: %{{customdata[1]:.0f}}<br>"
                      f"{y_axis_title}: %{{customdata[2]:.0f}}<br>"
    )

    fig.update_layout(
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
        font=dict(
            family="Gotham, sans-serif",
            size=17,
            color="#ED192D",
            weight='bold'
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        width=700,
        height=500,
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),

    )

    fig.update_xaxes(
        showticklabels=False,
        showline=True,
        linewidth=4,
        linecolor='#ED192D',
        title_text=x_axis_title
    )
    fig.update_yaxes(
        showticklabels=False,
        showline=True,
        linewidth=4,
        linecolor='#ED192D',
        title_text=y_axis_title
    )

    x_mean = grouped_df[x_col].mean()
    y_mean = grouped_df[y_col].mean()
    x_range = [grouped_df[x_col].min(), grouped_df[x_col].max()]
    y_range = [grouped_df[y_col].min(), grouped_df[y_col].max()]

    fig.add_shape(
        type='line',
        x0=x_range[0],
        x1=x_range[1],
        y0=y_mean,
        y1=y_mean,
        line=dict(
            color='black',
            width=1,
            dash='dash',
        ),
        layer='below'
    )

    fig.add_shape(
        type='line',
        x0=x_mean,
        x1=x_mean,
        y0=y_range[0],
        y1=y_range[1],
        line=dict(
            color='black',
            width=1,
            dash='dash',
        ),
        layer='below'
    )

    fig.add_annotation(
        x=x_mean - (x_mean - x_range[0]) * 0.50,
        y=y_mean + (y_range[1] - y_mean) * 0.50,
        text="GRUPO 1",
        showarrow=False,
        font=dict(
            family="Gotham, sans-serif",
            size=17,
            color="grey",
        )
    )

    fig.add_annotation(
        x=x_mean + (x_range[1] - x_mean) * 0.50,
        y=y_mean + (y_range[1] - y_mean) * 0.50,
        text="GRUPO 2",
        showarrow=False,
        font=dict(
            family="Gotham, sans-serif",
            size=17,
            color="grey",
        )
    )

    fig.add_annotation(
        x=x_mean - (x_mean - x_range[0]) * 0.50,
        y=y_mean - (y_mean - y_range[0]) * 0.50,
        text="GRUPO 3",
        showarrow=False,
        font=dict(
            family="Gotham, sans-serif",
            size=17,
            color="grey",
        )
    )

    fig.add_annotation(
        x=x_mean + (x_range[1] - x_mean) * 0.50,
        y=y_mean - (y_mean - y_range[0]) * 0.50,
        text="GRUPO 4",
        showarrow=False,
        font=dict(
            family="Gotham, sans-serif",
            size=17,
            color="grey",
        )
    )

    for i, row in grouped_df.iterrows():
        img_buffer = recortar_imagen(row['Foto'])
        fig.add_layout_image(
            dict(
                source=img_buffer,
                xref="x",
                yref="y",
                x=row[x_col],
                y=row[y_col],
                sizex=(grouped_df[x_col].max() - grouped_df[x_col].min()) * 0.15,
                sizey=(grouped_df[y_col].max() - grouped_df[y_col].min()) * 0.15,
                xanchor="center",
                yanchor="middle"
            )
        )

    return fig





#CALLBACK PARA TITULOS DEL EJE DEL SCATTER PLOT
@app.callback(
    [Output('store-x-axis-title', 'data'),
     Output('store-y-axis-title', 'data')],
    [Input('dropdown-scatter-plot', 'value')]
)
def update_axis_titles(selected_filter):
    if selected_filter == 'duelos_aereos':
        x_axis_title = 'TOTAL DE DUELOS AEREOS GANADOS'
        y_axis_title = 'DUELOS AEREOS GANADOS'
    elif selected_filter == 'tiros':
        x_axis_title = 'TOTAL DE TIROS'
        y_axis_title = 'TIROS AL ARCO'
    elif selected_filter == 'perdidas':
        x_axis_title = 'PERDIDAS POR PASE'
        y_axis_title = 'PERDIDAS POR GAMBETA'
    elif selected_filter == 'duelos_1v1':
        x_axis_title = 'TOTAL DE DUELOS 1VS1'
        y_axis_title = 'DUELOS 1VS1 GANADOS'
    elif selected_filter == 'pases':
        x_axis_title = 'TOTAL DE PASES'
        y_axis_title = 'PASES COMPLETOS' 
    elif selected_filter == 'pases_largos':
        x_axis_title = 'PASES LARGOS'
        y_axis_title = 'PASES LARGOS COMPLETOS'               
    elif selected_filter == 'exceso_gambeta':
        y_axis_title = 'duelos 1vs1 ganados'
        x_axis_title = 'Perdidas x gambeta'
    elif selected_filter == 'peligro_esperado':
        x_axis_title = 'Peligro esperado'
        y_axis_title = 'Peligro esperado'
    elif selected_filter == 'peligro_tate':
        x_axis_title = 'Pases Filtrados Efectivos'
        y_axis_title = 'Recepcion a espaldas del volante'
    elif selected_filter == 'regates':
        x_axis_title = 'Intentos de regates'
        y_axis_title = 'Regates efectivos'
    else:
        x_axis_title = ''
        y_axis_title = ''
    
    return x_axis_title, y_axis_title

#CALLBACK PARA TITULOS DEL EJE DEL SCATTER PLOT DEFENSIVO
@app.callback(
    [Output('store-x-axis-titleD', 'data'),
     Output('store-y-axis-titleD', 'data')],
    [Input('dropdown-scatter-plotD', 'value')]
)
def update_axis_titles(selected_filter):
    if selected_filter == 'duelos_aereosD':
        x_axis_title = 'TOTAL DE DUELOS AEREOS'
        y_axis_title = 'DUELOS AEREOS GANADOS'
    elif selected_filter == 'duelos_1v1D':
        x_axis_title = 'TOTAL DE DUELOS 1VS1'
        y_axis_title = 'DUELOS 1VS1 GANADOS'
    elif selected_filter == 'recuperaciones':
        x_axis_title = 'RECUPERACIONES POR INTERVENCIÓN'
        y_axis_title = 'RECUPERACIONES POSICIÓNALES'                 
    else:
        x_axis_title = ''
        y_axis_title = ''
    
    return x_axis_title, y_axis_title



# CALLBACK PARA EL TEXTO DEL CUADRADO ROJO ARRIBA DEL GRAFICO DE BARRAS VERTICAL
@app.callback(
    [Output('effectiveness', 'children'),
     Output('store-x-stat-value', 'data'),
     Output('store-y-stat-value', 'data')],
    [Input('dropdown-scatter-plot', 'value'),
     Input('dropdown-division', 'value'),
     Input('dropdown-partidos', 'value'),
     Input('store-filtro', 'data'),
     Input('dropdown-jugador', 'value')]
)
def update_stats(selected_filter, selected_division, selected_partidos, selected_filtro, selected_jugador):
    if selected_division:
        filtered_df = df[df['División'] == selected_division]
        if selected_partidos:
            filtered_df = filtered_df[filtered_df['Rival'].isin(selected_partidos)]
    else:
        filtered_df = df

    if selected_filtro == 'posicion' and selected_jugador:
        if selected_jugador in df['Jugador'].values:
            posicion = df[df['Jugador'] == selected_jugador]['Posición'].iloc[0]
            filtered_df = filtered_df[filtered_df['Posición'] == posicion]
        else:
            print(f"Jugador {selected_jugador} no encontrado en el DataFrame.")
            return "0%", 0, 0

    if selected_filter == 'duelos_aereos':
        filtered_df['Duelos Aereos Total'] = filtered_df['DAO+']
        y_col = 'Duelos Aereos Total'
        x_col = 'DAOfensivo'
    elif selected_filter == 'tiros':
        y_col = 'Arco'
        x_col = 'Tiros'
    elif selected_filter == 'duelos_1v1':
        x_col = 'Ofensivo'
        y_col = '1v1O+'
    elif selected_filter == 'perdidas':
        x_col = 'PERDIDAS: xPase'
        y_col = 'PERDIDAS: xGambeta'        
    elif selected_filter == 'pases':
        x_col = 'PASES'
        y_col = 'PCompletos'
    elif selected_filter == 'pases_largos':
        x_col = 'PASES LARGOS'
        y_col = 'Largo Completo'        
    elif selected_filter == 'exceso_gambeta':
        x_col = '1v1O+'
        y_col = 'PERDIDAS: xGambeta'
    elif selected_filter == 'peligro_esperado':
        x_col = 'xT'
        y_col = 'xT'
    elif selected_filter == 'peligro_tate':
        x_col = 'Filtrado'
        y_col = 'Recepcion a espaldas del volante'
    elif selected_filter == 'regates':
        x_col = 'Regates'
        y_col = 'R+'
    else:
        return "0%", 0, 0

    if selected_partidos:
        selected_df = filtered_df[filtered_df['Rival'].isin(selected_partidos)]

    grouped_by_rival = selected_df.groupby(['Jugador', 'Rival']).agg({
        'Minutos Jugados': 'first',
        x_col: 'sum',
        y_col: 'sum',
        'Foto': 'first'
    }).reset_index()

    grouped_by_rival.fillna(0, inplace=True)

    if len(selected_partidos) > 1:
        grouped_df = grouped_by_rival.groupby('Jugador').agg({
            'Minutos Jugados': 'sum',
            x_col: 'sum',
            y_col: 'sum',
            'Foto': 'first'
        }).reset_index()
        grouped_df[x_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[x_col]
        grouped_df[y_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[y_col]
    else:
        grouped_df = grouped_by_rival
        grouped_df[x_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[x_col]
        grouped_df[y_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[y_col]

    grouped_df.fillna(0, inplace=True)

    if selected_jugador:
        jugador_data = grouped_df[grouped_df['Jugador'] == selected_jugador]
        if not jugador_data.empty:
            if selected_filter == 'peligro_esperado':
                efectividad_text = "-"
                x_stat_value = "-"
                y_stat_value = "-"
            else:
                efectividad = (jugador_data[y_col].iloc[0] / jugador_data[x_col].iloc[0]) * 100
                efectividad_text = f"{round(efectividad)}%" if not pd.isna(efectividad) else "0%"
                x_stat_value = round(jugador_data[x_col].iloc[0], 3)
                y_stat_value = round(jugador_data[y_col].iloc[0], 3)
        else:
            efectividad_text = "0%"
            x_stat_value = 0
            y_stat_value = 0
    else:
        efectividad_text = "0%"
        x_stat_value = 0
        y_stat_value = 0

    return efectividad_text, x_stat_value, y_stat_value



# CALLBACK PARA EL TEXTO DEL CUADRADO ROJO ARRIBA DEL GRAFICO DE BARRAS VERTICAL DEFENSIVO
@app.callback(
    [Output('effectivenessD', 'children'),
     Output('store-x-stat-valueD', 'data'),
     Output('store-y-stat-valueD', 'data')],
    [Input('dropdown-scatter-plotD', 'value'),
     Input('dropdown-division', 'value'),
     Input('dropdown-partidos', 'value'),
     Input('store-filtro', 'data'),
     Input('dropdown-jugador', 'value')]
)
def update_stats(selected_filter, selected_division, selected_partidos, selected_filtro, selected_jugador):
    if selected_division:
        filtered_df = df[df['División'] == selected_division]
        if selected_partidos:
            filtered_df = filtered_df[filtered_df['Rival'].isin(selected_partidos)]
    else:
        filtered_df = df

    if selected_filtro == 'posicion' and selected_jugador:
        if selected_jugador in df['Jugador'].values:
            posicion = df[df['Jugador'] == selected_jugador]['Posición'].iloc[0]
            filtered_df = filtered_df[filtered_df['Posición'] == posicion]
        else:
            print(f"Jugador {selected_jugador} no encontrado en el DataFrame.")
            return "0%", 0, 0

    if selected_filter == 'duelos_aereosD':
        filtered_df['Duelos Aereos Total'] = filtered_df['DAD+']
        y_col = 'Duelos Aereos Total'
        x_col = 'DADefensivo'
    elif selected_filter == 'duelos_1v1D':
        filtered_df['Duelos 1vs1 Total'] = filtered_df['1v1D+']
        y_col = 'Duelos 1vs1 Total'
        x_col = 'Defensivo'    
    elif selected_filter == 'recuperaciones':
        filtered_df['Recuperaciones'] = filtered_df['RECUPERACION xIntervencion']
        y_col = 'RECUPERACION xIntervencion'
        x_col = 'RECUPERACION xPosicional' 
    else:
        return "0%", 0, 0

    if selected_partidos:
        selected_df = filtered_df[filtered_df['Rival'].isin(selected_partidos)]

    grouped_by_rival = selected_df.groupby(['Jugador', 'Rival']).agg({
        'Minutos Jugados': 'first',
        x_col: 'sum',
        y_col: 'sum',
        'Foto': 'first'
    }).reset_index()

    grouped_by_rival.fillna(0, inplace=True)

    if len(selected_partidos) > 1:
        grouped_df = grouped_by_rival.groupby('Jugador').agg({
            'Minutos Jugados': 'sum',
            x_col: 'sum',
            y_col: 'sum',
            'Foto': 'first'
        }).reset_index()
        grouped_df[x_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[x_col]
        grouped_df[y_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[y_col]
    else:
        grouped_df = grouped_by_rival
        grouped_df[x_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[x_col]
        grouped_df[y_col] = (90 / grouped_df['Minutos Jugados'].replace(0, np.nan)) * grouped_df[y_col]

    grouped_df.fillna(0, inplace=True)

    if selected_jugador:
        jugador_data = grouped_df[grouped_df['Jugador'] == selected_jugador]
        if not jugador_data.empty:
            if selected_filter == 'peligro_esperado':
                efectividad_text = "-"
                x_stat_value = "-"
                y_stat_value = "-"
            else:
                efectividad = (jugador_data[y_col].iloc[0] / jugador_data[x_col].iloc[0]) * 100
                efectividad_text = f"{round(efectividad)}%" if not pd.isna(efectividad) else "0%"
                x_stat_value = round(jugador_data[x_col].iloc[0], 3)
                y_stat_value = round(jugador_data[y_col].iloc[0], 3)
        else:
            efectividad_text = "0%"
            x_stat_value = 0
            y_stat_value = 0
    else:
        efectividad_text = "0%"
        x_stat_value = 0
        y_stat_value = 0

    return efectividad_text, x_stat_value, y_stat_value






# CALLBACK PARA MOSTRAR EL NÚMERO DEL DATO X EN EL CUADRADO ROJO DE LA DERECHA 
@app.callback(
    Output('x-start-value', 'children'),
    [Input('store-x-stat-value', 'data')]
)
def update_x_stat_value(x_stat_value):
    if x_stat_value == "-":
        return "-"
    else:
        return str(round(x_stat_value))



#CALLBACK PARA MOSTRAR EL NUMERO DEL DATO X EN EL CUADRADO ROJO DE LA DERECHA  DEFENSIVO
@app.callback(
    Output('x-start-valueD', 'children'),
    [Input('store-x-stat-valueD', 'data')]
)
def update_x_stat_valueD(x_stat_valueD):
    return str(round(x_stat_valueD))



# CALLBACK PARA MOSTRAR EL NÚMERO DEL DATO Y EN EL CUADRADO ROJO DE LA DERECHA 
@app.callback(
    Output('y-start-value', 'children'),
    [Input('store-y-stat-value', 'data')]
)
def update_x_stat_value(x_stat_value):
    if x_stat_value == "-":
        return "-"
    else:
        return str(round(x_stat_value))

#CALLBACK PARA MOSTRAR EL NUMERO DEL DATO EN EL CUADRADO ROJO DE LA DERECHA DEFENSIVO
@app.callback(
    Output('y-start-valueD', 'children'),
    [Input('store-y-stat-valueD', 'data')]
)
def update_y_stat_valueD(y_stat_valueD):
    return str(round(y_stat_valueD))

# CALLBACK PARA MOSTRAR EL TITULO DEL EJE X EN EL CUADRADO ROJO DE LA DERECHA
@app.callback(
    Output('texto-eje-x', 'children'),
    [Input('store-x-axis-title', 'data')]
)
def update_x_axis_title(x_axis_title):
    return f"{x_axis_title} x90"

# CALLBACK PARA MOSTRAR EL TITULO DEL EJE X EN EL CUADRADO ROJO DE LA DERECHA DEFENSIVO
@app.callback(
    Output('texto-eje-xD', 'children'),
    [Input('store-x-axis-titleD', 'data')]
)
def update_x_axis_titleD(x_axis_titleD):
    return f"{x_axis_titleD} x90"

# CALLBACK PARA MOSTRAR EL TITULO DEL EJE Y EN EL CUADRADO ROJO DE LA DERECHA
@app.callback(
    Output('texto-eje-y', 'children'),
    [Input('store-y-axis-title', 'data')]
)
def update_y_axis_title(y_axis_title):
    return f"{y_axis_title} x90"

# CALLBACK PARA MOSTRAR EL TITULO DEL EJE Y EN EL CUADRADO ROJO DE LA DERECHA DEFENSIVO
@app.callback(
    Output('texto-eje-yD', 'children'),
    [Input('store-y-axis-titleD', 'data')]
)
def update_y_axis_titleD(y_axis_titleD):
    return f"{y_axis_titleD} x90"



import random

from dash.exceptions import PreventUpdate

@app.callback(
    [Output('dropdown-jugador', 'options'),
     Output('dropdown-jugador', 'value'),
     Output('dropdown-partidos', 'options'),
     Output('dropdown-partidos', 'value')],
    [Input('dropdown-division', 'value'),
     Input('dropdown-jugador', 'value')]
)
def update_dropdowns(selected_division, selected_jugador):
    if not selected_division:
        raise PreventUpdate

    # Filtrar los datos por división
    filtered_df = df[df['División'] == selected_division]
    
    # Opciones de jugadores
    jugador_options = [{'label': jugador, 'value': jugador} for jugador in filtered_df['Jugador'].unique()]
    
    # Determinar el jugador seleccionado
    if not selected_jugador or selected_jugador not in filtered_df['Jugador'].unique():
        selected_jugador = filtered_df['Jugador'].unique()[0] if jugador_options else None

    # Opciones y valores para partidos
    if selected_jugador:
        partidos_options = [{'label': partido, 'value': partido} for partido in filtered_df[filtered_df['Jugador'] == selected_jugador]['Rival'].unique()]
        default_partidos = [partido['value'] for partido in partidos_options]
    else:
        partidos_options = []
        default_partidos = []

    return jugador_options, selected_jugador, partidos_options, default_partidos








#CALLBACK NOMBRE DEL JUGADOR EN CARTA PRINCIPAL
@app.callback(
    Output('player-name', 'children'),
    [Input('dropdown-jugador', 'value')]
)
def update_player_name(selected_player):
    return selected_player if selected_player else '-'

#CALLBACK PARA LA IMAGEN DEL JUGADOR EN CARTA PRINCIPAL
@app.callback(
    Output('player-image-container', 'children'),
    [Input('dropdown-jugador', 'value')]
)
def update_player_image(selected_player):
    if selected_player:
        filtered_df = df[df['Jugador'] == selected_player]
        img_url = filtered_df['Foto'].iloc[0]
        return html.Img(src=img_url, className='player-image')
    return html.Div()



# CALLBACK POSICION DEL JUGADOR EN CARTA PRINCIPAL
@app.callback(
    Output('player-position', 'children'),
    [Input('dropdown-jugador', 'value')]
)
def update_player_position(selected_player):
    try:
        if selected_player:
            filtered_df = df[df['Jugador'] == selected_player]
            posicion = filtered_df['Posición especifica'].iloc[0]
            palabras = posicion.split()
            if len(palabras) == 2:
                posicion_formateada = html.Div([
                    html.Span(palabras[0]),
                    html.Span(palabras[1])
                ], className='posicion-vertical')
            else:
                posicion_formateada = posicion

            return posicion_formateada

        else:
            return html.Div("Jugador no seleccionado", className="small-text")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")  # Registra el error completo
        return html.Div("Error al procesar el archivo: " + str(e), className="small-text")  # Devuelve el error completo como texto




# Asegúrate de que la columna Nacimiento es de tipo datetime
df['Nacimiento'] = pd.to_datetime(df['Nacimiento'], errors='coerce')

@app.callback(
    Output('player-fecha', 'children'),
    [Input('dropdown-jugador', 'value')]
)
def update_player_fecha(selected_player):
    try:
        if selected_player:
            filtered_df = df[df['Jugador'] == selected_player]
            nacimiento = filtered_df['Nacimiento'].iloc[0]
            if pd.isna(nacimiento):
                return html.Div("Fecha de nacimiento no disponible", className="small-text")
            # Formatear la fecha como cadena de texto
            return nacimiento.strftime('%d/%m/%Y')  # Cambia el formato según tus necesidades
        else:
            return html.Div("Jugador no seleccionado", className="small-text")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return html.Div("Error al procesar el archivo", className="small-text")
    


#CALLBACK MINUTOS DEL JUGADOR EN CARTA PRINCIPAL
@app.callback(
    Output('player-minutos', 'children'),
    [Input('dropdown-jugador', 'value')]
)
def update_player_fecha(selected_player):
    try:
        if selected_player:
            filtered_df = df[df['Jugador'] == selected_player]
            nacimiento = filtered_df['Minutos Jugados'].iloc[0]
            return nacimiento
        else:
            return html.Div("Jugador no seleccionado", className="small-text")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return html.Div("Error al procesar el archivo", className="small-text")
    

    

#CALLBACK DE PIE HABIL DEL JUGADOR EN CARTA PRINCIPAL
@app.callback(
    Output('player-pie', 'children'),
    [Input('dropdown-jugador', 'value')]
)
def update_player_pie(selected_player):
    try:
        if selected_player:
            filtered_df = df[df['Jugador'] == selected_player]
            pie = filtered_df['Pie habil'].iloc[0]
            pie = pie[:-1]  # Elimina el último carácter
            return pie
        else:
            return html.Div("Jugador no seleccionado", className="small-text")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return html.Div("Error al procesar el archivo", className="small-text")


# CALLBACK SUMA DE PARTIDOS JUGADOS DEL JUGADOR EN CARTA PRINCIPAL
@app.callback(
    Output('player-pj', 'children'),
    [Input('dropdown-jugador', 'value'),
     Input('dropdown-partidos', 'value')]  # Agregar el filtro de partidos
)
def update_player_fecha(selected_player, selected_partidos):
    try:
        if selected_player:
            # Filtra el DataFrame para el jugador seleccionado
            player_data = grouped_df[grouped_df['Jugador'] == selected_player]
            
            # Si hay un filtro de partidos, aplica el filtro
            if selected_partidos:
                player_data = player_data[player_data['Rival'].isin(selected_partidos)]
            
            # Cuenta la cantidad de partidos jugados
            player_count = player_data.shape[0]
            
            # Suma los minutos jugados
            total_minutes = round(player_data['Minutos Jugados'].sum())
            
            return html.Span([
                f"{player_count} ",
                html.Span(f"({total_minutes} minutos)", className="small-text")
            ])
        else:
            return html.Div("Jugador no seleccionado", className="small-text")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return html.Div("Error al procesar el archivo", className="small-text")




# CALLBACK SUMA DE ASISTENCIAS DEL JUGADOR EN CARTA PRINCIPAL
@app.callback(
    Output('player-asistencias', 'children'),
    [Input('dropdown-jugador', 'value')]
)
def update_player_asistencias(selected_player):
    try:
        if selected_player:
            # Filtra el DataFrame para el jugador seleccionado
            player_data = df[df['Jugador'] == selected_player]
            
            # Suma las asistencias de ambas columnas
            total_asistencias = player_data['PAsistencia'].sum() + player_data['CAsistencia'].sum()
            
            return f"{total_asistencias}"
        else:
            return html.Div("Jugador no seleccionado", className="small-text")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return html.Div("Error al procesar el archivo", className="small-text")


# CALLBACK SUMA DE GOLES DEL JUGADOR EN CARTA PRINCIPAL
@app.callback(
    Output('player-goles', 'children'),
    [Input('dropdown-jugador', 'value')]
)
def update_player_asistencias(selected_player):
    try:
        if selected_player:
            # Filtra el DataFrame para el jugador seleccionado
            player_data = df[df['Jugador'] == selected_player]
            
            # Suma las asistencias
            total_asistencias = player_data['Gol'].sum()
            
            return f"{total_asistencias}"
        else:
            return html.Div("Jugador no seleccionado", className="small-text")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return html.Div("Error al procesar el archivo", className="small-text")






# PIZZA CHART
@app.callback(
    Output('radar-chart-container', 'children'),
    [Input('dropdown-jugador', 'value'),
     Input('dropdown-partidos', 'value'),
     Input('store-filtro', 'data')]
)
def update_barras(selected_player, selected_partidos, selected_filtro):
    radar_chart = []  # Lista para almacenar los componentes del radar chart

    # Definir los valores por defecto en 0
    params = [
        'Remates al arco', 'Duelo 1v1 of.', 'Duelo Aereo of.', 'Pases Clave', 'Regates', 
        'Duelo Aereo def.', 'Intervencion Defensiva', 'Duelo 1v1 def.', 'Recuperaciones', 
        'Recepcion Entre Lineas', 'Toques en Area Rival'
    ]
    default_values = [0] * len(params)
    slice_colors = ["#8a7171"] * 5 + ["#000000"] * 4 + ["#B8BAB8"] * 2 
    text_colors = ["#ffffff"] * len(params)

    try:
        # Si no hay partidos seleccionados, mostrar valores por defecto
        if not selected_partidos:
            values = default_values
        else:
            # Filtra el DataFrame por el jugador seleccionado y los partidos seleccionados
            jugador_df = df[(df['Jugador'] == selected_player) & (df['Rival'].isin(selected_partidos))]

            if not jugador_df.empty:
                if len(selected_partidos) == 1:
                    # Si se selecciona solo un partido, tomar los minutos jugados de ese partido
                    M_jugados = jugador_df.iloc[0]['Minutos Jugados']
                    # Suma las acciones del partido seleccionado
                    jugador_df['recuperaciones'] = jugador_df['RECUPERACION xIntervencion'] + jugador_df['RECUPERACION xPosicional']
                    values_sum = jugador_df[['Arco', 'Ofensivo', 'DAOfensivo', 'Clave', 'Regates', 'DADefensivo', 'Intervencion Defensiva', 'Defensivo', 'recuperaciones', 'Recepcion entre Lineas', 'Toques en Area Rival']].sum()
                    # Aplica la fórmula a cada valor y redondea los resultados
                    values = [round((90 / M_jugados) * value) for value in values_sum]
                else:
                    # Si se seleccionan múltiples partidos, sumar los minutos jugados y las acciones de todos los partidos
                    M_jugados_total = jugador_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()
                    jugador_df['recuperaciones'] = jugador_df['RECUPERACION xIntervencion'] + jugador_df['RECUPERACION xPosicional']
                    values_sum = jugador_df[['Arco', 'Ofensivo', 'DAOfensivo', 'Clave', 'Regates', 'DADefensivo', 'Intervencion Defensiva', 'Defensivo', 'recuperaciones', 'Recepcion entre Lineas', 'Toques en Area Rival']].sum()
                    # Aplica la fórmula a cada valor y redondea los resultados
                    values = [round((90 / M_jugados_total) * value) for value in values_sum]
            else:
                values = default_values
    except Exception as e:
        # Maneja la excepción mostrando un mensaje adecuado al usuario
        print(f"Error al procesar el archivo: {e}")
        values = default_values

    # Define los parámetros y valores para el gráfico de pizza
    baker = PyPizza(
        params=params,
        background_color="#ED192D",
        straight_line_color="#ED192D",
        straight_line_lw=1,
        last_circle_lw=0,
        other_circle_lw=0,
        inner_circle_size=5,
    )

    # Genera el gráfico de pizza
    fig, ax = baker.make_pizza(
        values,
        figsize=(4.2, 4.4),
        color_blank_space="same",
        slice_colors=slice_colors,
        value_colors=text_colors,
        value_bck_colors=slice_colors,
        blank_alpha=0.4,
        kwargs_slices=dict(
            edgecolor="#F2F2F2", zorder=2, linewidth=1
        ),
        kwargs_params=dict(
            color="#ffffff",
            fontsize=10,
            va="center"
        ),
        kwargs_values=dict(
            color="#ffffff", fontsize=11,
            zorder=3,
            bbox=dict(
                edgecolor="#ffffff", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        )
    )

    # Establece los límites del eje y
    ax.set_ylim(0, 10)

    # Ajusta las posiciones de los textos y divide los textos largos en dos líneas
    for txt in ax.texts:
        x, y = txt.get_position()
        # Ajusta la posición y para mantener el texto dentro del gráfico
        if y > 15:
            txt.set_position((x, 13))
        # Divide los textos largos en dos líneas
        if len(txt.get_text()) > 15:
            lines = txt.get_text().split(' ')
            if len(lines) == 1:
                txt.set_text('\n'.join([lines[0][:5], lines[0][5:]]))
            else:
                txt.set_text('\n'.join(lines))

    # Convertir la figura de Matplotlib a una imagen base64
    img_data = io.BytesIO()
    fig.savefig(img_data, format='png')
    img_data.seek(0)
    encoded_img = base64.b64encode(img_data.getvalue()).decode('utf-8')

    # Genera el componente de imagen HTML para mostrar en Dash
    radar_chart.append(html.Img(src='data:image/png;base64,{}'.format(encoded_img)))

    return radar_chart






#CALLBACK BOTONES POSICION!DIVISION
@app.callback(
    Output('store-filtro', 'data'),
    [Input('button-posicion', 'n_clicks'),
     Input('button-division', 'n_clicks')]
)
def actualizar_filtro(n_clicks_posicion, n_clicks_division):
    ctx = dash.callback_context

    if not ctx.triggered:
        return 'division'
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'button-posicion':
        return 'posicion'
    elif button_id == 'button-division':
        return 'division'
    else:
        return 'division'

# Callback para actualizar los estilos de los botones
@app.callback(
    [Output('button-posicion', 'className'),
     Output('button-division', 'className')],
    [Input('store-filtro', 'data')])
def update_button_classes(selected_filter):
    if selected_filter == 'posicion':
        return 'button button-selected', 'button'
    elif selected_filter == 'division':
        return 'button', 'button button-selected'
    else:
        return 'button', 'button'









#GRAFICO DE BARRAS DUELOS AEREOS
@app.callback(
    Output('barras-duelos-aereos', 'children'),
    [Input('dropdown-jugador', 'value'),
     Input('dropdown-partidos', 'value'),
     Input('store-filtro', 'data')]
)
def update_barras(selected_player, selected_partidos, selected_filtro):
    if not selected_player:
        return None

    default_value = 0
    max_value = 10

    try:
        if selected_partidos:
            jugador_df = df[(df['Jugador'] == selected_player) & (df['Rival'].isin(selected_partidos))]
        else:
            jugador_df = df[df['Jugador'] == selected_player]

        if jugador_df.empty:
            player_value = default_value
            suma_filtro = default_value
        else:
            # Calcular los minutos jugados del jugador seleccionado
            M_jugados_total = jugador_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()
            # Si no se selecciona un filtro válido, calcular la suma general de "DAO+"
            suma_filtro = df['DAO+'].sum() - jugador_df['DAO+'].sum()

        if selected_filtro == 'posicion':
            # Calcular la suma de "DAO+" según la posición del jugador y los partidos seleccionados
            position_filtered_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0])]
            if selected_partidos:
                position_filtered_df = position_filtered_df[position_filtered_df['Rival'].isin(selected_partidos)]
            suma_filtro = position_filtered_df['DAO+'].sum() - jugador_df['DAO+'].sum()
            # Calcular el número de jugadores en la posición del jugador seleccionado, excluyendo al jugador seleccionado
            num_jugadores = position_filtered_df['Jugador'].nunique() - 1
        elif selected_filtro == 'division':
            # Calcular la suma de "DAO+" según la división y los partidos seleccionados
            division_filtered_df = df[df['Rival'].isin(selected_partidos)]
            suma_filtro = division_filtered_df['DAO+'].sum() - jugador_df['DAO+'].sum()
            # Calcular el número de jugadores en la división seleccionada, excluyendo al jugador seleccionado
            num_jugadores = division_filtered_df['Jugador'].nunique() - 1

        # Asegurarse de que num_jugadores no sea menor a 1 para evitar división por cero
        if num_jugadores < 1:
            num_jugadores = 1

        # Calcular los minutos jugados de los partidos seleccionados para la posición/división R+
        if selected_partidos:
            if selected_filtro == 'posicion':
                filtered_partidos_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0]) & (df['Rival'].isin(selected_partidos))]
            elif selected_filtro == 'division':
                filtered_partidos_df = df[df['Rival'].isin(selected_partidos)]
            M_jugados_filtered = filtered_partidos_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()

            # Calcular la suma de acciones dividida por los minutos jugados de los partidos seleccionados
            suma_filtro = round((90 / M_jugados_filtered) * suma_filtro)

        # Dividir la suma_filtro por el número de jugadores
        if num_jugadores > 0:
            suma_filtro = suma_filtro / num_jugadores

        promedio = suma_filtro / 2
        # Calcular el valor del jugador basado en los minutos jugados
        player_value = round((90 / M_jugados_total) * jugador_df['DAO+'].sum())

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        player_value = default_value
        suma_filtro = default_value

    # Crear figura de gráfico de barras
    fig = go.Figure()

    # Agregar la barra del jugador con el texto dentro de la barra
    fig.add_trace(go.Bar(
        y=['DAO+'],
        x=[player_value],
        orientation='h',
        marker=dict(color='#ED192D'),
        name='Jugador',
        text=[player_value],  # Añadir el valor del jugador como texto
        textposition='inside'  # Posicionar el texto dentro de la barra
    ))

    # Añadir una línea negra que muestra el promedio de 'DAO+' según el filtro seleccionado
    fig.add_shape(
        type="line",
        x0=suma_filtro,
        x1=suma_filtro,
        y0=-0.5,
        y1=0.5,
        line=dict(color="Black", width=4)  
    )

    fig.update_layout(
        xaxis=dict(showticklabels=False, range=[0, max_value + 2]),  # Añade un poco de espacio al final
        yaxis=dict(showticklabels=False),
        margin=dict(t=0, b=0, l=0, r=0),  # Reduce los márgenes
        paper_bgcolor='#ED192D',  # Fondo rojo
        plot_bgcolor='white',  # Fondo del gráfico blanco
        width=250,  # Ajusta el ancho del gráfico
        height=40,  # Ajusta la altura del gráfico
        dragmode=False,  # Deshabilitar el modo de arrastre
        modebar=dict(
            remove=['zoom', 'pan', 'select', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toImage']
        )  # Remover herramientas específicas, incluyendo 'toImage' para eliminar 'Download plot as PNG'
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False}) 


#GRAFICO DE BARRAS DUELOS AEREOS
@app.callback(
    Output('barras-duelos-aereosD', 'children'),
    [Input('dropdown-jugador', 'value'),
     Input('dropdown-partidos', 'value'),
     Input('store-filtro', 'data')]
)
def update_barras(selected_player, selected_partidos, selected_filtro):
    if not selected_player:
        return None

    default_value = 0
    max_value = 10

    try:
        if selected_partidos:
            jugador_df = df[(df['Jugador'] == selected_player) & (df['Rival'].isin(selected_partidos))]
        else:
            jugador_df = df[df['Jugador'] == selected_player]

        if jugador_df.empty:
            player_value = default_value
            suma_filtro = default_value
        else:
            # Calcular los minutos jugados del jugador seleccionado
            M_jugados_total = jugador_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()
            # Si no se selecciona un filtro válido, calcular la suma general de "DAD+"
            suma_filtro = df['DAD+'].sum() - jugador_df['DAD+'].sum()

        if selected_filtro == 'posicion':
            # Calcular la suma de "DAD+" según la posición del jugador y los partidos seleccionados
            position_filtered_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0])]
            if selected_partidos:
                position_filtered_df = position_filtered_df[position_filtered_df['Rival'].isin(selected_partidos)]
            suma_filtro = position_filtered_df['DAD+'].sum() - jugador_df['DAD+'].sum()
            # Calcular el número de jugadores en la posición del jugador seleccionado, excluyendo al jugador seleccionado
            num_jugadores = position_filtered_df['Jugador'].nunique() - 1
        elif selected_filtro == 'division':
            # Calcular la suma de "DAD+" según la división y los partidos seleccionados
            division_filtered_df = df[df['Rival'].isin(selected_partidos)]
            suma_filtro = division_filtered_df['DAD+'].sum() - jugador_df['DAD+'].sum()
            # Calcular el número de jugadores en la división seleccionada, excluyendo al jugador seleccionado
            num_jugadores = division_filtered_df['Jugador'].nunique() - 1

        # Asegurarse de que num_jugadores no sea menor a 1 para evitar división por cero
        if num_jugadores < 1:
            num_jugadores = 1

        # Calcular los minutos jugados de los partidos seleccionados para la posición/división R+
        if selected_partidos:
            if selected_filtro == 'posicion':
                filtered_partidos_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0]) & (df['Rival'].isin(selected_partidos))]
            elif selected_filtro == 'division':
                filtered_partidos_df = df[df['Rival'].isin(selected_partidos)]
            M_jugados_filtered = filtered_partidos_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()

            # Calcular la suma de acciones dividida por los minutos jugados de los partidos seleccionados
            suma_filtro = round((90 / M_jugados_filtered) * suma_filtro)

        # Dividir la suma_filtro por el número de jugadores
        if num_jugadores > 0:
            suma_filtro = suma_filtro / num_jugadores

        promedio = suma_filtro / 2
        # Calcular el valor del jugador basado en los minutos jugados
        player_value = round((90 / M_jugados_total) * jugador_df['DAD+'].sum())

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        player_value = default_value
        suma_filtro = default_value

    # Crear figura de gráfico de barras
    fig = go.Figure()

    # Agregar la barra del jugador con el texto dentro de la barra
    fig.add_trace(go.Bar(
        y=['DAD+'],
        x=[player_value],
        orientation='h',
        marker=dict(color='#ED192D'),
        name='Jugador',
        text=[player_value],  # Añadir el valor del jugador como texto
        textposition='inside'  # Posicionar el texto dentro de la barra
    ))

    # Añadir una línea negra que muestra el promedio de 'DAD+' según el filtro seleccionado
    fig.add_shape(
        type="line",
        x0=suma_filtro,
        x1=suma_filtro,
        y0=-0.5,
        y1=0.5,
        line=dict(color="Black", width=4)  
    )

    fig.update_layout(
        xaxis=dict(showticklabels=False, range=[0, max_value + 2]),  # Añade un poco de espacio al final
        yaxis=dict(showticklabels=False),
        margin=dict(t=0, b=0, l=0, r=0),  # Reduce los márgenes
        paper_bgcolor='#ED192D',  # Fondo rojo
        plot_bgcolor='white',  # Fondo del gráfico blanco
        width=250,  # Ajusta el ancho del gráfico
        height=40,  # Ajusta la altura del gráfico
        dragmode=False,  # Deshabilitar el modo de arrastre
        modebar=dict(
            remove=['zoom', 'pan', 'select', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toImage']
        )  # Remover herramientas específicas, incluyendo 'toImage' para eliminar 'Download plot as PNG'
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False}) 



#GRAFICO DE BARRAS 1VS1 OFENSIVO +
@app.callback(
    Output('barras-1v1-ofensivo', 'children'),
    [Input('dropdown-jugador', 'value'),
     Input('dropdown-partidos', 'value'),
     Input('store-filtro', 'data')]
)
def update_barras(selected_player, selected_partidos, selected_filtro):
    if not selected_player:
        return None

    default_value = 0
    max_value = 10

    try:
        if selected_partidos:
            jugador_df = df[(df['Jugador'] == selected_player) & (df['Rival'].isin(selected_partidos))]
        else:
            jugador_df = df[df['Jugador'] == selected_player]

        if jugador_df.empty:
            player_value = default_value
            suma_filtro = default_value
        else:
            # Calcular los minutos jugados del jugador seleccionado
            M_jugados_total = jugador_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()
            # Si no se selecciona un filtro válido, calcular la suma general de "1v1O+"
            suma_filtro = df['1v1O+'].sum() - jugador_df['1v1O+'].sum()

            if selected_filtro == 'posicion':
                # Calcular la suma de "1v1O+" según la posición del jugador y los partidos seleccionados
                position_filtered_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0])]
                if selected_partidos:
                    position_filtered_df = position_filtered_df[position_filtered_df['Rival'].isin(selected_partidos)]
                suma_filtro = position_filtered_df['1v1O+'].sum() - jugador_df['1v1O+'].sum()
                # Calcular el número de jugadores en la posición del jugador seleccionado
                num_jugadores = position_filtered_df['Jugador'].nunique()
            elif selected_filtro == 'division':
                # Calcular la suma de "1v1O+" según la división y los partidos seleccionados
                division_filtered_df = df[df['Rival'].isin(selected_partidos)]
                suma_filtro = division_filtered_df['1v1O+'].sum() - jugador_df['1v1O+'].sum()
                # Calcular el número de jugadores en la división seleccionada
                num_jugadores = division_filtered_df['Jugador'].nunique()

            # Calcular los minutos jugados de los partidos seleccionados para la posición/división
            if selected_partidos:
                if selected_filtro == 'posicion':
                    filtered_partidos_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0]) & (df['Rival'].isin(selected_partidos))]
                elif selected_filtro == 'division':
                    filtered_partidos_df = df[df['Rival'].isin(selected_partidos)]
                M_jugados_filtered = filtered_partidos_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()

                # Calcular la suma de acciones dividida por los minutos jugados de los partidos seleccionados
                suma_filtro = round((90 / M_jugados_filtered) * suma_filtro)

            # Dividir la suma_filtro por el número de jugadores
            if num_jugadores > 0:
                suma_filtro = suma_filtro / num_jugadores

            promedio = suma_filtro / 2
            # Calcular el valor del jugador basado en los minutos jugados
            player_value = round((90 / M_jugados_total) * jugador_df['1v1O+'].sum())

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        player_value = default_value
        suma_filtro = default_value

    # Crear figura de gráfico de barras
    fig = go.Figure()

    # Agregar la barra del jugador con el texto dentro de la barra
    fig.add_trace(go.Bar(
        y=['1v1O+'],
        x=[player_value],
        orientation='h',
        marker=dict(color='#ED192D'),
        name='Jugador',
        text=[player_value],  # Añadir el valor del jugador como texto
        textposition='inside'  # Posicionar el texto dentro de la barra
    ))

    # Añadir una línea negra que muestra el promedio de '1v1O+' según el filtro seleccionado
    fig.add_shape(
        type="line",
        x0=suma_filtro,
        x1=suma_filtro,
        y0=-0.5,
        y1=0.5,
        line=dict(color="Black", width=4)  
    )

    fig.update_layout(
        xaxis=dict(showticklabels=False, range=[0, max_value + 2]),  # Añade un poco de espacio al final
        yaxis=dict(showticklabels=False),
        margin=dict(t=0, b=0, l=0, r=0),  # Reduce los márgenes
        paper_bgcolor='#ED192D',  # Fondo rojo
        plot_bgcolor='white',  # Fondo del gráfico blanco
        width=250,  # Ajusta el ancho del gráfico
        height=40,  # Ajusta la altura del gráfico
        dragmode=False,  # Deshabilitar el modo de arrastre
        modebar=dict(
            remove=['zoom', 'pan', 'select', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toImage']
        )  # Remover herramientas específicas, incluyendo 'toImage' para eliminar 'Download plot as PNG'
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False}) 

#GRAFICO DE BARRAS 1VS1 DEFENSIVO +
@app.callback(
    Output('barras-1v1-ofensivoD', 'children'),
    [Input('dropdown-jugador', 'value'),
     Input('dropdown-partidos', 'value'),
     Input('store-filtro', 'data')]
)
def update_barras(selected_player, selected_partidos, selected_filtro):
    if not selected_player:
        return None

    default_value = 0
    max_value = 10

    try:
        if selected_partidos:
            jugador_df = df[(df['Jugador'] == selected_player) & (df['Rival'].isin(selected_partidos))]
        else:
            jugador_df = df[df['Jugador'] == selected_player]

        if jugador_df.empty:
            player_value = default_value
            suma_filtro = default_value
        else:
            # Calcular los minutos jugados del jugador seleccionado
            M_jugados_total = jugador_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()
            # Si no se selecciona un filtro válido, calcular la suma general de "1v1O+"
            suma_filtro = df['1v1D+'].sum() - jugador_df['1v1D+'].sum()

            if selected_filtro == 'posicion':
                # Calcular la suma de "1v1O+" según la posición del jugador y los partidos seleccionados
                position_filtered_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0])]
                if selected_partidos:
                    position_filtered_df = position_filtered_df[position_filtered_df['Rival'].isin(selected_partidos)]
                suma_filtro = position_filtered_df['1v1D+'].sum() - jugador_df['1v1D+'].sum()
                # Calcular el número de jugadores en la posición del jugador seleccionado
                num_jugadores = position_filtered_df['Jugador'].nunique()
            elif selected_filtro == 'division':
                # Calcular la suma de "1v1D+" según la división y los partidos seleccionados
                division_filtered_df = df[df['Rival'].isin(selected_partidos)]
                suma_filtro = division_filtered_df['1v1D+'].sum() - jugador_df['1v1D+'].sum()
                # Calcular el número de jugadores en la división seleccionada
                num_jugadores = division_filtered_df['Jugador'].nunique()

            # Calcular los minutos jugados de los partidos seleccionados para la posición/división
            if selected_partidos:
                if selected_filtro == 'posicion':
                    filtered_partidos_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0]) & (df['Rival'].isin(selected_partidos))]
                elif selected_filtro == 'division':
                    filtered_partidos_df = df[df['Rival'].isin(selected_partidos)]
                M_jugados_filtered = filtered_partidos_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()

                # Calcular la suma de acciones dividida por los minutos jugados de los partidos seleccionados
                suma_filtro = round((90 / M_jugados_filtered) * suma_filtro)

            # Dividir la suma_filtro por el número de jugadores
            if num_jugadores > 0:
                suma_filtro = suma_filtro / num_jugadores

            promedio = suma_filtro / 2
            # Calcular el valor del jugador basado en los minutos jugados
            player_value = round((90 / M_jugados_total) * jugador_df['1v1D+'].sum())

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        player_value = default_value
        suma_filtro = default_value

    # Crear figura de gráfico de barras
    fig = go.Figure()

    # Agregar la barra del jugador con el texto dentro de la barra
    fig.add_trace(go.Bar(
        y=['1v1D+'],
        x=[player_value],
        orientation='h',
        marker=dict(color='#ED192D'),
        name='Jugador',
        text=[player_value],  # Añadir el valor del jugador como texto
        textposition='inside'  # Posicionar el texto dentro de la barra
    ))

    # Añadir una línea negra que muestra el promedio de '1v1O+' según el filtro seleccionado
    fig.add_shape(
        type="line",
        x0=suma_filtro,
        x1=suma_filtro,
        y0=-0.5,
        y1=0.5,
        line=dict(color="Black", width=4)  
    )

    fig.update_layout(
        xaxis=dict(showticklabels=False, range=[0, max_value + 2]),  # Añade un poco de espacio al final
        yaxis=dict(showticklabels=False),
        margin=dict(t=0, b=0, l=0, r=0),  # Reduce los márgenes
        paper_bgcolor='#ED192D',  # Fondo rojo
        plot_bgcolor='white',  # Fondo del gráfico blanco
        width=250,  # Ajusta el ancho del gráfico
        height=40,  # Ajusta la altura del gráfico
        dragmode=False,  # Deshabilitar el modo de arrastre
        modebar=dict(
            remove=['zoom', 'pan', 'select', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toImage']
        )  # Remover herramientas específicas, incluyendo 'toImage' para eliminar 'Download plot as PNG'
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False}) 


#GRAFICO DE BARRAS FILTRADO
@app.callback(
    Output('barras-indice-tactico', 'children'),
    [Input('dropdown-jugador', 'value'),
     Input('dropdown-partidos', 'value'),
     Input('store-filtro', 'data')]
)
def update_barras(selected_player, selected_partidos, selected_filtro):
    if not selected_player:
        return None

    default_value = 0
    max_value = 10

    try:
        if selected_partidos:
            jugador_df = df[(df['Jugador'] == selected_player) & (df['Rival'].isin(selected_partidos))]
        else:
            jugador_df = df[df['Jugador'] == selected_player]

        if jugador_df.empty:
            player_value = default_value
            suma_filtro = default_value
        else:
            # Calcular el valor de la columna Filtrado para el jugador seleccionado
            jugador_df['Filtrado'] = jugador_df['Recepcion entre Lineas'] + jugador_df['Toques en Area Rival'] + jugador_df['Recepcion a espaldas del volante'] + jugador_df['Roptura en conduccion'] + jugador_df['Recepción al espacio']
            M_jugados_total = jugador_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()
            # Si no se selecciona un filtro válido, calcular la suma general del valor Filtrado
            suma_filtro = df[['Recepcion entre Lineas', 'Toques en Area Rival', 'Recepcion a espaldas del volante', 'Roptura en conduccion', 'Recepción al espacio']].sum().sum() - jugador_df['Filtrado'].sum()

        if selected_filtro == 'posicion':
            # Calcular el valor Filtrado según la posición del jugador y los partidos seleccionados
            position_filtered_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0])]
            if selected_partidos:
                position_filtered_df = position_filtered_df[position_filtered_df['Rival'].isin(selected_partidos)]
            position_filtered_df['Filtrado'] = position_filtered_df['Recepcion entre Lineas'] + position_filtered_df['Toques en Area Rival'] + position_filtered_df['Recepcion a espaldas del volante'] + position_filtered_df['Roptura en conduccion'] + position_filtered_df['Recepción al espacio']
            suma_filtro = position_filtered_df['Filtrado'].sum() - jugador_df['Filtrado'].sum()
            num_jugadores = position_filtered_df['Jugador'].nunique() - 1
        elif selected_filtro == 'division':
            # Calcular el valor Filtrado según la división y los partidos seleccionados
            division_filtered_df = df[df['Rival'].isin(selected_partidos)]
            division_filtered_df['Filtrado'] = division_filtered_df['Recepcion entre Lineas'] + division_filtered_df['Toques en Area Rival'] + division_filtered_df['Recepcion a espaldas del volante'] + division_filtered_df['Roptura en conduccion'] + division_filtered_df['Recepción al espacio']
            suma_filtro = division_filtered_df['Filtrado'].sum() - jugador_df['Filtrado'].sum()
            num_jugadores = division_filtered_df['Jugador'].nunique() - 1

        if num_jugadores < 1:
            num_jugadores = 1

        if selected_partidos:
            if selected_filtro == 'posicion':
                filtered_partidos_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0]) & (df['Rival'].isin(selected_partidos))]
            elif selected_filtro == 'division':
                filtered_partidos_df = df[df['Rival'].isin(selected_partidos)]
            M_jugados_filtered = filtered_partidos_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()
            suma_filtro = round((90 / M_jugados_filtered) * suma_filtro)

        if num_jugadores > 0:
            suma_filtro = suma_filtro / num_jugadores

        promedio = suma_filtro / 2
        player_value = round((90 / M_jugados_total) * jugador_df['Filtrado'].sum())

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        player_value = default_value
        suma_filtro = default_value

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=['Filtrado'],
        x=[player_value],
        orientation='h',
        marker=dict(color='#ED192D'),
        name='Jugador',
        text=[player_value],
        textposition='inside'
    ))

    fig.add_shape(
        type="line",
        x0=suma_filtro,
        x1=suma_filtro,
        y0=-0.5,
        y1=0.5,
        line=dict(color="Black", width=4)  
    )

    fig.update_layout(
        xaxis=dict(showticklabels=False, range=[0, max_value + 2]),
        yaxis=dict(showticklabels=False),
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor='#ED192D',
        plot_bgcolor='white',
        width=250,
        height=40,
        dragmode=False,
        modebar=dict(
            remove=['zoom', 'pan', 'select', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toImage']
        )
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False})


#GRAFICO DE BARRAS TIROS AL ARCO
@app.callback(
    Output('barras-tiros-arco', 'children'),
    [Input('dropdown-jugador', 'value'),
     Input('dropdown-partidos', 'value'),
     Input('store-filtro', 'data')]
)
def update_barras(selected_player, selected_partidos, selected_filtro):
    if not selected_player:
        return None

    default_value = 0
    max_value = 10

    try:
        if selected_partidos:
            jugador_df = df[(df['Jugador'] == selected_player) & (df['Rival'].isin(selected_partidos))]
        else:
            jugador_df = df[df['Jugador'] == selected_player]

        if jugador_df.empty:
            player_value = default_value
            suma_filtro = default_value
        else:
            # Calcular los minutos jugados del jugador seleccionado
            M_jugados_total = jugador_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()
            # Si no se selecciona un filtro válido, calcular la suma general de "Arco"
            suma_filtro = df['Arco'].sum() - jugador_df['Arco'].sum()

        if selected_filtro == 'posicion':
            # Calcular la suma de "Arco" según la posición del jugador y los partidos seleccionados
            position_filtered_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0])]
            if selected_partidos:
                position_filtered_df = position_filtered_df[position_filtered_df['Rival'].isin(selected_partidos)]
            suma_filtro = position_filtered_df['Arco'].sum() - jugador_df['Arco'].sum()
            # Calcular el número de jugadores en la posición del jugador seleccionado, excluyendo al jugador seleccionado
            num_jugadores = position_filtered_df['Jugador'].nunique() - 1
        elif selected_filtro == 'division':
            # Calcular la suma de "Arco" según la división y los partidos seleccionados
            division_filtered_df = df[df['Rival'].isin(selected_partidos)]
            suma_filtro = division_filtered_df['Arco'].sum() - jugador_df['Arco'].sum()
            # Calcular el número de jugadores en la división seleccionada, excluyendo al jugador seleccionado
            num_jugadores = division_filtered_df['Jugador'].nunique() - 1

        # Asegurarse de que num_jugadores no sea menor a 1 para evitar división por cero
        if num_jugadores < 1:
            num_jugadores = 1

        # Calcular los minutos jugados de los partidos seleccionados para la posición/división R+
        if selected_partidos:
            if selected_filtro == 'posicion':
                filtered_partidos_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0]) & (df['Rival'].isin(selected_partidos))]
            elif selected_filtro == 'division':
                filtered_partidos_df = df[df['Rival'].isin(selected_partidos)]
            M_jugados_filtered = filtered_partidos_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()

            # Calcular la suma de acciones dividida por los minutos jugados de los partidos seleccionados
            suma_filtro = round((90 / M_jugados_filtered) * suma_filtro)

        # Dividir la suma_filtro por el número de jugadores
        if num_jugadores > 0:
            suma_filtro = suma_filtro / num_jugadores

        promedio = suma_filtro / 2
        # Calcular el valor del jugador basado en los minutos jugados
        player_value = round((90 / M_jugados_total) * jugador_df['Arco'].sum())

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        player_value = default_value
        suma_filtro = default_value

    # Crear figura de gráfico de barras
    fig = go.Figure()

    # Agregar la barra del jugador con el texto dentro de la barra
    fig.add_trace(go.Bar(
        y=['Arco'],
        x=[player_value],
        orientation='h',
        marker=dict(color='#ED192D'),
        name='Jugador',
        text=[player_value],  # Añadir el valor del jugador como texto
        textposition='inside'  # Posicionar el texto dentro de la barra
    ))

    # Añadir una línea negra que muestra el promedio de 'Arco' según el filtro seleccionado
    fig.add_shape(
        type="line",
        x0=suma_filtro,
        x1=suma_filtro,
        y0=-0.5,
        y1=0.5,
        line=dict(color="Black", width=4)  
    )

    fig.update_layout(
        xaxis=dict(showticklabels=False, range=[0, max_value + 2]),  # Añade un poco de espacio al final
        yaxis=dict(showticklabels=False),
        margin=dict(t=0, b=0, l=0, r=0),  # Reduce los márgenes
        paper_bgcolor='#ED192D',  # Fondo rojo
        plot_bgcolor='white',  # Fondo del gráfico blanco
        width=250,  # Ajusta el ancho del gráfico
        height=40,  # Ajusta la altura del gráfico
        dragmode=False,  # Deshabilitar el modo de arrastre
        modebar=dict(
            remove=['zoom', 'pan', 'select', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toImage']
        )  # Remover herramientas específicas, incluyendo 'toImage' para eliminar 'Download plot as PNG'
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False}) 


#GRAFICO DE BARRAS REGATES OFENSIVO +
@app.callback(
    Output('barras-regates-ofensivo', 'children'),
    [Input('dropdown-jugador', 'value'),
     Input('dropdown-partidos', 'value'),
     Input('store-filtro', 'data')]
)
def update_barras(selected_player, selected_partidos, selected_filtro):
    if not selected_player:
        return None

    default_value = 0
    max_value = 10

    try:
        if selected_partidos:
            jugador_df = df[(df['Jugador'] == selected_player) & (df['Rival'].isin(selected_partidos))]
        else:
            jugador_df = df[df['Jugador'] == selected_player]

        if jugador_df.empty:
            player_value = default_value
            suma_filtro = default_value
        else:
            # Calcular los minutos jugados del jugador seleccionado
            M_jugados_total = jugador_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()
            # Si no se selecciona un filtro válido, calcular la suma general de "R+"
            suma_filtro = df['R+'].sum() - jugador_df['R+'].sum()

        if selected_filtro == 'posicion':
            # Calcular la suma de "R+" según la posición del jugador y los partidos seleccionados
            position_filtered_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0])]
            if selected_partidos:
                position_filtered_df = position_filtered_df[position_filtered_df['Rival'].isin(selected_partidos)]
            suma_filtro = position_filtered_df['R+'].sum() - jugador_df['R+'].sum()
            # Calcular el número de jugadores en la posición del jugador seleccionado, excluyendo al jugador seleccionado
            num_jugadores = position_filtered_df['Jugador'].nunique() - 1
        elif selected_filtro == 'division':
            # Calcular la suma de "R+" según la división y los partidos seleccionados
            division_filtered_df = df[df['Rival'].isin(selected_partidos)]
            suma_filtro = division_filtered_df['R+'].sum() - jugador_df['R+'].sum()
            # Calcular el número de jugadores en la división seleccionada, excluyendo al jugador seleccionado
            num_jugadores = division_filtered_df['Jugador'].nunique() - 1

        # Asegurarse de que num_jugadores no sea menor a 1 para evitar división por cero
        if num_jugadores < 1:
            num_jugadores = 1

        # Calcular los minutos jugados de los partidos seleccionados para la posición/división
        if selected_partidos:
            if selected_filtro == 'posicion':
                filtered_partidos_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0]) & (df['Rival'].isin(selected_partidos))]
            elif selected_filtro == 'division':
                filtered_partidos_df = df[df['Rival'].isin(selected_partidos)]
            M_jugados_filtered = filtered_partidos_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()

            # Calcular la suma de acciones dividida por los minutos jugados de los partidos seleccionados
            suma_filtro = round((90 / M_jugados_filtered) * suma_filtro)

        # Dividir la suma_filtro por el número de jugadores
        if num_jugadores > 0:
            suma_filtro = suma_filtro / num_jugadores

        promedio = suma_filtro / 2
        # Calcular el valor del jugador basado en los minutos jugados
        player_value = round((90 / M_jugados_total) * jugador_df['R+'].sum())

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        player_value = default_value
        suma_filtro = default_value

    # Crear figura de gráfico de barras
    fig = go.Figure()

    # Agregar la barra del jugador con el texto dentro de la barra
    fig.add_trace(go.Bar(
        y=['R+'],
        x=[player_value],
        orientation='h',
        marker=dict(color='#ED192D'),
        name='Jugador',
        text=[player_value],  # Añadir el valor del jugador como texto
        textposition='inside'  # Posicionar el texto dentro de la barra
    ))

    # Añadir una línea negra que muestra el promedio de 'R+' según el filtro seleccionado
    fig.add_shape(
        type="line",
        x0=suma_filtro,
        x1=suma_filtro,
        y0=-0.5,
        y1=0.5,
        line=dict(color="Black", width=4)  
    )

    fig.update_layout(
        xaxis=dict(showticklabels=False, range=[0, max_value + 2]),  # Añade un poco de espacio al final
        yaxis=dict(showticklabels=False),
        margin=dict(t=0, b=0, l=0, r=0),  # Reduce los márgenes
        paper_bgcolor='#ED192D',  # Fondo rojo
        plot_bgcolor='white',  # Fondo del gráfico blanco
        width=250,  # Ajusta el ancho del gráfico
        height=40,  # Ajusta la altura del gráfico
        dragmode=False,  # Deshabilitar el modo de arrastre
        modebar=dict(
            remove=['zoom', 'pan', 'select', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toImage']
        )  # Remover herramientas específicas, incluyendo 'toImage' para eliminar 'Download plot as PNG'
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False}) 



#GRAFICO DE BARRAS PASES CLAVE
@app.callback(
    Output('barras-pases-clave', 'children'),
    [Input('dropdown-jugador', 'value'),
     Input('dropdown-partidos', 'value'),
     Input('store-filtro', 'data')]
)
def update_barras(selected_player, selected_partidos, selected_filtro):
    if not selected_player:
        return None

    default_value = 0
    max_value = 10

    try:
        if selected_partidos:
            jugador_df = df[(df['Jugador'] == selected_player) & (df['Rival'].isin(selected_partidos))]
        else:
            jugador_df = df[df['Jugador'] == selected_player]

        if jugador_df.empty:
            player_value = default_value
            suma_filtro = default_value
        else:
            # Calcular los minutos jugados del jugador seleccionado
            M_jugados_total = jugador_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()
            # Si no se selecciona un filtro válido, calcular la suma general de "Clave"
            suma_filtro = df['Clave'].sum() - jugador_df['Clave'].sum()

        if selected_filtro == 'posicion':
            # Calcular la suma de "Clave" según la posición del jugador y los partidos seleccionados
            position_filtered_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0])]
            if selected_partidos:
                position_filtered_df = position_filtered_df[position_filtered_df['Rival'].isin(selected_partidos)]
            suma_filtro = position_filtered_df['Clave'].sum() - jugador_df['Clave'].sum()
            # Calcular el número de jugadores en la posición del jugador seleccionado, excluyendo al jugador seleccionado
            num_jugadores = position_filtered_df['Jugador'].nunique() - 1
        elif selected_filtro == 'division':
            # Calcular la suma de "Clave" según la división y los partidos seleccionados
            division_filtered_df = df[df['Rival'].isin(selected_partidos)]
            suma_filtro = division_filtered_df['Clave'].sum() - jugador_df['Clave'].sum()
            # Calcular el número de jugadores en la división seleccionada, excluyendo al jugador seleccionado
            num_jugadores = division_filtered_df['Jugador'].nunique() - 1

        # Asegurarse de que num_jugadores no sea menor a 1 para evitar división por cero
        if num_jugadores < 1:
            num_jugadores = 1

        # Calcular los minutos jugados de los partidos seleccionados para la posición/división R+
        if selected_partidos:
            if selected_filtro == 'posicion':
                filtered_partidos_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0]) & (df['Rival'].isin(selected_partidos))]
            elif selected_filtro == 'division':
                filtered_partidos_df = df[df['Rival'].isin(selected_partidos)]
            M_jugados_filtered = filtered_partidos_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()

            # Calcular la suma de acciones dividida por los minutos jugados de los partidos seleccionados
            suma_filtro = round((90 / M_jugados_filtered) * suma_filtro)

        # Dividir la suma_filtro por el número de jugadores
        if num_jugadores > 0:
            suma_filtro = suma_filtro / num_jugadores

        promedio = suma_filtro / 2
        # Calcular el valor del jugador basado en los minutos jugados
        player_value = round((90 / M_jugados_total) * jugador_df['Clave'].sum())

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        player_value = default_value
        suma_filtro = default_value

    # Crear figura de gráfico de barras
    fig = go.Figure()

    # Agregar la barra del jugador con el texto dentro de la barra
    fig.add_trace(go.Bar(
        y=['Clave'],
        x=[player_value],
        orientation='h',
        marker=dict(color='#ED192D'),
        name='Jugador',
        text=[player_value],  # Añadir el valor del jugador como texto
        textposition='inside'  # Posicionar el texto dentro de la barra
    ))

    # Añadir una línea negra que muestra el promedio de 'Clave' según el filtro seleccionado
    fig.add_shape(
        type="line",
        x0=suma_filtro,
        x1=suma_filtro,
        y0=-0.5,
        y1=0.5,
        line=dict(color="Black", width=4)  
    )

    fig.update_layout(
        xaxis=dict(showticklabels=False, range=[0, max_value + 2]),  # Añade un poco de espacio al final
        yaxis=dict(showticklabels=False),
        margin=dict(t=0, b=0, l=0, r=0),  # Reduce los márgenes
        paper_bgcolor='#ED192D',  # Fondo rojo
        plot_bgcolor='white',  # Fondo del gráfico blanco
        width=250,  # Ajusta el ancho del gráfico
        height=40,  # Ajusta la altura del gráfico
        dragmode=False,  # Deshabilitar el modo de arrastre
        modebar=dict(
            remove=['zoom', 'pan', 'select', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toImage']
        )  # Remover herramientas específicas, incluyendo 'toImage' para eliminar 'Download plot as PNG'
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False}) 


#GRAFICO DE BARRAS PASES CLAVE DEFENSIVO (REC TRAS PERDIDA)
@app.callback(
    Output('barras-pases-claveD', 'children'),
    [Input('dropdown-jugador', 'value'),
     Input('dropdown-partidos', 'value'),
     Input('store-filtro', 'data')]
)
def update_barras(selected_player, selected_partidos, selected_filtro):
    if not selected_player:
        return None

    default_value = 0
    max_value = 10

    try:
        if selected_partidos:
            jugador_df = df[(df['Jugador'] == selected_player) & (df['Rival'].isin(selected_partidos))]
        else:
            jugador_df = df[df['Jugador'] == selected_player]

        if jugador_df.empty:
            player_value = default_value
            suma_filtro = default_value
        else:
            # Calcular los minutos jugados del jugador seleccionado
            M_jugados_total = jugador_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()
            # Si no se selecciona un filtro válido, calcular la suma general de "Tras Perdida"
            suma_filtro = df['Tras Perdida'].sum() - jugador_df['Tras Perdida'].sum()

        if selected_filtro == 'posicion':
            # Calcular la suma de "Tras Perdida" según la posición del jugador y los partidos seleccionados
            position_filtered_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0])]
            if selected_partidos:
                position_filtered_df = position_filtered_df[position_filtered_df['Rival'].isin(selected_partidos)]
            suma_filtro = position_filtered_df['Tras Perdida'].sum() - jugador_df['Tras Perdida'].sum()
            # Calcular el número de jugadores en la posición del jugador seleccionado, excluyendo al jugador seleccionado
            num_jugadores = position_filtered_df['Jugador'].nunique() - 1
        elif selected_filtro == 'division':
            # Calcular la suma de "Tras Perdida" según la división y los partidos seleccionados
            division_filtered_df = df[df['Rival'].isin(selected_partidos)]
            suma_filtro = division_filtered_df['Tras Perdida'].sum() - jugador_df['Tras Perdida'].sum()
            # Calcular el número de jugadores en la división seleccionada, excluyendo al jugador seleccionado
            num_jugadores = division_filtered_df['Jugador'].nunique() - 1

        # Asegurarse de que num_jugadores no sea menor a 1 para evitar división por cero
        if num_jugadores < 1:
            num_jugadores = 1

        # Calcular los minutos jugados de los partidos seleccionados para la posición/división R+
        if selected_partidos:
            if selected_filtro == 'posicion':
                filtered_partidos_df = df[(df['Posición'] == jugador_df['Posición'].iloc[0]) & (df['Rival'].isin(selected_partidos))]
            elif selected_filtro == 'division':
                filtered_partidos_df = df[df['Rival'].isin(selected_partidos)]
            M_jugados_filtered = filtered_partidos_df.drop_duplicates(subset=['Rival'])['Minutos Jugados'].sum()

            # Calcular la suma de acciones dividida por los minutos jugados de los partidos seleccionados
            suma_filtro = round((90 / M_jugados_filtered) * suma_filtro)

        # Dividir la suma_filtro por el número de jugadores
        if num_jugadores > 0:
            suma_filtro = suma_filtro / num_jugadores

        promedio = suma_filtro / 2
        # Calcular el valor del jugador basado en los minutos jugados
        player_value = round((90 / M_jugados_total) * jugador_df['Tras Perdida'].sum())

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        player_value = default_value
        suma_filtro = default_value

    # Crear figura de gráfico de barras
    fig = go.Figure()

    # Agregar la barra del jugador con el texto dentro de la barra
    fig.add_trace(go.Bar(
        y=['Tras Perdida'],
        x=[player_value],
        orientation='h',
        marker=dict(color='#ED192D'),
        name='Jugador',
        text=[player_value],  # Añadir el valor del jugador como texto
        textposition='inside'  # Posicionar el texto dentro de la barra
    ))

    # Añadir una línea negra que muestra el promedio de 'Tras Perdida' según el filtro seleccionado
    fig.add_shape(
        type="line",
        x0=suma_filtro,
        x1=suma_filtro,
        y0=-0.5,
        y1=0.5,
        line=dict(color="Black", width=4)  
    )

    fig.update_layout(
        xaxis=dict(showticklabels=False, range=[0, max_value + 2]),  # Añade un poco de espacio al final
        yaxis=dict(showticklabels=False),
        margin=dict(t=0, b=0, l=0, r=0),  # Reduce los márgenes
        paper_bgcolor='#ED192D',  # Fondo rojo
        plot_bgcolor='white',  # Fondo del gráfico blanco
        width=250,  # Ajusta el ancho del gráfico
        height=40,  # Ajusta la altura del gráfico
        dragmode=False,  # Deshabilitar el modo de arrastre
        modebar=dict(
            remove=['zoom', 'pan', 'select', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toImage']
        )  # Remover herramientas específicas, incluyendo 'toImage' para eliminar 'Download plot as PNG'
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False}) 



#DROPDOWN PARA TITULO AL SELECCIONAR ESTADISTICA
@app.callback(
    Output('titulo-dropdown', 'children'),
    [Input('dropdown-scatter-plot', 'value')]
)
def update_titulo_dropdown(selected_value):
    # Mapea los valores a los nombres legibles
    options_dict = {
        'duelos_aereos': 'DUELOS AÉREOS',
        'tiros': 'TIROS',
        'duelos_1v1': 'DUELOS 1VS1',
        'perdidas': 'PERDIDAS',
        'pases': 'PASES',
        'pases_largos': 'PASES LARGOS',
        'exceso_gambeta': 'EXCESO GAMBETA',
        'peligro_esperado': 'PELIGRO ESPERADO',
        'regates': 'REGATES',
        'peligro_tate': 'PELIGRO EN 3/4'

    }
    return options_dict.get(selected_value, "SELECCIONE UNA ESTADISTICA")


#DROPDOWN PARA TITULO AL SELECCIONAR ESTADISTICA
@app.callback(
    Output('titulo-dropdownD', 'children'),
    [Input('dropdown-scatter-plotD', 'value')]
)
def update_titulo_dropdownD(selected_value):
    # Mapea los valores a los nombres legibles
    options_dict = {
        'duelos_aereosD': 'DUELOS AÉREOS',
        'duelos_1v1D': 'DUELOS 1VS1',
        'recuperaciones': 'RECUPERACIONES',
    }
    return options_dict.get(selected_value, "SELECCIONE UNA ESTADISTICA")



# Definir contenido de cada pestaña
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'individual':
        return contenido_individual
    elif tab == 'evolutivo':
        return html.Div([html.H1("Contenido Arqueros")])
    elif tab == 'comparacion':
        return html.Div([html.H1("Contenido Comparación")])





if __name__ == '__main__':
    app.run_server(debug=True)