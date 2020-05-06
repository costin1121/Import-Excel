import pandas as p
import os
from os import path
import time
import database
import sys
import datetime
class Furnizori():

    def setdbObject(self,dbObject):
        self._dbObject = dbObject
        
    def getdbObject(self):
        return self._dbObject
        
    
    def existaFurnizor(self,db,codFurnizor):
        params = [codFurnizor]
        sql = "SELECT IDFURN FROM FURNIZORI WHERE WEB = UPPER(?)"
        db.execute(sql,params)
        
        row = db.fetchOne()
        if row is None:
            return False
        else:
            return True
    
    def getFurnizoriFromXLS(self,pathName,real_database):
        #functia merge aici
        if path.exists(pathName):
            objectDb = self.getdbObject()    
            lstErrori=[]
            erorCode = 0
            data = p.read_excel(pathName)
            start_time = time.time()
            index = 1 # PENTRU CA 1 ESTE HEADERUL
            for row in data.itertuples():
                codFurnizor = str(row[1])
                denumire    = str(row[2]).upper()
                codFiscal   = str(row[3])
                nrRc        = str(row[4])
                localitate  = str(row[5])
                adresa      = str(row[6])
                observatii  = str(row[7])
                if row[8] == p.notna:
                    zileScadenta = float(row[8])
                else:
                    zileScadenta = 0
                   
                
                telefon = str(row[9])
                fax     = str(row[10])
                mobil   = str(row[11])
                email   = str(row[12])
                iln     = str(row[13])
                cont    = str(row[14])
                banca   = str(row[15])
                if row[16]== p.notna:
                    tvaIncasare = float(row[16])
                else:
                    tvaIncasare = 0
                    
                if row[17] == p.notna:
                    platitorTva = float(row[17])
                else:
                    platitorTva = 0 
                
                
                if row[18] == p.notna:
                    schimbDate = float(row[18])
                else:
                    schimbDate = 0
                    
                if row[19] == p.notna:
                    isTrusted = float(row[19])
                else:
                    isTrusted = 0
                    
                #selectez sa vad daca exista furniozorul inainte sa il inserez
                isFurnizor = self.existaFurnizor(objectDb,codFurnizor)
                try:
                    if not isFurnizor:
                        #codul pentru insert
                        self.InsertIntoFurnizori(objectDb,codFurnizor,denumire,codFiscal,nrRc,localitate,adresa,observatii,zileScadenta,telefon,fax,mobil,email,iln,cont,banca,tvaIncasare,platitorTva,schimbDate,isTrusted)
                        #print("Furnziorul " + codFurnizor + " a fost inserat cu succes!")
                    else:
                        erorCode = -1
                        lstErrori.append("Furnizorul cu codul {0} exista in nomenclatorul de furnizori \n".format(codFurnizor))
                except:
                    erorCode = -1
                    #print("Eroare la linia " + str(index) + " furnizorul cu codul " + codFurnizor + " nu a putut fi inserat in baza de date")
                    lstErrori.append("Eroare la linia {0} furnizorul cu codul {1} nu a putut fi inserat...Eroare Originala: {2} \n".format(str(index),codFurnizor,sys.exc_info()[1]))
                print('Se importa linia : '+ str(index) + '/' + str(len(data)), end='\r')
               
                index +=1
                
            elapsed_time = time.time() - start_time
            print(str(index-1) + " de linii au fost executate in: " + str(elapsed_time))
            if len(lstErrori) > 0:
                username = os.getlogin()
                if not os.path.exists(r"C:\Users\{0}\erori".format(username)):
                    os.mkdir(r"C:\Users\{0}\erori".format(username))
               
                real_time = datetime.datetime.today()
                formatTime = "{0}_{1}_{2}_{3}_{4}_{5}".format(real_time.day,real_time.month,real_time.year,real_time.hour,real_time.minute,real_time.second)
                fileName = "eroriFurnizori_{0}.txt".format(formatTime)
                erorFile = open(r"C:\Users\{0}\erori\{1}".format(username,fileName),"w+")
                for item in lstErrori:
                    erorFile.write(item)
                    erorFile.write("\n")

                erorFile.close()
                if erorCode == -1:
                    print("Una sau mai multe linii contin date invalide si nu au putut fi importate \nVerificati fisierul salvat in calea {0}".format(fileName))    
        else:
            print("Fisierul " + pathName + " nu exista")


    
    def InsertIntoFurnizori(self,objectDb,codFurnizor,denumire,codFiscal,nrRc,localitate,adresa,observatii,zileScadenta,telefon,fax,mobil,email,iln,cont,banca,tvaIncasare,platitorTva,schimbDate,isTrusted):
        #functie de insert
        aIdFurnizor = objectDb.FetchGenerator('FURNIZORI_IDFURN')
        params = [aIdFurnizor,denumire,localitate,telefon,fax,mobil,email,codFurnizor, codFiscal, nrRc,cont,banca,adresa,observatii,0,zileScadenta,tvaIncasare,platitorTva,schimbDate,isTrusted]
        sql = "INSERT INTO FURNIZORI(IDFURN, NUME, ORAS, TELEFON, FAX , MOBIL, EMAIL, WEB, CODFISC, REGCOM, CONT, BANCA, ADRESAM, OBS, INACTIV, ZILEPLATA, ISTVAINCASARE, ISPLATITOR_TVA,TYPEOF_EXCHANGEINFO, ISTRUSTED_SUPPLIER,MODIFICAT,TRIMIS) VALUES(?, ?, ?, ?, ? , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,1,0)"     
        objectDb.execute(sql,params)   
        objectDb.commit() 
            
        

        
        
    
        
    