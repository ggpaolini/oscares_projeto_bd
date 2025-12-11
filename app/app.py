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

@APP.route('/cerimonias/<int:number>')
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
    return render_template('mostrar_cerimonias', cerimonia=cerimonia, nomeacoes=nomeacoes)

@APP.route('/classes/')
def list_classes():
    classes = db.execute(
        '''
SELECT * FROM CLASS ORDER BY ClassName
'''
    ).fetchall()
    return render_template('listar_classes.html', classes=classes)

@APP.route('/classes/<string:name>')
def show_classes(name):
    classe = db.execute(
        '''
select * from class where classname=?
''', [name]
    ).fetchone()

    categorias= db.execute(
        '''
select * from category
where classname = ?
''', [name]
    ).fetchall()
    return render_template('mostrar_classes', classe=classe, categorias=categorias)

@APP.route('/categorias/')
def list_categorias():
    categorias = db.execute(
        '''
SELECT * FROM CATEGORY ORDER BY ClassName, CanonicalCategory
'''
    ).fetchall()
    return render_template('listar_categorias.html', categorias=categorias)

@APP.route('/filmes/')
def list_filmes():
    filmes = db.execute(
        '''
SELECT * FROM FILM ORDER BY FilmName
'''
    ).fetchall()
    return render_template('listar_filmes.html', filmes=filmes)

#@APP.route('/filmes/<int:id')

@APP.route('/nomeados/')
def list_nomeados():
    nomeados = db.execute(
        '''
SELECT * FROM NOMINEE ORDER BY Name
'''
    ).fetchall()
    return render_template('listar_nomeados.html', nomeados=nomeados)

@APP.route('/nomeados/<int:id>/')
def show_nomeado(id):
    nomeado = db.execute(
        '''
SELECT * FROM NOMINEE WHERE NomineeId = ?
''', [id]
    ).fetchone()
    nomeacoes = db.execute(
        '''
    select * from nomination where NomId in 
    (
    select nomid from nominee
    natural join nomination_nominee
    natural join nomination
    where NomineeId= ?
    )
''', [id]
    ).fetchall()
    filmes = db.execute(
        '''
    select * from film where (FilmId, FilmName) in 
    (
    select filmid, filmname from nominee
    natural join nomination_nominee
    natural join nomination
    natural join nomination_film
    where NomineeId= ?
    )
''', [id]
    )
    return render_template('mostrar_nomeado', nomeado=nomeado, nomeacoes=nomeacoes, filmes=filmes)


@APP.route('/nomeacoes/')
def list_nomeacoes():
    nomeacoes = db.execute(
        '''
SELECT * FROM NOMINATION ORDER BY CeremonyNumber, ClassName, CanonicalCategory, NomId
'''
    ).fetchall()
    return render_template('listar_nomeacoes.html', nomeacoes=nomeacoes)

#@APP.route('/nomeacoes/<int:nomid>')
#def show_nomeacoes(id):
#ainda nao sei o que meter aqui

