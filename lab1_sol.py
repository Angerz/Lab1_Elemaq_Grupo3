#Librerías necesarias
import numpy as np  #Para los cálculos algebraicos
import seaborn as sn    #Para el gráfico de Mohr
import matplotlib.pyplot as plt     #Para mostrar la imagen de los puntos críticos

def variando_ab():
    global ab
    #Definimos el vector de valores de AB que se analizarán
    ab_inf = float(input("Define el rango de valores que quieres para la longitud de la barra AB\nLímite inferior: "))
    ab_sup = float(input("Límite superior: "))
    ab = np.linspace(ab_inf, ab_sup, num=50)

def variando_cd():
    global cd
    #Definimos el vector de valores de CD que se analizarán
    cd_inf = float(input("Define el rango de valores que quieres para la longitud de la barra CD\nLímite inferior: "))
    cd_sup = float(input("Límite superior: "))
    cd = np.linspace(cd_inf, cd_sup, num=50)

def esfuerzos_seccion():
    global esf_norm_flex, esf_cort_tors, esf_cort_cort
    '''Calcula los esfuerzos presentes en la sección A con los valores originales del problema'''
    #Calculo de esfuerzos
    #Esfuerzo cortante por carga cortante
    a = np.pi*((d_ab/2)**2) #Area de la sección transversal de la barra AB
    v = fy #Esfuerzo cortante
    esf_cort_cort = ((4/3)*(v/a))     #Dividido entre 1000 para pasarlo a kpsi

    #Esfuerzo cortante por torsión
    t=fy*cd #Momento torzor
    j=(np.pi*(d_ab**4))/32  #Momento polar
    esf_cort_tors = ((t*(d_ab/2))/j)   #Dividido entre 1000 para pasarlo a kpsi

    #Esfuerzo normal por flexión
    m = fy*(ab+bc)  #Momento flector
    i = j/2 #Momento lineal
    esf_norm_flex = ((m*(d_ab/2))/i)    #Dividido entre 1000 para pasarlo a kpsi


def esfuerzos_ab_variable(ab):
    global esf_norm_flex, esf_cort_tors, esf_cort_cort
    '''Calcula los esfuerzos presentes en la sección A con los valores de AB variables'''
    #Calculo de esfuerzos
    #Esfuerzo cortante por carga cortante
    a = np.pi*((d_ab/2)**2) #Area de la sección transversal de la barra AB
    v = fy #Esfuerzo cortante
    esf_cort_cort = (4/3)*(v/a)

    #Esfuerzo cortante por torsión
    t=fy*cd #Momento torzor
    j=(np.pi*(d_ab**4))/32  #Momento polar
    esf_cort_tors = (t*(d_ab/2))/j

    #Esfuerzo normal por flexión
    m = fy*(ab+bc)  #Momento flector
    i = j/2 #Momento lineal
    esf_norm_flex = (m*(d_ab/2))/i


def esfuerzos_cd_variable(cd):
    global esf_norm_flex, esf_cort_tors, esf_cort_cort
    '''Calcula los esfuerzos presentes en la sección A con los valores de AB variables'''
    #Calculo de esfuerzos
    #Esfuerzo cortante por carga cortante
    a = np.pi*((d_ab/2)**2) #Area de la sección transversal de la barra AB
    v = fy #Esfuerzo cortante
    esf_cort_cort = (4/3)*(v/a)

    #Esfuerzo cortante por torsión
    t=fy*cd #Momento torzor
    j=(np.pi*(d_ab**4))/32  #Momento polar
    esf_cort_tors = (t*(d_ab/2))/j

    #Esfuerzo normal por flexión
    m = fy*(ab+bc)  #Momento flector
    i = j/2 #Momento lineal
    esf_norm_flex = (m*(d_ab/2))/i 

def circulo_mohr():
    global A, B, C
    #Definir los puntos del círculo de Mohr
    A = (esf_norm_flex, esf_cort_tors)
    B = (0, -esf_cort_tors)
    C = (esf_norm_flex/2, 0)

def esfuerzos_principales():
    global sigma_1, sigma_2, tau_max
    # Cálculo de los esfuerzos principales
    sigma_1 = (esf_norm_flex/2 + np.sqrt((esf_norm_flex/2)**2 + esf_cort_tors**2))
    sigma_2 = (esf_norm_flex/2 - np.sqrt((esf_norm_flex/2)**2 + esf_cort_tors**2))

    # Cálculo de los esfuerzos cortantes máximos
    tau_max = np.sqrt(((esf_norm_flex-0))**2 + 4 * esf_cort_tors**2) / 2


def grafica():
    '''Grafica de todos los valores correspondientes dentro del circulo de Mohr'''
    # Configuración de Seaborn
    sn.set(style='whitegrid')
    # Configuración del gráfico
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlabel('Esfuerzo normal (psi)')    
    ax.set_ylabel('Esfuerzo de corte (psi)')

    # Agregar líneas punteadas de los ejes de coordenadas
    ax.axhline(0, color='yellow', linestyle='dashed')
    ax.axvline(0, color='yellow', linestyle='dashed')

    # Graficar el círculo de Mohr
    ax.plot([A[0], B[0]], [A[1], B[1]], color='blue')
    ax.plot(A[0], A[1], marker='o', color='red')
    ax.plot(B[0], B[1], marker='o', color='red')
    ax.plot(C[0], C[1], marker='o', color='red')

    # Etiquetas de los puntos
    ax.text(A[0], A[1], 'A', ha='right', va='bottom')
    ax.text(B[0], B[1], 'B', ha='right', va='top')
    ax.text(C[0], C[1], 'C', ha='left', va='center')

    # Calcular el centro del círculo de Mohr
    centro_x = (A[0] + B[0]) / 2
    centro_y = (A[1] + B[1]) / 2

    # Calcular el radio del círculo de Mohr
    radio = np.sqrt((A[0] - centro_x) ** 2 + (A[1] - centro_y) ** 2)

    # Generar los puntos del círculo de Mohr
    theta = np.linspace(0, 2 * np.pi, 100)
    parte_x = centro_x + radio * np.cos(theta)
    parte_y = centro_y + radio * np.sin(theta)

    # Graficar el círculo de Mohr
    ax.plot(parte_x, parte_y, color='green')

    # Graficar los esfuerzos principales y los esfuerzos cortantes máximos en el círculo de Mohr
    ax.plot(sigma_1, 0, marker='o', color='purple')
    ax.plot(sigma_2, 0, marker='o', color='purple')
    ax.plot(0, tau_max, marker='o', color='purple')

    # Etiquetas de los esfuerzos principales y los esfuerzos cortantes máximos
    ax.text(sigma_1, 0, 'σ₁', ha='left', va='center')
    ax.text(sigma_2, 0, 'σ₂', ha='right', va='center')
    ax.text(0, tau_max, 'τ_max', ha='right', va='bottom')

    # Graficar la línea punteada horizontal
    ax.hlines(tau_max, 0, esf_norm_flex/2, color='purple', linestyle='dashed')

    # Mostrar el gráfico
    plt.show()

def von_mises(factor_seguridad):
    #Calcula el esfuerzo de Von Mises y el asfuerzo admisible
    global esfuerzo_admisible, esfuerzo_von_mises

    esfuerzo_von_mises = np.sqrt(esf_norm_flex**2+3*(esf_cort_tors**2))
    esfuerzo_fluencia = 53600  # Esfuerzo de fluencia para AISI 1020 estirado en frío (en KPSI)
    esfuerzo_admisible = esfuerzo_fluencia / factor_seguridad

def verificar_falla(n):
    #Función que verifica si la pieza falla aplicando la teoría de fallas de Von Misses
    if opcion == "1":
        #Comprueba si el esfuerzo de Von Mises es mayor que el esfuerzo admisible
        if esfuerzo_von_mises > esfuerzo_admisible:
            print("El material ha fallado según la teoría de Von Mises.")
        
        else:
            print("El material no ha fallado según la teoría de Von Mises.")

    elif opcion == "2":
        #Comprueba si el esfuerzo de Von Mises es mayor que el esfuerzo admisible
        if esfuerzo_von_mises > esfuerzo_admisible:
            #Va añadiendo cada uno de los valores al arreglo correspondiente dependiendo si falla o no
            ab_falla.append(n)    
        else:
            ab_no_falla.append(n)
        
    else:
        #Comprueba si el esfuerzo de Von Mises es mayor que el esfuerzo admisible
        if esfuerzo_von_mises > esfuerzo_admisible:
            #Va añadiendo cada uno de los valores al arreglo correspondiente dependiendo si falla o no
            cd_falla.append(n)    
        else:
            cd_no_falla.append(n)

def comprobacion_fs(fs):
    #Comprueba la validez del factor de seguridad

    if fs <=1:
        raise Exception("El factor de seguridad debe ser mayor a 1")        #Arroja una error si el factor de seguriad no es mayor que 1
    
def punto_critico():
    #Muestra la imgaen de la ubicación del punto crítico analizado
    sn.set()
    fig, ax = plt.subplots(figsize=(10,10))
    # Cargar la imagen desde un archivo
    imagen = plt.imread("SeccionA.jpeg")  #Ruta de la imagen

    ax.imshow(imagen)
    plt.axis('off')  # Para ocultar los ejes x e y

    # Agregar texto en la parte superior derecha
    texto = "Analizando los esfuerzos en los 4 puntos se determina que los puntos críticos son P (compresión) y Q (tensión)"
    ax.text(1.1, 1, texto, ha='right', va='top', transform=ax.transAxes, fontsize=11, fontweight='bold', color='black')


    # Mostrar la figura con la imagen
    plt.show(block=False)       #Muestra la figura sin dejar de correr el código


if __name__ == "__main__":
    #Inicializa el script
    #-----------------------------------------------------------------------------------------------------------------
    #Definiendo variables y datos del problema

    #Longitudes
    ab, bc, cd, oa = 9, 2, 12, 2 #Proporcionadas por el ejercicio

    #Diámetros
    d_ab, d_bc, d_cd, d_oa = 1, 1.5, 0.75, 1.5#No considerando el diámetro del filete

    #Fuerzas
    fx = 0
    fz = 0

    #Vectores comprobación de falla, nos servirán para determinar entre que rangos de las longitudes dadas la barra falla o no falla
    ab_falla = []
    ab_no_falla = []
    cd_falla = []
    cd_no_falla = []

    #Solicita valores iniciales al usuario
    #-----------------------------------------------------------------------------------------------------------------
    print('MATERIAL AISI 1020 ESTIRADO EN FRÍO (CD)')
    fy = float(input("Valor de la fuerza en Y (Valor del problema Fy = 250): "))
    #Se comprueba que el factor de seguridad ingresado sea correcto
    fs = float(input("Ingrese el factor de seguridad: "))
    comprobacion_fs(fs) 
    # Ejecutar la opción seleccionada, de esta dependerá el proceso a seguir.
    opcion = input("Seleccione una opción:\n1. Calcular con los valores originales\n2. Calcular variando AB\n3. Calcular variando CD\n")
    #Dependeiendo de la opción elegida se seguirá un proceso determinado

    #Procesos
    #-----------------------------------------------------------------------------------------------------------------
    #Proceso 1
    #Calcula los esfuerzos principales, el esfuerzo cortante máximo, grafica el círculo de Mohr y determina si la barra falla o no falla.
    if opcion == "1":  
        #Calcula los esfuerzos en la sección A. 
        esfuerzos_seccion() 
        print("Esfuerzo por Cortante: ", esf_cort_cort, " psi", "\nEsfuerzo por Torsion: ", esf_cort_tors, " psi",
              "\nEsfuerzo por flexión: ", esf_norm_flex, " psi")

        #Grafica el punto crítico
        punto_critico()

        #Calcula los puntos necesarios y grafica el círculo de Mohr
        circulo_mohr()

        #Calculo de los esfuerzos principales
        esfuerzos_principales()
        print('Esfuerzo principal 1: ', sigma_1," psi", '\nEsfuerzo principal 2: ' ,sigma_2, " psi")
        print('Esfuerzo cortante máximo: ', tau_max, " psi")

        #Calcula el esfuerzo de Von Mises
        von_mises(fs)
        print("Esfuerzo de Von Mises: ", esfuerzo_von_mises, " psi")
        print("Esfuerzo admisible: ", esfuerzo_admisible, " psi")

        #Verifica si la barra falla o no
        verificar_falla(any)

        #Grafica el círculo de Mohr
        grafica()

    #Proceso 2
    #Calcula los esfuerzos principales, el esfuerzo cortante máximo, determina si la barra falla o no falla para valores de AB variables.
    #Arroja como salida el rango de valores de AB para los que la barra falla o no falla.
    elif opcion == "2":
        #Genera el vector de valores de AB
        variando_ab()

        #Itera los valores de AB y calcula los esfuerzos para cada uno de ellos
        for i in ab:
            #Calcula los esfuerzos en la sección A. Teniendo como parámetro el valor actual de AB
            esfuerzos_ab_variable(i)

            #Calcula los esfuerzos principales para la vuelta actual
            esfuerzos_principales()

            #Calcula los esfuerzos de Von Mises para la vuelta actual
            von_mises(fs)

            #Verifica si falla la barra para el valor actual de AB
            verificar_falla(i)

        #Verifica si alguna de los arreglos de la comprobación de falla no tiene elementos y devuelve que todos los casos pertenecen al otro arreglo
        if len(ab_falla) == 0:
            print("La barra no falla para todos los valores ingresados")
        elif len(ab_no_falla) ==0:
            print("La barra falla para todos los valores ingresados")
        
        #Si es que ninguno de ellos tiene un numero de elementos igual a 0, muestra el rango de valores para cuando falla y para cuando no falla
        else: 
            comprobacion_falla = [ab_falla[0], ab_falla[-1]]
            comprobacion_no_falla = [ab_no_falla[0], ab_no_falla[-1]]
            print("Falla para: ",comprobacion_falla,"\nNo falla para: ", comprobacion_no_falla)

    
    elif opcion == "3":
        #Genera el vector de valores de CD
        variando_cd()

        #Itera los valores de CD y calcula los esfuerzos para cada uno de ellos
        for i in cd:
            #Calcula los esfuerzos en la sección A. Teniendo como parámetro el valor actual de CD
            esfuerzos_cd_variable(i)

            #Calcula los esfuerzos principales para la vuelta actual
            esfuerzos_principales()

            #Calcula los esfuerzos de Von Mises para la vuelta actual
            von_mises(fs)

            #Verifica si falla la barra para el valor actual de CD
            verificar_falla(i)
        print(cd_falla, cd_no_falla)
        #Verifica si alguna de los arreglos de la comprobación de falla no tiene elementos y devuelve que todos los casos pertenecen al otro arreglo
        if len(cd_falla) == 0:
            print("La barra no falla para todos los valores ingresados")
        elif len(cd_no_falla) ==0:
            print("La barra falla para todos los valores ingresados")
        
        #Si es que ninguno de ellos tiene un numero de elementos igual a 0, muestra el rango de valores para cuando falla y para cuando no falla
        else: 
            comprobacion_falla = [cd_falla[0], cd_falla[-1]]
            comprobacion_no_falla = [cd_no_falla[0], cd_no_falla[-1]]
            print("Falla para: ",comprobacion_falla,"\nNo falla para: ", comprobacion_no_falla)
            
    else:
        raise Exception("Opción inválida. Por favor, seleccione una opción válida.")    #Lanza un error si la opción es inválida
    