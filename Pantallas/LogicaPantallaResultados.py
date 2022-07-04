from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

import distribuciones
from Pantallas import LogicaPantallaRK


class PantallaResultados(QMainWindow):
    """Incializar clase"""

    def __init__(self):
        super().__init__()

        """Cargar la GUI"""
        uic.loadUi("Pantallas/pantallaResultados.ui", self)

        self.btnRungeKutta.clicked.connect(self.mostrarRungeKutta)


    def mostrarRungeKutta(self):
        self.pantallaRK = LogicaPantallaRK.PantallaRK()
        self.pantallaRK.mostrarRK(self.RungeKutta)
        self.pantallaRK.show()



    def mostrarResultados(self, datos, estadisticos, RungeKutta, inicio):
        self.cargarTabla(datos, inicio)
        self.cargarEstadisticas(estadisticos)
        self.RungeKutta = RungeKutta

    def cargarTabla(self, datos, inicio):
        fila = 0

        cantFilas = len(datos)

        #if cantFilas < 400:
        final = cantFilas
        self.tablaResultados.setRowCount(cantFilas)
        """
        else:
            final = 400 + inicio
            self.tablaResultados.setRowCount(401)
        """

        #for i in range(inicio, final):
        for i in range(0, final):
            self.tablaResultados.setItem(fila, 0, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "Reloj"], 4))))
            self.tablaResultados.setItem(fila, 1, QTableWidgetItem(str(datos.at[i, "Evento"])))
            self.tablaResultados.setItem(fila, 2, QTableWidgetItem(str(datos.at[i, "VehicEvento"])))
            self.tablaResultados.setItem(fila, 3, QTableWidgetItem(str(distribuciones.truncate(datos.at[i, "RNDServ"]
                                                                                               , 4))))
            self.tablaResultados.setItem(fila, 4, QTableWidgetItem(str(datos.at[i, "Servidor"])))
            self.tablaResultados.setItem(fila, 5, QTableWidgetItem(str(distribuciones.truncate(datos.at[i, "RNDVehic"]
                                                                                               , 4))))
            self.tablaResultados.setItem(fila, 6, QTableWidgetItem(str(datos.at[i, "Vehiculo"])))
            self.tablaResultados.setItem(fila, 7, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "RNDQuiereLimpieza"], 4))))
            self.tablaResultados.setItem(fila, 8, QTableWidgetItem(str(datos.at[i, "Quiere Limpieza"])))
            self.tablaResultados.setItem(fila, 9, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "RND Llegada"], 4))))
            self.tablaResultados.setItem(fila, 10, QTableWidgetItem(str(
                distribuciones.truncate(datos.at[i, "Tiempo Hasta Prox. Llegada"], 4))))
            self.tablaResultados.setItem(fila, 11, QTableWidgetItem(str(
                distribuciones.truncate(datos.at[i, "Prox. Llegada"], 4))))
            self.tablaResultados.setItem(fila, 12, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "RND Tanque Inicial"], 4))))
            self.tablaResultados.setItem(fila, 13, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "Tanque Inicial"], 4))))
            self.tablaResultados.setItem(fila, 14, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "Tiempo Carga"], 4))))
            self.tablaResultados.setItem(fila, 15, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "Fin Carga 1"], 4))))
            self.tablaResultados.setItem(fila, 16, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "Fin Carga 2"], 4))))
            self.tablaResultados.setItem(fila, 17, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "RND Tiempo Limpieza"], 4))))
            self.tablaResultados.setItem(fila, 18, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "Tiempo Limpieza"], 4))))
            self.tablaResultados.setItem(fila, 19, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "Fin Limpieza 1"], 4))))
            self.tablaResultados.setItem(fila, 20, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "Fin Limpieza 2"], 4))))
            self.tablaResultados.setItem(fila, 21, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "RND Tiempo Cobro"], 4))))
            self.tablaResultados.setItem(fila, 22, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "Tiempo Cobro"], 4))))
            self.tablaResultados.setItem(fila, 23, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "Fin Cobro 1"], 4))))
            self.tablaResultados.setItem(fila, 24, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "Fin Cobro 2"], 4))))
            self.tablaResultados.setItem(fila, 25, QTableWidgetItem(str(datos.at[i, "Estado Emp 1"])))
            self.tablaResultados.setItem(fila, 26, QTableWidgetItem(str(datos.at[i, "Ocupado 1 Por"])))
            self.tablaResultados.setItem(fila, 27, QTableWidgetItem(str(datos.at[i, "Cola Emp 1"])))
            self.tablaResultados.setItem(fila, 28, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "Tiempo Ocup Emp 1"], 4))))
            self.tablaResultados.setItem(fila, 29, QTableWidgetItem(str(datos.at[i, "Estado Emp 2"])))
            self.tablaResultados.setItem(fila, 30, QTableWidgetItem(str(datos.at[i, "Ocupado 2 Por"])))
            self.tablaResultados.setItem(fila, 31, QTableWidgetItem(str(datos.at[i, "Cola Emp 2"])))
            self.tablaResultados.setItem(fila, 32, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "Tiempo Ocup Emp 2"], 4))))
            self.tablaResultados.setItem(fila, 33, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "AC Tiempo Permanencia"], 4))))
            self.tablaResultados.setItem(fila, 34, QTableWidgetItem(str(datos.at[i, "Cant Vehiculos Atendidos"])))
            self.tablaResultados.setItem(fila, 35, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[i, "AC Tiempo Espera"], 4))))
            self.tablaResultados.setItem(fila, 36, QTableWidgetItem(str(datos.at[i, "Llegadas"])))

            fila = fila + 1

        if not (cantFilas < 400):
            self.tablaResultados.setItem(fila, 0, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "Reloj"], 4))))
            self.tablaResultados.setItem(fila, 1, QTableWidgetItem(str(datos.at[(cantFilas - 1), "Evento"])))
            self.tablaResultados.setItem(fila, 2, QTableWidgetItem(str(datos.at[(cantFilas - 1), "VehicEvento"])))
            self.tablaResultados.setItem(fila, 3, QTableWidgetItem(str(distribuciones.truncate(datos.at[(cantFilas - 1), "RNDServ"]
                                                                                               , 4))))
            self.tablaResultados.setItem(fila, 4, QTableWidgetItem(str(datos.at[(cantFilas - 1), "Servidor"])))
            self.tablaResultados.setItem(fila, 5, QTableWidgetItem(str(distribuciones.truncate(datos.at[(cantFilas - 1), "RNDVehic"]
                                                                                               , 4))))
            self.tablaResultados.setItem(fila, 6, QTableWidgetItem(str(datos.at[(cantFilas - 1), "Vehiculo"])))
            self.tablaResultados.setItem(fila, 7, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "RNDQuiereLimpieza"], 4))))
            self.tablaResultados.setItem(fila, 8, QTableWidgetItem(str(datos.at[(cantFilas - 1), "Quiere Limpieza"])))
            self.tablaResultados.setItem(fila, 9, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "RND Llegada"], 4))))
            self.tablaResultados.setItem(fila, 10, QTableWidgetItem(str(
                distribuciones.truncate(datos.at[(cantFilas - 1), "Tiempo Hasta Prox. Llegada"], 4))))
            self.tablaResultados.setItem(fila, 11, QTableWidgetItem(str(
                distribuciones.truncate(datos.at[(cantFilas - 1), "Prox. Llegada"], 4))))
            self.tablaResultados.setItem(fila, 12, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "RND Tanque Inicial"], 4))))
            self.tablaResultados.setItem(fila, 13, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "Tanque Inicial"], 4))))
            self.tablaResultados.setItem(fila, 14, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "Tiempo Carga"], 4))))
            self.tablaResultados.setItem(fila, 15, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "Fin Carga 1"], 4))))
            self.tablaResultados.setItem(fila, 16, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "Fin Carga 2"], 4))))
            self.tablaResultados.setItem(fila, 17, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "RND Tiempo Limpieza"], 4))))
            self.tablaResultados.setItem(fila, 18, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "Tiempo Limpieza"], 4))))
            self.tablaResultados.setItem(fila, 19, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "Fin Limpieza 1"], 4))))
            self.tablaResultados.setItem(fila, 20, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "Fin Limpieza 2"], 4))))
            self.tablaResultados.setItem(fila, 21, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "RND Tiempo Cobro"], 4))))
            self.tablaResultados.setItem(fila, 22, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "Tiempo Cobro"], 4))))
            self.tablaResultados.setItem(fila, 23, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "Fin Cobro 1"], 4))))
            self.tablaResultados.setItem(fila, 24, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "Fin Cobro 2"], 4))))
            self.tablaResultados.setItem(fila, 25, QTableWidgetItem(str(datos.at[(cantFilas - 1), "Estado Emp 1"])))
            self.tablaResultados.setItem(fila, 26, QTableWidgetItem(str(datos.at[(cantFilas - 1), "Ocupado 1 Por"])))
            self.tablaResultados.setItem(fila, 27, QTableWidgetItem(str(datos.at[(cantFilas - 1), "Cola Emp 1"])))
            self.tablaResultados.setItem(fila, 28, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "Tiempo Ocup Emp 1"], 4))))
            self.tablaResultados.setItem(fila, 29, QTableWidgetItem(str(datos.at[(cantFilas - 1), "Estado Emp 2"])))
            self.tablaResultados.setItem(fila, 30, QTableWidgetItem(str(datos.at[(cantFilas - 1), "Ocupado 2 Por"])))
            self.tablaResultados.setItem(fila, 31, QTableWidgetItem(str(datos.at[(cantFilas - 1), "Cola Emp 2"])))
            self.tablaResultados.setItem(fila, 32, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "Tiempo Ocup Emp 2"], 4))))
            self.tablaResultados.setItem(fila, 33, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "AC Tiempo Permanencia"], 4))))
            self.tablaResultados.setItem(fila, 34, QTableWidgetItem(str(datos.at[(cantFilas - 1), "Cant Vehiculos Atendidos"])))
            self.tablaResultados.setItem(fila, 35, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas - 1), "AC Tiempo Espera"], 4))))
            self.tablaResultados.setItem(fila, 36, QTableWidgetItem(str(datos.at[(cantFilas - 1), "Llegadas"])))


        """
        if not (cantFilas < 400):

            self.tablaResultados.setItem(fila, 0, QTableWidgetItem(str(distribuciones.truncate(datos.at[(cantFilas-1),
                                                                                                        "Reloj"], 4))))
            self.tablaResultados.setItem(fila, 1, QTableWidgetItem(str(datos.at[(cantFilas-1), "tipo"])))
            self.tablaResultados.setItem(fila, 2, QTableWidgetItem(str(datos.at[(cantFilas-1), "avion"])))
            self.tablaResultados.setItem(fila, 3, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas-1), "tiempo hasta la prox llegada"], 4))))
            self.tablaResultados.setItem(fila, 4, QTableWidgetItem(str(datos.at[(cantFilas-1), "prox llegada"])))
            self.tablaResultados.setItem(fila, 5, QTableWidgetItem(str(datos.at[(cantFilas-1), "proximo ataque"])))
            self.tablaResultados.setItem(fila, 6, QTableWidgetItem(str(datos.at[(cantFilas-1), "objetivo del ataque"])))
            self.tablaResultados.setItem(fila, 7, QTableWidgetItem(str(datos.at[(cantFilas-1), "duracion del ataque"])))

            self.tablaResultados.setItem(fila, 8, QTableWidgetItem(str(datos.at[(cantFilas-1),
                                                                                "proximo avion que sale"])))
            self.tablaResultados.setItem(fila, 9, QTableWidgetItem(str(datos.at[(cantFilas-1), "estado pista"])))
            self.tablaResultados.setItem(fila, 10, QTableWidgetItem(str(datos.at[(cantFilas-1), "usada por"])))
            self.tablaResultados.setItem(fila, 11, QTableWidgetItem(str(distribuciones.truncate(
                datos.at[(cantFilas-1), "porcentaje ocupacion"], 4))))
            self.tablaResultados.setItem(fila, 12, QTableWidgetItem(str(datos.at[(cantFilas-1), "llegadas"])))
            self.tablaResultados.setItem(fila, 13, QTableWidgetItem(str(datos.at[(cantFilas-1), "aterrizajes"])))
            self.tablaResultados.setItem(fila, 14, QTableWidgetItem(str(datos.at[(cantFilas-1), "salidas"])))
            self.tablaResultados.setItem(fila, 15, QTableWidgetItem(str(datos.at[(cantFilas-1), "derivados"])))
            self.tablaResultados.setItem(fila, 16, QTableWidgetItem(str(datos.at[(cantFilas-1), "cola aire"])))
            self.tablaResultados.setItem(fila, 17, QTableWidgetItem(str(datos.at[(cantFilas-1), "cola tierra"])))
            self.tablaResultados.setItem(fila, 18, QTableWidgetItem(str(datos.at[(cantFilas-1), "aviones en tierra"])))
        """


    def cargarEstadisticas(self, estadisticos):
        self.txtTiempoPromPermEstacion.setText(str(distribuciones.truncate(estadisticos[0], 4)))
        self.txtTiempoPromOcupEmpleados.setText(str(distribuciones.truncate(estadisticos[1], 4)))
        self.cantVehicAtendidos.setText(str(estadisticos[2]))
        self.txtTiempoPromPermEnCola.setText(str(distribuciones.truncate(estadisticos[3], 4)))
