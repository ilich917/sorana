from flask import Flask, render_template, request, redirect, url_for, flash, session
#from flask.ext.session import Session
from flask_mysqldb import MySQL

import os

app = Flask(__name__)


SESSION_TYPE = 'redis'
app.config.from_object(__name__)
#Session(app)

app.secret_key = 'esto-es-una-clave-muy-secreta'
app.config['MYSQL_HOST'] = 'us-cdbr-east-04.cleardb.com'
app.config['MYSQL_USER'] = 'bb673b520dd784'
app.config['MYSQL_PASSWORD'] = '32a17440'
app.config['MYSQL_DB'] = 'heroku_abca1c21f295eab'
mysql = MySQL(app)

# ___________________________

import plotly.graph_objects as go
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple


@app.route('/')
def Index():
    for key in list(session.keys()):
     session.pop(key)
    session.clear()
    return render_template('index.html')


@app.route('/results', methods=['POST'])
def results():
    if request.method == 'POST':
        r1 =request.form['r1']
        r2 =request.form['r2']
        r3 =request.form['r3']
        r4 =request.form['r4']
        r5 =request.form['r5']
        r6 =request.form['r6']
        r7 =request.form['r7']
        r8 =request.form['r8']
        r9 =request.form['r9']
        r10 =request.form['r10']
        r11 =request.form['r11']
        r12 =request.form['r12']
        
        cur = mysql.connection.cursor()
        
        cur.execute('INSERT INTO respuestas(r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12))
        mysql.connection.commit()
        session['r1'] = r1
        session['r2'] = r2
        session['r3'] = r3
        session['r4'] = r4
        session['r5'] = r5
        session['r6'] = r6
        session['r7'] = r7
        session['r8'] = r8
        session['r9'] = r9
        session['r10'] = r10
        session['r11'] = r11
        session['r12'] = r12
        
        return redirect(url_for('render_dash'))
    
# ____________________________


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dashapp = dash.Dash(__name__, server=app, url_base_pathname='/dash/')

fig = go.Figure(data=go.Scatterpolar(
    r=[1,1,1,1],
    theta=['Agotamiento Emocional', 'Desrealización Profesional', 'Despersonalización', 'Improductividad Subjetiva'],
    fill='toself'))

fig.update_layout(
        polar=dict(
        radialaxis=dict(
            visible=True
        ),
        ),
        showlegend=False
    )

dashapp.layout = html.Div([
            html.H1('Nivel de Burnout', style={'textAlign': 'center'}),
            dcc.Graph(figure=fig),
            html.Div(dcc.Link(html.Button('Volver'), id='volver', href='/', refresh=True), style={'textAlign': 'center'} ),
            html.Div(html.H3('Con base a tus respuestas, es probable que presentes burnout en tu trabajo, lo que implica que el estrés que experimentas por tu trabajo puede o ha empezado a afectar negativamente en tu vida, tus emociones y con tus seres queridos. Con base a tus respuestas es recomendable que busques actividades recreativas fuera del contexto laboral (salir a pasear, salir con amigos, visitar a familiares o actividades recreativas como pintar o practicar algún deporte), así mismo de ser posible dedica unos 15 min diarios (puedes usar la alarma de esta aplicación para programar esta actividad) para practicar respiración diafragmática (haz clic aquí para una práctica guiada de esta respiración). Reportes generales de burnout de tu área y recomendaciones serán proporcionados a recursos humanos para que tomen medidas adecuadas para ayudar a que disminuya el estrés que sientes  (no tendrán acceso a resultados por persona, por lo que tus respuestas y resultado se mantendrán anónimos). Si consideras que requieres ayuda terapéutica derivado de los resultados o por otra razón da click en el siguiente botón.'), style={'textAlign': 'center'} )
        ])

#error?

# _____________________

@app.route('/dash_plotly', methods=['GET'])
def render_dash():
    
    r1 = int(session.get('r1', None))
    r2 = int(session.get('r2', None))
    r3 = int(session.get('r3', None))
    r4 = int(session.get('r4', None))
    r5 = int(session.get('r5', None))
    r6 = int(session.get('r6', None))
    r7 = int(session.get('r7', None))
    r8 = int(session.get('r8', None))
    r9 = int(session.get('r9', None))
    r10 = int(session.get('r10', None))
    r11 = int(session.get('r11', None))
    r12 = int(session.get('r12', None))
    
    min_por_area = 7
    burnout = r2+r5+r12 + 15-(r1+r4+r8)+ r3+r6+r9 + 15-(r7+r10+r11)
    
    session.clear()
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
    r=[r2+r5+r12, 15-(r1+r4+r8), r3+r6+r9,15-(r7+r10+r11)],
    theta=['Agotamiento Emocional', 'Desrealización Profesional', 'Despersonalización', 'Improductividad Subjetiva'],
    fill='toself'))
    
    fig.add_trace(go.Scatterpolar(
    r=[min_por_area, min_por_area, min_por_area, min_por_area],
    theta=['Agotamiento Emocional', 'Desrealización Profesional', 'Despersonalización', 'Improductividad Subjetiva'],
    fill='toself'))
    
    fig.update_layout(
        polar=dict(
        radialaxis=dict(
            visible=True
        ),
        ),
        showlegend=True
    )
    if int(burnout) > 22:
        dashapp.layout = html.Div([
            html.H1('Nivel de Burnout', style={'textAlign': 'center'}),
            dcc.Graph(figure=fig),
            html.Div(dcc.Link(html.Button('Volver'), id='volver', href='/', refresh=True), style={'textAlign': 'center'} ),
            html.Div(html.H3('Con base a tus respuestas, es probable que presentes burnout en tu trabajo, lo que implica que el estrés que experimentas por tu trabajo puede o ha empezado a afectar negativamente en tu vida, tus emociones y con tus seres queridos. Con base a tus respuestas es recomendable que busques actividades recreativas fuera del contexto laboral (salir a pasear, salir con amigos, visitar a familiares o actividades recreativas como pintar o practicar algún deporte), así mismo de ser posible dedica unos 15 min diarios (puedes usar la alarma de esta aplicación para programar esta actividad) para practicar respiración diafragmática (haz clic aquí para una práctica guiada de esta respiración). Reportes generales de burnout de tu área y recomendaciones serán proporcionados a recursos humanos para que tomen medidas adecuadas para ayudar a que disminuya el estrés que sientes  (no tendrán acceso a resultados por persona, por lo que tus respuestas y resultado se mantendrán anónimos). Si consideras que requieres ayuda terapéutica derivado de los resultados o por otra razón da click en el siguiente botón.'), style={'textAlign': 'center'} )
        ])
    else:
        dashapp.layout = html.Div([
            html.H1('Nivel de Burnout', style={'textAlign': 'center'}),
            dcc.Graph(figure=fig),
            html.Div(dcc.Link(html.Button('Volver'), id='volver', href='/', refresh=True), style={'textAlign': 'center'} ), 
            html.Div(html.H3('Con base a tus respuestas, es probable que no estés presentando burnout en estos momentos, es decir, tu trabajo no te impide disfrutar del día a día y no es impedimento para mantener tu calidad de vida. Continúa dedicando el tiempo que actualmente le dedicas a tu trabajo así como a actividades recreativas o que te gusten. Es importante que te evalúes por lo menos una vez al mes para detectar algún posible cambio.  Reportes generales de burnout de tu área y recomendaciones serán proporcionados a recursos humanos para que tomen medidas adecuadas y seguir mejorando tu espacio de trabajo para que te sientas cada vez más comodo y a gusto con lo que haces (no tendrán acceso a resultados por persona, por lo que tus respuestas y resultado se mantendrán anónimos)'), style={'textAlign': 'center'} )        
        ])
            
    return redirect('dash')

    
if __name__ == '__main__':
    run_simple('0.0.0.0', 8080, app, use_reloader=True, use_debugger=False)