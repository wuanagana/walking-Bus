import copy
import sys
import os.path
from itertools import izip
from math import sqrt


def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)

def readDatFile(filename):
    nNodes = 0
    alpha = 0
    coordX = []
    coordY = []
    costs = []
    danger = []
    readX = False
    readY = False
    readD = False
    f = open(filename, 'r')
    for line in f:
        line = line.strip()
        s = line.split()
        if len(s)>1 and s[0] == "param" and s[1] == "n":
            readX = False
            readY = False
            readD = False
            nNodes = int(s[-1])
            coordX = [0] * (nNodes + 1)
            coordY = [0] * (nNodes + 1)
            costs = [costs[:] for costs in [[0] * (nNodes + 1)] * (nNodes + 1)]
        elif len(s)>1 and s[0] == "param" and s[1] == "alpha":
            readX = False
            readY = False
            readD = False
            alpha = float(s[-1])
        elif len(s)>1 and s[0] == "param" and s[1] == "coordX":
            readX = True
            readY = False
            readD = False
        elif len(s)>1 and s[0] == "param" and s[1] == "coordY":
            readX = False
            readY = True
            readD = False
        elif len(s) > 1 and s[0] == "param" and s[1] == "d":
            readX = False
            readY = False
            readD = True
        elif (len(s)>0 and s[0] == ";") or len(s) <= 0:
            readX = False
            readY = False
            readD = False
        else:
            if readX:
                for i, j in pairwise(s):
                    coordX[int(i)] = int(j)
            elif readY:
                for i, j in pairwise(s):
                    coordY[int(i)] = int(j)
            elif readD:
                if s[-1] != ':=':
                    row = []
                    for col in s[1:]:
                        row.append(float(col))
                    danger.append(row)
    f.close()
    for i in range(0, (nNodes + 1)):
        for j in range(0, (nNodes + 1)):
            costs[i][j] = float("{0:.4f}".format(sqrt((coordX[i]-coordX[j])**2 + (coordY[i]-coordY[j])**2)))
    return nNodes, alpha, costs, coordX, coordY, danger

##funzione che ritorna il minore della riga

def minoreRiga(rigaCorrente,appoggio,numberOfNodes):
    minore = 10000000000
    costo_minore = 0
    for j in range (0,numberOfNodes+1):
        if appoggio[rigaCorrente][j] < minore:
            minore=appoggio[rigaCorrente][j]
            index_min = j
            costo_minore = appoggio[rigaCorrente][j]
    appoggio[rigaCorrente][index_min]=1000000000
    
    return costo_minore,index_min,appoggio

##funzione che controlla se il nodo puo' essere inserito nella soluzione per la sua distanza

def inserimentoDefinitivo(distanza,nodo,adulti,n_strade,distalpha):
    flag=0

    if (adulti[n_strade]+distanza<=distalpha[nodo]):
        adulti[n_strade]=adulti[n_strade]+distanza
        flag=1
      
    return flag,adulti

def main():
    numberOfNodes = 0
    alpha = 0
    distalpha = []
    costs = []
    appoggio = []
    coordX = []
    coordY = []
    danger = []
    adulti = []
    percorsi = []
    nodi_visitati = []
    n_strade = 0
    riga = 0
    
    costoMinore = 0
    indiceMinimo = 0
    contatore = 0
    

    for arg in sys.argv[1:]:
        filename, file_extension = os.path.splitext(arg)
        basename = os.path.basename(filename)
        if (os.path.isfile(arg) and file_extension == ".dat"):
            numberOfNodes, alpha, costs, coordX, coordY, danger = readDatFile(arg)
    
##creo delle strutture di appoggio per non modificare l'originale che mi servira' per controllare il rischio

    appoggio = copy.deepcopy(costs)
    appoggio_costs = copy.deepcopy(costs)
   
    for i in range (0, numberOfNodes + 1):
        distalpha.append(costs[0][i]*alpha)
    
    for i in range (0,numberOfNodes+1):
        adulti.append(0)
        
    for i in range (0,numberOfNodes+1):
        for j in range(0,numberOfNodes+1):
            if(appoggio[i][j]==0):
                appoggio[i][j]=1000000000
                
    
    for i in range(0,numberOfNodes+1):
            appoggio[i][0]=1000000000
    
    contatore=0
    nodi_visitati.append(0)
    percorsi.append(0)
    cont_percorsi=0
   
    #for i in range(0,numberOfNodes+1):
     #   print appoggio[i]
##controllo la tabella di tutte le distanze partendo dal nodo piu' vicino all'origine 0
##se va bene per la distanza*alpha allora lo inserisco nella lista delle soluzioni
##se finisco una riga vuol dire che per quel percorso non ci sono piu' possibili collegamenti quindi inizio un nuovo percorso
    

    while 1:
        #print "Hey sono qua e non riesco ad uscire"
        [costoMinore,indiceMinimo,appoggio] = minoreRiga(riga,appoggio,numberOfNodes)
        [flag,adulti] = inserimentoDefinitivo(costoMinore,indiceMinimo,adulti,n_strade,distalpha)
        if(flag == 1):
            riga=indiceMinimo
            appoggio[indiceMinimo][riga]=1000000000
            nodi_visitati.append(indiceMinimo)
            percorsi.append(indiceMinimo)
            for i in range (0,numberOfNodes+1):
                appoggio[i][indiceMinimo]=1000000000
            
        else:
            contatore=0
            for i in range(0, numberOfNodes+1):
                if(appoggio[riga][i]==1000000000):
                    contatore=contatore+1
            if(contatore==numberOfNodes+1):
                riga=0
                n_strade=n_strade+1
                cont_percorsi=cont_percorsi+1
                percorsi.append(0)
        
        
        ##
        #for i in range(0,numberOfNodes+1):
         #   print appoggio[i]
        #print     
        

        if(len(nodi_visitati)==numberOfNodes+1):
            break
            
    final_array = []

##scompongo il risultato per inserire nelle soluzioni gli zero perche' nelle soluzioni
##mancava il nodo radice
   
    zeroes_positions = [i for i,x in enumerate(percorsi) if x == 0]  
    i = 0   
    for index in zeroes_positions:
        if(i != len(zeroes_positions)-1):
            link = percorsi[index:zeroes_positions[i+1]]
            i=i+1
        else:
            link = percorsi[index:]
        final_array.append(link)
            
    cont_percorsi=cont_percorsi+1
    
##calcolo la lunghezza massima della lista delle soluzioni

    massimo = 0
    for i in range (0,len(final_array)):
        if (massimo < len(final_array[i])):
            massimo = len(final_array[i])
    
##finche non riusciamo a creare una matrice dinamica ovvero una lista di liste accedibili

    pericolo = [pericolo[:] for pericolo in [[0] * (massimo)] * (cont_percorsi)]
    somme_pesate = [somme_pesate[:] for somme_pesate in [[0] * (massimo)] * (cont_percorsi)]
    rischi_pesati = [rischi_pesati[:] for rischi_pesati in [[0] * (massimo)] * (cont_percorsi)]
    
    somma = 0
    somma_rischi = 0
    appoggio_danger = []
    appoggio_danger= copy.deepcopy(danger)    

##calcolo tutte le distanze pesate e i rischi pesati per tenerli come confronto
##per esempio seconda soluzione 3 nodo avro la distanza dei primi 3 nodi e il rischio dei primi 3 nodi

    for i in range (0,len(final_array)):
        for j in range (0, len(final_array[i])-1):
            if(len(final_array[i])==2):
                somme_pesate[i][j]=appoggio_costs[0][final_array[i][j]]
                rischi_pesati[i][j]=appoggio_danger[final_array[i][j]][0]
            
            else:
                somme_pesate[i][j]=somma+appoggio_costs[final_array[i][j+1]][final_array[i][j]]
                rischi_pesati[i][j]=somma_rischi+appoggio_danger[final_array[i][j+1]][final_array[i][j]]
                somma = somma + appoggio_costs[final_array[i][j+1]][final_array[i][j]]
                somma_rischi = somma_rischi+ appoggio_danger[final_array[i][j+1]][final_array[i][j]]
    
##
    
    for i in range (0,len(final_array)):
        for j in range (0, len(final_array[i])-1):
            pericolo[i][j]=danger[final_array[i][j+1]][final_array[i][j]]
    
##inizializzo i pericoli perche' quelli con pericolo 0 mi creano problemi 
            
    for i in range (0,numberOfNodes+1):
        for j in range(0,numberOfNodes+1):
            if(appoggio_danger[i][j]==0):
                appoggio_danger[i][j]=1000000000
    
    
    for i in range (0,cont_percorsi):
        for j in range(0,massimo):
            if(pericolo[i][j]==0):
                pericolo[i][j]=1000000000   
   
    maximo=0
    indice_maximo=0
    #massimo del primo nodo
    appoggio_final_array = []
    appoggio_final_array = copy.deepcopy(final_array)    
    minimum=0
    rigaTaglio = 0
    colonnaTaglio = 0 
    tagliMinimi = []
    contTagliMinimi=0
    sommaSingola = 0
    contatoreSomma = 0
    flagDistanza = 0

##guardo se un primo nodo puo' essere attaccato ad un qualsiasi altro nodo
    
    for andrea in range (0,cont_percorsi):
        for m in range (cont_percorsi):
            if(maximo<pericolo[m][0]):
                maximo=pericolo[m][0]
                indice_maximo=m
        ##il final_array[indice_maximo][1] dove posso attaccarlo?"
        for i in range(1,numberOfNodes+1):
            
            ##final_array[indice_maximo][1],"posso attaccarlo al nodo",i,"?" 
            for j in range (0,cont_percorsi):
                
                ##print "Sto anallizando il percorso",j
                for k in range (0,len(final_array[j])):
                    
                    ## "l'elemento",final_array[j][k],"puo andare bene?"
                    if(i not in final_array[indice_maximo]):
                        #print final_array[j][k]
                        if(i==final_array[j][k]):
                            ## final_array[indice_maximo][indice_maximo+1],"posso attaccarlo al nodo",i,"perche non e del mio percorso"
                            ## "Ho trovato il nodo",i,"nei percrosi ammissibili"
                            rigaTaglio=j
                            colonnaTaglio=k

                            ##controlliamo la distanza tra",final_array[indice_maximo][1],"e",i,"ed e",costs[final_array[indice_maximo][1]][i]+somme_pesate[rigaTaglio][colonnaTaglio-1],"<",distalpha[final_array[indice_maximo][1]],"??"
                            if(costs[final_array[indice_maximo][1]][i]+somme_pesate[rigaTaglio][colonnaTaglio-1]<distalpha[final_array[indice_maximo][1]]):    
                                
                                #print "la distanza tra",i,"e 0 +",i,"e",final_array[indice_maximo][1],"e uguale a",costs[i][0]+costs[final_array[indice_maximo][1]][i]
                                ##print "######",final_array[rigaTaglio]
                                ##print "######",final_array[indice_maximo]
                                sommaSingola=0
                                for z in range(0,len(final_array[rigaTaglio])):
                                    if(final_array[rigaTaglio][z]==final_array[rigaTaglio][colonnaTaglio]):
                                        break
                                    ##print final_array[rigaTaglio][z],"e",final_array[rigaTaglio][z+1]
                                    sommaSingola=sommaSingola+costs[final_array[rigaTaglio][z]][final_array[rigaTaglio][z+1]]
                                    ##print sommaSingola
                                
                                
                                sommaSingola=sommaSingola+costs[final_array[indice_maximo][1]][final_array[rigaTaglio][colonnaTaglio]]

                                flagDistanza=0
                                
                                ##controllo se ogni nodo della soluzione del primo nodo che sto tentando di attaccare da qualche parte rispetta la condizione della distanza
                                for a in range(2,len(final_array[indice_maximo])+1):
                                    if(sommaSingola>=costs[final_array[indice_maximo][a-1]][0]*alpha):
                                        ##print "Qualcosa che non va"
                                        flagDistanza=1
                                        
                                    if(a<len(final_array[indice_maximo])):
                                        sommaSingola=sommaSingola+costs[final_array[indice_maximo][a-1]][final_array[indice_maximo][a]]

                                 
                                ##"controlliamo il pericolo",appoggio_danger[final_array[indice_maximo][1]][i],"<",appoggio_danger[final_array[indice_maximo][1]][0]
                                if(appoggio_danger[final_array[indice_maximo][1]][i] < appoggio_danger[final_array[indice_maximo][1]][0] and flagDistanza==0):
        
                                ##se passo tutti i controlli creo una lista con un possibile taglio e il suo parametro di pericolosita'    
                                    tagliMinimi.append(final_array[indice_maximo][1])
                                    tagliMinimi.append(i)
                                    tagliMinimi.append(appoggio_danger[final_array[indice_maximo][1]][0]-appoggio_danger[final_array[indice_maximo][1]][i])
        
        maximo=0
        pericolo[indice_maximo][0]=0
        

    taglioMassimo = 0
    indiceMassimo = 0
    divieto = []
    count = 0
    aggiungiDivieto = 0 
 
 ##controllo nella lista dei tagli partendo dal taglio con paremtro di pericolosita' piu' basso ovvero il miglior risparmio di pericolosita'
 ##se applico il taglio devo assicurarmi che nessun nodo del percorso attaccato sia coinvolto in un possibile taglio
 ##perche vuol dire che il piedibus dopo che si unisce si divide e non e' possibile
    
    flag = 0
    if(len(tagliMinimi)!=0):
        while 1:
            for i in range (2,len(tagliMinimi),3):
                if(tagliMinimi[i]>taglioMassimo):
                    taglioMassimo=tagliMinimi[i]
                    indiceMassimo=i
            if(len(divieto)!=0):
            ##print "nuovo giro"
                for a in range(0,aggiungiDivieto):
                    for b in range(0,len(divieto[a])):
                     if (divieto[a][b]==tagliMinimi[indiceMassimo-1]):
                        ##print "ho violato la legge"
                        flag=1
        ##print tagliMinimi[indiceMassimo-1]
            if (tagliMinimi[indiceMassimo-1] in divieto == false):
             #print"sono nel divieto"
                flag=1
        #print indiceMassimo
            count=count+1
        ##print "il contatore", count
            for j in range (0,cont_percorsi):
              for k in range (0,len(final_array[j])):
                #print tagliMinimi[indiceMassimo-2]
                #print tagliMinimi[indiceMassimo-1]
                #print "divieto corrente",divieto
                #print tagliMinimi[indiceMassimo-1],"e presente in divieto",tagliMinimi[indiceMassimo-1] in divieto,"volte"
                    if(final_array[j][k]==tagliMinimi[indiceMassimo-2] and flag==0):
                    
                    #print tagliMinimi[indiceMassimo-1]
                        appoggio_final_array[j][0]=tagliMinimi[indiceMassimo-1]
                        flag=0
                        for l in range (0,cont_percorsi):
                            for m in range (0,len(final_array[l])):
                                if(final_array[l][m]==tagliMinimi[indiceMassimo-1]):
                                ##print "elemento della nuova lista",appoggio_final_array[l][m]
                                ##print "nuovo divieto",appoggio_final_array[l]
                                    divieto.append(final_array[l])
                                    aggiungiDivieto=aggiungiDivieto+1
                                    break
                        ##print "modifica effettuata",appoggio_final_array[j]

                        tagliMinimi[indiceMassimo]=0
                        taglioMassimo=0
                    
            
            
        
            if(count==(len(tagliMinimi)/3)):
                break
            
            
    
    #Scrivo sui file il risultato
    nomeFile = os.path.basename(os.path.splitext(sys.argv[1])[0])+".sol"
    print nomeFile

    out_file = open(nomeFile,"w")
    for i in range (0,cont_percorsi):
        
        for j in range (len(final_array[i])-1,0,-1):
            out_file.write(str(appoggio_final_array[i][j])+" "+str(appoggio_final_array[i][j-1])+"\n")
    out_file.close()    
    
    
        
        
if __name__ == "__main__":
    main()
