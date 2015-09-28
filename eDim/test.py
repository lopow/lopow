import psycopg2


conn = psycopg2.connect(host="10.112.0.5", port ="5432", dbname="eDimnikar", user="postgres", password="root")
cur = conn.cursor()

sql= """
         SELECT max(id) FROM "eDimnikar".uporabnik limit 10;
     """

cur.execute(sql)

rows = cur.fetchone()
lastUser = rows[0]


print(lastUser)





    query_podrobnosti = """
        SELECT "eDimnikar".uporabnik.id,
                "eDimnikar".uporabnik.naziv_1,
                "eDimnikar".uporabnik.naziv_2,
                "eDimnikar".uporabnik.naslov,
                "eDimnikar".uporabnik.posta_st_fk,
                "eDimnikar".postne_stevilke.naziv_poste,
                "eDimnikar".uporabnik.naselje,
                "eDimnikar".uporabnik.tip_uporabnika_fk,
                "eDimnikar".upr_tip.naziv,
                "eDimnikar".upr_sm.sifra,
                "eDimnikar".upr_sm.naziv,
                "eDimnikar".uporabnik.aktivnost,
                "eDimnikar".uporabnik.davcni_zavezanec,
                "eDimnikar".uporabnik.id_za_ddv,
                "eDimnikar".uporabnik.trr,
                "eDimnikar".uporabnik.kontakt
        FROM
                "eDimnikar".uporabnik,
                "eDimnikar".upr_tip,
                "eDimnikar".upr_sm,
                "eDimnikar".postne_stevilke
        WHERE
                "eDimnikar".uporabnik.id = {}
        AND
                "eDimnikar".uporabnik.tip_uporabnika_fk = "eDimnikar".upr_tip.id
        AND
                "eDimnikar".uporabnik.sm_id_fk = "eDimnikar".upr_sm.id
        AND
                "eDimnikar".postne_stevilke.sifra_poste = "eDimnikar".uporabnik.posta_st_fk
       """.format(cell)

    cursor.execute(query_podrobnosti)
    row = cursor.fetchall()

    print (row)
    tip= (str(row[0][7]) +' ... '+ (row[0][8]))
    
    posta= (str(row[0][4])) +'  '+ (row[0][5])
    main.uporLeSifra.setText(str(row[0][0]))
    main.uporLeNaziv.setText((row[0][1]))
    main.uporLeNaziv2.setText(row[0][2])
    main.uporLeNaslov.setText(row[0][3])
    main.uporCbPosta.setCurrentIndex(row[0][4])
    main.uporLePosta.setText(posta)
    main.uporLeNaselje.setText(row[0][6])
    main.uporCbTip.addItems(str(tip))

    main.uporLeTip.setText((str(row[0][7]) +' ... '+ (row[0][8])))
    main.uporLeSm.setText((str(row[0][9]) +' ... '+ (row[0][10])))
    vnos_kn.leUporabnik.setText(str(row[0][0])+ '  '+(str(row[0][1])))

    if row[0][11]:
        main.uporCbAktivnost.setCheckState(True)
    else:
        main.uporCbAktivnost.setCheckState(False)
    if row[0][12]:
        main.uporCbDavcni.setCheckState(True)
    else:
        main.uporCbDavcni.setCheckState(False)
    main.uporLeDdv.setText(row[0][13])
    main.uporLeTrr.setText(row[0][14])
    main.uporLeKontankt.setText(row[0][15])

    return row,cell













#
#conn = psycopg2.connect(host="10.112.0.5", port ="5432", dbname="eDimnikar", user="postgres", password="root")
#cur = conn.cursor()
#sql= """
#         SELECT * FROM "eDimnikar".kn_lokacije;
#     """

#cur.execute(sql)

#rows = cur.fetchall()
#for row in rows:
#    print (row[0], row[1])
    
#id_uporabnika = 1
#kn_lokacije = "Kurilnica"
#kn_vrste_namenov = "Ogrevanje"
#kn_vrste_goriv = "Lahko kurilno olje - ELKO"
#kn_vrste_zalaganja = ""
#kn_materiali_dimnikov = "Šamotni / keramični"
#kn_znamka = "Buderus"
#letnik = 2000
#moc = 28
#opombe = "Prva vnesena kurilna naprava" 


#lokacija_sql = """SELECT id FROM "eDimnikar".kn_lokacije
#        WHERE lokacija='{}';
#        """.format(kn_lokacije)
        
#namen_sql = """SELECT id FROM "eDimnikar".kn_vrste_namenov
#            WHERE naziv='{}';
#        """.format(kn_vrste_namenov)

#3vrste_goriv_sql = """SELECT id FROM "eDimnikar".kn_vrste_goriv
 #       WHERE naziv='{}';
 #       """.format(kn_vrste_goriv)
    
#materiali_dimnikov_sql = """SELECT id FROM "eDimnikar".kn_materiali_dimnikov
#        WHERE naziv='{}';
#        """.format(kn_materiali_dimnikov)

#znamka_sql = """SELECT id FROM "eDimnikar".kn_znamka
#        WHERE naziv='{}';
 #       """.format(kn_znamka)


#cur.execute(lokacija_sql)
#rows = cur.fetchall()
#kn_lokacije_fk = (rows[0][0])

#cur.execute(namen_sql)
#rows = cur.fetchall()
#kn_vrste_namenov_fk = (rows[0][0])

#cur.execute(vrste_goriv_sql)
#rows = cur.fetchall()
#print (rows)
#kn_vrste_goriv_fk = (rows[0][0])

#cur.execute(materiali_dimnikov_sql)
#rows = cur.fetchall()
#kn_materiali_dimnikov_fk = (rows[0][0])

#cur.execute(znamka_sql)
#rows = cur.fetchall()
#kn_znamka_fk = (rows[0][0])

#insert_kn = """
#                INSERT INTO "eDimnikar".kn_upor    (
#                    id_uporabnika_fk, 
#                    kn_lokacije_fk, 
#                    kn_vrste_namenov_fk, 
#                    kn_vrste_goriv_fk, 
#                    kn_materiali_dimnikov_fk, 
#                    letnik, 
#                    kn_znamka_fk,
#                    moc, 
#                    opombe )
#                VALUES ({},{},{},{},{},{},{},{},'{}');
#                
#""".format(id_uporabnika, kn_lokacije_fk, kn_vrste_namenov_fk, kn_vrste_goriv_fk, kn_materiali_dimnikov_fk, letnik, kn_znamka_fk, moc, opombe)
#cur.execute(insert_kn)
##conn.commit()#

#uporabnik_kn_query = """SELECT naziv_1 FROM  "eDimnikar".uporabnik,"eDimnikar"., ;
#       
#       
#                       """

