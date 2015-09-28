import psycopg2
from PyQt4 import QtCore, QtGui, uic
from decimal import Decimal
from datetime import datetime
from _datetime import timedelta
from datetime import date
import xlwt






app = QtGui.QApplication([])

planiranje = uic.loadUi("design/planiranje.ui")

def sql_cxn():
    """
    Povezava s podatkovno bazo
    @return:
    """
    try:
        #conn=psycopg2.connect("dbname=eDimnikar user=postgres password=drejko99")
        conn = psycopg2.connect(host="10.112.0.5", port ="5432", dbname="eDimnikar", user="postgres", password="root")
        #conn = psycopg2.connect(host="localhost", port ="5432", dbname="postgres", user="postgres", password="drejko99")
        cursor = conn.cursor()
        return cursor,conn
    except:
        return  "Povezava s streznikom ni uspela."
    
def rpe_obcine():
    cursor=sql_cxn()[0]
    query = """
            SELECT
                "eDimnikar".rpe_obcine.sifra_obcine,
                "eDimnikar".rpe_obcine.naziv
            FROM
                "eDimnikar".rpe_obcine
            ;"""
    cursor.execute(query)
    rpe_obcine = []
    row = cursor.fetchall()
    for i in range(len(row)):
        rpe_obcine.append(row[i][1])
    return rpe_obcine      

obcine = rpe_obcine()
planiranje.cbObcina.addItems(obcine)

def izbiraObcine():
  
    izbranaObcina = planiranje.cbObcina.currentText()
    return izbranaObcina

def izbiraNaselja():
    cursor=sql_cxn()[0]
    queryIdObcine = """
                SELECT
                    "eDimnikar".rpe_obcine.sifra_obcine
                FROM
                    "eDimnikar".rpe_obcine
                WHERE
                    "eDimnikar".rpe_obcine.naziv = '{}'
    ;""".format(izbiraObcine())
    cursor.execute(queryIdObcine)
    row = cursor.fetchall()
    query_naselje= """
                SELECT
                    "eDimnikar".rpe_obcine.naziv,
                    "eDimnikar".rpe_naselje.naziv
                FROM
                    "eDimnikar".rpe_naselje,
                    "eDimnikar".rpe_obcine
                WHERE
                    "eDimnikar".rpe_naselje.sifra_obcine = "eDimnikar".rpe_obcine.sifra_obcine
                AND
                   "eDimnikar".rpe_obcine.sifra_obcine = {}
                    
                ;""".format(row[0][0])
                
    cursor.execute(query_naselje)
    row = cursor.fetchall()
    rpe_naselje = []
    for i in range(len(row)):
        rpe_naselje.append(row[i][1])
        
    planiranje.cbNaselje.clear()
    planiranje.cbNaselje.addItems(rpe_naselje)  
    return(rpe_naselje)

def izbranoNaselje():
    izbranoNaselje = planiranje.cbNaselje.currentText()
    return izbranoNaselje

def izbiraUlice():
    cursor=sql_cxn()[0]
    #print(izbiraObcine())
    #print(izbranoNaselje())
    queryIdObcine = """
                SELECT
                    "eDimnikar".rpe_obcine.sifra_obcine
                FROM
                    "eDimnikar".rpe_obcine
                WHERE
                    "eDimnikar".rpe_obcine.naziv = '{}'
    ;""".format(izbiraObcine())
    cursor.execute(queryIdObcine)
    row = cursor.fetchall()
    sifraObcine = row[0][0]
    queryNaseljeId= """
                SELECT
                    "eDimnikar".rpe_naselje.sifra_naselja
                FROM
                    "eDimnikar".rpe_naselje,
                    "eDimnikar".rpe_obcine
                WHERE
                    "eDimnikar".rpe_naselje.sifra_obcine = "eDimnikar".rpe_obcine.sifra_obcine
                AND
                   "eDimnikar".rpe_obcine.sifra_obcine = {}
                AND 
                    "eDimnikar".rpe_naselje.naziv = '{}'
                ;""".format((row[0][0]),izbranoNaselje())
                
    cursor.execute(queryNaseljeId)
    row = cursor.fetchall()
    sifraNaselja = row[0][0]
    queryUlice = """
                SELECT 
                    "eDimnikar".rpe_ulice.naziv_ulice
                FROM
                    "eDimnikar".rpe_ulice
                WHERE
                    "eDimnikar".rpe_ulice.sifra_obcine = {}
                AND
                    "eDimnikar".rpe_ulice.sifra_naselja = {}
    ;""".format(sifraObcine, sifraNaselja)
    cursor.execute(queryUlice)
    row = cursor.fetchall()
    rpeUlice = []
    for i in range(len(row)):
        rpeUlice.append(row[i][0])
    planiranje.cbUlica.clear()
    planiranje.cbUlica.addItems(rpeUlice)     

def IzbranaUlica():
    izbranaUlica = planiranje.cbUlica.currentText()
    return izbranaUlica

tabela = []

def seznamUlic():
    obcina = izbiraObcine()
    naselje = izbranoNaselje()
    ulica = IzbranaUlica()
    szn = obcina, naselje, ulica
    tabela.append(szn)
    planiranje.tbSeznamUlic.append(szn[2])
    return tabela

def seznamDimnikarjev():
    cursor=sql_cxn()[0]
    query = """
            SELECT
                "eDimnikar".zaposleni.priimek_ime
            FROM
                "eDimnikar".zaposleni
            ;"""
    cursor.execute(query)
    zaposleni = []
    row = cursor.fetchall()
    for i in range(len(row)):
        zaposleni.append(row[i][0])
    return zaposleni      
zaposleni = seznamDimnikarjev()
planiranje.cbZaposleni.addItems(zaposleni)
    
    
def izbrisiSeznam():
    planiranje.exit()

    


    
def izbraniPodatki():
    cursor=sql_cxn()[0]
    planiranje.cbUlica.clear()
    seznam = seznamUlic()
    danes = date.today()
    leto = timedelta(days=365)

    tabela = []
    vsota = 0
    for i in range(len(seznam)-1):
        obcina = seznam[i][0]
        naselje = seznam[i][1]
        ulica = seznam[i][2]
        
        obcina = obcina.replace(' ','%')
        naselje = naselje.replace(' ','%')
        ulica = ulica.replace(' ','%')
    
    
        queryPrikazi = """
        SELECT    *
        FROM 
            "eDimnikar".uporabnik
            LEFT  OUTER JOIN     
                (
                SELECT
                    "eDimnikar".fakture_vasco.sifra_kupca, 
                    "eDimnikar".fakture_vasco.znesek,
                    "eDimnikar".fakture_vasco.izvajalec,
                    "eDimnikar".zaposleni.priimek_ime,
                    "eDimnikar".fakture_vasco.datum_storitve,
                    rank()
                OVER 
                (
                    PARTITION BY sifra_kupca
                    ORDER BY datum_storitve
                    DESC
                )
                
                FROM "eDimnikar".fakture_vasco
                    LEFT JOIN     
                        "eDimnikar".zaposleni 
                    ON 
                        "eDimnikar".zaposleni.stara_sifra =  "eDimnikar".fakture_vasco.izvajalec  
                ) sub_query
            ON uporabnik.sifra_stara = sub_query.sifra_kupca
            LEFT JOIN     
                "eDimnikar".postne_stevilke
            ON 
                "eDimnikar".postne_stevilke.sifra_poste = "eDimnikar".uporabnik.posta_st_fk       
        WHERE
            "eDimnikar".uporabnik.rpe_obcina ILIKE '%{}%'
        AND    
            "eDimnikar".uporabnik.rpe_naselje ILIKE '%{}'
        AND 
            "eDimnikar".uporabnik.rpe_ulica ILIKE '%{}'
        AND
        (rank = 1 or rank IS NULL)
            ORDER BY "eDimnikar".uporabnik.naslov
                    ASC   ;""".format(obcina,naselje, ulica)
        
        cursor.execute(queryPrikazi)
        
        row = cursor.fetchall()
       
        hisnaOd=planiranje.planiranjeHsOd.text()
        hisnaDo=planiranje.planiranjeHsDo.text() 
        #print(hisnaDo, hisnaOd) 
        
        for i in row:
            if hisnaDo ==''and hisnaOd=='':
                tabela.append((str((i[1])),i[2],i[4],str(i[30]),str(i[31]),i[28],str(i[25]),i[26], i[17]))
                rowCount=len(tabela)
            
            elif int(i[22])>=int(hisnaOd) and int([22])<=int(hisnaDo):
                tabela.append((str((i[1])),i[2],i[4],str(i[2]),str(i[28]),i[28],str(i[25]),i[26],i[17]))
                rowCount=len(tabela)

    planiranje.twPlaniranje.setRowCount(rowCount)

    for i in range(len(tabela)):
        for j in range(len(tabela[i])):
            if (j==5):
                if tabela[i][5] !=None:
                    datum = tabela[i][5]

                    if (danes-datum) < leto:
                        print(danes-datum)
                        datumS=str(str(tabela[i][j]))
                        datumS=datumS[8:]+'.'+datumS[5:-3]+'.'+datumS[:4]
                        value = QtGui.QTableWidgetItem(datumS)
                        value1 = QtGui.QTableWidgetItem("ne naroči")
                        planiranje.twPlaniranje.setItem(i,9,value1)
                        planiranje.twPlaniranje.setItem(i,j,value)
                    else: 
                        datumS=str(str(tabela[i][j]))
                        datumS=datumS[8:]+'.'+datumS[5:-3]+'.'+datumS[:4]
                        value = QtGui.QTableWidgetItem(datumS)
                        #value = QtGui.QTableWidgetItem(str(tabela[i][j]))
                        planiranje.twPlaniranje.setItem(i,j,value)
            elif (j==6) and tabela[i][j] != 'None' :
                cena = float(tabela[i][6].strip(' "'))
                zDavkom = cena*1.22
                value3 = QtGui.QTableWidgetItem('{:.2f}'.format(zDavkom))
                planiranje.twPlaniranje.setItem(i,j,value3)
            elif (j==6) and tabela[i][j] == 'None':
                value3 = QtGui.QTableWidgetItem('')
                planiranje.twPlaniranje.setItem(i,j,value3)
                
            else:
                value = QtGui.QTableWidgetItem((tabela[i][j]))
                planiranje.twPlaniranje.setItem(i,j,value)
         

    planiranje.twPlaniranje.resizeColumnsToContents()
    
    for i in tabela:
        if i[6] != 'None':
            cena = Decimal(i[6].strip(' "'))
            vsota = vsota+cena
            
 
    planiranje.planiranjeLeReal.setText('{:.2f}'.format(vsota))
    return tabela
    
planiranje.twPlaniranje.setColumnCount(10)
planiranje.twPlaniranje.setColumnHidden(0,False)


planiranje.twPlaniranje.setSortingEnabled(True)
naslov=('Šifra', 'Naziv', 'Naslov', 'Poštna št.','Pošta','Datum zadnje st.', 'Znesek','Dimnikar', 'Opombe','Novi  datum')
planiranje.twPlaniranje.setHorizontalHeaderLabels(naslov)   
 


def izpisiExcel():
    cursor=sql_cxn()[0]
    dimnikar = planiranje.cbZaposleni.currentText()
    queryGsm= """
        SELECT 
            "eDimnikar".zaposleni.priimek_ime,
            "eDimnikar".zaposleni.gsm
        FROM 
            "eDimnikar".zaposleni
        WHERE
            "eDimnikar".zaposleni.priimek_ime ILIKE '%{}%'
        ;""".format(dimnikar)
            
    cursor.execute(queryGsm)
    row = cursor.fetchall()
    ime = row[0][0]
    stevilka = row[0][1]
    
    styleHeader=xlwt.easyxf('font: name Calibri, height 250; borders: left thin, right thin, top thin, bottom thin')
    
    excel=[]
    excelIzpis = xlwt.Workbook()
    delovniList = excelIzpis.add_sheet(dimnikar)
    epps = excelIzpis.add_sheet("epps")

    rows = planiranje.twPlaniranje.rowCount()
    column = planiranje.twPlaniranje.columnCount()
    
    for i in range(len(naslov)):
        delovniList.write(0,i,naslov[i])

    for row in range(rows):
        vrsta = []
        for column in range(10):
            data = planiranje.twPlaniranje.item(row,column)
            if data == None:
                vrsta.append(' ')
                delovniList.write(row+1, column, ' ')
            else:
                vrsta.append(data.text())
                delovniList.write(row+1, column, data.text())
                
        excel.append(vrsta)

    
    excelIzpis.save("d:/tabele/tabela_{}_{}.xls".format(date.today(),ime))



        
QtCore.QObject.connect(planiranje.cbObcina, QtCore.SIGNAL("currentIndexChanged(const QString &)"), izbiraObcine) 
QtCore.QObject.connect(planiranje.cbObcina, QtCore.SIGNAL("currentIndexChanged(const QString &)"), izbiraNaselja) 
QtCore.QObject.connect(planiranje.cbNaselje, QtCore.SIGNAL("currentIndexChanged(const QString &)"), izbranoNaselje) 
QtCore.QObject.connect(planiranje.cbNaselje, QtCore.SIGNAL("currentIndexChanged(const QString &)"), izbiraUlice) 

QtCore.QObject.connect(planiranje.pbIzpisi, QtCore.SIGNAL("clicked()"), izbraniPodatki)
QtCore.QObject.connect(planiranje.pbPrikazi, QtCore.SIGNAL("clicked()"), seznamUlic)
QtCore.QObject.connect(planiranje.pbZacniZnova, QtCore.SIGNAL("clicked()"), izbrisiSeznam)
QtCore.QObject.connect(planiranje.pbIzpisiExcel, QtCore.SIGNAL("clicked()"), izpisiExcel)


planiranje.show()
app.exec_()


