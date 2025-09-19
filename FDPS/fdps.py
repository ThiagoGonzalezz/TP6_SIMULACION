import math
import random
from scipy.stats import weibull_min
from scipy.stats import beta
from scipy.stats import exponweib
from scipy.stats import lognorm

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