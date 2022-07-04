import random

import pandas as pd

class Controlador():
    def rungeKuttaCarga(self, fun, xi, yi, cantLitrosCarga):
        dfCarga = pd.DataFrame(
            {"xi": [], "yi": [], "k1": [], "k2": [], "k3": [], "k4": [], "xi+1": [], "yi+1": []})
        h = 0.05
        while yi < cantLitrosCarga:
            fila = pd.DataFrame({"xi": [], "yi": [], "k1": [], "k2": [], "k3": [], "k4": [], "xi+1": [], "yi+1": []})

            k1 = fun(xi, yi)
            k2 = fun(xi + h / 2, yi + h / 2 * k1)
            k3 = fun(xi + h / 2, yi + h / 2 * k2)
            k4 = fun(xi + h, yi + h * k3)

            fila.at[0, "xi"] = xi
            fila.at[0, "yi"] = yi

            yi = yi + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
            xi += h

            fila.at[0, "k1"] = k1
            fila.at[0, "k2"] = k2
            fila.at[0, "k3"] = k3
            fila.at[0, "k4"] = k4
            fila.at[0, "xi+1"] = xi
            fila.at[0, "yi+1"] = yi

            dfCarga = pd.concat([dfCarga, fila], ignore_index=True)

        return xi, dfCarga

    def calcularRKCarga(self, inicioTanque, cantLitrosCarga):
        ecDif = lambda t, C: 30 * C + 10
        valor, dfCarga = self.rungeKuttaCarga(ecDif, 0, inicioTanque, cantLitrosCarga)
        valorReal = valor * 10
        return dfCarga, valorReal


