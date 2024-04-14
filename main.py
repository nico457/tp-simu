from random import random
def distrUniforme(a,b):
    return round(a + random() * (b-a),4)

def menu():
    cad = 'Menu de Opciones\n' \
          '==============================================\n' \
          '1 ----- Distribucion Uniforme \n' \
          '2 ----- Distribucion Exponencia\n' \
          '3 ----- Distribucion Normal\n' \
          '0 ----- Salir\n' \
          'Ingrese su opcion: '
    return int(input(cad))

if __name__ == '__main__':
    opcion = -1
    while opcion != 0:
        opcion = menu()
        n = int(input("Ingrese el tamaño de muestra (MAX 1.000.000): "))
        if (n >= 1000000):
            print("El tamaño de muestra es muy grande")
        if opcion == 1:
            li = int(input("Ingrese el limite inferior: "))
            ls = int(input("Ingrese el limite superior: "))
            for i in range(n):
                print( distrUniforme(li,ls),end=",")

