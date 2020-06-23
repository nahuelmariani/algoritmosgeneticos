# -*- coding: utf-8 -*-
from pick import pick
import sys

def imprimir(metodo, solucion, volMax, valMax, unidad):
    return "{}".format(metodo) + "\nElementos a cargar:" + ",".join(str(s) for s in solucion) + unidad.format(volMax) + "\nValor: ${}".format(valMax)

def dec_to_bin(x): # Funcion para pasar de decimal a binario (de tipo string)
       return str(bin(x)[2:]) # Le saco los dos primeros dígitos porque bin() dice que "3 es igual a 0b11" (sólo quiero 11)

def combs(n): # Funcion para crear todas las combinaciones posibles de 'n' elementos
    combinaciones=[]
    for k in range(2**n): # Cantidad de combinaciones posibles n elementos = 2**n.
        binario = dec_to_bin(k) # Paso k (decimal) a binario (string)
        comb = []
        for i, c in enumerate(reversed(binario)): # i: índice, c: caracter. enumerate() genera (0, binario[0]), (1, binario[1])) reverse: para que tome en orden los elementos del 1 al 10 sino el 1 en binario es el objeto 10 en lugar del 1
            if c=="1": # Si el caracter (dígito) es 1, agrega el índice a la combinacion.
                comb.append(i)
        combinaciones.append(comb) # Cuando termina el for para una combinacion, la guarda.
    return combinaciones

def exhaustivo(vol,val,volLimite,unidad): # Búsqueda Exhaustiva
    valMax = 0 # Valor máximo cargado en la mochila
    dataE = [] # Tupla de volúmenes y valores
    for i in range(len(vol)):
        dataE.append((vol[i],val[i])) # Columnas: [Volumen, Valor]

    combinaciones = combs(len(vol)) # Creo todas las combinaciones posibles
    for com in combinaciones: # Accedo a cada combinacion.
        volOcupado = 0
        valAcum = 0
        for e in com: # Accedo a cada elemento de la combinacion.
            volOcupado += dataE[e][0] # Acumulo volumen del elemento 'e' en la mochila (columna 0 de dataE)
            valAcum += dataE[e][1] # Acumulo valor del elemento 'e' (columna 1 de dataE)
        if volOcupado <= volLimite and valAcum > valMax: # Si caben en la mochila y si el valor es máximo:
            volMax = volOcupado # Guardo el volumen máximo
            valMax = valAcum # Guardo el valor máximo
            solucionE = com # Guardo la combinacion que es la mejor solucion hasta el momento

    # Sumo 1 al numero en la combinacion para que se corresponda con el numero de elemento del problema.
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
    
    for e in dataG: #recorro cada elemento de la lista dataG. Cada elemento a su vez es una lista de 4 elementos: [Elemento, Volumen, Valor, Proporcion]
        if e[1] + volOcupado <= volLimite:  # Si el volumen del elemento i más el volumen ya ocupado no supera el limite:
            volOcupado += e[1] # Acumulo el volumen
            valAcum += e[2]  # Acumulo el valor
            solucionG.append(e[0]) # Agrego elemento a la solución
        else:
            break

    return imprimir('ALGORITMO GREEDY',solucionG,volOcupado,valAcum,unidad)

def menu():
    titulo1 = 'Problema de la Mochila'
    opciones1 = ['Volumen', 'Peso', 'Salir']
    opcion1, index1 = pick(opciones1, titulo1)
    if opcion1 == 'Volumen':
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
    if opcion2 == 'Exhaustiva':
        resultado = exhaustivo(vol,val,volLimite,unidad)
    elif opcion2 == 'Greedy':
        resultado = greedy(vol,val,volLimite,unidad)
    if opcion2 == 'Volver':
        menu()
    else:
        seguir, index = pick(['Si','Salir'], '{}\n\nContinuar?'.format(resultado))
        if seguir == 'Si':
            menu()
        else:
            sys.exit()

menu()
