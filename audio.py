import pandas as pd
import numpy as np
import re

def si(a,b):
    
    if len(a) >= 1: return a
    else:return b

def preproceso(file1, file2):
    
    columnas = {'ga:dimension3': 'clientID', 
                'ga:dimension4': 'sessionID', 
                'ga:deviceCategory': 'deviceCategory',
                'ga:channelGrouping': 'channelGrouping', 
                'ga:pageDepth': 'PageDepth', 
                'ga:landingPagePath': 'landingPagePath',
                'ga:exitPagePath': 'exitPagePath', 
                'ga:sessions': 'sessions', 
                'ga:bounces': 'bounces', 
                'ga:sessionDuration': 'sessionDuration',
                'ga:transactions': 'transactions', 
                'ga:operatingSystem': 'operatingSystem',
                'ga:sourceMedium': 'sourceMedium'}


    df1 = pd.read_csv(file1).drop('Unnamed: 0', axis = 1)
    df2 = pd.read_csv(file2).drop('Unnamed: 0', axis = 1)
    df= df1.merge(df2[['ga:dimension4', 'ga:operatingSystem', 'ga:sourceMedium']], on = 'ga:dimension4')

    df= df.rename(columns = columnas)

    #recodificación de rebotes mayores que 1
    df['bounces'] = np.where(df['bounces']>=1, 1, 0)

    #Vector objetivo
    df['transactions'] = np.where(df['transactions']>=1, 1, 0)

    #Palabras clave de la página de destino
    df['landingPageKeyWord'] = df['landingPagePath']\
                            .apply(lambda x: si(re.findall('\w+', str(x)), [''])[0])\
                            .replace('', 'home')


    #Palabras clave de la página de salida
    df['exitPageKeyWord'] = df['exitPagePath']\
                            .apply(lambda x: si(re.findall('\w+', str(x)), [''])[0:])

    #De que parte viene el usuario
    df['fuente'] = df['sourceMedium'].apply(lambda x: x.split('/')[0].strip())

    #A traves de que medio llego el usuario
    df['transporte'] = df['sourceMedium'].apply(lambda x: x.split('/')[1].strip())
    df = df.drop(['exitPageKeyWord', 'clientID', 'sessionID', 'landingPagePath', 'exitPagePath', 'sourceMedium', 'sessions'], axis =1)
    df = df.query("bounces == 0 and sessionDuration > 0").drop("bounces", axis = 1)

    df = df.query("""
              deviceCategory in ('desktop', 'mobile') and operatingSystem in ('Windows', 'Macintosh') and \
              fuente in ('google', '(direct)') and transporte in ('organic', 'cpc', '(none)' ) and \
              channelGrouping in ('Organic Search', 'Direct', 'Paid Search') and \
              landingPageKeyWord in ('checkout', 'home', 'product', 'search') \
              """)
    
    return df