# -*- coding: utf-8 -*-
########################################################################
##
## Sesiones de diputados
##
########################################################################

import urllib2
from bs4 import BeautifulSoup
import re

class sesion():
	"""
	Clase que contiene una sesion de la camara de diputados
	"""
	def __init__(self, periodo, reunion, sesion, tipo_sesion, fecha):
		"""
		Almacena las variables propias de la sesion
		
		Argumentos
		-------------------------
		periodo: periodo que corresponde a la sesion
		reunion: numero de reunion
		sesion: sesion de la reunion y el periodo 
		tipo_sesion: si es ordinaria o extraordinaria
		fecha: fecha en formato dd/mm/aaaa
		"""
		self.periodo = periodo
		self.reunion = reunion
		self.sesion = sesion
		self.tipo_sesion = tipo_sesion
		self.fecha = fecha
		
		self.html_version_taquigrafica = None
		self.dialogo = None
		self.intervenciones = []
		self.intervenciones_por_diputado = {}
		
	def getVersionTaquigrafica(self, file = None):
		"""
		Devuelve el texto de la version taquigrafica dado un numero de periodo y reunion
		Construye una url para consulta de la pagina de diputados y la parsea
		
		Arguemntos
		-------------------------
		file: si hay una ruta a un archivo intenta parsear la version taquigrafica desde ahi sino la saca de internet
		"""
		
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
		"""		
		Toma el source html de la pagina y usa beautiful soup para sacar las etiquetas span
		luego concatena el texto y lo devuelve
		
		"""
		##print self.html_version_taquigrafica
		bsp = BeautifulSoup(self.html_version_taquigrafica)
		
		expresiones = bsp.find_all('span')
		
		texto = ''
		for elemento in expresiones:
			texto += elemento.getText()
		
		self.dialogo = texto

	def getDiputados(self):
		"""
		Toma la conversacion del senado y extrae las menciones a los diputados que participan hablando en la sesion.
		Reconoce los diputados como el texto qu esta entre un 'sr.' o 'sra.' y un '.-'
		Devuelve una lista de tuplas con los nombres, el inicio de la posicion dle nombre y el final
		"""
		
		prog = re.compile('(sr.|sra.).*,*(\.-)', re.IGNORECASE)
		result = prog.finditer(self.dialogo)
		
		lista_diputados = []
		for diputado in result:
			lista_diputados.append((self.dialogo[diputado.span()[0]:diputado.span()[1]], diputado.span()))
		
		return lista_diputados
	
	def getIntervencionesDiputados (self):
		""" 
		Devuelve un diccionario donde la clave son los diputados y dentro 
		de cada una esta el texto concatenado de todas las entradas
		
		Rellena la variable	intervenciones_por_diputado	
		"""
		prog_indices = re.compile('(sr.|sra.).*', re.IGNORECASE)
		prog_nombre = re.compile('(sr.|sra.).*,*(\.-)', re.IGNORECASE)

		result = prog_indices.finditer(self.dialogo)
		
		indices = []		
		for i in result:
			indices.append(i.span()[0])
		
		dips = []
		for indice in range(len(indices)-1):
			
			inicio, final = prog_nombre.match(self.dialogo[indices[indice]:indices[indice+1]]).span()
			
			discurso = self.dialogo[indices[indice]:indices[indice+1]]
			
			nombre = discurso[inicio:final]
			dips.append(nombre)
			self.intervenciones.append([nombre, discurso])
		
		dips_unicos = list(set(dips))
		
		for dip in dips_unicos:
			temp_dip = []
			for entrada in self.intervenciones:
				if dip == entrada[0]:
					temp_dip.append(entrada[1])
			
			self.intervenciones_por_diputado[dip] = temp_dip
			
		
		
	def getActaVotacion(self):
		"""
		Toma la url de un acta de votacion y guarda el archivo en un 
		directorio temporal para el posterior procesamineto
		"""
		return None

	def getVotacionesSesion(self, anio, reunion):
		"""	
		Devuelve una lista de objetos votaciones dados un periodo y una reunion
		Lista las url de las votaciones de la pagina que coinciden con el periodo y reunion dadas
		
		"""
		
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
		
		return links_votaciones
		
	
	def getVotacion(self, url):
		"""		
		Devuelve un objeto que contiene una matriz de diputado, partido 
		al que pertenece y votacion que realizo y tambien una identificacion
		en referencia a lo que se voto
		
		"""
	
class diputado(sesion):
	"""
	Objeto que contiene la informacion de un diputado en una sesion dada
	"""
	def __init__(self):
		self.nombre = None
		self.intervenciones = None
		self.n_intervenciones = None
		self.presente = None
		
	def getIntervenciones():
		"""
		Devuelve una cadena de texto que es todo lo que dijo el diputado
		concatenado dado el nombre del diputado
		"""

class votacion(sesion):
	"""
	Objeto que contiene la informacion de una votacion expandir explicacion
	"""
	def __init__(self):
		self.expediente = None
		self.matriz_votacion = None
	
	def getArchivoVotacion():
		"""
		obtiene el archivo del resultado de la votacion y lo guarda en el disco?
		"""
	def construirMatriz_votacion():
		"""
		Devuelve una matriz de votacion dado un archivo de resultado de votacion
		"""

##class listaVotaciones():
	##"""
	##Coleccion de elementos votacion
	##"""	
	##def __init__():
		##self.
			##
##class listaDiputados():
	##"""
	##Coleccion de elementos diputados
	##"""
	##
	##def __init__():
		##self.
		##


if __name__ == '__main__':
	ss =  sesion(129, 10, 7, 'especial', '30/11/2011')
	ss.getVersionTaquigrafica()

	ss.getDialogo()
	ss.getIntervencionesDiputados()
	
	##for diputado in ss.getDiputados():
		##print diputado
	##for i in ss.intervenciones:
		##print i[0]
	print type(ss.intervenciones_por_diputado)
	raw_input()
	##for i in ss.intervenciones_por_diputado:
		##print i
		##raw_input()
	print ss.intervenciones_por_diputado
