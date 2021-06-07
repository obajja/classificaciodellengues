# coding=utf-8
import numpy as np
from time import time
from aux import *

'''
Obre un fitxer a partir del seu nom i guarda cada una de les seves línies en cada posició d'una llista
Paràmetres:
    - fileName: Nom del fitxer que es vol obrir.
Return:
    - llista amb les paraules que conformen la llista Swadesh d'un idioma en concret
'''


def openFile(fileName):
    f = open(fileName, 'r')
    llistaParaules = list()
    lines = f.readlines()
    for line in lines:
        llistaParaules.append(line)  # afegim a cada posició de la llista una paraula
    return llistaParaules


'''
Determina si un fonema és una vocal o no.
Paràmetres:
    - char: Fonema
Return:
    - True si char és vocal
    - False si char no és vocal (i per tant és consonant)
'''


def esVocal(char):
    if char in vocals_transcr:
        return True  # és vocal
    return False  # no és vocal


'''
Calcula la distància entre dues paraules. Per fer-ho crea una matriu a partir d'un diccionari i es calcula el nombre
mínim de canvis que s'ha de dur a terme per tal d'arribar d'una paraula a una altra. Normalitza la distància en funció de
la mida de la paraula més llarga.

La distància total entre dues paraules es troba a la posició més inferior a la dreta de la matriu.

Paràmetres:
    - str1: una de les paraules que es vol comparar
    - str2: l'altra paraula que es vol comparar
Return:
    - La distància normalitzada entre les dues paraules
'''


def distancia_paraula_lexic(str1, str2):
    d = dict()  # declarem un diccionari que utilitzarem de matriu
    # numerem les lletres de cada paraula
    for i in range(len(str1) + 1):
        d[i] = dict()
        d[i][0] = i
    for i in range(len(str2) + 1):
        d[0][i] = i
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            # calculem tots els elements de la matriu
            d[i][j] = min(d[i][j - 1] + 1, d[i - 1][j] + 1, d[i - 1][j - 1] + (not str1[i - 1] == str2[j - 1]))

    #print ('distància entre ', str1, " i ", str2, '=', d[len(str1)][len(str2)])

    distancia = d[len(str1)][len(str2)]  ##retornem el valor de la última posició de la matriu
    normalitzador = max(len(str1), len(str2))  # calculem el nombre de lletres de la paraula més llarga
    res = distancia / normalitzador  # normalitzem la distància

    return res


'''
Calcula la distància entre dues transcripcions fonètiques de dues paraules. Per fer-ho crea una matriu a partir d'un 
diccionari i s'adapta la distància de Levenshtein de manera que el cost de la substitució és la distància que hi ha entre 
dos fonemes (es calcula amb la funció distanciaFonemes(fonema1,fonema2))

La distància total entre les dues transcripcons es troba a la posició més inferior a la dreta de la matriu.

Paràmetres:
    - str1: una de les transcripcions que es vol comparar
    - str2: l'altra transcripció que es vol comparar
Return:
    - La distància normalitzada entre les dues dues transcripcions
'''


def distancia_paraula_fonema(str1, str2):
    d = dict()  # declarem un diccionari que utilitzarem de matriu
    # numerem les lletres de cada paraula
    for i in range(len(str1) + 1):
        d[i] = dict()
        d[i][0] = i
    for i in range(len(str2) + 1):
        d[0][i] = i
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            # calculem tots els elements de la matriu
            d[i][j] = min(d[i][j - 1] + 1, d[i - 1][j] + 1,
                          d[i - 1][j - 1] + distanciaFonemes(str1[i - 1], str2[j - 1]))

    #print ('distància entre ', str1, ' i ', str2, ' = ', d[len(str1)][len(str2)])

    distancia = d[len(str1)][len(str2)]  ##retornem el valor de la última posició de la matriu
    normalitzador = max(len(str1), len(str2))  # calculem el nombre de lletres de la paraula més llarga
    res = distancia / normalitzador  # normalitzem la distància

    return res


'''
Calcula la distància entre dos fonemes. Per fer-ho mira si els dos fonemes que es comparen són els dos vocàlics o 
consonàntics. Si els dos són vocàlics es crida a la funció distanciaVocals(fonema1,fonema2), que calcula la distància 
entre dos sons que es corresponen a vocals. Si els dos són consonàntics es crida a la funció 
distanciaConsonants(fonema1,fonema2), que calcula la distància entre dos sons que es corresponen a consonants. Si un fonema
és una vocal i l'altre és una consonant, la distància que se li atorga a l'operació és 1.
Paràmetres:
    - fonema1
    - fonema2
Return:
    - La distància entre els dos fonemes
'''


def distanciaFonemes(fonema1, fonema2):
    if esVocal(fonema1) and esVocal(fonema2):  # mirem si els dos fonemes són vocals
        distancia = distanciaVocals(fonema1, fonema2)  # calculem la distància entre els fonemes

    elif not (esVocal(fonema1)) and not (esVocal(fonema2)):  # mirem si els dos fonemes són consonants
        distancia = distanciaConsonants(fonema1, fonema2)  # calculem la distància entre els fonemes

    else:
        #print("Vocal i consonant!")
        distancia = 1  # si tractem amb una vocal i una consonant, la distància és màxima

    #print ("Distància entre ", fonema1, " i ", fonema2, " = ", distancia)
    return distancia


'''
Calcula la distància, des d'un punt de vista lèxic, acumulada entre dos idiomes. Per fer-ho suma la distància de totes 
les paraules dels dos idiomes i les normalitza dividint-les per 207, que és el nombre de paraules que hi ha a cada llista. 
Paràmetres:
    - idioma1: llista de paraules d'un idioma escrites des d'un punt de vista lèxic 
    - idioma2: llista de paraules d'un idioma escrites des d'un punt de vista lèxic 
Return:
    - La distància total que hi ha entre dos idiomes. És un valor entre 0 i 1.
'''


def distanciaIdioma_lexic(idioma1, idioma2):
    distanciaAcumulada = 0

    for x in range(1, 207):
        distanciaAcumulada += distancia_paraula_lexic(idioma1[x], idioma2[x])  # calculem la distància entre els idiomes

    distanciaAcumulada = distanciaAcumulada / 207  # dividim pel nombre de paraules per normalitzar

    #print ("La distància acumulada entre ", idioma1[0], " i ", idioma2[0], "és de ", distanciaAcumulada)
    return distanciaAcumulada


'''
Calcula la distància fonètica acumulada entre dos idiomes. Per fer-ho suma la distància de totes les paraules dels dos
idiomes i les normalitza dividint-les per 207, que és el nombre de paraules que hi ha a cada llista. 
Paràmetres:
    - idioma1: llista de transcripcions fonètiques de les paraules d'un idioma
    - idioma2: llista de transcripcions fonètiques de les paraules d'un idioma
Return:
    - La distància total que hi ha entre dos idiomes. És un valor entre 0 i 1.
'''


def distanciaIdioma_fonetic(idioma1, idioma2):
    distanciaAcumulada = 0

    for x in range(1, 207):
        distanciaAcumulada += distancia_paraula_fonema(idioma1[x],
                                                       idioma2[x])  # calculem la distància entre els idiomes

    distanciaAcumulada = distanciaAcumulada / 207  # dividim pel nombre de paraules per normalitzar

    #print ("La distància acumulada entre ", idioma1[0], " i ", idioma2[0], "és de ", distanciaAcumulada)
    return distanciaAcumulada


'''
Calcula la distància fonètica entre dos vocals. Per fer-ho mira quines posicions ocupa cada vocal dins de la 
taula de fonemes vocàlics obtenint els seus índex i els compara per veure en quines característiques coincideixen 
(és a dir, mira si els fonemes coincideixen en fila, columna i costat de la columna de la matriu que modeolitza els 
sons vocàlics). Si comparteixen tres característiques, la distància és 0; si comparteixen 2 característiques la 
distància és 1/3; si comparteixen 1, la distància és de 2/3 i si comparteixen cap característica la distància és 1.

En el cas del fonema w es fa un tractament especial perquè ocupa la mateixa posició que el fonema u. Això es deu a que 
expressen el mateix so en situacions diferents. Per simplificar, s'ha considerat a la matriu el so u i, per tenir en compte
el so w, s'utilitzen uns if's per determinar quina posició hauria d'ocupar.

Paràmetres:
    - v1: fonema a comparar
    - v2: fonema a comparar
Return:
    - La distància entre els dos fonemes comparats que pot ser 0, 1/3, 2/3 o 1
'''


def distanciaVocals(v1, v2):
    denominador = 3
    numerador = 3
    v1_pos = (0, 0, 0)
    v2_pos = (0, 0, 0)

    # calculem els índexs de la primera vocal
    for i in range(0, 7):
        for j in range(0, 3):
            for k in range(0, 2):

                if v1 == vocals_transcr_mat[i][j][k]:
                    v1_pos = (i, j, k)
                    #print(v1_pos)

    # calculem els índexs de la segona vocal
    for i in range(0, 7):
        for j in range(0, 3):
            for k in range(0, 2):

                if v2 == vocals_transcr_mat[i][j][k]:
                    v2_pos = (i, j, k)
                    #print(v2_pos)

    # si el fonema és w, calculem la seva posició directament perquè no es troba a la matriu
    if v1 == 'w':
        v1_pos = (0, 2, 1)

    if v2 == 'w':
        v2_pos = (0, 2, 1)

    for i in range(0, 3):
        if v1_pos[i] == v2_pos[i]:
            numerador -= 1

    distancia = numerador / denominador

    #print ("Distància entre les vocals ", v1, " i ", v2, " = ", distancia)
    return distancia


'''
Calcula la distància fonètica entre dos consonant. Per fer-ho mira quines posicions ocupa cada consonant dins de la 
taula de fonemes consonàntics obtenint els seus índex i els compara per veure en quines característiques coincideixen 
(és a dir, mira si els fonemes coincideixen en fila, columna i costat de la columna de la matriu que modeolitza els sons
vocàlics). Si comparteixen tres característiques, la distància és 0; si comparteixen 2 característiques la distància és 
1/3; si comparteixen 1, la distància és de 2/3 i si comparteixen cap característica la distància és 1.


Paràmetres:
    - c1: fonema a comparar
    - c2: fonema a comparar
Return:
    - La distància entre els dos fonemes comparats que pot ser 0, 1/3, 2/3 o 1
'''


def distanciaConsonants(c1, c2):
    denominador = 3
    numerador = 3

    c1_pos = (0, 0, 0)
    c2_pos = (0, 0, 0)

    # calculem els índexs de la primera consonant
    for i in range(0, 8):
        for j in range(0, 9):
            for k in range(0, 2):

                if c1 == conson_transcr_mat[i][j][k]:
                    c1_pos = (i, j, k)
                    #print(c1_pos)

    # calculem els índexs de la segona consonant
    for i in range(0, 8):
        for j in range(0, 9):
            for k in range(0, 2):

                if c2 == conson_transcr_mat[i][j][k]:
                    c2_pos = (i, j, k)
                    #print(c2_pos)

    for i in range(0, 3):
        if c1_pos[i] == c2_pos[i]:
            numerador -= 1

    distancia = numerador / denominador

    #print ("Distància entre les consonants ", c1, " i ", c2, " = ", distancia)
    return distancia


'''
Crida a les altres funcions i mostra per pantalla els resultats obtinguts
'''
if __name__ == '__main__':

    start = time()

    # obrim els fitxer per a cada parella d'idiomes possibles
    for i in range(0, 8):
        for j in range(0, 8):
            idioma1 = openFile("Llistes/" + llista_idiomes[i])
            idioma2 = openFile("Llistes/" + llista_idiomes[j])

            # calculem la distància lèxica entre cada aprella d'idiomes possible
            matriu_resultant_lexic[i][j] = distanciaIdioma_lexic(idioma1, idioma2)

        #print ("\n")

    # transformem la llista en un np.array per simplificar la impressió per pantalla
    matriu_resultant_array_lexic = np.array(matriu_resultant_lexic)

    # obrim els fitxer per a cada parella de transcripcions fonètiques d'idiomes possibles
    for i in range(0, 9):
        for j in range(0, 9):
            idioma3 = openFile("Llistes/" + llista_idiomes_fonetic[i])
            idioma4 = openFile("Llistes/" + llista_idiomes_fonetic[j])

            # calculem la distància fonètica els fitxer per a cada parella de transcripcions fonètiques d'idiomes possible
            matriu_resultant_fonetica[i][j] = distanciaIdioma_fonetic(idioma3, idioma4)

        #print ("\n")

    matriu_resultant_array_fonetic = np.array(
        matriu_resultant_fonetica)  # transformem la llista en un np.array per simplificar la impressió per pantalla

    np.set_printoptions(precision=3)  # determinem que el nombre de decimals a mostrar és 3

    # imprimim per pantalla les matrius de distàncies
    print("Matriu de distàncies lèxiques: \n")
    print(matriu_resultant_array_lexic)

    print ("\n")

    print("Matriu de distàncies fonètiques: \n")
    print (matriu_resultant_array_fonetic)

    print ("\n")

    end = time()
    time_elapsed = end - start #calculem el que triga l'execució

    print("Time elapsed: ")
    print(time_elapsed)
