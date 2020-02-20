import json
import pandas as pd
from pandas.io.json import json_normalize
jsonFile='./data2.json'
with open(jsonFile, 'r') as f:
    jsonList = json.load(f)
from pandas.io.json import json_normalize
data=json_normalize(jsonList)
data['dt_in']=pd.to_datetime(data['dt_in'])
data['dt_out']=pd.to_datetime(data['dt_out'])
data['dt_bet']=data['dt_out']-data['dt_in']
#Respuestas
#Tiempo de espera promedio en la zona A
print(data[data.zone.isin(['AE1','AE2'])]['dt_bet'].mean())
#Tiempo de espera promedio en la zona B
print(data[data.zone.isin(['BE1','BE2'])]['dt_bet'].mean())
#Porcentaje de faenas con AW2 o BW2
print(data[data.zone.isin(['AW2','BW2'])].count()[0]/len(data)*100)


##Análisis propuestos
#Análisis estadístico exploratorio
data[['asset','zone','cycle','dt_bet']].groupby(['asset','zone']).describe().to_csv('describe.csv')
#Al observar el resumen estadístico generado se concluyen diversas cosas, 
#entre ellas que:
# probablemente los datos provienen de rangos equiespaciados en el tiempo  y no 
# de variables observadas reales, 
# De esta forma  construir modelos estadísticos o proceso que involucren 
# distribuciones no tendría sentido. (Puede ser que esté equivocado)


#Top ten de tiempo mínimo efectivo de trabajo AW1
print(data[data.zone.isin(['AW1'])][['asset','dt_bet']].sort_values('dt_bet',ascending=True).head(10))

# Análisis gráfico y en frecuencia de uso versus tiempo pen zona de trabajo A 
# durante algunos días
import datetime
import matplotlib.pyplot as plt
import numpy as np
zone='A'
in_outAsset=data[data.zone==zone][['asset','dt_in','dt_out','dt_bet']].groupby('asset')
for asset,info in in_outAsset:
    assetStateOn=pd.DataFrame(info.dt_in)
    assetStateOn['state']=1
    assetStateOn.columns=['time','state']
    
    assetStateOff=pd.DataFrame(info.dt_out)
    assetStateOff['state']=1
    assetStateOff.columns=['time','state']
    assetState=assetStateOn.append(assetStateOff,sort=True)
    
    assetStateOffEnding=pd.DataFrame(info.dt_in-datetime.timedelta(0,0.1))
    assetStateOffEnding['state']=0
    assetStateOffEnding.columns=['time','state']
    assetState=assetState.append(assetStateOffEnding,sort=True)
    
    assetStateOnEnding=pd.DataFrame(info.dt_out+datetime.timedelta(0,0.1))
    assetStateOnEnding['state']=0
    assetStateOnEnding.columns=['time','state']
    assetState=assetState.append(assetStateOnEnding,sort=True)
    
    assetState=assetState.sort_values('time')
  
    #Gráfica de frecuencia de uso por asset
    assetStatePlot=assetState.set_index('time')
    plt.figure(1)
    assetStatePlot.head(50).plot(style='-k',title='Operación de '+asset+' en zona '+zone)
    plt.savefig('FREQ'+asset+zone+'.png')
    plt.show()


    #Cálculo y gráfica del dutycycle por asset
    dt_in=np.array(info.dt_in) 
    dt_bet=np.array(info.dt_bet)    
    periodos=dt_in[1:]-dt_in[:-1]
    dutyCycle=np.multiply(np.divide(dt_bet[:-1],periodos),100)
    dataFramePlot=pd.DataFrame(dt_in[:-1])
    dataFramePlot['dutycycle']=pd.DataFrame(dutyCycle)
    dataFramePlot.columns=['dt_in','dutycycle']
    dataFramePlot=dataFramePlot.set_index('dt_in')
    plt.figure(2)
    axis=dataFramePlot.plot(style='-k',title='Dutycycle de '+asset+' en zona '+zone)
    axis.set_ylabel('% duty cycle')
    plt.savefig('DC'+asset+zone+'.png')
    plt.show()

    
