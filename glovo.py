import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats





def condiciones_iniciales(t, tf):
    global T, TF
    global N, ITD #TODO: Ver porque carajo las inicializa antes y las declara aca
    global TPP 
    global TC
    global NT, NA
    global Desc, DD, SD 
    global V, TVE, TVO, SU, SSU
    global TEntrega, TEspera, STEspera, TU
    global PF, IT
    global STO
    global PER, PTO, PSU, PUA, GN, PCD, PCR


    T = t  
    T = tf

    TPP = 0

    TC = [0 for i in range(N)]

    NT = NA = 0

    Desc = DD = SD = 0

    V = TVE = TVO = SU = SSU = 0

    TEntrega = TEspera = STEspera = TU = 0

    PF = IT = 0

    STO = 0

    PER = PTO = PSU = PUA = GN = PCD = PCR = 0


def buscar_menor_tiempo_comprometido():
    global TC, N
    menor = float('inf')
    posicion = -1
    for i in range(N):
        if TC[i] < menor:
            menor = TC[i]
            posicion = i
    return posicion

def calcular_velocidad_esperada():
    global V
    
    random = np.random.rand()

    if(random <= 0.6):
        V = 35
    elif(random <= 0.85):
        V = 50
    else:
        V = 35


def arrepentimiento():
    global TU, TEspera, DD, SD, Desc, NA

    random = np.random.rand()

    if(random <= 0.7):
        TU = 20
    elif(random <= 0.9):
        TU = 10
    else:
        TU = 5

    if(TEspera > TU):
        DD = 0.5 * (TEspera - TU)
        if(Desc < DD):
            NA += 1
            # TODO: prox orden
        else:
          return  
    else:
        return
    
def calcular_tiempo_entrega(DE):
    global TEntrega
    if(DE <= 5):
        TEntrega = obtener_TE0()  
    elif(DE <= 10):
        TEntrega = obtener_TE5()
    else:
        TEntrega = obtener_TE10()


def calificar_servicio():
    global V, TVE

    calcular_velocidad_esperada()

    TVE = DE*V

    TVO = #TODO TC -T -TEspera

    random = np.random.rand()

    if(TVO <= TVE):
        if(random <= 0.8):
            SU = 5
        elif(random <= 0.95):
            SU = 4
        else:
            SU = 3
    else:
        if(random <= 0.8):
            SU = 2
        elif(random <= 0.9):
            SU = 1

    SSU += SU


def calcular_IP():
    #TODO
    return 5

def obtener_TE0():
    #TODO
    return 3

def obtener_TE5():
    #TODO
    return 4

def obtener_TE10():
    #TODO
    return 5

def obtener_PP():
    #TODO
    return 5

def obtener_DE():
    #TODO
    return 5

def simular():
    #TODO: Implementar la simulacion completa
    return 0


def calcular_resultados():
    global PER, PTO, PSU, PUA, PCD, PCR
    global NT, STE

    PER = STE / NT

    PTO = (STO / T) * 100

    PSU = SSU / (NT - NA)

    PUA = (NA / NT) * 100

    PCD = (SD/CT) * 100

    PCR = (CR/CT) * 100