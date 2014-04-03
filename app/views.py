from app import app
#from app import db_connection
from flask import render_template, request, g, session
import sqlite3 as lite

#con = None
#try:
#	con = lite.connect('app/db')
#	cur = con.cursor()
#	cur.execute('select * from empresasqq')
#	empresas_rows = cur.fetchall()
#except lite.Error, e:
#	print 'Error %s' % e.args[0]
#finally:
#	if con:
#		con.close()

DATABASE = 'app/db'

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = lite.connect(DATABASE)
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

data = {}


@app.route('/')
def index():
	return render_template('layout.html')
@app.route('/empresas')
def empresas():
	#print 'SQLite version %s' % data
	#cur = get_db()
	print dir(session)

	data['empresas_rows'] = get_db().execute('select * from empresasqq').fetchall()
	return render_template('empresas.html',rows=data['empresas_rows'])
@app.route('/empresa', methods=['GET'])
def empresa():
	#print data.keys()
	#print data['empresas_rows'][0]
	cur = get_db().execute('select * from empresasqq')
	empresas_rows = cur.fetchall()
	id = request.args.get('id', None)
	for row in empresas_rows:
		if row[0] == int(id):
			item = row
			break
	d = {}
	for idx, col in enumerate(cur.description):
		d[col[0]] = row[idx]

	cur = get_db().execute('select * from actividadesqq where idactividad='+str(d['IDActividad']))
	d['actividad'] = cur.fetchone()[1]

	cur = get_db().execute('select * from directivosqq where idempresa='+str(d['IDEmpresa']))
	d['directivos_c'] = cur.fetchall()

	cur = get_db().execute('select * from cargosqq')
	cargos = dict(cur.fetchall())
	#print cargos
	#print d['directivos_c']
	d['directivos'] = []
	for directivo in d['directivos_c']:
		#print directivo[2:5]
		d['directivos'].append((cargos[directivo[2]], directivo[3], directivo[4]))
	#print d['directivos']
	#return str(actividad_row)
	return render_template('empresa.html', item=d)
@app.route('/categorias')
def categorias():
	return "Yay"
@app.route('/redessociales')
def redessociales():
	return "Yay"
@app.route('/vidaeconomica')
def vidaeconomica():
	return "Yay"
@app.route('/desarrollador')
def desarrollador():
	return "Yay"
