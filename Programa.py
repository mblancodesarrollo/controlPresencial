'''
Created on 14 dic. 2020

@author: ottod
'''
import regex as re
import cv2
import csv
from io import open
import pandas as pd
from datetime import datetime, time
from os import path
if __name__ == '__main__':
    
    def leer_log():
        if path.exists("log.txt"):
            archivo = open("log.txt", "r")
        else:
            return []
        archivo = open("log.txt","r")
        lineas = archivo.readlines()
        archivo.close()
        return lineas
    
    def lastLogLine():
        if path.exists("log.txt"):
            archivo = open("log.txt", "r")
        else:
            return False
        lineas = archivo.readlines()
        archivo.close()
        if lineas:
            return lineas[-1]
        return False


    def validaLocacion(locacion):
        campus_re = r'^\d{2}'
        edificio_re = r'ED(\d{3})'
        try:
            campus = re.search(campus_re, locacion).group(0)
        except:
            campus = '0'
        try:
            edificio = re.search(edificio_re, locacion).group(1)
        except:
            return False
        if campus and edificio:       
            for index, campusItem, edificioItem in zip(range(len(dicList['campus'])),dicList['campus'],dicList['edificio']):
                if campus != '0':
                    if campus == campusItem and edificio == edificioItem:
                        return True
                else:
                    if edificio == edificioItem:
                        return True
                    
        return False

    def comprobarRutaQR(ruta):
        #Cualquier cosa que este antes de un punto y termine en png mayusculas o minusculas
        patron_rutaQR = r'^.+\.[Pp][Nn][Gg]$'
        er_rutaQR = re.compile(patron_rutaQR)
        patron_codigoPatrimonial = r'^(\d{2} *[\.\_] *)?ED\_?\d{3} *[\.\_] *B\d{1} *[\.\_] *\-?(\d{1,2}|(EN)|(CU)) *[\.\_] *\d{3} *[\.]? *[A-Za-z0-9]?$'
        er_codigoPatrimonial = re.compile(patron_codigoPatrimonial)
        resul = er_rutaQR.fullmatch(ruta)
        if resul:
            imagen = cv2.imread(ruta)
            if imagen is None:
                print('La imagen no existe.')   
                return False 
            else:
                detectorQR = cv2.QRCodeDetector()
                texto, puntos, _ = detectorQR.detectAndDecode(imagen)
                resul_codigo = er_codigoPatrimonial.fullmatch(texto)
            if resul_codigo:
                cod = resul_codigo.group(0)
                if validaLocacion(cod):
                    return cod
                return False
            else:
                campus = encuentraCampus(locacion)
                if campus:
                    resul_codigo = er_codigoPatrimonial.fullmatch(campus+texto)
                    if resul_codigo:
                        return True
                    return False
        else:
            print('Ruta QR no válida.')
            return False 
        return False

    def encuentraCampus(locacion):
        edificio_re = r'ED(\d{3})'
        edificio = re.search(edificio_re, locacion).group(1)
        if edificio:
            for index, edificioItem in zip(range(len(dicList['edificio'])),dicList['edificio']):
                if edificio == edificioItem:
                    return dicList['campus'][index]
        return False
    
    
    def add_registro():
        patron_fecha = r'(3[01]|[12][0-9]|0[1-9])[\-\/](0[1-9]|1[0-2])[\-\/](20[0-9]{2})'
        patron_hora = r'^([01]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$'
        patron_telefono = r'^(\d{3})\s?(\d{3})\s?(\d{3})$'
        patron_rutaQR = r'^.+\.[Pp][Nn][Gg]$'
        patron_codigoPatrimonial =  r'^((\d{2})[\.\_])?ED\_?(\d{3})[\.\_]B(\d{1})[\.\_]\-?((\d{1,2}|(EN)|(CU)))[\.\_](\d{3})[\.]?([A-Za-z0-9]?)$'
        patron_accion = r'[iI][nN]|[oO][uU][tT]'
        er_fecha = re.compile(patron_fecha)
        er_hora = re.compile(patron_hora)
        er_telefono = re.compile(patron_telefono)
        er_rutaQR = re.compile(patron_rutaQR)
        er_codigoPatrimonial = re.compile(patron_codigoPatrimonial)
        er_accion = re.compile(patron_accion)
        fechaRegistro = 1
        horaRegistro = 1
        rutaQR = 1
        telefonoRegistro = 1
        accion = 1
        while fechaRegistro != '':
            fechaRegistro = input("Fecha: ")
            resFecha = er_fecha.fullmatch(fechaRegistro.rstrip())
            if resFecha:
                fecha = resFecha.group(0)
                if fecha.find('/') == -1:
                    fechaInput = re.split(r'\-',fecha) 
                else:
                    fechaInput = re.split(r'\/',fecha) 
                ultimaLinea = lastLogLine()
                if ultimaLinea:
                    fechaLog_re = r'Day *(\d{4})[ -]+(\d{2})[ -]+(\d{2})[ ,]+(\d{2})[ :]+(\d{2})[ :]+(\d{2}) *]'
                    dia = re.search(fechaLog_re, ultimaLinea).group(3)
                    mes = re.search(fechaLog_re, ultimaLinea).group(2)
                    anio = re.search(fechaLog_re, ultimaLinea).group(1)
                    dLog = datetime (int(anio) ,int(mes) ,int(dia))
                    dInput = datetime(int(fechaInput[2]) ,int(fechaInput[1]) ,int(fechaInput[0])) 
                    if (dInput.strftime('%a') in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']):
                        if (dInput >= dLog):           
                            break
                        else:
                            print("No puede ser anterior a la ultima guardada.\nIntentelo nuevamente..")
                    else:
                        print("Fecha esta fuera del rango de dias de semana permitido.\nIntentelo nuevamente..")
                else:
                    dInput = datetime(int(fechaInput[2]) ,int(fechaInput[1]) ,int(fechaInput[0])) 
                    if (dInput.strftime('%a') in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']): 
                        break
                    else:
                        print("Fecha esta fuera del rango de dias de semana permitido.\nIntentelo nuevamente..")
            elif fechaRegistro == '':
                return False
            else:
                print("Fecha no válida, formato DD/MM/YYYY o DD-MM-YYYY requerido.\nIntentelo nuevamente..")
        while horaRegistro != '':
            horaRegistro = input("Hora: ")
            resHora = er_hora.fullmatch(horaRegistro.rstrip())
            if resHora:
                resHora_ = resHora.group(0)
                horaLista = re.split(r':',resHora_)
                hora = re.search(fechaLog_re, ultimaLinea).group(4)
                minuto= re.search(fechaLog_re, ultimaLinea).group(5)
                segundo = re.search(fechaLog_re, ultimaLinea).group(6)
                actual = time(int(horaLista[2]), int(horaLista[1]), int(horaLista[0]))
                manana = time(8, 30, 0)
                noche = time(21, 0, 0)
                dInput = datetime(int(fechaInput[2]) ,int(fechaInput[1]) ,int(fechaInput[0]), int(horaLista[0]), int(horaLista[1]), int(horaLista[2])) 
                try:  
                    dLog = datetime (int(anio) ,int(mes) ,int(dia), int(hora),int(minuto),int(segundo))
                    if (manana <= actual and actual <= noche):
                        if (dInput > dLog):           
                            break
                        else:
                            print("No puede ser anterior a la ultima guardada.\nIntentelo nuevamente..")
                    else:
                        print("Hora fuera del tiempo de estadia permitido.\nIntentelo nuevamente..")
                except:
                    if (manana <= actual and actual <= noche):
                        break
                    else:
                        print("Hora fuera del rango permitido.\nIntentelo nuevamente..")
            elif horaRegistro == '':
                return False
            else:
                print("Hora no válida formato HH:MM:SS requerido.\nIntentelo nuevamente..")
        while rutaQR != '' :
            rutaQR = input("Ruta QR: ")
            texto = comprobarRutaQR(rutaQR.replace(' ',''))
            if texto:
                break 
            elif rutaQR == '':
                return False
            else:
                print("Intentelo nuevamente...")

        while telefonoRegistro != '':
            telefonoRegistro = input("Telefono: ")
            resTelefono = er_telefono.fullmatch(telefonoRegistro.rstrip())
            if resTelefono:
                break
            elif telefonoRegistro == '':
                return False
            else:
                print("Telefono no valido.\nIntentelo nuevamente..")
       
        while accion != '':
            accion = input("Accion: ")
            resAccion = er_accion.fullmatch(accion.rstrip())
            if resAccion:
                break
            elif accion == '':
                return False
            else:
                print("Accion no valida.\nIntentelo nuevamente..")
        
        if path.exists("log.txt"):
            archivo = open("log.txt", "a")
        else:
            archivo = open("log.txt", "w")

        registro = str("[ "+"Day "+resFecha.group(3)+" - "+resFecha.group(2)+" - "+resFecha.group(1)+" , "+resHora.group(1)+" : "+resHora.group(2)+" : "+resHora.group(3)+" ] "+ "Location : "+ texto+" , "+"User : "+resTelefono.group(1)+" "+resTelefono.group(2)+" "+resTelefono.group(3)+" "+accion.lower()+'\n')
        print(registro)
        archivo.write(registro)
        archivo.close()
        return True

    def generaSalida():
        #Itero en el archivo log y busco registros 
        if path.exists("log.txt"):
            archivo = open("log.txt", "r")
        else:
            return False
        lineas = archivo.readlines()
        archivo.close()
        erroneas = 0
        validos = 0
        redundantes = 0
        faltantes = 0
        fechaLog_re = r'Day *(\d{4})[ -]+(\d{2})[ -]+(\d{2})[ ,]+(\d{2})[ :]+(\d{2})[ :]+(\d{2}) *]'
        codigoPatrimonial_re =  r': +((\d{2})[\.\_]+)?ED\_?(\d{3})[\.\_]B(\d{1})[\.\_]\-?((\d{1,2}|(EN)|(CU)))[\.\_](\d{3})[\.]?([A-Za-z0-9]?)'
        total_re = r'\[ *Day.+\] *Location.+User.+'
        accion_re = r'[iI][nN]|[oO][uU][tT]'
        registros = {'fecha':[],'usuario':[],'recinto':[],'accion':[]}
        for index,linea in enumerate(lineas[1:]):
            #print (linea)
            #Revision de errores
            #Primero el formato total
            total = re.search(total_re, linea)
            if total == None:
                erroneas += 1
                print ('La linea ' + str(index)+ ' esta errada.\n')
                continue
            try:
                dia = re.search(fechaLog_re, linea).group(3)
                mes = re.search(fechaLog_re, linea).group(2)
                anio = re.search(fechaLog_re, linea).group(1)
                hora = re.search(fechaLog_re, linea).group(4)
                minuto= re.search(fechaLog_re, linea).group(5)
                segundo = re.search(fechaLog_re, linea).group(6)
            except:
                erroneas += 1
                print ('La linea ' + str(index)+ ' esta errada.\n')
                continue
            dInput = datetime(int(anio) ,int(mes) ,int(dia))
            if (dInput.strftime('%a') not in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']):  
                erroneas += 1
                print ('La linea ' + str(index)+ ' esta errada.\n')
                continue
            actual = time(int(hora), int(minuto), int(segundo))
            manana = time(8, 30, 0)
            noche = time(21, 0, 0)
            if not (manana <= actual and actual <= noche):
                erroneas += 1
                print ('La linea ' + str(index)+ ' esta errada.\n')
                continue
            codigoPatrimonial = re.search(codigoPatrimonial_re,linea)
            if codigoPatrimonial == None:
                erroneas += 1
                print ('La linea ' + str(index)+ ' esta errada.\n')
                continue
            if not validaLocacion(codigoPatrimonial.group(0)):
                erroneas += 1
                print ('La linea ' + str(index)+ ' esta errada.\n')
                continue
            telefono_re = r'User.*(\d{3})\s?(\d{3})\s?(\d{3})'
            telefono = re.search(telefono_re,linea)
            if telefono == None:
                erroneas += 1
                print ('La linea ' + str(index)+ ' esta errada.\n')
                continue 
            accion = re.search(accion_re,linea)
            if accion == None:
                erroneas += 1
                print ('La linea ' + str(index)+ ' esta errada.\n')
                continue  
            fechaRegistro = datetime(int(anio), int(mes), int(dia),int(hora), int(minuto), int(segundo))
            telefono = telefono.group(0).replace(' ','').replace('User:','')
            codigoPatrimonial = codigoPatrimonial.group(0).replace(':','').replace(' ','')
            accion = accion.group(0).lower()
            registros['fecha'].append(fechaRegistro)
            registros['usuario'].append(telefono)
            registros['recinto'].append(codigoPatrimonial)
            registros['accion'].append(accion)  
        print ('Registros válidos: : '+str(validos))
        print ('Registros erróneos : '+str(erroneas))        
        print ('Registros redundates: : '+str(redundantes))
        print ('Registros faltantes: : '+str(faltantes)) 
    
    def menu():
        print ("Selecciona una opción")
        print ("\t1 - A : Añadir registro de presencia.")
        print ("\t2 - G : Generar salida.")
        print ("\t3 - C : Control de presencia.")
        print ("\t9 - S : Salir del programa.")
 


 
listaEdificios = []
archivoEdificios = open("edificios.csv", encoding="utf-8")
lector = csv.reader(archivoEdificios)
for edificio in lector:
    for edif in edificio:
        listaEdificios.append(edif)
archivoEdificios.close()
dicList = {'campus':[],'edificio':[],'nombre':[]}
for element in listaEdificios[1:]:
    line = element.split(';')
    dicList['campus'].append('0'+line[0])
    if (len(line[1])==1):
        dicList['edificio'].append('00'+line[1])
    elif (len(line[1])==2):
        dicList['edificio'].append('0'+line[1])
    else:
        dicList['edificio'].append(line[1])
        
    dicList['nombre'].append(line[2])
    
while True:
    # Mostramos el menu
    menu()
    # solicitamos una opción al usuario
    opcionMenu = input("inserta un valor >> ")
 
    if opcionMenu=="A":
        
        if (add_registro()):
            print ('Registro Exitoso!\n')
        else:
            print ('Registro Abortado.\n')
        # print ("")
        #input("Has pulsado la opción 1...\npulsa una tecla para continuar")
    elif opcionMenu=="G":
        generaSalida()
        #input("Has pulsado la opción G...\npulsa una tecla para continuar")
    elif opcionMenu=="C":
        print ("")
        input("Has pulsado la opción C...\npulsa una tecla para continuar")
    elif opcionMenu=="S":
        break
    else:
        print ("")
        input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")