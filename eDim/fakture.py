#coding='UTF-8'
import psycopg2
import os
from PyQt4 import QtCore, QtGui, uic

app = QtGui.QApplication([])
main = uic.loadUi("design/fakturiranje.ui")




#main.twIzdaneFakture.setColumnCount(4)
#main.twIzdaneFakture.setColumnHidden(0,False)
#main.twIzdaneFakture.setSortingEnabled(True)
#naslov=('Št.rač.', 'Datum', 'Znesek','Izvajalec')

#main.twIzdaneFakture.setHorizontalHeaderLabels(naslov)



conn = psycopg2.connect(host="10.112.0.5", port ="5432", dbname="eDimnikar", user="postgres", password="root")
cursor = conn.cursor()

data = 64071
query = """ SELECT  
                "eDimnikar".fakture_vasco.st_racuna,
                "eDimnikar".fakture_vasco.datum_storitve,
                "eDimnikar".fakture_vasco.znesek,
                "eDimnikar".zaposleni.priimek_ime
            FROM
                "eDimnikar".fakture_vasco,
                "eDimnikar".uporabnik,
                "eDimnikar".zaposleni
            WHERE
                "eDimnikar".uporabnik.sifra_stara = {}
            AND
               "eDimnikar".zaposleni.stara_sifra =  "eDimnikar".fakture_vasco.izvajalec 
            AND       
                "eDimnikar".uporabnik.sifra_stara = "eDimnikar".fakture_vasco.sifra_kupca
""".format(data)
#cursor.execute(query)
#row = cursor.fetchall()



#imenik1 = []
#for i in row:
#    imenik1.append((str((i[0])),str(i[1]),(i[2]),str(i[3])))
    
#stRacuna = imenik1[0][0]
#datumSt = imenik1[0][1]


#rowCount=len(imenik1)
#main.twIzdaneFakture.setRowCount(rowCount)
#for i in range(len(imenik1)):
#    for j in range(len(imenik1[i])):
#        value = QtGui.QTableWidgetItem(imenik1[i][j])
        #main.twIzdaneFakture.setItem(i,j,value)


#main.twIzdaneFakture.resizeColumnsToContents()


#main.twPodrobnostiFakture.setColumnCount(4)
#main.twPodrobnostiFakture.setColumnHidden(0,False)
#main.twPodrobnostiFakturesetSortingEnabled(True)
naslov1=('Šifra.', 'Naziv', 'Cena brez DDV','Količina')

#main.twPodrobnostiFakture.setHorizontalHeaderLabels(naslov1)

#queryArtkli = """ 
#                SELECT 
#                        "eDimnikar".fakture_vasco_artikli.sifra,
#                        "eDimnikar".fakture_vasco_artikli.naziv_1,
#                        "eDimnikar".fakture_vasco_artikli.naziv_2,
#                        "eDimnikar".fakture_vasco_artikli.kolicina,
#                        "eDimnikar".fakture_vasco_artikli.cena
#                FROM
#                        "eDimnikar".fakture_vasco,
#                        "eDimnikar".fakture_vasco_artikli
#                WHERE    
#                        "eDimnikar".fakture_vasco.st_racuna = {}
#                AND
#                        "eDimnikar".fakture_vasco.datum_storitve = '{}'
#                AND
#                        "eDimnikar".fakture_vasco.st_racuna = "eDimnikar".fakture_vasco_artikli.st_racuna
#                AND
#                        "eDimnikar".fakture_vasco.datum_storitve = "eDimnikar".fakture_vasco_artikli.datum_storitve
                        

#"""#.#format(stRacuna, datumSt)
#cursor.execute(queryArtkli)

#row = cursor.fetchall()
#artikli = []
#for i in row:
#    artikli.append(i)
#artikliFormat = []

#for i in artikli:
#    for j in range(len(i)):
#            print(i[j])

main.show()
app.exec_()

