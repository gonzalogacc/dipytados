########################################################################
##
##
##
########################################################################

import urllib, urllib2
import cookielib
from bs4 import BeautifulSoup
import re

def page_parsing(url, saveToFile=False):
	'''
	(url str, saveToFile str) -> html source de la pagina (str), archivo con source html
	
	Toma la direccion de la pagina y devuelve una cadena de texto con el codigo html de la pagina
	Si se pasa el argumento saveToFile el codigo tambien se guarda en un archivo de este mismo nombre
	'''
	print url
	##opener = urllib2.build_opener()
	##req = urllib2.Request(url)
	response = urllib2.urlopen(url)
	the_page = response.read()
	if saveToFile != False:
		file(saveToFile,'w').write(the_page)
	return the_page

def getConversation(parsed_page):
	'''
	(srt parsed_page) -> str cadena de texto con toda la conversacion de la sesion
	
	Toma el source html de la pagina y usa beautiful soup para sacar las etiquetas span
	luego concatena el texto y lo devuelve
	'''
	
	bsp = BeautifulSoup(parsed_page)
	
	expresiones = bsp.find_all('span')
	
	texto = ''
	for elemento in expresiones:
		texto += elemento.getText()
	
	return texto

def getDiputados(text):
	'''
	(str) -> list
	
	Toma una conversacion del senado y extrae las menciones a los diputados que participan hablando en la sesion.
	Reconoce los diputados como el texto qu esta entre un 'sr.' o 'sra.' y un '.-'
	Devuelve una lista de tuplas con los nombres, el inicio de la posicion dle nombre y el final
	'''
	
	prog = re.compile('(sr.|sra.).*,*(\.-)', re.IGNORECASE)
	result = prog.finditer(text)
	
	lista_diputados = []
	for diputado in result:
		lista_diputados.append((conversacion[diputado.span()[0]:diputado.span()[1]], diputado.span()))
	
	return lista_diputados

##pagina = page_parsing('http://www1.hcdn.gov.ar/sesionesxml/reunion.asp?p=129&r=10', '/home/gonza/Escritorio/temporal/sourcesesion_definitiva.html')
pagina = open('/home/gonza/Escritorio/dipytados/sourcesesion_definitiva.html', 'r').read()
	
conversacion = getConversation(pagina)

lista_diputados = getDiputados(conversacion)
print lista_diputados
