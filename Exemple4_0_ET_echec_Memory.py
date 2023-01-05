import pandas as pd
import os
import xml.etree.ElementTree as ET
import re

repertoireSource=os.getcwd()+'/EXEMPLE4_0/fichiers_source'
repertoirePassage=os.getcwd()+'/EXEMPLE4_0/fichiers_passage'
repertoireSortieET=os.getcwd()+'/EXEMPLE4_0/fichiers_entete'
repertoireSortieDE=os.getcwd()+'/EXEMPLE4_0/fichiers_detail'

for filename in os.listdir(repertoireSource):
	fichierxml=os.path.join(repertoireSource, filename)
	with open(fichierxml, 'r', encoding='utf-8') as f:
		xml=f.read()
		f.close()
	xml2=xml
	if re.search(r'<root>',xml) is None:
		xml2 =re.sub(r"(<\?xml[^>]+\?>)", r"\1\n<root>", xml) + '\n' + "</root>"
	fichierxml2 = os.path.join(repertoirePassage, 'fichiertransit')
	with open(fichierxml2, 'w', encoding='utf-8') as f:
		f.write(xml2)
		f.close()

	tree = ET.parse(fichierxml2)
	root = tree.getroot()

	ticket_items=[]
	all_tickets_items=[]
	line_items=[]
	all_line_items=[]

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

		for lineno in ticketno.iter('ligne'):
			ligneNo = lineno.attrib.get('id')
			ligneProduit = lineno.find('produitId').text
			lignedesignation = lineno.find('designation').text
			ligneQuantite = lineno.find('quantite').text
			ligneTauxtva = lineno.find('tauxTVA').text
			ligneTotalTTC = lineno.find('totalTTC').text
			ligneTotalHT = lineno.find('totalHT').text
			line_items = [ticketNo, ticketOperation, ticketCaisse, ticketDate, ticketTTC, ticketHT, ligneProduit,
						  lignedesignation, \
						  ligneQuantite, ligneTotalHT, ligneTotalTTC]
			all_line_items.append(line_items)

		tickets_items = [ticketNo, ticketOperation, ticketCaisse, ticketDate, ticketTTC, ticketHT]
		all_tickets_items.append(tickets_items)

	lineDf = pd.DataFrame(all_line_items, columns=['Noticket', 'Operation', 'Caisse', 'Date', 'TicketTTC', 'TicketHT', \
	                                               'Produit','Désignation','Quantite','LigneHT','LigneTTC'])
	ticketDf = pd.DataFrame(all_tickets_items, columns=[
	  'NoTicket',  'Operation', 'Caisse', 'Date', 'TicketTTC', 'TicketHT'])

	lineDf.to_csv(os.path.join(repertoireSortieDE, filename.split(".")[0] + "_detailP.csv"),index=False)
	ticketDf.to_csv(os.path.join(repertoireSortieET, filename.split(".")[0] + "_enteteP.csv"),index=False)