import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from flask import render_template, Flask
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    stats = db.execute(
        '''
SELECT *
FROM (SELECT COUNT(*) AS n_ceremony FROM CEREMONY)
JOIN (SELECT COUNT(*) AS n_class FROM CLASS)
JOIN (SELECT COUNT(*) AS n_category FROM CATEGORY)
JOIN (SELECT COUNT(*) AS n_nomination FROM NOMINATION)
JOIN (SELECT COUNT(*) AS n_film FROM FILM)
JOIN (SELECT COUNT(*) AS n_nominee FROM NOMINEE)
    ''').fetchone()
    logging.info(stats)
    return render_template('index.html',stats=stats)

@APP.route('/cerimonias/')
def list_ceremonies():
    cerimonias = db.execute(
        '''
SELECT * FROM Ceremony ORDER BY CeremonyNumber
'''
    ).fetchall()
    return render_template('listar_cerimonias.html', cerimonias=cerimonias)

@APP.route('/cerimonias/<int:number>/')
def show_ceremonies(number):
    cerimonia = db.execute(
        '''
select * from ceremony where ceremonyNumber = ?
''', [number]
    ).fetchone()

    nomeacoes = db.execute(
        '''
select * from nomination where ceremonyNumber=?
''', [number]
    ).fetchall()
    return render_template('mostrar_cerimonias.html', cerimonia=cerimonia, nomeacoes=nomeacoes)

@APP.route('/classes/')
def list_classes():
    classes = db.execute(
        '''
SELECT * FROM CLASS ORDER BY ClassName
'''
    ).fetchall()
    return render_template('listar_classes.html', classes=classes)

@APP.route('/classes/<string:name>/')
def show_classes(name):
    classe = db.execute(
        f'''
        select * from class where classname='{name}'
        '''
        ).fetchone()

    categorias= db.execute(
        f'''
        select * from category
        where classname = '{name}'
        '''
        ).fetchall()
    return render_template('mostrar_classes.html', classe=classe, categorias=categorias)

@APP.route('/categorias/')
def list_categorias():
    categorias = db.execute(
        '''
SELECT * FROM CATEGORY ORDER BY ClassName, CanonicalCategory
'''
    ).fetchall()
    return render_template('listar_categorias.html', categorias=categorias)

@APP.route('/categorias/<string:name>/')
def show_categorias(name):
    name = name.replace("%20"," ")
    categoria = db.execute(
        f'''
        SELECT * FROM CATEGORY WHERE CategoryName =?
        ''', [name]
    ).fetchone()
    nomeacoes = db.execute(
        f'''
        SELECT * FROM nomination WHERE CategoryName =?
        ''', [name]
        )
    return render_template('mostrar_categorias.html', categoria=categoria,nomeacoes=nomeacoes)


@APP.route('/filmes/')
def list_filmes():
    filmes = db.execute(
        '''
SELECT * FROM FILM ORDER BY FilmName
'''
    ).fetchall()
    return render_template('listar_filmes.html', filmes=filmes)

@APP.route('/filmes/<string:id_name>')
def show_filmes(id_name):
    t = id_name.lower()      # Tentei evitar algumas injeções aqui
    if any(i in t for i in ("join","--","drop","table")): raise Exception("Nice Try")  #Checking for injections
    id,name = id_name.split("_")
    name = name.replace("%20"," ").replace("'","''")
    filme = db.execute(
        f'''
    SELECT * FROM FILM WHERE FilmId =? and FilmName =?
    ''', [id, name]
    ).fetchone()
    nomeacoes = db.execute(
        f'''
        select * from nomination where NomId in 
        (
        select nomid from nominee
        natural join nomination_film
        WHERE FilmId = '{id}' and FilmName = '{name}'
        )
        '''
        ).fetchall()
    nomeados = db.execute(
        f'''
        select distinct n.* FROM nomination
        natural join nomination_film
        natural join nomination_nominee
        natural join nominee n
        WHERE FilmId =? and FilmName =?
        ''', [id, name]
        ).fetchall()
    return render_template('mostrar_filmes.html', filme=filme,nomeacoes=nomeacoes,nomeados=nomeados)

@APP.route('/nomeados/')
def list_nomeados():
    nomeados = db.execute(
        '''
SELECT * FROM NOMINEE ORDER BY Name
'''
    ).fetchall()
    return render_template('listar_nomeados.html', nomeados=nomeados)

@APP.route('/nomeados/<string:id>/')
def show_nomeado(id):
    nomeado = db.execute(
        f'''
        SELECT * FROM nominee WHERE NomineeId =?
        ''', [id]
        ).fetchone()
    nomeacoes = db.execute(
        f'''
        select * from nomination where NomId in 
        (
        select nomid from nominee
        natural join nomination_nominee
        natural join nomination
        where NomineeId=?
        )
        ''', [id]
        ).fetchall()
    filmes = db.execute(
        f'''
        select * from film where (FilmId, FilmName) in 
        (
        select filmid, filmname from nominee
        natural join nomination_nominee
        natural join nomination
        natural join nomination_film
        where NomineeId=?
        )
        ''', [id]
        ).fetchall()
    return render_template('mostrar_nomeado.html', nomeado=nomeado, nomeacoes=nomeacoes, filmes= filmes)


@APP.route('/nomeacoes/')
def list_nomeacoes():
    nomeacoes = db.execute(
        '''
    SELECT * FROM NOMINATION ORDER BY CeremonyNumber, ClassName, CategoryName, NomId
    '''
    ).fetchall()
    return render_template('listar_nomeacoes.html', nomeacoes=nomeacoes)

@APP.route('/nomeacoes/<int:nomid>/')
def show_nomeacoes(nomid):
    nomeacao = db.execute('''
        SELECT * FROM NOMINATION where NomId = ?
        '''
        ,[nomid]).fetchone()
    filmes = db.execute(
        '''
        select f.* FROM nomination
        natural join nomination_film f
        where NomId = ?
        '''
        ,[nomid]).fetchall()
    nomeados = db.execute(
        '''
        select n.* FROM nomination
        natural join nomination_nominee
        natural join nominee n
        where NomId = ?
        '''
        ,[nomid]).fetchall()
    return render_template('mostrar_nomeacoes.html',nomeacao=nomeacao,filmes=filmes,nomeados=nomeados)
    


