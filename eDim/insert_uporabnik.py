#coding='UTF-8'
import psycopg2
#conn = psycopg2.connect(host="10.112.0.5", port ="5432", dbname="eDimnikar", user="postgres", password="root")
conn = psycopg2.connect(host="localhost", port ="5432", dbname="eDimnikar", user="postgres", password="drejko99")
cur = conn.cursor()

sql= """
         SELECT max(id) FROM "eDimnikar".uporabnik;
     """
cur.execute(sql)
rows = cur.fetchone()
lastUser = rows[0]

id_1 = str(lastUser)
naziv_1 = "Andrej Ficko"
naziv_2 = "Ficko Andrej"
naslov = "Gornji Crnci 13"
posta = "9261"
naselje = "Gornji Crnci"
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
            
            
#cur.execute(sql_insert)
conn.commit()            
            
            
    