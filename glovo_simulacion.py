import numpy as np
from scipy.stats import weibull_min, beta, exponweib, lognorm
import math
import random

HV = float('inf')

# Variables globales de simulación
T = TF = 0
N = ITD = 0
TPP = 0
TC = []
NT = NA = 0
Desc = DD = SD = 0
V = TVE = TVO = SU = SSU = 0
TEntrega = TEspera = STE = TU = 0
PF = IT = 0
STO = 0
PER = PTO = PSU = PUA = GN = PCD = PCR = 0
DE = 0
CR = CT = 0  
SR = 0

def condiciones_iniciales(t, tf):
    global T, TF, TPP, TC
    global NT, NA, Desc, DD, SD
    global V, TVE, TVO, SU, SSU
    global TEntrega, TEspera, STE, TU
    global PF, IT, STO
    global PER, PTO, PSU, PUA, GN, PCD, PCR

    T = t
    TF = tf
    TPP = 0
    TC = [0 for _ in range(N)]
    NT = NA = 0
    Desc = DD = SD = 0
    V = TVE = TVO = SU = SSU = 0
    TEntrega = TEspera = STE = TU = 0
    PF = IT = 0
    STO = 0
    PER = PTO = PSU = PUA = GN = PCD = PCR = 0

def getIP():
    c = 3.274918273645872918273 
    loc = -0.000012345678901234567 
    scale = 1.532849275019283746
    R = random.uniform(0, 1)
    intervalo = weibull_min.ppf(R, c, loc=loc, scale=scale)
    return max(0, math.ceil(intervalo))


def getPP():
    a = 1.681212960359686
    b = 3.2564104863050165
    loc = -36.62681888121217
    scale = 6872.8132072791395
    R = random.uniform(0, 1)
    intervalo = beta.ppf(R, a, b, loc=loc, scale=scale)
    return max(0, math.ceil(intervalo))


def getDE():
    a = 0.06596328958329858
    c = 15.129221894112517
    loc = 0.4967176809771827
    scale = 4.296799972501318
    R = random.uniform(0, 1)
    intervalo = exponweib.ppf(R, a, c, loc=loc, scale=scale)
    return max(0, math.ceil(intervalo))


def getTEntrega():
    a = 0.9712502130246116
    b = 0.9816062509561512
    loc = 9.999999999999998
    scale = 10.98333420209909
    R = random.uniform(0, 1)
    intervalo = beta.ppf(R, a, b, loc=loc, scale=scale)
    return max(0, math.ceil(intervalo))

def buscar_menor_tiempo_comprometido():
    global TC, N
    menor = HV
    posicion = -1
    for i in range(N):
        if TC[i] < menor:
            menor = TC[i]
            posicion = i
    return posicion


def calcular_velocidad_esperada():
    global V
    r = np.random.rand()
    if r <= 0.6:
        V = 10
    elif r <= 0.85:
        V = 15
    else:
        V = 20


def arrepentimiento():
    global TU, TEspera, DD, Desc, NA
    r = np.random.rand()
    if r <= 0.7:
        TU = 6
    elif r <= 0.9:
        TU = 3
    else:
        TU = 2

    if TEspera > TU:
        try:
            DD = 0.5 * (TEspera - TU) / 10
            if DD > 1: 
                DD = 1
        except OverflowError:
            DD = 1
        if Desc < DD:
            NA += 1
            return True #se arrepiente
        else:
            return False
    else:
        return False


def calificar_servicio(tc):
    global V, TVE, TVO, SU, SSU, DE, TEspera, TEntrega
    calcular_velocidad_esperada()
    TVE = (DE / V) * 60
    TVO = TEntrega
    retraso = TVO - TVE

    if retraso <= 7.5:
        SU = 5
    elif retraso <= 10:
        SU = 4
    elif retraso <= 12.5:
        SU = 3
    elif retraso <= 15:
        SU = 2
    else:
        SU = 1
    SSU += SU


def calcular_resultados():
    global PER, PSU, PUA, PCD, PCR, NT, STE, SD, CR, CT
    

    PER = STE // (NT - NA) if NT > 0 else 0
    PSU = SSU / (NT) if (NT) > 0 else 0
    PUA = (NA / NT) * 100 if NT > 0 else 0
    PCD = (SD / CT) * 100 if CT > 0 else 0
    PCR = (CR / CT) * 100 if CT > 0 else 0


def imprimir_resultados():
    MAX_PRINT = 10**6  
    print(f"Cantidad de repartidores: {N:.2f}")
    print(f"Intervalo de tiempo entre descuentos: {ITD:.2f}")
    print(f"Promedio de espera hasta que un pedido sea atendido por un repartidor: {PER:.2f}")
    print(f"Promedio de satisfaccion del usuario: {PSU:.2f}")
    print(f"Porcentaje de usuarios arrepentidos: {PUA:.2f}%")
    print(f"Porcentaje de costos destinados a descuentos: {PCD:.2f}%")
    print(f"Porcentaje de costos destinados a repartidores: {PCR:.2f}%")
    print(f"Ganancia neta: {GN:.2f}")


def simular():
    global T, TF, NT, N, ITD, TPP, TC, TEspera, STE, Desc, SD, PF, IT, GN, DE, PF, STO, SR, CR, CT, SSU, TEntrega

    if N <= 0 or ITD <= 0:
        print(f"El valor de las variables de control debe ser mayor a 0: N={N}, ITD={ITD}")
        return
    if TF <= T:
        print(f"El valor de TF debe ser mayor que T: T={T}, TF={TF}")
        return
    if T < 0 or TF < 0:
        print(f"T y TF no pueden ser negativos: T={T}, TF={TF}")
        return

    STE = 0
    SR = 65000 #Salario Por Mes
    print(f"Inicio de simulacion: T={T}, TF={TF}")

    CR = SR * N 
    GN -= CR

    while True:
        T = TPP
        NT += 1
        IP = getIP()
        TPP = T + IP
        PP = getPP()
        DE = getDE()
        TEntrega = getTEntrega()
        idx_TC = buscar_menor_tiempo_comprometido()
        arrepentido = False

        if idx_TC == -1:
            print("No hay repartidores disponibles")
            break

        menorTC = TC[idx_TC]
        if T >= menorTC:
            TEspera = 0
            TC[idx_TC] = T + TEntrega
            PF = PP
        else:
            TEspera = TC[idx_TC] - T
            Desc = min(5, (TEspera // ITD)) * 0.05  #máximo 6 descuentos acumulados (25%)
            PF = max(0, PP - Desc*PP)
            arrepentido = arrepentimiento()
            if arrepentido==True:
                SSU += 1
            if arrepentido==False:
                STE += TEspera
                TC[idx_TC] += TEntrega
                SD = SD + Desc*PP

        if arrepentido==False:
            IT += PP*0.05
            GN += PP*0.05 - Desc*PP
            calificar_servicio(TC[idx_TC])

        if T > TF:
            CT = SR*N + SD
            calcular_resultados()
            imprimir_resultados()
            break


N = 12
ITD = 2
condiciones_iniciales(t = 0, tf = 30 * 60 * 24)  # 10 dias
simular()