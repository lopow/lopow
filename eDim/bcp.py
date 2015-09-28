        queryPrikazi = """
        SELECT    *
        FROM 
            "eDimnikar".uporabnik
            LEFT  JOIN     
                (
                SELECT
                    "eDimnikar".fakture_vasco.sifra_kupca, 
                    "eDimnikar".fakture_vasco.znesek,
                    "eDimnikar".fakture_vasco.izvajalec,
                    "eDimnikar".zaposleni.priimek_ime,
                    first_value ("eDimnikar".fakture_vasco.datum_storitve)
                OVER 
                (
                    PARTITION BY sifra_kupca, datum_storitve
                    ORDER BY datum_storitve
                    DESC
                )datum_storitve
                
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
            "eDimnikar".uporabnik.rpe_naselje ILIKE '%{}%'
        AND 
            "eDimnikar".uporabnik.rpe_ulica ILIKE '%{}%'

            ORDER BY "eDimnikar".uporabnik.naslov
                    ASC   ;""".format(obcina,naselje, ulica)
        
        cursor.execute(queryPrikazi)
                      