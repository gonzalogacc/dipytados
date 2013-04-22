########################################################################
##
## Sesiones de diputados
##
########################################################################

import urllib2
from bs4 import BeautifulSoup
import re


class sesion():
	'''
	Clase que contiene una sesion de la camara de diputados
	'''
	def __init__(self, periodo, reunion, sesion, tipo_sesion, fecha):
		'''
		Variables propias de la sesion
		'''
		self.periodo = periodo
		self.reunion = reunion
		self.sesion = sesion
		self.tipo_sesion = tipo_sesion
		self.fecha = fecha
		
		self.html_version_taquigrafica = None
		self.dialogo = None
		
	def getVersionTaquigrafica(self, file = None):
		'''
		(int, int) -> str
		periodo, reunion -> texto de la version taquigrafica
		
		Devuelve el texto de la version taquigrafica dado un numero de 
		periodo y reunion
		Construye una url para consulta de la pagina de diputados y la parsea
		
		'''
		
		if file != None:
			self.version_taquigrafica = open('/home/gonza/Escritorio/dipytados/sourcesesion_definitiva.html', 'r').read()
			
			return version_taquigrafica
		
		else:
			url = 'http://www1.hcdn.gov.ar/sesionesxml/reunion.asp?p='+str(self.periodo)+'&r='+str(self.reunion)
			
			print url
			response = urllib2.urlopen(url)
			version_taquigrafica = response.read()
			
			self.html_version_taquigrafica = version_taquigrafica
	
	def getDialogo(self):
		'''
		(srt parsed_page) -> str cadena de texto con toda la conversacion de la sesion
		
		Toma el source html de la pagina y usa beautiful soup para sacar las etiquetas span
		luego concatena el texto y lo devuelve
		'''
		##print self.html_version_taquigrafica
		bsp = BeautifulSoup(self.html_version_taquigrafica)
		
		expresiones = bsp.find_all('span')
		
		texto = ''
		for elemento in expresiones:
			texto += elemento.getText()
		
		self.dialogo = texto

	def getDiputados(self):
		'''
		(str) -> list
		
		Toma una conversacion del senado y extrae las menciones a los diputados que participan hablando en la sesion.
		Reconoce los diputados como el texto qu esta entre un 'sr.' o 'sra.' y un '.-'
		Devuelve una lista de tuplas con los nombres, el inicio de la posicion dle nombre y el final
		'''
		
		prog = re.compile('(sr.|sra.).*,*(\.-)', re.IGNORECASE)
		result = prog.finditer(self.dialogo)
		
		lista_diputados = []
		for diputado in result:
			lista_diputados.append((self.dialogo[diputado.span()[0]:diputado.span()[1]], diputado.span()))
		
		return lista_diputados
	
		
	def getActaVotacion(self):
		'''
		Toma la url de un acta de votacion y guarda el archivo en un 
		directorio temporal para el posterior procesamineto
		'''
		

	def getVotacionesSesion(self, anio, reunion):
		'''
		(int, int) -> lista_votaciones
		periodo, reunion -> lista_votaciones
		
		Devuelve una lista de objetos votaciones dados un periodo y una reunion
		Lista las url de las votaciones de la pagina que coinciden con el periodo y reunion dadas
		
		'''
		
		url = 'http://www.diputados.gov.ar/secadmin/ds_electronicos/periodo/'+str(anio)+'/index.html'
		response = urllib2.urlopen(url)
		the_page = response.read()
		
		## Filtra los links de la pagina que corresponden a actas de votacion
		bsp = BeautifulSoup(the_page)
		links = bsp.find_all('a', attrs = {"title": "Acta pdf"})
		
		## Filtra los que correspnden a la reunion de interes y agrega los links a la lista
		links_votaciones = []
		for link in links:	
			candidato = link['href']
			if candidato[-6:-4] == reunion:
				links_votaciones.append(candidato)
		
		
	
	def getVotacion(self, url):
		'''
		(reunion, periodo, expediente) -> objeto votacion
		
		Devuelve un objeto que contiene una matriz de diputado, partido 
		al que pertenece y votacion que realizo y tambien una identificacion
		en referencia a lo que se voto
		
		'''

class votacion(sesion):
	'''
	Objeto que contiene la informacion de una votacion expandir explicacion
	'''
	def __init__(self):
		self.expediente = None
		self.matriz_votacion = None
	
	def getArchivoVotacion():
		'''
		obtiene el archivo del resultado de la votacion y lo guarda en el disco?
		'''
	def construirMatriz_votacion():
		'''
		Devuelve una matriz de votacion dado un archivo de resultado de votacion
		'''
	
class diputado(sesion):
	'''
	Objeto que contiene la informacion de un diputado en una sesion dada
	'''
	def __init__(self):
		self.nombre = None
		self.intervenciones = None
		self.n_intervenciones = None
		self.presente = None
		
	def getIntervenciones():
		'''
		
		Devuelve una cadena de texto que es todo lo que dijo el diputado
		concatenado dado el nombre del diputado
		'''

##class listaVotaciones():
	##'''
	##Coleccion de elementos votacion
	##'''	
	##def __init__():
		##self.
			##
##class listaDiputados():
	##'''
	##Coleccion de elementos diputados
	##'''
	##
	##def __init__():
		##self.
		##


ss =  sesion(129, 10, 7, 'especial', '30/11/2011')
ss.getVersionTaquigrafica()

ss.getDialogo()
##print ss.dialogo

for i in ss.getDiputados():
	print i
	
