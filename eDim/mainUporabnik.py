import psycopg2
import os
from PyQt4 import QtCore, QtGui, uic
from decimal import Decimal


app = QtGui.QApplication([])
main = uic.loadUi("design/uporabnik.ui")
vnos_kn = uic.loadUi("design/vnos_kn.ui")
vstopno = uic.loadUi("design/main.ui")
narocanje = uic.loadUi("design/narocanje.ui")

def vstop():
    main.show()
    vstopno.close()    

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

def dodaUporabnikak():
    conn=sql_cxn()
    cursor = conn.cursor()
    naziv = main.naziv.setText("")
    naslov = main.naslov.setText("")

def addUporabnik():
    cursor = sql_cxn()[0]
    query_id = """
        SELECT
            MAX("eDimnikar".uporabnik.id)
        FROM
            "eDimnikar".uporabnik
            """
    cursor.execute(query_id)
    row = cursor.fetchall()
    nova_sifra = int(row[0][0])+1
    main.uporLeSifra.setText(str(nova_sifra))
    main.uporLeNaziv.setText('')
    main.uporLeNaziv2.setText('')
    main.uporLeNaslov.setText('')
    main.uporLeNaziv2.setText('')
    main.uporLeNaslov.setText('')
    main.uporCbPosta.setCurrentIndex(row[0][4])
    main.uporLePosta.setText('')
    main.uporLeNaselje.setText('')
    #main.uporCbTip.addItems(str(tip))
    main.uporLeTip.setText('')
    main.uporLeSm.setText('')
    main.uporLeKontankt.setText('')
    return nova_sifra

def shraniUporabnika():
    #conn=psycopg2.connect("dbname=eDimnikar user=postgres password=drejko99")
    conn = psycopg2.connect(host="10.112.0.5", port ="5432", dbname="eDimnikar", user="postgres", password="root")

    cur = conn.cursor()
    
    naziv_1 = main.uporLeNaziv.text()
    naziv_2 = main.uporLeNaslov.text()
    naslov = main.uporLeNaslov.text()
    #posta = main.uporLeNaslov.text()
    naselje = main.uporLeNaslov.text()
    #tip = main.uporLeNaslov.text()
    #sm = main.uporLeNaslov.text()
    sql= """
         SELECT max(id) FROM "eDimnikar".uporabnik;
     """
    cur.execute(sql)
    rows = cur.fetchone()
    lastUser = rows[0]

    id_1 = str(lastUser+1)
    #naziv_1 = "Andrej Ficko"
    #naziv_2 = "Ficko Andrej"
    #naslov = "Gornji Crnci 13"
    posta = "9261"
    #naselje = "Gornji Crnci"
    tip = "Privat stranka"
    sm = "Domzale"
    aktivnost = "Da"
    davcni = "Ne"
    id_ddv = ""
    tudi_placnik = "Da"
    placnik = 1
    trr = "0123 4567 8910 123"
    kontakt = "andrejficko@gmail.com"
    opombe = ""
    
    
    tip_sql = """SELECT id FROM "eDimnikar".upr_tip
            WHERE naziv ='{}';
            """.format(tip)      
    cur.execute(tip_sql)
    rows = cur.fetchall()
    tip_uporabnika_fk = (rows[0][0])

    sm_sql = """SELECT id FROM "eDimnikar".upr_sm
        WHERE naziv ='{}';
        """.format(sm)
    cur.execute(sm_sql)
    rows = cur.fetchall()

    sm_uporabnika_fk = 1


    if aktivnost == "Da": akt = True
    else: akt = False

    if davcni == "Da": dav = True 
    else: dav=  False

    if tudi_placnik == "Da": tudi_pl = True
    else: tudi_pl = False

    sql_insert = """INSERT INTO "eDimnikar".uporabnik (
                    id,
                    naziv_1,
                    naziv_2,
                    naslov,
                    posta_st_fk,
                    naselje,
                    tip_uporabnika_fk,
                    sm_id_fk,
                    aktivnost,
                    davcni_zavezanec,
                    id_za_ddv,
                    tudi_placnik,
                    placnik_id,
                    trr,
                    kontakt)
                VALUES
                ({},'{}','{}','{}',{},'{}',{},{},{},{},'{}',{},'{}','{}','{}')
            """.format(id_1, naziv_1, naziv_2, naslov, posta, naselje, tip_uporabnika_fk, sm_uporabnika_fk, akt, dav, id_ddv, tudi_pl, placnik, trr, kontakt)
            
            
    cur.execute(sql_insert)
    conn.commit()      
    main.pbShraniUporabnika.hide()      
                       

def iskanjeUporabnika():
    cursor=sql_cxn()[0]
    qniz=main.uporLeIskanje.text()
    niz = qniz.replace(' ','\xa0')

    q=("""
        SELECT
            "eDimnikar".uporabnik.sifra_stara,
            "eDimnikar".uporabnik.naziv_1,
            "eDimnikar".uporabnik.naslov
        FROM "eDimnikar".uporabnik
        WHERE
        "eDimnikar".uporabnik.naslov ILIKE '{}%' 
        OR
        "eDimnikar".uporabnik.naziv_1 ILIKE '{}%' 


    limit 50;
    """).format(niz,niz)
    #"eDimnikar".uporabnik.naziv_1 ILIKE '{}%'
    #     OR

    cursor.execute(q)
    
    imenik = []
    for row in cursor:
        imenik.append((str((row[0])),row[1],row[2]))
    
 
    rowCount=len(imenik)
    main.uporTwRezultati.setRowCount(rowCount)

    for i in range(len(imenik)):
        for j in range(len(imenik[i])):
            value = QtGui.QTableWidgetItem(imenik[i][j])
            main.uporTwRezultati.setItem(i,j,value)
    main.uporTwRezultati.resizeColumnsToContents()



#@Pokažigf
def pokaziPodrobnosti():
#Ta funkcija......
    cursor = sql_cxn()[0]

    row = main.uporTwRezultati.currentItem().row()
    cell = main.uporTwRezultati.item(row,0).text()

    query_podrobnosti = """
                SELECT 
                "eDimnikar".uporabnik.id,
                "eDimnikar".uporabnik.naziv_1,
                "eDimnikar".uporabnik.naziv_2,
                "eDimnikar".uporabnik.naslov,
                "eDimnikar".uporabnik.posta_st_fk,
                "eDimnikar".postne_stevilke.naziv_poste,
                "eDimnikar".uporabnik.naselje,
                "eDimnikar".upr_sm.sifra,
                "eDimnikar".upr_sm.naziv,
                "eDimnikar".uporabnik.aktivnost,
                "eDimnikar".uporabnik.davcni_zavezanec,
                "eDimnikar".uporabnik.id_za_ddv,
                "eDimnikar".uporabnik.trr,
                "eDimnikar".uporabnik.opombe
        FROM
                "eDimnikar".uporabnik,

                "eDimnikar".upr_sm,
                "eDimnikar".postne_stevilke
        WHERE
                "eDimnikar".uporabnik.sifra_stara = {}

        AND
                "eDimnikar".uporabnik.sm_id_fk = "eDimnikar".upr_sm.id
        AND
                "eDimnikar".postne_stevilke.sifra_poste = "eDimnikar".uporabnik.posta_st_fk
       """.format(cell)

    cursor.execute(query_podrobnosti)
    row = cursor.fetchall()
  

    
    #posta= (str(row[0][3])) +'  '+ (row[0][4])
    main.uporLeSifra.setText(str(row[0][0]))
    main.uporLeNaziv.setText((row[0][1]))
    main.uporLeNaziv2.setText(row[0][2])
    main.uporLeNaslov.setText(row[0][3])
    main.uporCbPosta.setCurrentIndex(row[0][4])
    #main.uporLePosta.setText(posta)
    main.uporLeNaselje.setText(row[0][6])
    #main.uporCbTip.addItems(str(tip))

    main.uporLeSm.setText((str(row[0][7]) +' ... '+ (row[0][8])))
    #main.uporLeSm.setText((str(row[0][9]) +' ... '+ (row[0][10])))
    vnos_kn.leUporabnik.setText(str(row[0][0])+ '  '+(str(row[0][1])))

    if row[0][9]:
        main.uporCbAktivnost.setCheckState(True)
    else:
        main.uporCbAktivnost.setCheckState(False)
    if row[0][10]:
        main.uporCbDavcni.setCheckState(True)
    else:
        main.uporCbDavcni.setCheckState(False)
    main.uporLeDdv.setText(row[0][11])
    main.uporLeTrr.setText(row[0][12])
    main.uporTeOpombe.setText(row[0][13])
    
    
    query = """ SELECT  
                "eDimnikar".fakture_vasco.st_racuna,
                "eDimnikar".fakture_vasco.datum_storitve,
                "eDimnikar".fakture_vasco.znesek,
                "eDimnikar".fakture_vasco.knjizenje,
                "eDimnikar".fakture_vasco.izvajalec

            FROM
                "eDimnikar".fakture_vasco,
                "eDimnikar".uporabnik

            WHERE
                "eDimnikar".uporabnik.sifra_stara = {}
      
            AND       
                "eDimnikar".uporabnik.sifra_stara = "eDimnikar".fakture_vasco.sifra_kupca
            ORDER BY "eDimnikar".fakture_vasco.datum_storitve
            DESC
    """.format(cell)
    cursor.execute(query)
    row1 = cursor.fetchall()
    imenik1 = []
    for i in row1:
        imenik1.append((str((i[0])),str(i[1]),str(i[2]),str(i[3]),str(i[4])))
        
    rowCount=len(imenik1)
    main.twIzdaneFakture.setRowCount(rowCount)
    for i in range(len(imenik1)):
        for j in range(len(imenik1[i])):
            if j==1:
                datumS=str(str(imenik1[i][j]))
                datumS=datumS[8:]+'.'+datumS[5:-3]+'.'+datumS[:4]
                value = QtGui.QTableWidgetItem(datumS)
                main.twIzdaneFakture.setItem(i,j,value)
            elif j==2:
                cena = Decimal(imenik1[i][j].strip(' "'))
                value = QtGui.QTableWidgetItem(('{:.2f}'.format(cena)))
                main.twIzdaneFakture.setItem(i,j,value)
            elif j==3:
                if imenik1[i][3] == '1':
                    value = QtGui.QTableWidgetItem('Gotovina')
                    main.twIzdaneFakture.setItem(i,j,value)
                else:
                    value = QtGui.QTableWidgetItem('DN')
                    main.twIzdaneFakture.setItem(i,j,value)
            else:
                value = QtGui.QTableWidgetItem((imenik1[i][j]))
                main.twIzdaneFakture.setItem(i,j,value)
         
                
                    

    main.twIzdaneFakture.resizeColumnsToContents()

    return row1,cell

def rpe_obcine():
    cursor = sql_cxn()[0]
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

def rpe_naselje(rpe_obcine):
    cursor = sql_cxn()[0]
    obcina1 = izbranaObcina(rpe_obcine)
    q = """
        SELECT
            "eDimnikar".rpe_obcine.naziv,
            "eDimnikar".rpe_naselje.naziv
        FROM
            "eDimnikar".rpe_obcine,
            "eDimnikar".rpe_naselje
        WHERE "eDimnikar".rpe_obcine.sifra_obcine = "eDimnikar".rpe_naselje.sifra_obcine
        AND         "eDimnikar".rpe_obcine.naziv = '{}';
    """.format(obcina1)
    cursor.execute(q)
    rpe_naselje = []
    row = cursor.fetchall()
    for i in range(len(row)):
        rpe_naselje.append(row[i][1])

    return rpe_naselje
    rpe_obcine = rpe_obcine()
    for i in rpe_obcine:
        main.cbRpeObcine.addItem(i)

def izbranaObcina(obcina):
    return obcina

def vnos_naprave():
    vnos_kn.show()

def narocanjeStrank():
    narocanje.show()


#print (izbranaObcina(main.cbRpeObcine.currentText()))


(QtCore.QObject.connect(main.cbRpeObcine, QtCore.SIGNAL('activated(QString)'), izbranaObcina))
#obcina = main.cbRpeObcine.currentText()
#print(obcina)
#rpe_naselje = rpe_naselje(naselje)
#print(rpe_naselje)
#for i in rpe_naselje:
#    main.cbRpeNaselje.addItem(i)


def tipUporabnika():
    cursor=sql_cxn()[0]
    tip =[]
    query_1="""
        SELECT "eDimnikar".upr_tip.id,"eDimnikar".upr_tip.naziv FROM "eDimnikar".upr_tip;
            """
    cursor.execute(query_1)
    row = cursor.fetchall()
    for i in row:
        tip.append(str(i[0])+' '+i[1])
    return tip

tipUporabnika = tipUporabnika()
#main.uporCbTip.addItems(tipUporabnika)

#text = main.uporCbTip.item()

#print(text)

def oProgramu():
    os.startfile("D:/eDim/eDim/files/Program.pdf")
    
QtCore.QObject.connect(main.pbShraniUporabnika,QtCore.SIGNAL("clicked()"), shraniUporabnika)
QtCore.QObject.connect(main.pbDodajUporabnika,QtCore.SIGNAL("clicked()"), addUporabnik)
#QtCore.QObject.connect(main.nov,QtCore.SIGNAL("clicked()"), novUporabnik)
QtCore.QObject.connect(main.pbPrikaziPodrobnosti,QtCore.SIGNAL("clicked()"), pokaziPodrobnosti)
QtCore.QObject.connect(main.uporLeIskanje, QtCore.SIGNAL("textChanged(const QString &)"), iskanjeUporabnika)
QtCore.QObject.connect(main.pbVnosKn,QtCore.SIGNAL("clicked()"), vnos_naprave)
QtCore.QObject.connect(main.pbNarocanjeStrank, QtCore.SIGNAL("clicked()"),narocanjeStrank)

main.uporTwRezultati.setColumnCount(4)
main.uporTwRezultati.setColumnHidden(0,False)


#main.uporTwRezultati.keyPressEvent= test
main.uporTwRezultati.setSortingEnabled(True)
naslov=('Šifra', 'Naziv', 'Naslov','Pošta')
main.uporTwRezultati.setHorizontalHeaderLabels(naslov)

main.twIzdaneFakture.setColumnCount(5)
main.twIzdaneFakture.setColumnHidden(0,False)

main.twIzdaneFakture.setSortingEnabled(True)
naslov1=('Št.računa', 'Datum st.', 'Znesek neto' ,'Plačilo','Izvajalec')
main.twIzdaneFakture.setHorizontalHeaderLabels(naslov1)

main.pushButton_14.hide()
main.pbShraniUporabnika.hide()
main.uporPbIzbrisi.hide()

main.pbPrikaziPodrobnosti.setIcon(QtGui.QIcon('design/icons/User-Files-icon.png'))
main.uporPbIzbrisi.setIcon(QtGui.QIcon('design/icons/delete.png'))
main.pbShraniUporabnika.setIcon(QtGui.QIcon('design/icons/document_save.png'))
main.pushButton_14.setIcon(QtGui.QIcon('design/icons/preklic.png'))
main.pbDodajUporabnika.setIcon(QtGui.QIcon('design/icons/novo.png'))
main.toolBox.setCurrentIndex(3)

QtCore.QObject.connect(vstopno.pb_vstopi, QtCore.SIGNAL("clicked()"), vstop)
QtCore.QObject.connect(vstopno.pb_o_programu, QtCore.SIGNAL("clicked()"), oProgramu)
#vstopno.show()

main.show()
app.exec_()


