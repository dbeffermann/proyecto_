import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

import pickle
from sklearn.metrics import roc_curve

import streamlit as st
from streamlit.caching import cache
import streamlit.components.v1 as components

from audio import preproceso
from sklearn.metrics import classification_report

from IPython.display import HTML
import plotly.express as px

###############ESTETICO#########################
#st.set_page_config(initial_sidebar_state="collapsed", layout = 'wide')
st.set_page_config(layout = 'wide', page_icon="🎧", initial_sidebar_state="collapsed")
st.image("logo_dscience.png", width=250)
st.title("Propensión de Compra")
st.sidebar.title("⚙️ Ajustes")
#accion = st.button('🎸 Obtener Predicción')
col1, col2 = st.beta_columns([1,1])

##############FUNCIONAL#####################

@cache
def cargar_datos():
    #file1 = "audiomusica_24_30_1.csv"
    #file2 = "audiomusica_24_30_2.csv"
    #return preproceso(file1, file2)
    return pd.read_csv('validacion.csv').drop(columns = 'Unnamed: 0')



#@cache
def filtros(df, sidebar = True):
    with st.spinner():
        
        obj = {}
        for colname, serie in df.select_dtypes('O').iteritems():

            if sidebar:
                obj[colname] = st.sidebar.multiselect(colname, serie.unique())
            else:
                obj[colname] = col2.multiselect(colname, serie.unique())


        filtros = []
        for key,value in obj.items():

            if value:
                #print(f"{key} in {tuple(value)}")
                filtros.append(f"{key} in {tuple(value)}")
        
        filtro = ' and '.join(filtros)

        return filtro




@cache
def predecir(df):

    df_dummies = pd.get_dummies(df, drop_first = True)
    X = df_dummies.drop(columns = 'transactions')
    Y = df_dummies['transactions']

    modelo = pickle.load(open( "forest.sav", "rb" ))

    return df.assign(transactions_pred = modelo.predict(X))

#######MAIN#######
df = cargar_datos()
#filtrar = filtros(df)

df.to_csv("validacion.csv")


#if accion:
    
pred = predecir(df)

#if filtros(df):
    #df = df.query(filtrar)
#fig = px.bar(x=pred['deviceCategory'], y = pred['transactions_pred'], color = pred['transactions']).to_html()

#components.html(fig, width=1000, height = 600, scrolling = True)

st.sidebar.subheader('Características')
var = st.sidebar.selectbox('', pred.columns)

if var:
    fig = px.bar(data_frame = pred, x='transactions_pred', y = 'transactions', color = pred[var], title = 'Predicciones').to_html()
else:

    fig = px.bar(data_frame = pred, x='transactions_pred', y = 'transactions', color = pred['landingPageKeyWord'], title = 'Predicciones').to_html()

components.html(fig, width=1000, height = 1200, scrolling = True)



#st.line_chart(pred.groupby(['transactions', 'transactions_pred'], as_index=False).sum())






