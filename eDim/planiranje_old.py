import psycopg2
from PyQt4 import QtCore, QtGui, uic
from insert_uporabnik import naselje



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

def izbraniPodatki():
    cursor=sql_cxn()[0]
    obcina = izbiraObcine()
    naselje = izbranoNaselje()
    ulica = IzbranaUlica()
    

    queryPrikazi = """
                SELECT
                    "eDimnikar".uporabnik.sifra_stara,
                    "eDimnikar".uporabnik.naziv_1,
                    "eDimnikar".uporabnik.naslov,
                    "eDimnikar".fakture_vasco.datum_storitve,
                    "eDimnikar".fakture_vasco.znesek,
                    "eDimnikar".fakture_vasco_artikli.sifra,
                    "eDimnikar".zaposleni.priimek_ime
                FROM 
                    "eDimnikar".uporabnik
                LEFT JOIN     
                    "eDimnikar".fakture_vasco 
                ON 
                    "eDimnikar".uporabnik.sifra_stara = "eDimnikar".fakture_vasco.sifra_kupca
                LEFT JOIN     
                    "eDimnikar".zaposleni 
                ON 
                    "eDimnikar".zaposleni.stara_sifra =  "eDimnikar".fakture_vasco.izvajalec   
                LEFT JOIN 
                    "eDimnikar".fakture_vasco_artikli
                ON
                        "eDimnikar".fakture_vasco.st_racuna = "eDimnikar".fakture_vasco_artikli.st_racuna
                      
             
                WHERE
                    "eDimnikar".uporabnik.rpe_obcina = '{}'
                AND    
                    "eDimnikar".uporabnik.rpe_naselje = '{}'
                AND
                    "eDimnikar".uporabnik.rpe_ulica = '{}'
                        
         
                ORDER BY "eDimnikar".uporabnik.naslov ASC
                
    ;""".format(obcina,naselje,ulica)
    
    cursor.execute(queryPrikazi)
    row = cursor.fetchall()

    tabela = []
    for i in row:
        tabela.append((str((i[0])),i[1],i[2],i[3],str(i[4]),i[5],i[6]))
    rowCount=len(tabela)
    
    planiranje.twPlaniranje.setRowCount(rowCount)
    
    for i in range(len(tabela)):
        for j in range(len(tabela[i])):
            value = QtGui.QTableWidgetItem(tabela[i][j])
            planiranje.twPlaniranje.setItem(i,j,value)
       
    planiranje.twPlaniranje.resizeColumnsToContents()

planiranje.twPlaniranje.setColumnCount(8)
planiranje.twPlaniranje.setColumnHidden(0,False)


planiranje.twPlaniranje.setSortingEnabled(True)
naslov=('Šifra', 'Naziv', 'Naslov', 'Datum storitve','Cena','Šifra storitve','Izvajalec', 'Datum',)
planiranje.twPlaniranje.setHorizontalHeaderLabels(naslov)   
    
    
QtCore.QObject.connect(planiranje.cbObcina, QtCore.SIGNAL("currentIndexChanged(const QString &)"), izbiraObcine) 
QtCore.QObject.connect(planiranje.cbObcina, QtCore.SIGNAL("currentIndexChanged(const QString &)"), izbiraNaselja) 
QtCore.QObject.connect(planiranje.cbNaselje, QtCore.SIGNAL("currentIndexChanged(const QString &)"), izbranoNaselje) 
QtCore.QObject.connect(planiranje.cbNaselje, QtCore.SIGNAL("currentIndexChanged(const QString &)"), izbiraUlice) 
QtCore.QObject.connect(planiranje.pbPrikazi, QtCore.SIGNAL("clicked()"), izbraniPodatki)
planiranje.show()
app.exec_()


