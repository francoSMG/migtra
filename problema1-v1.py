#Ejemplo de solución usando estructura Json convertida a un iterable de Python
#Ventaja: respeta el formato original de Json
#Desventaja: los ciclos anidados de iterables son lo peor para los lenguajes compilados 
import json
jsonFile='./data1.json'
with open(jsonFile) as jsonFile:
    data=json.load(jsonFile)
    countCiudad=0
    sumVar1=0
    sumVar2Provincia2=0
    var1Region4=set()
    for region in data:
        #print(region['name'])
        for provincia in region['children']:
            #print(provincia['name'])
            for ciudad in provincia['children']:
                #print(ciudad)
                countCiudad+=1
                sumVar1+=ciudad['values']['var1']
                if provincia['name']=='Provincia2':
                    sumVar2Provincia2+=ciudad['values']['var2']
                if region['name']=='Region4':
                    var1Region4.add(ciudad['values']['var1'])
    
    ##Respuestas:
    #Promedio var1 global
    print(sumVar1/countCiudad)
    #Suma var2 en Provincia2
    print(sumVar2Provincia2)  
    #Máximo var1 en Región 4
    print(max(var1Region4))
