import database
import registry
import furnizori
import subclase
import articole

#citesc baza de date din registry
databaseName = registry.get_reg('database')
isNewDB = False
isDatabaseConnected = False
#intreb utilizatorul daca vrea sa foloseasca aceasi baza in cazul in care are o baza setata in cazul in care nu trebuie sa il pun sa isi seteze
if (databaseName == None):
    if (databaseName == None) or (isNewDB == True):
        databaseName = input("Introduceti calea bazei de date \n")
        if registry.set_reg('database',databaseName):
            print('Baza de date a fost salavata cu succes')
        else:
            print('Nu a putut sa fie citita baza de date')

        real_database = databaseName
    else:
        real_database = databaseName
else:
    isUserdatabase = True
    while isUserdatabase:
        userDatabase = input("Sunteti conectat la baza de date: "+ databaseName + " Doriti modificarea ei?Da/Nu \n")
        if (userDatabase == "Da") or (userDatabase == "DA") or (userDatabase == "da") or (userDatabase=="dA"):
            isNewDB = True 
            if (databaseName == None) or (isNewDB == True):
                databaseName = input("Introduceti calea bazei de date \n")
                if registry.set_reg('database',databaseName):
                    print('Baza de date a fost salavata cu succes')
                    isUserdatabase = False
                else:
                    print('Nu a putut sa fie citita baza de date')

                real_database = databaseName       
        elif(userDatabase == "Nu") or (userDatabase == "NU") or (userDatabase == "nu") or (userDatabase=="nU"):
                real_database = databaseName
                isUserdatabase = False
        else:
            print("Nu ati raspuns corect. Va rugam selectati da sau nu ")
        
        
# ma conectez la baza de date
try:    
    dbObject = database.Database(real_database)
    print("Conexiunea cu baza de date " + real_database + " a fost stabilita cu succes")
    isDatabaseConnected = True
except:
    #print("Nu a fost stabilita conexiunea cu baza de date")
    raise Exception("Nu a fost stabilita conexiunea cu baza de date")

#incepem importul     

isContinueImport = True
while isContinueImport:
    importChoice = input("Ce doriti sa importati? f - Furnizori, s - Subclase, c - Catalog, ca - Catalog Alternativ, e - exit \n")
    if (importChoice == "e" or importChoice == "E"):
        isContinueImport = False
    elif(importChoice == "f" or importChoice == "F"):
        #aici merge codul pentru furnizori
        isNewPathFurnizori = False
        furnizoriReg = registry.get_reg('furnizori')
        if furnizoriReg == None:
            #merge aici in cazul in care nu am selectat un folder
            furnizoriReg = input("Introduceti folderul unde se afla fisierul \n")
            if registry.set_reg("furnizori",furnizoriReg):
                print("Calea pentru importul furnizorilor a fost setata in " + furnizoriReg)
            else:
                isContinueImport = False
                print("Nu a putut fi setata calea fisierului")
                    
        else:
            isImportSetatFurnizori = True
            while isImportSetatFurnizori:
                userFurnizori = input("Calea fisierului este setata la " + furnizoriReg + " Doriti modificarea? Da/Nu \n")
                if(userFurnizori == "Da" or userFurnizori == "DA" or userFurnizori == "dA" or userFurnizori == "da"):
                    isNewPathFurnizori = True 
                    if(furnizoriReg == None) or (isNewPathFurnizori == True):
                        furnizoriReg = input("Introduceti folderul unde se afla fisierul \n")
                        if registry.set_reg('furnizori',furnizoriReg):
                            print("Calea pentru importul furnizorilor a fost setata in " + furnizoriReg)
                            isImportSetatFurnizori = False
                        else:
                            print("Nu a putut fi setata calea fisierului")
                   
                elif(userFurnizori == "Nu") or (userFurnizori == "NU") or (userFurnizori == "nu") or (userFurnizori=="nU"):
                    isImportSetatFurnizori = False
                else:
                    print("Nu ati raspuns corect. Va rog selectati da sau nu")
                    
                #functie de import furnizori 
                furnizoriObject = furnizori.Furnizori()
                furnizoriObject.setdbObject(dbObject)
                furnizoriObject.getFurnizoriFromXLS(furnizoriReg,real_database)   
    
    elif(importChoice == "s" or importChoice == "S"):
        #prima data verific daca am ceva clase sa fac importul
        subclaseObject = subclase.SubClase()
        subclaseObject.setdbObject(dbObject)
        isNotNullClase = subclaseObject.existaClase(dbObject)
        if isNotNullClase:
            #aici merge codul pentru subclase. Se executa codul doar daca exista clase 
            isChoiceIncorect = True
            while isChoiceIncorect:
                #import choice trebuie pasat in functie
                importChoiceSubclase = subclaseObject.getAvailableClase(dbObject)
                listaSubclaseIndex = str(subclaseObject.getIdClasaAvailable(dbObject))
                    
                if importChoiceSubclase in listaSubclaseIndex:
                    isChoiceIncorect = False
                    isNewPathSubclase = False
                    subclaseReg = registry.get_reg('subclase')
                    if subclaseReg == None:
                        #merge aici in cazul in care nu am selectat un folder
                        subclaseReg = input("Introduceti folderul unde se afla fisierul \n")
                        if registry.set_reg("subclase",subclaseReg):
                            print("Calea pentru importul subclaselor a fost setata in " + subclaseReg)
                        else:
                            isContinueImport = False
                            print("Nu a putut fi setata calea fisierului")
                    else:
                        isImportSetatSubclase = True
                        while isImportSetatSubclase:
                            userSubclase = input("Calea fisierului este setata la " + subclaseReg + " Doriti modificarea? Da/Nu \n") 
                            if(userSubclase == "Da" or userSubclase == "DA" or userSubclase == "dA" or userSubclase == "da"):
                                isNewPathSubclase = True 
                                if(subclaseReg == None) or (isNewPathSubclase == True):
                                    subclaseReg = input("Introduceti folderul unde se afla fisierul \n")
                                    if registry.set_reg('subclase',subclaseReg):
                                        print("Calea pentru importul subclaselor a fost setata in " + subclaseReg)
                                        isImportSetatFurnizori = False
                                    else:
                                        print("Nu a putut fi setata calea fisierului")
                            
                            elif(userSubclase == "Nu") or (userSubclase == "NU") or (userSubclase == "nu") or (userSubclase=="nU"):
                                isImportSetatSubclase = False
                            else:
                                print("Nu ati raspuns corect. Va rog selectati da sau nu") 

                            #functia pentru inserarea subclaselor merge aici 
                            subclaseObject.setIdS(importChoiceSubclase) 
                            subclaseObject.getSubclaseFromXLS(subclaseReg,real_database)                        

                else:
                    print("Nu ati raspuns corect. Va rog sa selectati o valoare valida")
        else:
            print("Nu exista nici o clasa unde se poate face importul")
    
    
    elif(importChoice == "c" or importChoice == "C"):
        #aici merge codul pentru furnizori
        isNewPathArticole = False
        articoleReg = registry.get_reg('articole')
        if articoleReg == None:
            #merge aici in cazul in care nu am selectat un folder
            articoleReg = input("Introduceti folderul unde se afla fisierul \n")
            if registry.set_reg("articole",articoleReg):
                print("Calea pentru importul articolelor a fost setata in " + articoleReg)
            else:
                isContinueImport = False
                print("Nu a putut fi setata calea fisierului")
                    
        else:
            isImportSetatArticole = True
            while isImportSetatArticole:
                userArticole = input("Calea fisierului este setata la " + articoleReg + " Doriti modificarea? Da/Nu \n")
                if(userArticole == "Da" or userArticole == "DA" or userArticole == "dA" or userArticole == "da"):
                    isNewPathArticole = True 
                    if(articoleReg == None) or (isNewPathArticole == True):
                        articoleReg = input("Introduceti folderul unde se afla fisierul \n")
                        if registry.set_reg('articole',articoleReg):
                            print("Calea pentru importul articolelor a fost setata in " + articoleReg)
                            isImportSetatArticole = False
                        else:
                            print("Nu a putut fi setata calea fisierului")
                   
                elif(userArticole == "Nu") or (userArticole == "NU") or (userArticole == "nu") or (userArticole=="nU"):
                    isImportSetatArticole = False
                else:
                    print("Nu ati raspuns corect. Va rog selectati da sau nu")
                    
                #functie de import articole vine aici
                print("Test articole")   
    else:
        print("Optiunea selectata nu exista!")

if isDatabaseConnected:
    dbObject.CloseCursor()
    dbObject.CloseConnection()    
    

