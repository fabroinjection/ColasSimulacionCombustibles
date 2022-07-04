import random

def eleccionServidor():
    rnd = random.random()
    if rnd < 0.5:
        return rnd, "Empleado 1"
    elif rnd < 1:
        return rnd, "Empleado 2"
    else:
        return rnd, "Error"

def definicionTipoVehiculo(probAuto, probMoto, probCamioneta):
    rnd = random.random()
    if rnd < probAuto:
        return rnd, "Auto", 45
    elif rnd < (probAuto + probMoto):
        return rnd, "Moto", 10
    elif rnd < (probAuto + probMoto + probCamioneta):
        return rnd, "Camioneta", 60
    else:
        return rnd, "Error", -10

def quiereLimpieza(probQuiereLimpieza):
    rnd = random.random()
    if rnd < probQuiereLimpieza:
        return rnd, True
    else:
        return rnd, False

def calcularTanqueInicial(tanqueEnLitros):
    rnd = random.random()
    return rnd, (rnd * tanqueEnLitros)
