from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

import distribuciones


class PantallaRK(QMainWindow):
    """Incializar clase"""

    def __init__(self):
        super().__init__()

        """Cargar la GUI"""
        uic.loadUi("Pantallas/pantallaRK.ui", self)

    def mostrarRK(self, rungeKuttaCarga):
        self.cargarTabla(rungeKuttaCarga, self.tblCarga)

    def cargarTabla(self, listaRK, tabla):
        fila = 0
        cantFilas = len(listaRK)

        if cantFilas == 0:
            tabla.setRowCount(1)
            tabla.setItem(fila, 0, QTableWidgetItem("No se tuvo que calcular RK."))
            return

        cantTotalFilas = 0
        for m in range(cantFilas):
            cantTotalFilas += len(listaRK[m])
        if cantFilas != 1:
            cantTotalFilas += (cantFilas - 1)
        tabla.setRowCount(cantTotalFilas)


        for j in range(cantFilas):
            cantFilasUnCalculo = len(listaRK[j])
            for i in range(cantFilasUnCalculo):
                tabla.setItem(fila, 0, QTableWidgetItem(str(distribuciones.truncate(listaRK[j].at[i, "xi"], 4))))
                tabla.setItem(fila, 1, QTableWidgetItem(str(distribuciones.truncate(listaRK[j].at[i, "yi"], 4))))
                tabla.setItem(fila, 2, QTableWidgetItem(str(distribuciones.truncate(listaRK[j].at[i, "k1"], 4))))
                tabla.setItem(fila, 3, QTableWidgetItem(str(distribuciones.truncate(listaRK[j].at[i, "k2"], 4))))
                tabla.setItem(fila, 4, QTableWidgetItem(str(distribuciones.truncate(listaRK[j].at[i, "k3"], 4))))
                tabla.setItem(fila, 5, QTableWidgetItem(str(distribuciones.truncate(listaRK[j].at[i, "k4"], 4))))
                tabla.setItem(fila, 6, QTableWidgetItem(str(distribuciones.truncate(listaRK[j].at[i, "xi+1"], 4))))
                tabla.setItem(fila, 7, QTableWidgetItem(str(distribuciones.truncate(listaRK[j].at[i, "yi+1"], 4))))

                fila += 1
            if cantFilas != 1 & (j != (cantFilas - 1)):
                tabla.setItem(fila, 0, QTableWidgetItem("Cálculo del otro evento:"))
                fila += 1

