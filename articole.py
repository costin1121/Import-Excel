import pandas as p
import os
from os import path
import time
import database
import sys
import datetime
import furnizori

class Articole():
    def setdbObject(self,dbObject):
        self._dbObject = dbObject
        
    def getdbObject(self):
        return self._dbObject


    def returnCoteTVA(self,db):
        sql = "SELECT TVA FROM TVA T"
        db.execute(sql)
        result = db.fetchAll()
        #intorc resultatul si o sa scot din for toate valorile.Valorile oricum imi vin in ordine
        return result

    def existaUMSale(self,um,db):
        params = [um]
        sql ="SELECT IDUM FROM UM WHERE UPPER(UM) = UPPER(?)"
        db.execute(sql,params)
        result = db.fetchOne()
        if result is None:
            return False
        else:
            return True


    def getArtnrArticolCat(self,cod,db):
        params = [cod]
        sql = "SELECT ARTNR FROM CODURI WHERE COD = ? AND NUMECOD = PLU"
        db.execute(sql,params)
        result = db.fetchOne()[0]
        if result is None:
            return -1
        else:
            return result

    def returnLastArtnrCatalog(self,db):
        sql = "SELECT FIRST 1 ARTNR FROM CATALOG ORDER BY ARTNR DESC"
        db.execute(sql)
        result = db.fetchOne()[0]
        if result is None:
            return -1
        else:
            return result

    def existaCod(self,codWithCRC,db):
        params = [codWithCRC]
        sql = "SELECT CODWITHCRC FROM CODURI WHERE CODWITHCRC = ?"
        db.execute(sql,params)
        result = db.fetchOne()[0]
        if result is None:
            return False
        else:
            return True





