import pandas as pd
import os
import xml.etree.ElementTree as ET
import re

repertoireSource=os.getcwd()+'/EXEMPLE4_0/fichiers_source'
repertoirePassage=os.getcwd()+'/EXEMPLE4_0/fichiers_passage'
repertoireSortieET=os.getcwd()+'/EXEMPLE4_0/fichiers_entete'
repertoireSortieDE=os.getcwd()+'/EXEMPLE4_0/fichiers_detail'

def ajoutbalisedebutfin(repertoireE, repertoireP, filename, newfilename):

    # cette fonction permet de préparer le fichier source pour ElementTree
    # en effet ElementTree attend un seul noeud racine qui contient tous les autres éléments
    # si le fichier XML n'est pas bien formé ElementTree ne pourra l'analyser
    # cette fonction consiste donc à contourner le problème en ajoutant un faux noeud racine au document
    # on ouvre en écriture le fichier "newfilename" dans le répertoire de passage"repertoireP"
    filewrite = open(os.path.join(repertoireP, newfilename), 'w' , encoding="utf-8")

    with open(os.path.join(repertoireE, filename), 'r', encoding='UTF-8') as fileread:
        # on lit la première ligne du fichier source et on l'écrit dans le nouveau fichier
        line = fileread.readline()
        ligneAEcrire = line
        filewrite.write(ligneAEcrire)

        # on intercale la balise de début root après la première ligne
        ligneAEcrire = "<root>\n"
        filewrite.write(ligneAEcrire)

        # on lit la ligne suivante du fichier source ie la deuxième ligne
        line = fileread.readline()

        # on lit les lignes suivantes du fichier ligne à ligne tant qu'on a pas atteint la fin du fichier et
        # on les écrit dans le nouveau fichier
        while line:
            ligneAEcrire = line

            filewrite.write(ligneAEcrire)

            # on lit la ligne suivante du fichier source
            line = fileread.readline()

        # lorsqu'on a lu toutes les lignes, on intercale la balise de fin root
        ligneAEcrire = r'</root>'
        filewrite.write(ligneAEcrire)

        # on ferme le fichier source
        fileread.close()

    # on ferme le fichier resultat
    filewrite.close()


# main

for filename in os.listdir(repertoireSource):
    # on prépare le fichier en ajoutant un faux noeud racine au document
    # le fichier ainsi créé est préfixé 'mef' et stocké dans le répertoire de passage
    ajoutbalisedebutfin(repertoireSource,repertoirePassage,filename,'mef'+filename)
    fichierxml=os.path.join(repertoirePassage, 'mef'+filename)
    # on lance l'analyse du fichier XML avec ElementTree
    tree = ET.parse(fichierxml)
    root = tree.getroot()

    ticket_items=[]
    all_tickets_items=[]
    line_items=[]
    all_line_items=[]

    # on itère sur les sous-éléments 'ticket'
    for ticketno in root.iter('ticket'):
        ticketNo = ticketno.find('document').text
        ticketOperation = ticketno.find('operation').text
        ticketCaisse = ticketno.find('caisse').text
        if ticketno.find('date') is not None:
            ticketDate = ticketno.find('date').text
        elif ticketno.find('horodatage') is not None:
            ticketDate = ticketno.find('horodatage').text
        ticketTTC = ticketno.find('totalTTC').text
        ticketHT = ticketno.find('totalHT').text

        # on itère sur les sous-éléments 'ligne'
        for lineno in ticketno.iter('ligne'):
            ligneNo = lineno.attrib.get('id')
            ligneProduit = lineno.find('produitId').text
            lignedesignation = lineno.find('designation').text
            ligneQuantite = lineno.find('quantite').text
            ligneTauxtva = lineno.find('tauxTVA').text
            ligneTotalTTC = lineno.find('totalTTC').text
            ligneTotalHT = lineno.find('totalHT').text
            # on stocke les données de détail du ticket dans une liste
            line_items = [ticketNo, ticketOperation, ticketCaisse, ticketDate, ticketTTC, ticketHT, ligneProduit,
                          lignedesignation, \
                          ligneQuantite, ligneTotalHT, ligneTotalTTC]
            all_line_items.append(line_items)

        # on stocke les données d'en-tete du ticket dans une liste
        tickets_items = [ticketNo, ticketOperation, ticketCaisse, ticketDate, ticketTTC, ticketHT]
        all_tickets_items.append(tickets_items)

    # on crée à partir de la liste un dataframe qui contient toutes les données de détail des tickets
    lineDf = pd.DataFrame(all_line_items, columns=['Noticket', 'Operation', 'Caisse', 'Date', 'TicketTTC', 'TicketHT', \
                                                   'Produit','Désignation','Quantite','LigneHT','LigneTTC'])
    # on crée à partir de la liste un dataframe qui contient toutes les données d'en-tête du ticket
    ticketDf = pd.DataFrame(all_tickets_items, columns=[
      'NoTicket',  'Operation', 'Caisse', 'Date', 'TicketTTC', 'TicketHT'])

    # on convertit les dataframes en fichiers csv
    lineDf.to_csv(os.path.join(repertoireSortieDE, filename.split(".")[0] + "_detailP.csv"),index=False)
    ticketDf.to_csv(os.path.join(repertoireSortieET, filename.split(".")[0] + "_enteteP.csv"),index=False)