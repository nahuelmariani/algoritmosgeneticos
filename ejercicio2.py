# -*- coding: utf-8 -*-
from pick import pick
import sys

def imprimir(metodo, solucion, volMax, valMax, unidad):
    return "{}".format(metodo) + "\nElementos a cargar:" + ",".join(str(s) for s in solucion) + unidad.format(volMax) + "\nValor: ${}".format(valMax)
        
def dec_to_bin(x): # Funcion para pasar de decimal a binario (de tipo string)
       return str(bin(x)[2:]) # Le saco los dos primeros dígitos porque bin() dice que "3 es igual a 0b11" (sólo quiero 11)

def combs(cant):
    combinaciones=[]
    for k in range(2**cant): # Recorro la cantidad de combinaciones posibles. 
        binario = dec_to_bin(k) # Paso k (decimal) a binario (string)
        #print("bin",binario)
        comb = []
        for i, c in enumerate(reversed(binario)): # i: índice, c: caracter. enumerate() genera (0, binario[0]), (1, binario[1]), (2, binario[2])
            #print("idx",i)
            #print("car",c)
            if c=="1": # Si el caracter (dígito) es 1, agrega el índice a la combinacion.
                comb.append(i)
        combinaciones.append(comb) # Cuando termina el for para una combinacion, la guarda.
    return combinaciones

def exhaustivo(vol,val,volLimite,unidad): # Búsqueda Exhaustiva
    valMax = 0 # Valor máximo cargado en la mochila
    dataE = [] # Tupla de volúmenes y valores
    for i in range(len(vol)):
        dataE.append((vol[i],val[i])) # Columnas: [Volumen, Valor]
    com = combs(len(vol))

    for i in range(len(com)): # Recorro cada combinacion. Ejemplo: para k=2, com[0] = (0,1)
        volOcupado = 0
        valAcum = 0
        for j in range(len(com[i])): # Accedo a cada elemento de la combinacion. Ejemplo: com[0][0] = 0, com[0][1] = 1 
            volOcupado += dataE[com[i][j]][0] # Acumulo volumen en la mochila. Ejemplo: data[0][0] es el 'Volumen del elemento' (columna 0) de índice 0
            valAcum += dataE[com[i][j]][1] # Acumulo valor de la mochila. Ejemplo: data[0][1] es el 'Valor del elemento' (columna 1) de índice 0
        if volOcupado <= volLimite and valAcum > valMax: # Si caben en la mochila y si el valor es máximo:
            volMax = volOcupado # Guardo el volumen máximo
            valMax = valAcum # Guardo el valor máximo
            solucionE = com[i] # Guardo la combinacion que es la mejor solucion hasta el momento

    # Paso de 'indice en tupla' a 'número de elemento'
    for i in range(len(solucionE)):
        solucionE[i] += 1 

    return imprimir('BUSQUEDA EXHAUSTIVA',solucionE,volMax,valMax,unidad)

def greedy(vol,val,volLimite,unidad): # Algoritmo Greedy
    dataG = []
    solucionG = []
    volOcupado = 0
    valAcum = 0

    for i in range(len(vol)):
        dataG.append((i+1,vol[i],val[i],val[i]/vol[i])) # Columnas: [Elemento, Volumen, Valor, Proporcion]

    dataG.sort(key=lambda tup: tup[3], reverse=True) # Ordeno la tupla por la columna Proporcion (índice 3)
    #print(dataG)

    for i in range(len(vol)):
        if dataG[i][1] + volOcupado <= volLimite: # Si el volumen del elemento i más el volumen ya ocupado no supera el limite:
            volOcupado += dataG[i][1] # Acumulo el volumen
            valAcum += dataG[i][2] # Acumulo el valor
            solucionG.append(dataG[i][0]) # Agrego elemento a la solución
        else:
            break

    return imprimir('ALGORITMO GREEDY',solucionG,volOcupado,valAcum,unidad)

def menu():
    titulo1 = 'Problema de la Mochila'
    opciones1 = ['Volumen', 'Peso', 'Salir']
    opcion1, index1 = pick(opciones1, titulo1)
    if opcion1 == 'Volumen' and index1 == 0:
        vol = [150,325,600,805,430,1200,770,60,930,353]
        val = [20,40,50,36,25,64,54,18,46,28]
        volLimite = 4200
        unidad = '\nVolumen: {} cm3'
    elif opcion1 == 'Peso':
        vol = [1800,600,1200] # peso
        val = [72,36,60] 
        volLimite = 3000 # pesoLimite
        unidad = '\nPeso: {} g'
    else:
        sys.exit()
    
    titulo2 = 'Tipo de busqueda'
    opciones2 = ['Exhaustiva','Greedy','Volver']
    opcion2, index2 = pick(opciones2, titulo2)
    if opcion2 == 'Exhaustiva' or index2 == 0: # Le agregué el 'or index' porque me cansó el warning
        resultado = exhaustivo(vol,val,volLimite,unidad)
    elif opcion2 == 'Greedy':
        resultado = greedy(vol,val,volLimite,unidad)
    if opcion2 == 'Volver':
        menu()
    else:
        seguir, index = pick(['Si','Salir'], '{}\n\nContinuar?'.format(resultado))
        if seguir == 'Si' or index == 0:
            menu()
        else:
            sys.exit()

menu()