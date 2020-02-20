#Ejemplo de solución usando estructura Json convertida a un data Frame de Pandas
#Ventaja: permite la integración a todos los otros módulos de data sciencia de Python
#Desventaja: costo computacional de aplanar el Json
import json
jsonFile='./data1.json'
with open(jsonFile, 'r') as f:
    jsonList = json.load(f)
from pandas.io.json import json_normalize
data=json_normalize(jsonList,['children',['children']],['name',['children','name']],record_prefix='_')
data.columns=['ciudad','var1','var2','region','provincia']   
##Respuestas:
#Promedio var1 global
print(data.var1.mean())  
#Suma var2 en Provincia2
print(data[data.provincia=='Provincia2'].var2.sum())
#Máximo var1 en Región 4
print(data[data.region=='Region4'].var1.max())