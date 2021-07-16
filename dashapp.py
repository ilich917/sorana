test = False
def run_dash(test):
  import plotly.graph_objects as go
  import dash
  import dash_core_components as dcc
  import dash_html_components as html
  
  if test == True:
    fig = go.Figure(data=go.Scatterpolar(
      r=[1, 5, 2],
      theta=['Agotamiento Emocional', 'Desrealización Profesional', 'Despersonalización'],
      fill='toself'
    ))

    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True
        ),
      ),
      showlegend=False
    )

    dashapp = dash.Dash(__name__, server=app, url_base_pathname='/dash')
    dashapp.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    dashapp.run_server(port=8050, debug=True, use_reloader=False)

run_dash(test)