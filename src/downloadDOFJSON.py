#! /usr/bin/python3

import time,sys,os
import urllib.request,json
from datetime import date
from datetime import timedelta

DOF_DIARIO_FULL = 'http://diariooficial.gob.mx/WS_getDiarioFull.php?year=%s&month=%s&day=%s'
DEBUG = True;

def getDOFResume(thisDate):
    response = urllib.request.urlopen(DOF_DIARIO_FULL % (thisDate.year, thisDate.month, thisDate.day))
    content = response.read()
    data = json.loads(content.decode('utf8')) 
    return data
    

def printHelp():
    print ('Este script sirve para descaragar el resumen de las publicaciones del DOF en un periodo determinado:')
    print ("\n\t" + os.path.basename(__file__) + " [DIAS | [FECHA_INICIO [FECHA_FINAL]]");
    print ("\nEl formato de fecha es %Y-%m-%d")
    print ("\n\nEjemplo:\n\t" + os.path.basename(__file__) + " 2\t\t\t\t Recupera las publicaciones de los últimos 2 días");
    print ("\t" + os.path.basename(__file__) + " 1900-1-1\t\t\t Recupera las apartir del 1 de enero de 1900");
    print ("\t" + os.path.basename(__file__) + " 1900-1-1 1900-1-5\t\t Recupera las apartir del 1 de enero de 1900 hasta el 5 de enero de 1900");
    print ("\t" + os.path.basename(__file__) + " \t\t\t\t Descarga el día actual");
    sys.exit();

def main():
    if len(sys.argv) <= 1:
        startDate = date.today()
        endDate = date.today()
        delta = timedelta(days = 0)
    else:
        if (sys.argv[1]=='-h' or sys.argv[1]=='--help' or sys.argv[1]=='?'):
            printHelp()
        elif len(sys.argv) == 2:
            endDate = date.today()
            if (sys.argv[1].isdigit()):
                delta = timedelta(days=int(sys.argv[1]))
                startDate = endDate - delta
            else:
                startDate = date.fromtimestamp(time.mktime(time.strptime(sys.argv[1],'%Y-%m-%d')));
                delta = endDate - startDate
        elif len(sys.argv) == 3:
            endDate = date.fromtimestamp(time.mktime(time.strptime(sys.argv[2],'%Y-%m-%d')));
            startDate = date.fromtimestamp(time.mktime(time.strptime(sys.argv[1],'%Y-%m-%d')));
            delta = endDate - startDate
        #print( str(today.year) + "/" + str(today.month) + "/" + str(today.day));
        #response = urllib.request.urlopen(DOF_DIARIO_FULL % (x[0], x[1], dia))
    if (delta.days<0):
        printHelp()

    for i in range (0,delta.days+1):
        thisDate = startDate + timedelta(days=i)
        response = getDOFResume(thisDate)
        if (DEBUG):
            print ("%s-%s-%s" % (thisDate.year,thisDate.month,thisDate.day) + "\t" + DOF_DIARIO_FULL % (thisDate.year, thisDate.month, thisDate.day), end="\t")
        print (response)

#Ejecución
main();
