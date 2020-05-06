import pandas as p
import os
from os import path
import time
import database
import sys
import datetime

class SubClase():

    def setdbObject(self,dbObject):
        self._dbObject = dbObject
        
    def getdbObject(self):
        return self._dbObject

    def setIdS(self,idS):
        self._idS = idS

    def getIdS(self):
        return self._idS


    def existaClasaFIsier(self,db,codClasa):
        idS = self.getIdS()
        params = [codClasa]
        sql = "SELECT COD FROM S{0} WHERE UPPER(COD) = UPPER(?)".format(str(idS))
        db.execute(sql,params)
        row = db.fetchOne()
        if row is None:
            return False
        else:
            return True

    def getAvailableClase(self,db):
        sql = "SELECT IDCOD, DESCRIERE FROM CLASEPRODUSE ORDER BY ORDER_INDEX"
        db.execute(sql)
        result = db.fetchAll()
        listaAfisare = []
        strLista = ""
        for row in result:
            listaAfisare.append("{0} - {1}".format(row[0],row[1]))

        for lst in listaAfisare:
            strLista += lst + "; " 
        importChoice = input("Selectati clasa unde doriti sa importati: {0} \n".format(strLista))
        return importChoice
            
            
    def existaClase(self,db):
        sql = "SELECT DESCRIERE FROM CLASEPRODUSE ORDER BY ORDER_INDEX"
        db.execute(sql)
        result = db.fetchAll()
        if len(result) == 0:
            return False
        else:
            return True

    def getIdClasaAvailable(self,db):
        sql = "SELECT IDCOD FROM CLASEPRODUSE ORDER BY ORDER_INDEX"
        db.execute(sql)
        result = db.fetchAll()
        return result

    def InsertIntoSubclase(self,db,idS,codS,denumire):
        sql = "SELECT FIRST 1 IDS{0} FROM S{1} ORDER BY IDS{2} DESC".format(str(idS),str(idS),str(idS))
        db.execute(sql)
        idRet = db.fetchOne()[0]
        idRet += 1

        params = [idRet,denumire,codS,idS]
        sqlInsert = "INSERT INTO S{0}(IDS{1},DESCR_S{2},COD,ORDER_INDEX) VALUES(?,?,?,?)".format(str(idS),str(idS),str(idS))
        db.execute(sqlInsert,params)
        db.commit()


    def getSubclaseFromXLS(self,pathName,real_database):
        if path.exists(pathName):
            objectDb = self.getdbObject()  
            idS       = self.getIdS()  
            lstErrori=[]
            erorCode = 0
            data = p.read_excel(pathName)
            start_time = time.time()
            index = 1 # PENTRU CA 1 ESTE HEADERUL
            print(data)
            for row in data.itertuples():
                codClasa = str(row[1])
                numeClasa = str(row[2])
                isSubclase = self.existaClasaFIsier(objectDb,codClasa)
                try:
                    if not isSubclase:
                        self.InsertIntoSubclase(objectDb,idS,codClasa,numeClasa)
                    else:
                        erorCode = -1
                        lstErrori.append("Subclasa cu codul {0} exista in nomenclatorul de subclase \n".format(codClasa))
                except:
                    erorCode = -1
                    lstErrori.append("Eroare la linia {0} subclasa cu codul {1} nu a putut fi inserata...Eroare Originala: {2} \n".format(str(index),codClasa,sys.exc_info()[1]))

                print('Se importa linia : '+ str(index) + '/' + str(len(data)), end='\r')

                index += 1
            elapsed_time = time.time() - start_time
            print(str(index-1) + " de linii au fost executate in: " + str(elapsed_time))
            if len(lstErrori) > 0:
                username = os.getlogin()
                if not os.path.exists(r"C:\Users\{0}\erori".format(username)):
                    os.mkdir(r"C:\Users\{0}\erori".format(username))
               
                real_time = datetime.datetime.today()
                formatTime = "{0}_{1}_{2}_{3}_{4}_{5}".format(real_time.day,real_time.month,real_time.year,real_time.hour,real_time.minute,real_time.second)
                fileName = "eroriSubclase_{0}.txt".format(formatTime)
                erorFile = open(r"C:\Users\{0}\erori\{1}".format(username,fileName),"w+")
                for item in lstErrori:
                    erorFile.write(item)
                    erorFile.write("\n")

                erorFile.close()
                if erorCode == -1:
                    print("Una sau mai multe linii contin date invalide si nu au putut fi importate \nVerificati fisierul salvat in calea {0}".format(fileName))
        else:
            print("Fisierul " + pathName + " nu exista")

