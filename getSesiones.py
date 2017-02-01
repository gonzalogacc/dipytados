
import sqlite3 as lite
import bs4
import urllib2
from urlparse import urlparse, parse_qs
import re

## abrir la base de datos
def dbConection(dbname):
    con = None
    try:
        con = lite.connect(dbname)
        cur = con.cursor()
        con.text_factory = str
        return con, cur

    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

def getIndiceSesiones(con, cur):
    """

    :return:
    """
    url = "http://www1.hcdn.gov.ar/sesionesxml/reuniones.shtml"
    print url

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)
    # response = urllib2.urlopen(url)
    pagina = response.read()

    soup = bs4.BeautifulSoup(pagina)
    links = soup.findAll("a")

    sesiones = []
    for a in links:
        if "item.asp" in a["href"]:
            iurl = a["href"]
            descripcion = a.text
            fecha = descripcion.split(' - ')[-1].replace(')', '').replace('(', '') #.split(' - ')[-1].translate(None, '()')

            param = urlparse(iurl)
            qs = parse_qs(param.query)
            print iurl, param, qs

            cur.execute("select id from sesiones where url == ?", (iurl, ))
            id = cur.fetchone()
            print id

            if id == None and 'per' in qs and 'r' in qs and 'n' in qs:
                cur.execute("INSERT INTO sesiones (url, periodo, reunion, n, status, proc_status) VALUES (?, ?, ?, ?, 'pendiente', 'pendiente')", (iurl, int(qs['per'][0]), int(qs['r'][0]), int(qs['n'][0])))
                con.commit()
            else:
                print "Le sesion ya esta cargada en la base con id %s" %(id, )

    return None


def getSesion(con, cur):
    """
    Baja las sesiones a archivos y actualiza la DB
    return:
    """

    ## Procesar una de las sesiones
    cur.execute("SELECT id, url FROM sesiones WHERE status == 'pendiente'")
    id, surl = cur.fetchone()
    print id
    if id == 0:
        ## la pagina ya esta procesada,
        print "No hay mas sesiones para procesar"
        return None

    ## cambiar por parseurl o join url o urllib o algo asi"
    url = 'http://www1.hcdn.gov.ar/sesionesxml/' + surl
    print url

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)
    # response = urllib2.urlopen(url)
    pagina = response.read()

    if pagina != None:

        # cur.execute("INSERT INTO sesiones (periodo, sesion, url, path_sesion) VALUES (?, ?, ?, ?)", (periodo, sesion, url, path_sesion))
        cur.execute("UPDATE sesiones SET html_text = ? where id == ?", (pagina, id))
        cur.execute("UPDATE sesiones SET status = 'listo' where id == ?", (id,))
        con.commit()

def processSesion(con, cur):
    """

    :param con:
    :param cur:
    :return:
    """

    cur.execute("SELECT id, html_text FROM sesiones WHERE status == 'listo' and proc_status == 'pendiente'")
    records = cur.fetchall()
    print len(records)

    regex = re.compile(r"sr*.-")
    for sesion in records:
        soup = bs4.BeautifulSoup(sesion[1])
        x = soup.find('body').text
        for c in x.split("\n\n"):
            if c[:2] == "sr":
                partida = c.split(".-")
                diputado = partida[0]
                texto = ' '.join(partida[1:]).strip().replace('\n', '').replace('\t', '')

                print diputado, "|", texto
                print "###################################"

                ## parametros para cargar la intervencion
                diputado_id = getDiputado(con, cur, diputado)
                # print diputado_id

                cur.execute("INSERT INTO intervencion (sesion, diputado, texto) VALUES (?, ?, ?)", (sesion[0], diputado_id, texto))

        ## ya se proceso la sesion, se cambia el proc_status
        cur.execute("UPDATE sesiones SET proc_status = 'listo' WHERE id = ?", (sesion[0], ))
        con.commit()


def getDiputado(con, cur, nombre):

    """
    Toma un nombre de diputado y devuelve un identificador
    Si esta devuelve el noombre, si no esta lo agrega y devuelve el identificador
    :param nombre:
    :return:
    """
    cur.execute("SELECT id FROM diputado where nombre == ?", (nombre, ))
    rta = cur.fetchone()

    if rta is not None:
        ## esta en la base y se devuelve el identificador
        return rta[0]

    else:
        ## no esta en la base, se agrega
        cur.execute("INSERT INTO diputado (nombre) VALUES (?)", (nombre, ))
        con.commit()

        ## ahora que si esta se toma el nombre nuevamente y se devuelve el id
        cur.execute("SELECT id FROM diputado where nombre == ?", (nombre, ))
        rta = cur.fetchone()
        return rta[0]

def extractFechas(con, cur):
    """

    :param con:
    :param cur:
    :return:
    """

    cur.execute("select id, html_text from sesiones where proc_status == 'listo'")
    rta = cur.fetchall()

    if rta == None:
        print 'No hay nada para procesar'
        return None

    for s in rta:
        soup = bs4.BeautifulSoup(s[1])
        r = soup.find('div')
        fecha = r.text.split('celebrada el')[1]
        print s[0], fecha
        cur.execute("UPDATE sesiones SET fecha = ? where id == ?", (fecha, s[0]))
        con.commit()

    return None

if __name__ == "__main__":
    con, cur = dbConection('senadodb.sqlite')
    # agarra el indice de las sesiones
    getIndiceSesiones(con, cur)

    # for x in range(1000):
        # getSesion(con, cur)

    # processSesion(con, cur)
    extractFechas(con, cur)