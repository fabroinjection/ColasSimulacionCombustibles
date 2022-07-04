import random
import numpy as np


def exponencialNegativa(media):
    rnd = random.random()
    return rnd, round(-media * np.log(1 - rnd), 2)

'''
def normal(media, desvEst):
    rnds = [random.random() for i in range(12)]
    return (np.sum(rnds) - 6) * desvEst + media
'''


def uniforme(a, b):
    rnd = random.random()
    segundaParte = rnd * (b - a)
    retorno = a + segundaParte
    return rnd, retorno


def truncate(values, decs=0):
    """funcion utilizada para truncar nuevaDistr y no trabajar con todos los decimales de python """
    if values == "":
        return ""
    return np.trunc(values * 10 ** decs) / (10 ** decs)