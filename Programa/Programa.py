'''
Created on 14 dic. 2020

@author: ottod
'''
import regex as re
import cv2
import csv
from io import open

if __name__ == '__main__':
    
    """ 
 Metodos de apoyo para vertificar  
    def leer_log():
        archivo = open("log.txt","r")
        lineas = archivo.readlines()
        archivo.close()
        return lineas
    
    def leer_edificios():
        
        listaEdificios = []
        archivoEdificios = open("edificios.csv", encoding="utf-8")
        lector = csv.reader(archivoEdificios)
        for edificio in lector:
            for edif in edificio:
                listaEdificios.append(edif)
        archivoEdificios.close()
        return listaEdificios
    
    def leer_logCsv():
"""        
    
    def comprobarRutaQR():
        patron_rutaQR = r'^*.png$'
        er_rutaQR = re.compile(patron_rutaQR)
        patron_codigoPatrimonial = r'^\d{2,2}?[a-zA-Z]{2,2}\d{3,3}[\._][a-zA-Z]\d[\._]\d[\._]\d{3,3}$'
        er_codigoPatrimonial = re.compile(patron_codigoPatrimonial)
        rutaQR = input('Ruta QR: ')
        resul = er_rutaQR.fullmatch(rutaQR)
        if resul:
            imagen = cv2.imread(rutaQR)
            if imagen is None:
                print('La imagen no existe.')
                comprobarRutaQR()
            else:
                detectorQR = cv2.QRCodeDetector()
                texto, puntos, _ = detectorQR.detectAndDecode(imagen)
                resul_codigo = er_codigoPatrimonial.fullmatch(texto)
            if resul_codigo:
                print(texto)
            else:
                print('Codigo patrimonial no válido.')
                comprobarRutaQR()
        else:
            print('Ruta QR no válida.')
            comprobarRutaQR()
    
    def add_registro():
        patron_fecha = r'^(3[01]|[12][0-9]|0[1-9])[\-/](0[1-9]|1[0-2])[\-/](2020)$'
        patron_hora = r'^([01]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$'
        patron_telefono = r'^(\d{3,3})\s?(\d{3,3})\s?(\d{3,3})$'
        patron_rutaQR = r'.+\.png'
        patron_codigoPatrimonial = r'(0[1-6][\._])?ED\d{3}[\._]B\d[\._](CU|EN|-\d|\d)[\._]\d{3}'
        patron_accion = r'(in|IN)|(out|OUT)'
        er_fecha = re.compile(patron_fecha)
        er_hora = re.compile(patron_hora)
        er_telefono = re.compile(patron_telefono)
        er_rutaQR = re.compile(patron_rutaQR)
        er_codigoPatrimonial = re.compile(patron_codigoPatrimonial)
        er_accion = re.compile(patron_accion)
        while True:
            fechaRegistro = input("Fecha: ")
            resFecha = er_fecha.fullmatch(fechaRegistro.rstrip())
            if resFecha:
                break
            else:
                print("Fecha no válida.\nIntentelo nuevamente..")
        while True:
            horaRegistro = input("Hora: ")
            resHora = er_hora.fullmatch(horaRegistro.rstrip())
            if resHora:
                break
            else:
                print("Hora no válida.\nIntentelo nuevamente..")
        while True:
            rutaQR = input("Ruta QR: ")
            resRutaQR = er_rutaQR.fullmatch(rutaQR.rstrip())
            if resRutaQR:
                imagen = cv2.imread(rutaQR)
                if imagen is None:
                    print('La imagen no existe.')
                    comprobarRutaQR()
                else:
                    detectorQR = cv2.QRCodeDetector()
                    texto, puntos, _ = detectorQR.detectAndDecode(imagen)
                    resCodigoPatrimonial = er_codigoPatrimonial.fullmatch(texto.rstrip())
                    if resCodigoPatrimonial:
                        break
                    else:
                        print('Codigo patrimonial no válido.')
                        comprobarRutaQR()
            else:
                print('Ruta QR no válida.')
                comprobarRutaQR()
        while True:
            telefonoRegistro = input("Telefono: ")
            resTelefono = er_telefono.fullmatch(telefonoRegistro.rstrip())
            if resTelefono:
                break
            else:
                print("Telefono no valido.\nIntentelo nuevamente..")
        while True:
            accion = input("Accion: ")
            resAccion = er_accion.fullmatch(accion.rstrip())
            if resAccion:
                break
            else:
                print("Accion no valida.\nIntentelo nuevamente..")        
        archivo = open("log.txt", "w")
        registro = str("[ "+"Day "+resFecha.group(3)+" - "+resFecha.group(2)+" - "+resFecha.group(1)+" , "+resHora.group(1)+" : "+resHora.group(2)+" : "+resHora.group(3)+" ] "+ "Location : "+ texto+" , "+"User : "+resTelefono.group(1)+" "+resTelefono.group(2)+" "+resTelefono.group(3)+" "+accion.lower())
        print(registro)
        archivo.write(registro)
        archivo.close()
        print("\nRegistro exitoso!\n")
        
    
    def menu():
        print ("Selecciona una opción")
        print ("\t1 - A : Añadir registro de presencia.")
        print ("\t2 - G : Generar salida.")
        print ("\t3 - C : Control de presencia.")
        print ("\t9 - S : Salir del programa.")
 
 
while True:
    # Mostramos el menu
    menu()
 
    # solicitamos una opción al usuario
    opcionMenu = input("inserta un valor >> ")
 
    if opcionMenu=="A":
        add_registro()
        # print ("")
        #input("Has pulsado la opción 1...\npulsa una tecla para continuar")
    elif opcionMenu=="G":
        print ("")
        input("Has pulsado la opción G...\npulsa una tecla para continuar")
    elif opcionMenu=="C":
        print ("")
        input("Has pulsado la opción C...\npulsa una tecla para continuar")
    elif opcionMenu=="S":
        break
    else:
        print ("")
        input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")