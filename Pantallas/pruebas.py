'''
DF PARA LAS ENTRADAS CON LIMPIEZA
                        df.at[0, "Reloj"] = clk
                        df.at[0, "Evento"] = eventos[0].getTipo()
                        df.at[0, "RNDServ"] = "n/a"
                        df.at[0, "Servidor"] = "Empleado 1"
                        df.at[0, "RNDVehic"] = rndTipoVehic
                        df.at[0, "Vehiculo"] = tipoVehic
                        df.at[0, "RNDQuiereLimpieza"] = rndQuiereLimpieza
                        if quiereLimpieza:
                            df.at[0, "Quiere Limpieza"] = "Si"
                        else:
                            df.at[0, "Quiere Limpieza"] = "No"
                        df.at[0, "RND Llegada"] = rndLlegada
                        df.at[0, "Tiempo Hasta La Prox. Llegada"] = tiempoLlegada
                        df.at[0, "Prox. Llegada"] = proximaLlegada
                        df.at[0, "RND Tanque Inicial"] = rndTanqueInicial
                        df.at[0, "Tanque Inicial"] = tanqueInicial
                        df.at[0, "Tiempo Carga"] = tiempoCarga
                        df.at[0, "Fin Carga 1"] = finCarga1
                        df.at[0, "Fin Carga 2"] = "n/a"
                        df.at[0, "RND Tiempo Cobro"] = "n/a"
                        df.at[0, "Tiempo Cobro"] = "n/a"
                        df.at[0, "Fin Cobro 1"] = "n/a"
                        df.at[0, "Fin Cobro 2"] = "n/a"
                        df.at[0, "Estado Emp 1"] = empleado1.getEstado()
                        df.at[0, "Ocupado 1 Por"] = vehiculo.getNombre() + " - " + vehiculo.getTipo()
                        df.at[0, "Cola Emp 1"] = empleado1.getCola()
                        # CAMBIAR
                        df.at[0, "Tiempo Ocup Emp 1"] = 0
                        df.at[0, "Estado Emp 2"] = empleado2.getEstado()
                        df.at[0, "Ocupado 2 Por"] = empleado2.getVehiculo().getNombre() + " - " \
                                                    + empleado2.getVehiculo().getTipo()
                        df.at[0, "Cola Emp 2"] = empleado2.getCola()
                        # CAMBIAR
                        df.at[0, "Tiempo Ocup Emp 2"] = 0
                        '''
