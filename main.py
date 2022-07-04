import sys

from PyQt5.QtWidgets import QApplication

import distribuciones
from Pantallas.LogicaPantallaIngreso import *
import clases
import bisect
import numpy as np
from rungeKutta import *
import random
import auxiliares

def simular(duracion, filaInicioMuestra, probAuto, probMoto, probCamioneta, probQuieraLimpieza, aLimpieza
            , bLimpieza, mediaLlegada, aCobro, bCobro):
    RKControlador = Controlador()
    RungeKutta = []

    nroFilas = 0
    ultimaFila = False
    cantTotalVehiculos = 0
    clk = 0
    cantVehicAtendidos = 0
    ACTiempoEspera = 0
    ACTiempoPermanencia = 0
    eventos = []

    #hayRNDServidor = False
    #hayRNDVehiculo = False
    #hayRNDLimpieza = False
    #hayRNDLlegada = False

    rndPrimerLlegada, tiempoPrimerLlegada = distribuciones.exponencialNegativa(mediaLlegada)

    primerLlegada = clases.Evento(tiempoPrimerLlegada,
                                  clases.Vehiculo("n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a",
                                                  "n/a", "n/a", "n/a")
                                  , "Llegada", "n/a")
    bisect.insort_right(eventos, primerLlegada)

    empleado1 = clases.Empleado("Libre", [], 0, "n/a", "n/a")
    empleado2 = clases.Empleado("Libre", [], 0, "n/a", "n/a")


    df = pd.DataFrame({
        "Reloj": [],
        "Evento": [],
        "VehicEvento": [],
        "RNDServ": [],
        "Servidor": [],
        "RNDVehic": [],
        "Vehiculo": [],
        "RNDQuiereLimpieza": [],
        "Quiere Limpieza": [],
        "RND Llegada": [],
        "Tiempo Hasta Prox. Llegada": [],
        "Prox. Llegada": [],
        "RND Tanque Inicial": [],
        "Tanque Inicial": [],
        "Tiempo Carga": [],
        "Fin Carga 1": [],
        "Fin Carga 2": [],
        "RND Tiempo Limpieza": [],
        "Tiempo Limpieza": [],
        "Fin Limpieza 1": [],
        "Fin Limpieza 2": [],
        "RND Tiempo Cobro": [],
        "Tiempo Cobro": [],
        "Fin Cobro 1": [],
        "Fin Cobro 2": [],
        "Estado Emp 1": [],
        "Ocupado 1 Por": [],
        "Cola Emp 1": [],
        "Tiempo Ocup Emp 1": [],
        "Estado Emp 2": [],
        "Ocupado 2 Por": [],
        "Cola Emp 2": [],
        "Tiempo Ocup Emp 2": [],
        "AC Tiempo Permanencia": [],
        "Cant Vehiculos Atendidos": [],
        "AC Tiempo Espera": [],
        "Llegadas": []
    })

    proximaLlegada = ""
    finCarga1 = ""
    finCarga2 = ""
    finLimpieza1 = ""
    finLimpieza2 = ""
    finCobro1 = ""
    finCobro2 = ""
    rndServidor = ""
    rndTipoVehic = ""
    rndQuiereLimpieza = ""
    rndLlegada = ""
    tiempoLlegada = ""
    rndTanqueInicial = ""
    tanqueInicial = ""
    tiempoCarga = ""
    rndLimpieza = ""
    rndCobro = ""
    tiempoCobro = ""

    while clk < duracion:
        tipoEvento = eventos[0].getTipo()
        clk = eventos[0].getTiempo()
        hayRNDServidor = False
        hayRNDVehiculo = False
        hayRNDQuiereLimpieza = False
        hayRNDLimpieza = False
        hayRNDLlegada = False
        hayRNDTanqueInicial = False
        hayRNDTiempoCobro = False
        #hayFinCarga1 = False
        #hayFinCarga2 = False

        dfRK = 0

        if clk > duracion:
            ultimaFila = True

        if tipoEvento == "Llegada":
            hayRNDLlegada = True

            if empleado1.estaLibre():
                hayRNDVehiculo = True
                hayRNDTanqueInicial = True
                rndTipoVehic, tipoVehic, cantLitrosTanque = auxiliares.definicionTipoVehiculo(probAuto, probMoto
                                                                                              , probCamioneta)
                rndTanqueInicial, tanqueInicial = auxiliares.calcularTanqueInicial(cantLitrosTanque)

                """
                vehiculo = clases.Vehiculo("siendoAtendido", tipoVehic, cantLitrosTanque, tanqueInicial, clk, "n/a", "n/a"
                                           , "n/a", "Empleado 1", clk, "")
                """
                vehiculo = eventos[0].getVehiculo()
                vehiculo.setEstado("siendoAtendido")
                vehiculo.setTipo(tipoVehic)
                vehiculo.setCantLitrosTanque(cantLitrosTanque)
                vehiculo.setTanqueInicial(tanqueInicial)
                vehiculo.setTiempoLlegada(clk)
                vehiculo.setServidorAtendido("Empleado 1")



                eventos[0].setEmpleado("Empleado 1")
                eventos[0].setVehiculo(vehiculo)


                if vehiculo.getTipo() == "Auto" or vehiculo.getTipo() == "Camioneta":

                    dfRK, tiempoCarga = RKControlador.calcularRKCarga(tanqueInicial, cantLitrosTanque)
                    RungeKutta.append(dfRK)

                    finCarga1 = tiempoCarga + clk

                    nuevoEvento = clases.Evento(finCarga1, vehiculo, "FinCarga1"
                                                , "Empleado 1")

                    rndQuiereLimpieza, quiereLimpieza = auxiliares.quiereLimpieza(probQuieraLimpieza)
                    hayRNDQuiereLimpieza = True

                    if quiereLimpieza:
                        rndLimpieza, tiempoLimpieza = distribuciones.uniforme(aLimpieza, bLimpieza)
                        tiempoLimpieza = tiempoLimpieza + (tiempoCarga + 0.5)
                        finLimpieza1 = tiempoLimpieza + clk
                        nuevoEvento2 = clases.Evento(finLimpieza1, vehiculo, "FinLimpieza1", "Empleado 1")

                        # meter Evento Limpieza en el vector de eventos
                        bisect.insort_right(eventos, nuevoEvento2)
                        vehiculo.setTiempoLimpieza(finLimpieza1)
                        vehiculo.setQuiereLimpieza("Si")
                        hayRNDLimpieza = True
                    else:
                        vehiculo.setQuiereLimpieza("No")

                    # meter Evento Carga en el vector de eventos
                    bisect.insort_right(eventos, nuevoEvento)
                    vehiculo.setTiempoCarga(finCarga1)
                    #hayFinCarga1 = True

                    empleado1.setTiempoInicioAtencion(clk)
                    empleado1.setEstado("Ocupado")
                    empleado1.setVehiculoActual(vehiculo)
                    #empleado1.quitarDeLaCola()

                elif vehiculo.getTipo() == "Moto":
                    dfRK, tiempoCarga = RKControlador.calcularRKCarga(tanqueInicial, cantLitrosTanque)
                    RungeKutta.append(dfRK)
                    finCarga1 = tiempoCarga + clk

                    nuevoEvento = clases.Evento(finCarga1, vehiculo, "FinCarga1"
                                                , "Empleado 1")

                    # meter Evento en el vector de eventos
                    bisect.insort_right(eventos, nuevoEvento)
                    vehiculo.setTiempoCarga(finCarga1)
                    vehiculo.setQuiereLimpieza("Moto")
                    #hayFinCarga1 = True

                    empleado1.setTiempoInicioAtencion(clk)
                    empleado1.setEstado("Ocupado")
                    empleado1.setVehiculoActual(vehiculo)
                    #empleado1.quitarDeLaCola()

            elif empleado2.estaLibre():
                hayRNDVehiculo = True
                hayRNDTanqueInicial = True
                rndTipoVehic, tipoVehic, cantLitrosTanque = auxiliares.definicionTipoVehiculo(probAuto, probMoto
                                                                                              , probCamioneta)

                rndTanqueInicial, tanqueInicial = auxiliares.calcularTanqueInicial(cantLitrosTanque)

                """
                vehiculo = clases.Vehiculo("siendoAtendido", tipoVehic, cantLitrosTanque, tanqueInicial, clk, "n/a", "n/a"
                                           , "n/a"
                                           , "Empleado 2", clk, "")
                """

                vehiculo = eventos[0].getVehiculo()
                vehiculo.setEstado("siendoAtendido")
                vehiculo.setTipo(tipoVehic)
                vehiculo.setCantLitrosTanque(cantLitrosTanque)
                vehiculo.setTanqueInicial(tanqueInicial)
                vehiculo.setTiempoLlegada(clk)
                vehiculo.setServidorAtendido("Empleado 2")

                eventos[0].setEmpleado("Empleado 2")
                eventos[0].setVehiculo(vehiculo)

                if vehiculo.getTipo() == "Auto" or vehiculo.getTipo() == "Camioneta":
                    dfRK, tiempoCarga = RKControlador.calcularRKCarga(tanqueInicial, cantLitrosTanque)
                    RungeKutta.append(dfRK)
                    finCarga2 = tiempoCarga + clk

                    nuevoEvento = clases.Evento(finCarga2, vehiculo, "FinCarga2"
                                                , "Empleado 2")

                    rndQuiereLimpieza, quiereLimpieza = auxiliares.quiereLimpieza(probQuieraLimpieza)
                    hayRNDQuiereLimpieza = True

                    if quiereLimpieza:
                        rndLimpieza, tiempoLimpieza = distribuciones.uniforme(aLimpieza, bLimpieza)
                        tiempoLimpieza = tiempoLimpieza + (tiempoCarga + 0.5)
                        finLimpieza2 = tiempoLimpieza + clk
                        nuevoEvento2 = clases.Evento(finLimpieza2, vehiculo, "FinLimpieza2", "Empleado 2")

                        # meter Evento Limpieza en el vector de eventos
                        bisect.insort_right(eventos, nuevoEvento2)
                        vehiculo.setTiempoLimpieza(finLimpieza2)
                        vehiculo.setQuiereLimpieza("Si")
                        hayRNDLimpieza = True
                    else:
                        vehiculo.setQuiereLimpieza("No")

                    # meter Evento Carga en el vector de eventos
                    bisect.insort_right(eventos, nuevoEvento)
                    vehiculo.setTiempoCarga(finCarga2)
                    #hayFinCarga2 = True


                    empleado2.setTiempoInicioAtencion(clk)
                    empleado2.setEstado("Ocupado")
                    empleado2.setVehiculoActual(vehiculo)
                    #empleado2.quitarDeLaCola()

                elif vehiculo.getTipo() == "Moto":
                    dfRK, tiempoCarga = RKControlador.calcularRKCarga(tanqueInicial, cantLitrosTanque)
                    RungeKutta.append(dfRK)
                    finCarga2 = tiempoCarga + clk

                    nuevoEvento = clases.Evento(finCarga2, vehiculo, "FinCarga2"
                                                , "Empleado 2")

                    # meter Evento en el vector de eventos
                    bisect.insort_right(eventos, nuevoEvento)
                    vehiculo.setTiempoCarga(finCarga2)
                    vehiculo.setQuiereLimpieza("Moto")
                    #hayFinCarga2 = True

                    empleado2.setTiempoInicioAtencion(clk)
                    empleado2.setEstado("Ocupado")
                    empleado2.setVehiculoActual(vehiculo)
                    #empleado2.quitarDeLaCola()

            else:
                hayRNDServidor = True
                hayRNDVehiculo = True
                rndServidor, servidor = auxiliares.eleccionServidor()
                if servidor == "Empleado 1":
                    rndTipoVehic, tipoVehic, cantLitrosTanque = auxiliares.definicionTipoVehiculo(probAuto, probMoto
                                                                                                  , probCamioneta)
                    """
                    vehiculo = clases.Vehiculo("esperandoAtencion", tipoVehic, cantLitrosTanque, "n/a", clk, "n/a", "n/a"
                                               , "n/a"
                                               , "Empleado 1", "n/a", "")
                    empleado1.agregarCola(vehiculo)
                    """
                    vehiculo = eventos[0].getVehiculo()
                    vehiculo.setEstado("esperandoAtencion")
                    vehiculo.setTipo(tipoVehic)
                    vehiculo.setCantLitrosTanque(cantLitrosTanque)
                    vehiculo.setTiempoLlegada(clk)
                    vehiculo.setServidorAtendido("Empleado 1")
                    empleado1.agregarCola(vehiculo)



                elif servidor == "Empleado 2":
                    rndTipoVehic, tipoVehic, cantLitrosTanque = auxiliares.definicionTipoVehiculo(probAuto, probMoto
                                                                                                  , probCamioneta)
                    """
                    vehiculo = clases.Vehiculo("esperandoAtencion", tipoVehic, cantLitrosTanque, "n/a", clk, "n/a", "n/a"
                                               , "n/a"
                                               , "Empleado 2", "n/a", "")
                    
                    """
                    vehiculo = eventos[0].getVehiculo()
                    vehiculo.setEstado("esperandoAtencion")
                    vehiculo.setTipo(tipoVehic)
                    vehiculo.setCantLitrosTanque(cantLitrosTanque)
                    vehiculo.setTiempoLlegada(clk)
                    vehiculo.setServidorAtendido("Empleado 2")
                    empleado2.agregarCola(vehiculo)

            rndLlegada, tiempoLlegada = distribuciones.exponencialNegativa(mediaLlegada)
            proximaLlegada = tiempoLlegada + clk
            nuevaLlegada = clases.Evento(proximaLlegada, clases.Vehiculo(), "Llegada", "n/a")
            bisect.insort_right(eventos, nuevaLlegada)
            cantTotalVehiculos += 1

        elif tipoEvento == "FinCarga1":
            vehiculo = empleado1.getVehiculoActual()
            if (vehiculo.quiereLimpieza()) == "Moto":
                empleado1.setEstado("Ocupado")
                rndCobro, tiempoCobro = distribuciones.uniforme(aCobro, bCobro)
                finCobro1 = tiempoCobro + clk
                vehiculo.setTiempoCobro(finCobro1)
                nuevoEvento = clases.Evento(finCobro1, vehiculo, "FinCobro1", "Empleado 1")
                bisect.insort_right(eventos, nuevoEvento)
                hayRNDTiempoCobro = True


            elif (vehiculo.quiereLimpieza()) != "Moto":
                empleado1.setEstado("Ocupado")
                if vehiculo.quiereLimpieza() == "Si":
                    if (vehiculo.getContadorPasoCobroOLimpieza()) == 1:
                        rndCobro, tiempoCobro = distribuciones.uniforme(aCobro, bCobro)
                        finCobro1 = tiempoCobro + clk
                        vehiculo.setTiempoCobro(finCobro1)
                        nuevoEvento = clases.Evento(finCobro1, vehiculo, "FinCobro1", "Empleado 1")
                        bisect.insort_right(eventos, nuevoEvento)
                        hayRNDTiempoCobro = True

                    elif (vehiculo.getContadorPasoCobroOLimpieza()) == 0:
                        vehiculo.setContadorPasoCobroOLimpieza(1)

                elif vehiculo.quiereLimpieza() == "No":
                    rndCobro, tiempoCobro = distribuciones.uniforme(aCobro, bCobro)
                    finCobro1 = tiempoCobro + clk
                    vehiculo.setTiempoCobro(finCobro1)
                    nuevoEvento = clases.Evento(finCobro1, vehiculo, "FinCobro1", "Empleado 1")
                    bisect.insort_right(eventos, nuevoEvento)
                    hayRNDTiempoCobro = True

            else:
                print("Hay un error con el tiempo limpieza")

        elif tipoEvento == "FinCarga2":
            vehiculo = empleado2.getVehiculoActual()
            if (vehiculo.quiereLimpieza()) == "Moto":
                empleado2.setEstado("Ocupado")
                rndCobro, tiempoCobro = distribuciones.uniforme(aCobro, bCobro)
                finCobro2 = tiempoCobro + clk
                vehiculo.setTiempoCobro(finCobro2)
                nuevoEvento = clases.Evento(finCobro2, vehiculo, "FinCobro2", "Empleado 2")
                bisect.insort_right(eventos, nuevoEvento)
                hayRNDTiempoCobro = True

            elif (vehiculo.quiereLimpieza()) != "Moto":
                empleado2.setEstado("Ocupado")
                if vehiculo.quiereLimpieza() == "Si":
                    if (vehiculo.getContadorPasoCobroOLimpieza()) == 1:
                        rndCobro, tiempoCobro = distribuciones.uniforme(aCobro, bCobro)
                        finCobro2 = tiempoCobro + clk
                        vehiculo.setTiempoCobro(finCobro2)
                        nuevoEvento = clases.Evento(finCobro2, vehiculo, "FinCobro2", "Empleado 2")
                        bisect.insort_right(eventos, nuevoEvento)
                        vehiculo.setContadorPasoCobroOLimpieza(2)
                        hayRNDTiempoCobro = True

                    elif (vehiculo.getContadorPasoCobroOLimpieza()) == 0:
                        vehiculo.setContadorPasoCobroOLimpieza(1)

                elif vehiculo.quiereLimpieza() == "No":
                    rndCobro, tiempoCobro = distribuciones.uniforme(aCobro, bCobro)
                    finCobro2 = tiempoCobro + clk
                    vehiculo.setTiempoCobro(finCobro2)
                    nuevoEvento = clases.Evento(finCobro2, vehiculo, "FinCobro2", "Empleado 2")
                    bisect.insort_right(eventos, nuevoEvento)
                    hayRNDTiempoCobro = True
            else:
                print("Hay un error con el tiempo limpieza")

        elif tipoEvento == "FinLimpieza1":
            empleado1.setEstado("Ocupado")
            vehiculo = empleado1.getVehiculoActual()
            if (vehiculo.getContadorPasoCobroOLimpieza()) == 1:
                rndCobro, tiempoCobro = distribuciones.uniforme(aCobro, bCobro)
                finCobro1 = tiempoCobro + clk
                vehiculo.setTiempoCobro(finCobro1)
                nuevoEvento = clases.Evento(finCobro1, vehiculo, "FinCobro1", "Empleado 1")
                bisect.insort_right(eventos, nuevoEvento)
                vehiculo.setContadorPasoCobroOLimpieza(2)
                hayRNDTiempoCobro = True

            elif (vehiculo.getContadorPasoCobroOLimpieza()) == 0:
                vehiculo.setContadorPasoCobroOLimpieza(1)
            else:
                print("Hay un error con el tiempo cobro")

        elif tipoEvento == "FinLimpieza2":
            empleado2.setEstado("Ocupado")
            vehiculo = empleado2.getVehiculoActual()
            if (vehiculo.getContadorPasoCobroOLimpieza()) == 1:
                rndCobro, tiempoCobro = distribuciones.uniforme(aCobro, bCobro)
                finCobro2 = tiempoCobro + clk
                vehiculo.setTiempoCobro(finCobro2)
                nuevoEvento = clases.Evento(finCobro2, vehiculo, "FinCobro2", "Empleado 2")
                bisect.insort_right(eventos, nuevoEvento)
                vehiculo.setContadorPasoCobroOLimpieza(2)
                hayRNDTiempoCobro = True

            elif (vehiculo.getContadorPasoCobroOLimpieza()) == 0:
                vehiculo.setContadorPasoCobroOLimpieza(1)
            else:
                print("Hay un error con el tiempo cobro")

        elif tipoEvento == "FinCobro1":

            tiempoOcupacionEmp1 = empleado1.getTiempoOcupacion()
            horaInicioAtencion = empleado1.getTiempoInicioAtencion()
            tiempoOcupacionEmp1 += (clk - horaInicioAtencion)
            empleado1.setTiempoOcupacion(tiempoOcupacionEmp1)
            cantVehicAtendidos += 1

            vehiculoViejo = empleado1.getVehiculoActual()
            tiempoPermanencia = vehiculoViejo.getTiempoLlegada()
            ACTiempoPermanencia += (clk - tiempoPermanencia)

            if len(empleado1.getCola()) != 0:
                empleado1.setEstado("Ocupado")
                # vehiculoViejo = empleado1.getVehiculoActual()
                vehiculoNuevo = empleado1.tomarProximoVehiculo()
                empleado1.setVehiculoActual(vehiculoNuevo)
                vehiculoNuevo.setTiempoInicioAtencion(clk)

                llegadaVehiculo = vehiculoNuevo.getTiempoLlegada()
                ACTiempoEspera += (clk - llegadaVehiculo)

                cantLitrosTanque = vehiculoNuevo.getCantLitrosTanque()
                rndTanqueInicial, tanqueInicial = auxiliares.calcularTanqueInicial(cantLitrosTanque)
                vehiculoNuevo.setTanqueInicial(tanqueInicial)
                hayRNDTanqueInicial = True

                if vehiculoNuevo.getTipo() == "Auto" or vehiculoNuevo.getTipo() == "Camioneta":
                    #print("Vehiculo: " + vehiculoNuevo.getNombre() + " Tanque Inicial: "
                    #      + str(vehiculoNuevo.getTanqueInicial()))
                    dfRK, tiempoCarga = RKControlador.calcularRKCarga(vehiculoNuevo.getTanqueInicial()
                                                                      , vehiculoNuevo.getCantLitrosTanque())
                    RungeKutta.append(dfRK)
                    finCarga1 = tiempoCarga + clk


                    nuevoEvento = clases.Evento(finCarga1, vehiculoNuevo, "FinCarga1"
                                                , "Empleado 1")

                    rndQuiereLimpieza, quiereLimpieza = auxiliares.quiereLimpieza(probQuieraLimpieza)
                    hayRNDQuiereLimpieza = True

                    if quiereLimpieza:
                        rndLimpieza, tiempoLimpieza = distribuciones.uniforme(aLimpieza, bLimpieza)
                        tiempoLimpieza = tiempoLimpieza + (tiempoCarga + 0.5)
                        finLimpieza1 = tiempoLimpieza + clk
                        nuevoEvento2 = clases.Evento(finLimpieza1, vehiculoNuevo, "FinLimpieza1", "Empleado 1")

                        # meter Evento Limpieza en el vector de eventos
                        bisect.insort_right(eventos, nuevoEvento2)
                        vehiculoNuevo.setTiempoLimpieza(finLimpieza1)
                        vehiculoNuevo.setQuiereLimpieza("Si")
                        hayRNDLimpieza = True
                    else:
                        vehiculoNuevo.setQuiereLimpieza("No")

                    # meter Evento Carga en el vector de eventos
                    bisect.insort_right(eventos, nuevoEvento)
                    vehiculoNuevo.setTiempoCarga(finCarga1)

                    empleado1.setTiempoInicioAtencion(clk)

                elif vehiculoNuevo.getTipo() == "Moto":
                    #print("Vehiculo: " + vehiculoNuevo.getNombre() + " Tanque Inicial: "
                     #     + str(vehiculoNuevo.getTanqueInicial()))
                    dfRK, tiempoCarga = RKControlador.calcularRKCarga(vehiculoNuevo.getTanqueInicial()
                                                                      , vehiculoNuevo.getCantLitrosTanque())
                    RungeKutta.append(dfRK)
                    finCarga1 = tiempoCarga + clk

                    nuevoEvento = clases.Evento(finCarga1, vehiculoNuevo, "FinCarga1"
                                                , "Empleado 1")

                    # meter Evento en el vector de eventos
                    bisect.insort_right(eventos, nuevoEvento)
                    vehiculoNuevo.setTiempoCarga(finCarga1)
                    vehiculoNuevo.setQuiereLimpieza("Moto")

                    empleado1.setTiempoInicioAtencion(clk)

            elif len(empleado1.getCola()) == 0:
                empleado1.setEstado("Libre")
                empleado1.setVehiculoActual("")


        elif tipoEvento == "FinCobro2":

            tiempoOcupacionEmp2 = empleado2.getTiempoOcupacion()
            horaInicioAtencion = empleado2.getTiempoInicioAtencion()
            tiempoOcupacionEmp2 += (clk - horaInicioAtencion)
            empleado2.setTiempoOcupacion(tiempoOcupacionEmp2)
            cantVehicAtendidos += 1

            vehiculoViejo = empleado2.getVehiculoActual()
            tiempoPermanencia = vehiculoViejo.getTiempoLlegada()
            ACTiempoPermanencia += (clk - tiempoPermanencia)

            if len(empleado2.getCola()) != 0:
                empleado2.setEstado("Ocupado")
                vehiculoNuevo = empleado2.tomarProximoVehiculo()
                empleado2.setVehiculoActual(vehiculoNuevo)
                vehiculoNuevo.setTiempoInicioAtencion(clk)

                llegadaVehiculo = vehiculoNuevo.getTiempoLlegada()
                ACTiempoEspera += (clk - llegadaVehiculo)

                cantLitrosTanque = vehiculoNuevo.getCantLitrosTanque()
                rndTanqueInicial, tanqueInicial = auxiliares.calcularTanqueInicial(cantLitrosTanque)
                vehiculoNuevo.setTanqueInicial(tanqueInicial)
                hayRNDTanqueInicial = True

                if vehiculoNuevo.getTipo() == "Auto" or vehiculoNuevo.getTipo() == "Camioneta":
                    #print("Vehiculo: " + vehiculoNuevo.getNombre() + " Tanque Inicial: "
                     #     + str(vehiculoNuevo.getTanqueInicial()))
                    dfRK, tiempoCarga = RKControlador.calcularRKCarga(vehiculoNuevo.getTanqueInicial()
                                                                      , vehiculoNuevo.getCantLitrosTanque())
                    RungeKutta.append(dfRK)
                    finCarga2 = tiempoCarga + clk

                    nuevoEvento = clases.Evento(finCarga2, vehiculoNuevo, "FinCarga2"
                                                , "Empleado 2")

                    rndQuiereLimpieza, quiereLimpieza = auxiliares.quiereLimpieza(probQuieraLimpieza)
                    hayRNDQuiereLimpieza = True

                    if quiereLimpieza:
                        rndLimpieza, tiempoLimpieza = distribuciones.uniforme(aLimpieza, bLimpieza)
                        tiempoLimpieza = tiempoLimpieza + (tiempoCarga + 0.5)
                        finLimpieza2 = tiempoLimpieza + clk
                        nuevoEvento2 = clases.Evento(finLimpieza2, vehiculoNuevo, "FinLimpieza2", "Empleado 2")

                        # meter Evento Limpieza en el vector de eventos
                        bisect.insort_right(eventos, nuevoEvento2)
                        vehiculoNuevo.setTiempoLimpieza(finLimpieza2)
                        vehiculoNuevo.setQuiereLimpieza("Si")
                        hayRNDLimpieza = True
                    else:
                        vehiculoNuevo.setQuiereLimpieza("No")

                    # meter Evento Carga en el vector de eventos
                    bisect.insort_right(eventos, nuevoEvento)
                    vehiculoNuevo.setTiempoCarga(finCarga2)

                    empleado2.setTiempoInicioAtencion(clk)

                elif vehiculoNuevo.getTipo() == "Moto":
                    #"Vehiculo: " + vehiculoNuevo.getNombre() + " Tanque Inicial: "
                      #    + str(vehiculoNuevo.getTanqueInicial()))
                    dfRK, tiempoCarga = RKControlador.calcularRKCarga(vehiculoNuevo.getTanqueInicial()
                                                                      , vehiculoNuevo.getCantLitrosTanque())
                    RungeKutta.append(dfRK)
                    finCarga2 = tiempoCarga + clk

                    nuevoEvento = clases.Evento(finCarga2, vehiculoNuevo, "FinCarga2"
                                                , "Empleado 2")

                    # meter Evento en el vector de eventos
                    bisect.insort_right(eventos, nuevoEvento)
                    vehiculoNuevo.setTiempoCarga(finCarga2)
                    vehiculoNuevo.setQuiereLimpieza("Moto")

                    empleado2.setTiempoInicioAtencion(clk)

            elif len(empleado2.getCola()) == 0:
                empleado2.setEstado("Libre")
                empleado2.setVehiculoActual("")

        else:
            print("Error en nombre tipoEvento!")

        nroFilas += 1

        if (filaInicioMuestra < nroFilas and nroFilas < 401 + filaInicioMuestra) or ultimaFila:  # True:

            fila = pd.DataFrame({
                "Reloj": [],
                "Evento": [],
                "VehicEvento": [],
                "RNDServ": [],
                "Servidor": [],
                "RNDVehic": [],
                "Vehiculo": [],
                "RNDQuiereLimpieza": [],
                "Quiere Limpieza": [],
                "RND Llegada": [],
                "Tiempo Hasta Prox. Llegada": [],
                "Prox. Llegada": [],
                "RND Tanque Inicial": [],
                "Tanque Inicial": [],
                "Tiempo Carga": [],
                "Fin Carga 1": [],
                "Fin Carga 2": [],
                "RND Tiempo Limpieza": [],
                "Tiempo Limpieza": [],
                "Fin Limpieza 1": [],
                "Fin Limpieza 2": [],
                "RND Tiempo Cobro": [],
                "Tiempo Cobro": [],
                "Fin Cobro 1": [],
                "Fin Cobro 2": [],
                "Estado Emp 1": [],
                "Ocupado 1 Por": [],
                "Cola Emp 1": [],
                "Tiempo Ocup Emp 1": [],
                "Estado Emp 2": [],
                "Ocupado 2 Por": [],
                "Cola Emp 2": [],
                "Tiempo Ocup Emp 2": [],
                "AC Tiempo Permanencia": [],
                "Cant Vehiculos Atendidos": [],
                "AC Tiempo Espera": [],
                "Llegadas": []
                })

            if tipoEvento == "FinCarga1":
                finCarga1 = ""
            elif tipoEvento == "FinCarga2":
                finCarga2 = ""
            elif tipoEvento == "FinLimpieza1":
                finLimpieza1 = ""
            elif tipoEvento == "FinLimpieza2":
                finLimpieza2 = ""
            elif tipoEvento == "FinCobro1":
                finCobro1 = ""
            elif tipoEvento == "FinCobro2":
                finCobro2 = ""

            stringRNDServidor = ""
            stringServidor = ""
            stringRNDVehiculo = ""
            stringRNDQuiereLimpieza = ""
            stringQuiereLimpieza = ""
            stringRNDLlegada = ""
            stringTiempoLlegada = ""
            stringProxLlegada = proximaLlegada
            stringRNDTanqueInicial = ""
            stringTanqueInicial = ""
            stringTiempoCarga = ""
            stringHayFinCarga1 = finCarga1
            stringHayFinCarga2 = finCarga2
            stringHayRNDLimpieza = ""
            stringTiempoLimpieza = ""
            stringFinLimpieza1 = finLimpieza1
            stringFinLimpieza2 = finLimpieza2
            stringRNDTiempoCobro = ""
            stringTiempoCobro = ""
            stringFinCobro1 = finCobro1
            stringFinCobro2 = finCobro2
            stringOcupado1Por = ""
            stringOcupado2Por = ""

            if tipoEvento == "Llegada":
                if hayRNDServidor:
                    stringRNDServidor = rndServidor
                    stringServidor = (eventos[0].getVehiculo()).getServidorAtendido()

                if hayRNDVehiculo:
                    stringRNDVehiculo = rndTipoVehic

                if hayRNDQuiereLimpieza:
                    stringRNDQuiereLimpieza = rndQuiereLimpieza
                    stringQuiereLimpieza = (eventos[0].getVehiculo()).quiereLimpieza()

                if hayRNDLlegada:
                    stringRNDLlegada = rndLlegada
                    stringTiempoLlegada = tiempoLlegada

                if hayRNDTanqueInicial:
                    stringRNDTanqueInicial = rndTanqueInicial
                    stringTanqueInicial = tanqueInicial
                    stringTiempoCarga = tiempoCarga

                if hayRNDLimpieza:
                    stringHayRNDLimpieza = rndLimpieza
                    stringTiempoLimpieza = tiempoLimpieza

            elif tipoEvento == "FinCarga1":
                if hayRNDTiempoCobro:
                    stringRNDTiempoCobro = rndCobro
                    stringTiempoCobro = tiempoCobro

            elif tipoEvento == "FinCarga2":
                if hayRNDTiempoCobro:
                    stringRNDTiempoCobro = rndCobro
                    stringTiempoCobro = tiempoCobro

            elif tipoEvento == "FinLimpieza1":
                if hayRNDTiempoCobro:
                    stringRNDTiempoCobro = rndCobro
                    stringTiempoCobro = tiempoCobro

            elif tipoEvento == "FinLimpieza2":
                if hayRNDTiempoCobro:
                    stringRNDTiempoCobro = rndCobro
                    stringTiempoCobro = tiempoCobro

            elif tipoEvento == "FinCobro1":
                if hayRNDQuiereLimpieza:
                    stringRNDQuiereLimpieza = rndQuiereLimpieza
                    stringQuiereLimpieza = vehiculoNuevo.quiereLimpieza()

                if hayRNDTanqueInicial:
                    stringRNDTanqueInicial = rndTanqueInicial
                    stringTanqueInicial = tanqueInicial
                    stringTiempoCarga = tiempoCarga

                if hayRNDLimpieza:
                    stringHayRNDLimpieza = rndLimpieza
                    stringTiempoLimpieza = tiempoLimpieza

            elif tipoEvento == "FinCobro2":
                if hayRNDQuiereLimpieza:
                    stringRNDQuiereLimpieza = rndQuiereLimpieza
                    stringQuiereLimpieza = vehiculoNuevo.quiereLimpieza()

                if hayRNDTanqueInicial:
                    stringRNDTanqueInicial = rndTanqueInicial
                    stringTanqueInicial = tanqueInicial
                    stringTiempoCarga = tiempoCarga

                if hayRNDLimpieza:
                    stringHayRNDLimpieza = rndLimpieza
                    stringTiempoLimpieza = tiempoLimpieza


            if stringQuiereLimpieza == "Moto":
                stringQuiereLimpieza = ""
            if (empleado1.getVehiculoActual()) != "" and (empleado1.getVehiculoActual()) != "n/a":
                stringOcupado1Por = (empleado1.getVehiculoActual()).getNombre()
            if (empleado2.getVehiculoActual()) != "" and (empleado2.getVehiculoActual()) != "n/a":
                stringOcupado2Por = (empleado2.getVehiculoActual()).getNombre()


            fila.at[0, "Reloj"] = clk
            fila.at[0, "Evento"] = tipoEvento
            fila.at[0, "VehicEvento"] = (eventos[0].getVehiculo()).getNombre()
            fila.at[0, "RNDServ"] = stringRNDServidor
            fila.at[0, "Servidor"] = stringServidor
            fila.at[0, "RNDVehic"] = stringRNDVehiculo
            fila.at[0, "Vehiculo"] = (eventos[0].getVehiculo()).getTipo()
            fila.at[0, "RNDQuiereLimpieza"] = stringRNDQuiereLimpieza
            fila.at[0, "Quiere Limpieza"] = stringQuiereLimpieza
            fila.at[0, "RND Llegada"] = stringRNDLlegada
            fila.at[0, "Tiempo Hasta Prox. Llegada"] = stringTiempoLlegada
            fila.at[0, "Prox. Llegada"] = stringProxLlegada
            fila.at[0, "RND Tanque Inicial"] = stringRNDTanqueInicial
            fila.at[0, "Tanque Inicial"] = stringTanqueInicial
            fila.at[0, "Tiempo Carga"] = stringTiempoCarga
            fila.at[0, "Fin Carga 1"] = stringHayFinCarga1
            fila.at[0, "Fin Carga 2"] = stringHayFinCarga2
            fila.at[0, "RND Tiempo Limpieza"] = stringHayRNDLimpieza
            fila.at[0, "Tiempo Limpieza"] = stringTiempoLimpieza
            fila.at[0, "Fin Limpieza 1"] = stringFinLimpieza1
            fila.at[0, "Fin Limpieza 2"] = stringFinLimpieza2
            fila.at[0, "RND Tiempo Cobro"] = stringRNDTiempoCobro
            fila.at[0, "Tiempo Cobro"] = stringTiempoCobro
            fila.at[0, "Fin Cobro 1"] = stringFinCobro1
            fila.at[0, "Fin Cobro 2"] = stringFinCobro2
            fila.at[0, "Estado Emp 1"] = empleado1.getEstado()
            fila.at[0, "Ocupado 1 Por"] = stringOcupado1Por
            fila.at[0, "Cola Emp 1"] = empleado1.getStringCola()
            fila.at[0, "Tiempo Ocup Emp 1"] = empleado1.getTiempoOcupacion()
            fila.at[0, "Estado Emp 2"] = empleado2.getEstado()
            fila.at[0, "Ocupado 2 Por"] = stringOcupado2Por
            fila.at[0, "Cola Emp 2"] = empleado2.getStringCola()
            fila.at[0, "Tiempo Ocup Emp 2"] = empleado2.getTiempoOcupacion()
            fila.at[0, "AC Tiempo Permanencia"] = ACTiempoPermanencia
            fila.at[0, "Cant Vehiculos Atendidos"] = cantVehicAtendidos
            fila.at[0, "AC Tiempo Espera"] = ACTiempoEspera
            fila.at[0, "Llegadas"] = cantTotalVehiculos

            df = pd.concat([df, fila], ignore_index=True)

        """
        vuelta += 1
        print(vuelta)
        for evento in eventos:
            print("Vuelta: " + str(vuelta) + " " + evento.toString())
        print(" ----------------------------- ")
        """

        print(clk)
        eventos.remove(eventos[0])


    return df, RungeKutta, ACTiempoPermanencia, cantVehicAtendidos, empleado1, empleado2, ACTiempoEspera, cantTotalVehiculos


def calculoEstadisticos(ACTiempoPermanencia, cantVehicAtendidos, empleado1, empleado2, ACTiempoEspera,
                        cantTotalVehiculos):

    estadisticos = np.zeros(4)

    # Tiempo Promedio Permanencia en la Estacion
    estadisticos[0] = ACTiempoPermanencia / cantVehicAtendidos

    # Tiempo Promedio Ocupacion de los Empleados
    ocupacionTotalEmp1 = empleado1.getTiempoOcupacion()
    ocupacionTotalEmp2 = empleado2.getTiempoOcupacion()
    estadisticos[1] = (ocupacionTotalEmp1 + ocupacionTotalEmp2) / 2

    # Cantidad de Vehículos Atendidos
    estadisticos[2] = cantVehicAtendidos

    # Tiempo Promedio de Permanencia en Cola
    estadisticos[3] = ACTiempoEspera / cantTotalVehiculos

    return estadisticos

def principal(pantallaIngreso, duracion, filaInicioMuestra, probAuto, probMoto, probCamioneta, probQuieraLimpieza, aLimpieza
            , bLimpieza, mediaLlegada, aCobro, bCobro):

    df, RungeKutta, ACTiempoPermanencia, cantVehicAtendidos, empleado1, empleado2, ACTiempoEspera, cantTotalVehiculos = \
        simular(duracion, filaInicioMuestra, probAuto, probMoto, probCamioneta, probQuieraLimpieza, aLimpieza
            , bLimpieza, mediaLlegada, aCobro, bCobro)

    estadisticos = \
        calculoEstadisticos(ACTiempoPermanencia, cantVehicAtendidos, empleado1, empleado2, ACTiempoEspera, cantTotalVehiculos)

    pantallaIngreso.mostrarResultados(df, estadisticos, RungeKutta, filaInicioMuestra)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = PantallaIngreso()
    GUI.show()
    sys.exit(app.exec_())
