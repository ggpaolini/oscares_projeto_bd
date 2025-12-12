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
        '''
        select * from class where classname=?
        ''', [name]
        ).fetchone()

    categorias= db.execute(
        '''
        select * from category
        where classname =?
        ''',[name]
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
        '''
        SELECT * FROM CATEGORY WHERE CategoryName =?
        ''', [name]
    ).fetchone()
    nomeacoes = db.execute(
        '''
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
    id,name = id_name.split("_")
    name = name.replace("%20"," ")
    filme = db.execute(
        '''
    SELECT * FROM FILM WHERE FilmId =? and FilmName =?
    ''', [id, name]
    ).fetchone()
    nomeacoes = db.execute(
        '''
        select * from nomination where NomId in 
        (
        select nomid from nominee
        natural join nomination_film
        WHERE FilmId =? and FilmName =?
        )
        ''', [id, name]
        ).fetchall()
    nomeados = db.execute(
        '''
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
        '''
        SELECT * FROM nominee WHERE NomineeId =?
        ''', [id]
        ).fetchone()
    nomeacoes = db.execute(
        '''
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
        '''
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
    
# Query 1
@APP.route('/q1')
def q1():
    row = db.execute("SELECT COUNT(*) AS total FROM NOMINATION").fetchone()
    return render_template("q1.html", total=row["total"])


# Query 2
@APP.route('/q2')
def q2():
    categorias = db.execute(
        "SELECT * FROM CATEGORY WHERE ClassName = ?", ("Directing",)
    ).fetchall()
    return render_template("q2.html", categorias=categorias)


# Query 3
@APP.route('/q3')
def q3():
    empresas = db.execute(
        "SELECT * FROM NOMINEE WHERE NomineeId LIKE 'co%'"
    ).fetchall()
    return render_template("q3.html", empresas=empresas)


# Query 4
@APP.route('/q4')
def q4():
    filmes = db.execute(
        """
        SELECT FilmId, FilmName
        FROM FILM
        NATURAL JOIN NOMINATION_FILM
        NATURAL JOIN NOMINATION
        WHERE CategoryName = 'BEST PICTURE' AND Winner = 'TRUE'
        """
    ).fetchall()
    return render_template("q4.html", filmes=filmes)


# Query 5
@APP.route('/q5')
def q5():
    row = db.execute(
        """
        SELECT AVG(NumNominees) AS media
        FROM (
            SELECT CeremonyNumber, COUNT(*) AS NumNominees
            FROM NOMINATION
            GROUP BY CeremonyNumber
        )
        """
    ).fetchone()
    return render_template("q5.html", media=row["media"])


# Query 6
@APP.route('/q6')
def q6():
    atores = db.execute(
        """
        SELECT NomineeId, Name, COUNT(*) AS Wins
        FROM NOMINEE
        NATURAL JOIN NOMINATION_NOMINEE
        NATURAL JOIN NOMINATION
        WHERE Winner = 'TRUE' AND NomineeId NOT LIKE 'co%'
        GROUP BY NomineeId, Name
        ORDER BY Wins DESC
        LIMIT 5
        """
    ).fetchall()
    return render_template("q6.html", atores=atores)


# Query 7
@APP.route('/q7')
def q7():
    filmes = db.execute(
        """
        SELECT FilmId, FilmName, COUNT(*) AS N_Nomeacoes
        FROM FILM
        NATURAL JOIN NOMINATION_FILM
        NATURAL JOIN NOMINATION
        GROUP BY FilmId, FilmName, CeremonyNumber
        ORDER BY N_Nomeacoes DESC
        """
    ).fetchall()
    return render_template("q7.html", filmes=filmes)


# Query 8
@APP.route('/q8')
def q8():
    nomeados = db.execute(
        """
        SELECT DISTINCT NomineeId, Name
        FROM NOMINEE
        NATURAL JOIN NOMINATION_NOMINEE
        NATURAL JOIN NOMINATION
        NATURAL JOIN NOMINATION_FILM
        NATURAL JOIN FILM
        WHERE FilmName = 'The Godfather'
        AND NomineeId NOT LIKE 'co%'
        """
    ).fetchall()
    return render_template("q8.html", nomeados=nomeados)


# Query 9
@APP.route('/q9')
def q9():
    filmes = db.execute(
        '''
SELECT F.FilmId, F.FilmName
FROM FILM F
WHERE NOT EXISTS (
    SELECT 1
    FROM NOMINATION_FILM NF
    JOIN NOMINATION N ON N.NomId = NF.NomId
    WHERE NF.FilmId = F.FilmId
      AND N.Winner = 'FALSE'
     
);'''
    ).fetchall()
    #print("teste") - a query é um pouco lenta, esta aqui é mais rapida
    return render_template("q9.html", filmes=filmes)


# Query 10
@APP.route('/q10')
def q10():
    rows = db.execute(
        """
        WITH Wins AS (
            SELECT DISTINCT NomineeId, Name, CeremonyNumber
            FROM NOMINATION
            NATURAL JOIN NOMINATION_NOMINEE
            NATURAL JOIN NOMINEE
            WHERE Winner = 'TRUE'
        )
        SELECT DISTINCT 
            w1.NomineeId, 
            w1.Name, 
            w1.CeremonyNumber AS Year1, 
            w2.CeremonyNumber AS Year2
        FROM Wins w1
        JOIN Wins w2
            ON w1.NomineeId = w2.NomineeId
           AND w2.CeremonyNumber = w1.CeremonyNumber + 1
        ORDER BY w1.NomineeId, w1.CeremonyNumber
        """
    ).fetchall()
    return render_template("q10.html", rows=rows)

"""
        SELECT FilmId, FilmName
        FROM FILM
        WHERE FilmId NOT IN (
            SELECT NF.FilmId
            FROM NOMINATION_FILM NF
            NATURAL JOIN NOMINATION N
            WHERE NF.FilmId NOT IN (
                SELECT NF2.FilmId
                FROM NOMINATION_FILM NF2
                NATURAL JOIN NOMINATION N2
                WHERE N2.Winner = 'TRUE'
                  AND NF2.FilmId = NF.FilmId
            )
        )
        """
