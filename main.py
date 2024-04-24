import math
from random import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2, ksone


def uniforme(a, b):
    return round(a + random() * (b - a), 4)


def exponencial(xlambda):
    return round((-1 / xlambda) * np.log(1 - random()), 4)


def normal(media, desviacion):
    x1=x2=0
    while x1 == 0 or x2 == 0:
        x1 = uniforme(0, 1)
        x2 = uniforme(0, 1)
    z1 = (math.sqrt(-2 * np.log(x1)) * math.cos(2 * math.pi * x2)) * desviacion + media
    z2 = (math.sqrt(-2 * np.log(x1)) * math.sin(2 * math.pi * x2)) * desviacion + media
    return round(z1, 4), round(z2, 4)


def graficar(datos, intervalos):
    plt.hist(datos, bins=intervalos, edgecolor='blue')
    plt.title('Histograma de Frecuencias')
    plt.xlabel('Intervalos')
    plt.ylabel('Frecuencia')
    plt.grid(False)
    plt.show()


def elegirIntervalo():
    num = int(input("Ingrese el número de intervalos (10, 12, 16 o 23): "))
    while num not in (10, 12, 16, 23):
        print("Cantidad de intervalos incorrecta")
        num = int(input("Ingrese el número de intervalos (10, 12, 16 o 23): "))
    return num


def menu():
    cad = '\nMenu de Opciones\n' \
          '==============================================\n' \
          '1 ----- Distribución Uniforme \n' \
          '2 ----- Distribución Exponencial\n' \
          '3 ----- Distribución Normal\n' \
          '0 ----- Salir\n'
    return print(cad)


def pruebasDeBondad(datos, intervalos, opcion, min, max, *parametros):
    chi2_calc = 0
    chi_tabulado = chi2.ppf(0.9 / 2, intervalos - len(parametros) - 1)
    ks_calc = ks_max = 0
    n = len(datos)
    frec_observadas, bins = np.histogram(datos, bins=intervalos)
    nivel_confianza = 0.9
    # Factor de correcion p/ que coincida con tabla
    ks_tabulado = ksone.ppf(nivel_confianza + 0.05, n)
    prob_observada_AC = prob_esperada_AC= 0

    if opcion == 1:
        frecuencia_esperada = n / intervalos
        frec_men_5 = frec_obs_ac = 0
        for i in range(intervalos):
            frec_obs_ac += frec_observadas[i]
            frec_men_5 += frecuencia_esperada
            prob_observada_AC += frec_observadas[i] / n
            prob_esperada_AC += frecuencia_esperada / n

            if frec_men_5 < 5:
                continue

            #Chi2
            chi2_calc += ((frec_obs_ac - frec_men_5) ** 2) / frec_men_5

            #KS
            ks_calc = abs(prob_observada_AC - prob_esperada_AC)
            if ks_calc > ks_max:
                ks_max = ks_calc

            if i == (intervalos - 1) and frec_men_5 < 5:
                chi2_incompleto = ((frec_obs_ac - frec_men_5) ** 2) / frec_men_5
                chi2_calc += chi2_incompleto

            frec_men_5 = frec_obs_ac = 0

    elif opcion == 2:
        amplitud = (max - min) / intervalos
        desde = min
        hasta = desde + amplitud
        frec_men_5 = frec_obs_ac = 0
        for i in range(intervalos):
            frec_obs_ac += frec_observadas[i]
            frecuencia_esperada = ((1 - math.exp(-parametros[0] * hasta)) - (1 - math.exp(-parametros[0] * desde))) * n
            frec_men_5 += frecuencia_esperada
            prob_observada_AC += frec_observadas[i] / n
            prob_esperada_AC += frecuencia_esperada / n

            if frec_men_5 < 5:
                continue
            #Chi2
            chi2_calc += ((frec_obs_ac - frec_men_5) ** 2) / frec_men_5

            #KS
            ks_calc = abs(prob_observada_AC - prob_esperada_AC)
            if ks_calc > ks_max:
                ks_max = ks_calc

            if i == (intervalos - 1) and frec_men_5 < 5:
                chi2_incompleto = ((frec_obs_ac - frec_men_5) ** 2) / frec_men_5
                chi2_calc += chi2_incompleto

            frec_men_5 = frec_obs_ac = 0
            desde = hasta
            hasta += amplitud

    elif opcion == 3:
        amplitud = (max - min) / intervalos
        desde = min
        hasta = desde + amplitud
        frec_men_5 = frec_obs_ac = 0
        for i in range(intervalos):
            frec_obs_ac += frec_observadas[i]
            marca = (desde + hasta) / 2
            frecuencia_esperada = ((math.exp(-0.5 * (((marca - parametros[0]) / parametros[1]) ** 2))) / (
                        parametros[1] * math.sqrt(2 * math.pi))) * (hasta - desde) * n
            frec_men_5 += frecuencia_esperada
            prob_observada_AC += frec_observadas[i] / n
            prob_esperada_AC += frecuencia_esperada / n

            if frec_men_5 < 5:
                continue

            #Chi2
            chi2_calc += ((frec_obs_ac - frec_men_5) ** 2) / frec_men_5

            #KS
            ks_calc = abs(prob_observada_AC - prob_esperada_AC)
            if ks_calc > ks_max:
                ks_max = ks_calc

            desde = hasta
            hasta += amplitud

    if chi2_calc <= chi_tabulado:
        print()
        print("Chi calculado < Chi tabulado")
        print(round(chi2_calc, 4), "<", round(chi_tabulado, 4))
        print("Se acepta la hipótesis nula H0")

    else:
        print()
        print("Chi calculado > Chi tabulado")
        print(round(chi2_calc, 4), ">", round(chi_tabulado, 4))
        print("No se acepta la hipótesis nula H0")

    if ks_max <= ks_tabulado:
        print()
        print("KS calculado < KS tabulado")
        print(round(ks_max, 4), "<", round(ks_tabulado, 4))
        print("Se acepta la hipótesis nula H0")
    else:
        print()
        print("KS calculado > KS tabulado")
        print(round(ks_max, 4), ">", round(ks_tabulado, 4))
        print("No se acepta la hipótesis nula H0")


if __name__ == '__main__':
    opcion = -1
    intervalos = 0

    while opcion != 0:

        menu()
        opcion = int(input("Ingrese su opcion: "))
        if opcion == 0:
            break
        dato = 0
        datos = []
        n = int(input("Ingrese el tamaño de muestra (MAX 1.000.000): "))
        intervalos = elegirIntervalo()

        if (n > 1000000):
            print("El tamaño de muestra es muy grande")
        if opcion == 1:

            li = int(input("Ingrese el limite inferior: "))
            ls = int(input("Ingrese el limite superior: "))
            min = li
            max = ls
            parametros = ()
            for i in range(n):
                dato = uniforme(li, ls)
                datos.append(dato)
                print(dato, end=",")

        elif opcion == 2:
            xlambda = float(input("Ingrese lambda: "))
            parametros = (xlambda,)

            for i in range(n):
                dato = exponencial(xlambda)
                datos.append((dato))
                print(dato, end=",")
                if i == 0:
                    min = datos[0]
                    max = datos[0]

                if dato < min:
                    min = dato
                if dato > max:
                    max = dato


        elif opcion == 3:
            media = float(input("Ingrese la media: "))
            desviacion = float(input("Ingrese la desviación: "))
            parametros = (media, desviacion)
            if n % 2 != 0:
                dato_extra = normal(media, desviacion)[0]
                datos.append(dato_extra)
                print(dato_extra, end=",")
            for i in range(n // 2):
                dato1, dato2 = normal(media, desviacion)
                datos.append(dato1)
                datos.append(dato2)
                print(dato1, ",", dato2, end=" , ")

                if i == 0:
                    min = datos[0]
                    max = datos[0]
                if dato1 < min:
                    min = dato1
                if dato1 > max:
                    max = dato1
        print()
        graficar(datos, intervalos)
        print("PRUEBAS DE BONDAD")
        pruebasDeBondad(datos, intervalos, opcion, min, max, *parametros)
