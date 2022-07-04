import random
import string

class Vehiculo():
    def __init__(self, estado="n/a", tipo="n/a", cantLitrosTanque="n/a", tanqueInicial="n/a", tiempoLlegada="n/a"
                 , tiempoCarga="n/a", tiempoLimpieza="n/a"
                 , tiempoCobro="n/a", servidorAtendido="n/a", horaInicioAtencion="n/a", quiereLimpieza="n/a"):
        self.__nombre = random.choice(string.ascii_letters) + str(random.randint(1, 100)) \
                        + random.choice(string.ascii_letters)
        self.__estado = estado
        self.__tipo = tipo
        self.__cantLitrosTanque = cantLitrosTanque
        self.__tanqueInicial = tanqueInicial
        self.__tiempoLlegada = tiempoLlegada
        self.__tiempoCarga = tiempoCarga
        self.__tiempoLimpieza = tiempoLimpieza
        self.__tiempoCobro = tiempoCobro
        self.__servidorAtendido = servidorAtendido
        self.__horaInicioAtencion = horaInicioAtencion
        self.__quiereLimpieza = quiereLimpieza
        self.__contadorPasoCobroOLimpieza = 0

    def setNombre(self, nombre):
        self.__nombre = nombre

    def getNombre(self):
        return self.__nombre

    def setTipo(self, tipo):
        self.__tipo = tipo

    def getTipo(self):
        return self.__tipo

    def getTiempoCarga(self):
        return self.__tiempoCarga

    def setTiempoCarga(self, tiempoCarga):
        self.__tiempoCarga = tiempoCarga

    def getTiempoLimpieza(self):
        return self.__tiempoLimpieza

    def setTiempoLimpieza(self, tiempoLimpieza):
        self.__tiempoLimpieza = tiempoLimpieza

    def getTiempoCobro(self):
        return self.__tiempoCobro

    def setTiempoCobro(self, tiempoCobro):
        self.__tiempoCobro = tiempoCobro

    def quiereLimpieza(self):
        return self.__quiereLimpieza

    def setQuiereLimpieza(self, quiereLimpieza):
        self.__quiereLimpieza = quiereLimpieza

    def getContadorPasoCobroOLimpieza(self):
        return self.__contadorPasoCobroOLimpieza

    def setContadorPasoCobroOLimpieza(self, contador):
        self.__contadorPasoCobroOLimpieza = contador

    def getTanqueInicial(self):
        return self.__tanqueInicial

    def setTanqueInicial(self, tanqueInicial):
        self.__tanqueInicial = tanqueInicial

    def getCantLitrosTanque(self):
        return self.__cantLitrosTanque

    def setCantLitrosTanque(self, cantLitrosTanque):
        self.__cantLitrosTanque = cantLitrosTanque

    def getServidorAtendido(self):
        return self.__servidorAtendido

    def setServidorAtendido(self, servidorAtendido):
        self.__servidorAtendido = servidorAtendido

    def getTiempoLlegada(self):
        return self.__tiempoLlegada

    def setTiempoLlegada(self, tiempoLlegada):
        self.__tiempoLlegada = tiempoLlegada

    def getEstado(self):
        return self.__estado

    def setEstado(self, estado):
        self.__estado = estado

    def setTiempoInicioAtencion(self, tiempoInicioAtencion):
        self.__horaInicioAtencion = tiempoInicioAtencion


class Empleado():
    def __init__(self, estado, cola, tiempoOcupacion, tiempoInicioAtencion, vehiculoActual):
        self.__estado = estado
        self.__cola = cola
        self.__tiempoOcupacion = tiempoOcupacion
        self.__tiempoInicioAtencion = tiempoInicioAtencion
        self.__vehiculoActual = vehiculoActual

    def estaLibre(self):
        if self.__estado == "Libre":
            return True
        elif self.__estado == "Ocupado":
            return False

    def agregarCola(self, vehiculo):
        self.__cola.append(vehiculo)

    def getEstado(self):
        return self.__estado

    def setEstado(self, estado):
        self.__estado = estado

    def getCola(self):
        '''
        for i in range(len(self.__cola)):
        cola += self.__cola[i]
        return cola
        '''
        return self.__cola

    def quitarDeLaCola(self):
        self.__cola.remove(self.__cola[0])

    def getTiempoInicioAtencion(self):
        return self.__tiempoInicioAtencion

    def setTiempoInicioAtencion(self, tiempoInicioAt):
        self.__tiempoInicioAtencion = tiempoInicioAt

    def getTiempoOcupacion(self):
        return self.__tiempoOcupacion

    def setTiempoOcupacion(self, tiempoOcupacion):
        self.__tiempoOcupacion = tiempoOcupacion

    def tomarProximoVehiculo(self):
        proxVehiculo = self.__cola[0]
        self.quitarDeLaCola()
        return proxVehiculo

    def getVehiculoActual(self):
        return self.__vehiculoActual

    def setVehiculoActual(self, nuevoVehic):
        self.__vehiculoActual = nuevoVehic

    def getStringCola(self):
        longitudCola = len(self.__cola)
        stringCola = ""
        for vehic in self.__cola:
            stringCola += vehic.getNombre() + ", "
        stringCola = str(longitudCola) + " (" + stringCola + ") "
        return stringCola




class Evento():
    def __init__(self, tiempo, vehiculo, tipo, empleado):
        self.__tiempo = tiempo
        self.__vehiculo = vehiculo
        self.__tipo = tipo
        self.__empleado = empleado

    def __lt__(self, other):
        return self.__tiempo < other.getTiempo()
    def __gt__(self, other):
        return self.__tiempo > other.getTiempo()

    def getTiempo(self):
        return self.__tiempo

    def setTiempo(self, tiempo):
        self.__tiempo = tiempo

    def getTipo(self):
        return self.__tipo

    def setTipo(self, tipo):
        self.__tipo = tipo

    def getVehiculo(self):
        return self.__vehiculo

    def setEmpleado(self, empleado):
        self.__empleado = empleado

    def setVehiculo(self, vehiculo):
        self.__vehiculo = vehiculo

    def toString(self):
        string = ""
        string += "Tiempo:" + str(self.__tiempo) + " "
        string += "Vehiculo:" + str(self.__vehiculo.getNombre()) + " "
        string += "Tipo:" + str(self.__tipo) + " "
        string += "Empleado:" + str(self.__empleado) + " "
        return string