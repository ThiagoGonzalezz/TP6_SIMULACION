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
    c = 1.002167470034177
    loc = -2.2262196250160577e-05
    scale = 31.56440023360133
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
    s = 10.147654780109296
    loc = 9.999999999999998
    scale = 0.18864986051840427
    R = random.uniform(0, 1)
    intervalo = lognorm.ppf(R, s, loc=loc, scale=scale)
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
        V = 35
    elif r <= 0.85:
        V = 50
    else:
        V = 35


def arrepentimiento():
    global TU, TEspera, DD, SD, Desc, NA
    r = np.random.rand()
    if r <= 0.7:
        TU = 20
    elif r <= 0.9:
        TU = 10
    else:
        TU = 5

    if TEspera > TU:
        DD = 0.5 * (TEspera - TU)
        if Desc < DD:
            NA += 1
            return True #se arrepiente
        else:
            return False
    else:
        return False


def calificar_servicio(tc):
    global V, TVE, TVO, SU, SSU, DE
    calcular_velocidad_esperada()
    TVE = DE * V
    TVO = tc - T - TEspera
    r = np.random.rand()
    if TVO <= TVE:
        if r <= 0.8:
            SU = 5
        elif r <= 0.95:
            SU = 4
        else:
            SU = 3
    else:
        if r <= 0.8:
            SU = 2
        elif r <= 0.9:
            SU = 1
        else:
            SU = 0
    SSU += SU


def calcular_resultados():
    global PER, PTO, PSU, PUA, PCD, PCR, NT, STE, SD, CR, CT
    CT = SR*N + SD


    PER = STE / (NT - NA) if NT > 0 else 0 #ste es sumatoria de tiempo de espera
    PTO = (STO / T) * 100 if T > 0 else 0
    PSU = SSU / (NT - NA) if (NT - NA) > 0 else 0
    PUA = (NA / NT) * 100 if NT > 0 else 0
    PCD = (SD / CT) * 100 if CT > 0 else 0
    PCR = (CR / CT) * 100 if CT > 0 else 0


def imprimir_resultados():
    print(f"Cantidad de repartidores: {N:.2f}")
    print(f"Intervalo de tiempo entre descuentos: {ITD:.2f}")
    print(f"Porcentaje de espera hasta que un pedido sea atendido por un Repartidor: {PER:.2f}")
    print(f"Porcentaje de tiempo ocioso: {PTO:.2f}%")
    print(f"Promedio de satisfaccion del usuario: {PSU:.2f}")
    print(f"Porcentaje de usuarios arrepentidos: {PUA:.2f}%")
    print(f"Porcentaje de costos destinados a descuentos: {PCD:.2f}%")
    print(f"Porcentaje de costos destinados a repartidores: {PCR:.2f}%")
    print(f"Ganancia neta: {GN:.2f}")


def simular():
    global T, TF, NT, N, ITD, TPP, TC, TEspera, STE, Desc, SD, PF, IT, GN, DE, PF, STO, SR, CR

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
    SR = 1000
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

        if T >= TC[idx_TC]:
            STO += T - TC[idx_TC]
            TEspera = 0
            TC[idx_TC] = T + TEntrega
            PF = PP
        else:
            TEspera = TC[idx_TC] - T
            STE += TEspera
            TC[idx_TC] += TEntrega
            Desc = min(3, (TEspera // ITD)) * 0.05 * PP #máximo 3 descuentos acumulados
            PF = max(0, PP - Desc)
            arrepentido = arrepentimiento()
            if arrepentido==False:
                SD += Desc

        if arrepentido==False:
            IT += PP
            GN += PF
            calificar_servicio(TC[idx_TC])

        if T > TF:
            calcular_resultados()
            imprimir_resultados()
            break

#N=10
#ITD = 20
#condiciones_iniciales(t = 0, tf = 3600 * 12 * 30)  # 20 dias
#simular()




mejor_ganancia = -float('inf')
mejor_N = 0
mejor_ITD = 0

for N_test in range(100, 1000):          # probando de 100 a 1000 repartidores
    for ITD_test in range(5, 101, 5):  # probando ITD de 5 a 100
        N = N_test
        ITD = ITD_test
        condiciones_iniciales(t=0, tf=3600*12*30)
        simular()
        if GN > mejor_ganancia:
            mejor_ganancia = GN
            mejor_N = N_test
            mejor_ITD = ITD_test

print(f"Mejor ganancia: {mejor_ganancia}, con N={mejor_N}, ITD={mejor_ITD}")
