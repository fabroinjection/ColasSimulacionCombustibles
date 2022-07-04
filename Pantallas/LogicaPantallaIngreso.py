from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from Pantallas import LogicaPantallaResultados
from main import *



class PantallaIngreso(QMainWindow):
    """Incializar clase"""

    def __init__(self):
        super().__init__()

        """Cargar la GUI"""
        uic.loadUi("Pantallas/pantallaIngreso.ui", self)

        self.btnSimular.clicked.connect(self.metodoAuxiliar)

    def metodoAuxiliar(self):

        if self.validarCamposNoVacios():
            if self.validarDatosCorrectos():
                if self.duracion.text() != "":
                    principal(self,
                              (float(self.duracion.text())),
                              (int(self.txtInicioFilas.text())),
                              (float(self.txtProbAutos.text()) / 100),
                              (float(self.txtProbMotos.text()) / 100),
                              (float(self.txtProbCamionetas.text()) / 100),
                              (float(self.txtProbQuiereLimpieza.text()) / 100),
                              (float(self.aLimpieza.text())),
                              (float(self.bLimpieza.text())),
                              (float(self.mediaExpoLlegadas.text())),
                              (float(self.aCobros.text())),
                              (float(self.bCobros.text())),
                              )


    def mostrarResultados(self, datos, estadisticos, RungeKutta, inicio):
        self.pantallaResultados = LogicaPantallaResultados.PantallaResultados()
        self.pantallaResultados.mostrarResultados(datos, estadisticos, RungeKutta, inicio)
        self.pantallaResultados.show()


    def validarCamposNoVacios(self):

        vectorStrings = [(float(self.duracion.text())),
                      (float(self.txtInicioFilas.text())),
                      (float(self.txtProbAutos.text()) / 100),
                      (float(self.txtProbMotos.text()) / 100),
                      (float(self.txtProbCamionetas.text()) / 100),
                      (float(self.txtProbQuiereLimpieza.text()) / 100),
                      (float(self.aLimpieza.text())),
                      (float(self.bLimpieza.text())),
                      (float(self.mediaExpoLlegadas.text())),
                      (float(self.aCobros.text())),
                      (float(self.bCobros.text()))]

        for string in vectorStrings:
            if string == '' or string == " ":
                QMessageBox.warning(self, "Alerta", "Debe ingresar valores en todos los campos.")
                return False
        return True

    def esEnteroPositivo(self):
        """la funcion nos dice si un numero es natural o 0 y en ese caso devuelve True"""

        if str(self.txtInicioFilas.text()).isnumeric():
            return True
        else:
            return False


    def validarDatosCorrectos(self):
        tiempoSimulacion = float(self.duracion.text())
        primeraFila = float(self.txtInicioFilas.text())

        if primeraFila > tiempoSimulacion:
            QMessageBox.warning(self, "Alerta", "La Primera Fila a mostrar no puede ser mayor al Tiempo de Simulación"
                                                " ya que no habrá información a mostrar.")
            return False

        vectorFlotante = [(float(self.duracion.text())),
                      (float(self.txtInicioFilas.text())),
                      (float(self.txtProbAutos.text()) / 100),
                      (float(self.txtProbMotos.text()) / 100),
                      (float(self.txtProbCamionetas.text()) / 100),
                      (float(self.txtProbQuiereLimpieza.text()) / 100),
                      (float(self.aLimpieza.text())),
                      (float(self.bLimpieza.text())),
                      (float(self.mediaExpoLlegadas.text())),
                      (float(self.aCobros.text())),
                      (float(self.bCobros.text()))]

        for numero in vectorFlotante:
            if numero < 0:
                QMessageBox.warning(self, "Alerta", "Los números no deben ser negativos ya que representan tiempos"
                                                    "o procentajes.")
                return False

        if float(self.aLimpieza.text()) > float(self.bLimpieza.text()):
            QMessageBox.warning(self, "Alerta",
                                "En la Distribución Uniforme de Limpieza el valor de A debe ser menor al valor de B.")
            return False

        if float(self.aCobros.text()) > float(self.bCobros.text()):
            QMessageBox.warning(self, "Alerta",
                                "En la Distribución Uniforme de Cobro el valor de A debe ser menor al valor de B.")
            return False

        if float(self.txtProbQuiereLimpieza.text()) > 100:
            QMessageBox.warning(self, "Alerta", "EL valor del porcentaje de Limpieza no debe superar el 100%.")
            return False

        if (float(self.txtProbAutos.text()) + (float(self.txtProbMotos.text()))
            + float(self.txtProbCamionetas.text())) > 100:
            QMessageBox.warning(self, "Alerta", "El valor del porcentaje de llegada todos los vehículos"
                                                "no debe superar el 100%.")
            return False

        if (float(self.txtProbAutos.text()) + (float(self.txtProbMotos.text()))
            + float(self.txtProbCamionetas.text())) < 100:
            QMessageBox.warning(self, "Alerta", "El valor del porcentaje de llegada todos los vehículos"
                                                "no debe superar el 100%.")
            return False

        if self.esEnteroPositivo():
            return True
        else:
            QMessageBox.warning(self, "Alerta", "EL valor de la fila de inicio debe ser entero.")
            return False

        return True



